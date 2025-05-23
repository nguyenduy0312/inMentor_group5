
from flask import Blueprint, request, jsonify, session
import requests



ai_service_bp = Blueprint('ai_service', __name__)  # Tạo Blueprint cho AI service

API_KEY = "app-b78TsFpOzdbiHxEg5rK5TwSy"

@ai_service_bp.route('/chat', methods=['POST'])
def chat():
    try:
        print("==> Header:", request.headers)
        print("==> Body:", request.get_data())

        data = request.json
        message_text = data.get('messageText')
        conversation_id = data.get('conversationId', '')
        inputs = data.get('inputs', {})
        ma_phien = data.get('phienId')

        if not message_text:
            return jsonify({"error": "Thiếu messageText"}), 400

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

        if response.status_code != 200:
            print("==> Lỗi từ Dify:", response.text)
            return jsonify({"error": "Dify trả về lỗi"}), response.status_code

        return jsonify(response.json()), 200

    except Exception as e:
        print("==> Lỗi xử lý request:", str(e))
        return jsonify({"error": "Lỗi xử lý server"}), 500

    

@ai_service_bp.route('/save_summary', methods=['POST'])
def save_summary():
    data = request.json
    session['score'] = data.get('score', '')
    session['strengths'] = data.get('strengths', '')
    session['weaknesses'] = data.get('weaknesses', '')
    return jsonify({"message": "Đã lưu đánh giá tổng quan!"}), 200

