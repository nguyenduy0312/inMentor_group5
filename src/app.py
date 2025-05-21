from flask import Flask, render_template, request, redirect, url_for, session, flash # type: ignore
from DataBase.connectdb import create_connection, close_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def index():
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if "email" in session:
        return render_template("trangchu.html", email=session["email"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Kết nối tới database
        conn = create_connection()
        cursor = conn.cursor()

        # Kiểm tra email và mật khẩu
        cursor.execute("SELECT Mat_Khau FROM user WHERE Email = %s", (email,))
        row = cursor.fetchone()
        close_connection(conn)

        if row:
            saved_password = row[0]  # Mật khẩu đã lưu trong DB (plain text)
            # So sánh trực tiếp
            if password == saved_password:
                session["email"] = email
                flash("Đăng nhập thành công!", "success")
                return redirect(url_for("index"))
            else:
                flash("Sai mật khẩu!", "danger")
        else:
            flash("Email không tồn tại!", "danger")

    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm = request.form["confirm"]

    if password != confirm:
        flash("Mật khẩu không khớp!", "danger")
        return redirect(url_for("login"))

    conn = create_connection()
    cursor = conn.cursor()

    # Kiểm tra trùng email
    cursor.execute("SELECT * FROM user WHERE Email = %s", (email,))
    if cursor.fetchone():
        flash("Email đã tồn tại!", "danger")
        close_connection(conn)
        return redirect(url_for("login"))

    # Thêm tài khoản mới
    cursor.execute("INSERT INTO user (Ho_Ten, Email, Mat_Khau) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()
    close_connection(conn)

    flash("Đăng ký thành công! Bạn có thể đăng nhập.", "success")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("email", None)
    flash("Đã đăng xuất!", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
