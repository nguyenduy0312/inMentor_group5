from flask import Blueprint, make_response, render_template, request, redirect, url_for, session, flash
from DataBase.connectdb import create_connection, close_connection
import base64

login_bp = Blueprint("login_bp", __name__, template_folder='../../templates')

# Route trang chủ
@login_bp.route("/")
def index():
    return render_template("trangchu.html", email=session.get("email"),ho_ten=session.get("ho_ten"))

# Route đăng nhập
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Mat_Khau FROM user WHERE Email = %s", (email,))
        row = cursor.fetchone()
        close_connection(conn)

        if row:
            saved_password = row[0]
            if password == saved_password:
                session["email"] = email
                
                flash("Đăng nhập thành công!", "success")
                return redirect(url_for("login_bp.profile"))
            else:
                flash("Sai mật khẩu!", "danger")
        else:
            flash("Email không tồn tại!", "danger")

    return render_template("login.html")

# Route đăng xuất
@login_bp.route("/logout")
def logout():
    session.clear()  # Xóa toàn bộ session
    flash("Đã đăng xuất!", "success")
    return redirect(url_for("login_bp.login"))


# Route lấy thông tin người dùng từ cơ sở dữ liệu
def get_user_from_db(email):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Ho_Ten, Email, SoDienThoai, skills, Picture FROM user WHERE Email = %s", (email,))
    user_data = cursor.fetchone()
    close_connection(conn)

    # Nếu có ảnh thì chuyển sang base64 để hiển thị được
    if user_data and user_data["Picture"]:
        user_data["Picture"] = base64.b64encode(user_data["Picture"]).decode('utf-8')
    else:
        user_data["Picture"] = None  # hoặc để chuỗi rỗng
    return user_data

# Route hiển thị thông tin người dùng
@login_bp.route("/profile")
def profile():
    if "email" not in session:
        # Tránh flash nếu vừa logout
        if request.referrer and "logout" not in request.referrer:
            flash("Vui lòng đăng nhập trước.", "warning")
        return redirect(url_for("login_bp.login"))

    email = session["email"]
    user_data = get_user_from_db(email)

    # Nếu không có dữ liệu, trả về mặc định
    if not user_data:
        user_data = {
            "Ho_Ten": "Chưa có tên",
            "Email": email,
            "SoDienThoai": "Chưa cập nhật",
            "skills": "Chưa cập nhật",
            "Picture": "",  # Có thể dùng ảnh mặc định
        }
    response = make_response(render_template("user.html", user=user_data))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
