from flask import Blueprint, request, jsonify
from services.interview_service import handle_create_session, handle_save_qa, handle_save_evaluation

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/phongvan', methods=['POST'])
def create_session():
    # Mặc định sử dụng user_id = 1
    user_id = 1
    phien_id = handle_create_session(user_id)
    return jsonify({'ma_phien': phien_id}), 201

@interview_bp.route('/cauhoitraloi', methods=['POST'])
def save_qa():
    data = request.json
    phien_id = data.get('phien_id')
    questions_answers = data.get('questions_answers')
    if not phien_id or not questions_answers:
        return jsonify({"error": "Thiếu phien_id hoặc questions_answers"}), 400

    if not isinstance(questions_answers, list):
        return jsonify({"error": "questions_answers phải là danh sách"}), 400

    try:
        handle_save_qa(phien_id, questions_answers)
    except Exception as e:
        return jsonify({"error": f"Lỗi khi lưu câu hỏi trả lời: {str(e)}"}), 500

    return jsonify({"message": "Đã lưu câu hỏi và trả lời"})

@interview_bp.route('/danhgia', methods=['POST'])
def save_evaluation():
    data = request.json
    phien_id = data.get('phien_id')
    danhgia = data.get('danhgia')
    diemso = data.get('diemso')
    if not phien_id or danhgia is None or diemso is None:
        return jsonify({"error": "Thiếu dữ liệu đánh giá"}), 400

    # Gọi service lưu đánh giá
    handle_save_evaluation(phien_id, danhgia, diemso)

    return jsonify({"message": "Đã lưu đánh giá"})
