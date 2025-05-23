from flask import Flask
from routes.interview_routes import interview_bp
from Controller.login.login import login_bp
from routes.static_routes import static_bp

from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

app.secret_key = "your_secret_key"

# Đăng ký các blueprint
app.register_blueprint(interview_bp, url_prefix="/api")
app.register_blueprint(login_bp)
app.register_blueprint(static_bp)



if __name__ == '__main__':
    app.run(debug=True)
