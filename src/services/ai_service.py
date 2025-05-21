from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = ""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message_text = data.get('messageText')
    conversation_id = data.get('conversationId', '')

    payload = {
        "query": message_text,
        "inputs": {"abc": "backend java"},
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

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=False)