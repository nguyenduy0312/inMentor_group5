from flask import Flask, render_template,session
#from routes.interview_routes import interview_bp
#from controller.login.login import login_bp
#from routes.static_routes import static_bp
from services.ai_service import ai_service_bp  # Import Blueprint của AI service

from flask_cors import CORS

app = Flask(__name__,template_folder='templates')
CORS(app)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')
@app.route('/summary')
def summary():
    score = session.get('score', 'Chưa có')
    strengths = session.get('strengths', 'Chưa có')
    weaknesses = session.get('weaknesses', 'Chưa có')
    return render_template('summary.html', score=score, strengths=strengths, weaknesses=weaknesses)

app.secret_key = "your_secret_key"

# Đăng ký các blueprint
#app.register_blueprint(interview_bp, url_prefix="/api")
#app.register_blueprint(login_bp)
#app.register_blueprint(static_bp)
app.register_blueprint(ai_service_bp, url_prefix="/api")  # Đăng ký AI service với tiền tố URL "/ai"

if __name__ == '__main__':
    app.run(debug=True)