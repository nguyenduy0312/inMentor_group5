from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from DataBase.connectdb import create_connection, close_connection

login_bp = Blueprint("login_bp", __name__, template_folder='../../templates')
# Đường dẫn đến thư mục templates

@login_bp.route("/")
def index():
    if "email" in session:
        return render_template("trangchu.html", email=session["email"])
    return redirect(url_for("login_bp.login"))

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
                return redirect(url_for("login_bp.index"))
            else:
                flash("Sai mật khẩu!", "danger")
        else:
            flash("Email không tồn tại!", "danger")

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("email", None)
    flash("Đã đăng xuất!", "success")
    return redirect(url_for("login_bp.login"))