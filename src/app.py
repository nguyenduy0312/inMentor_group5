from flask import Flask
from Controller.login.login import login_bp

app = Flask(__name__, template_folder='templates')  # Đây đúng rồi
app.secret_key = "your_secret_key"  # để session hoạt động

app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True)
