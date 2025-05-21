from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    from src.Controller.login import login_bp
    app.register_blueprint(login_bp)

    return app
