import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from DAO.cau_hoi_tra_loi_dao import add_question_answer  # 👈 DAO bạn cần viết
from DAO.phien_phong_van_dao import get_session_by_user  # 👈 Lấy ID phiên 
from routes.interview_routes import interview_bp  # 👈 Đường dẫn tới file interview_routes.py

app = Flask(__name__)
CORS(app)
app.register_blueprint(interview_bp) # Đăng ký blueprint cho các route liên quan đến phỏng vấn

API_KEY = "app-b78TsFpOzdbiHxEg5rK5TwSy"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json

    # 📌 1. Nhận dữ liệu từ frontend
    message_text = data.get('messageText')
    conversation_id = data.get('conversationId', '')
    inputs = data.get('inputs', {})
    user_id = data.get('userId', None)  # 👈 thêm user_id nếu có

    # 📌 2. Gửi câu hỏi tới Dify AI
    payload = {
        "query": message_text,
        "inputs": inputs,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": "abc-123",
        "files": []
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.dify.ai/v1/chat-messages",
        json=payload,
        headers=headers
    )

    ai_response = response.json()

    # 📌 3. Trích xuất câu trả lời từ AI
    answer_raw = ai_response.get("answer", "")
    if isinstance(answer_raw, list):
        answer_text = "\n".join(map(str, answer_raw))
    elif isinstance(answer_raw, str):
        answer_text = answer_raw
    else:
        answer_text = str(answer_raw)

    # 📌 4. (Tùy chọn) lấy ID phiên gần nhất nếu bạn lưu theo phiên
    interview_id = get_session_by_user(user_id)

    # 📌 5. Lưu vào bảng câu hỏi - trả lời
    add_question_answer( ma_phien=interview_id,
                         cau_hoi=message_text,
                         tra_loi=answer_text)

    # 📌 6. Trả phản hồi về client
    return jsonify(ai_response), response.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)
