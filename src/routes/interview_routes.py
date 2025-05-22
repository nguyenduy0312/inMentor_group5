from flask import Blueprint, request, jsonify
from services.interview_service import handle_create_session, handle_save_qa, handle_save_evaluation

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/phongvan', methods=['POST'])
def create_session():
    # Mặc định sử dụng user_id = 1
    user_id = 1
    phien_id = handle_create_session(user_id)
    return jsonify({'phien_id': phien_id}), 201
    
    # Gọi service tạo phiên phỏng vấn mới, trả về id phiên mới tạo
    phien_id = handle_create_session(user_id)
    
    if not phien_id:
        return jsonify({"error": "Tạo phiên phỏng vấn thất bại"}), 500

    return jsonify({"message": "Tạo phiên phỏng vấn thành công", "phien_id": phien_id})

@interview_bp.route('/cauhoitraloi', methods=['POST'])
def save_qa():
    data = request.json
    phien_id = data.get('phien_id')
    questions_answers = data.get('questions_answers')
    if not phien_id or not questions_answers:
        return jsonify({"error": "Thiếu phien_id hoặc questions_answers"}), 400
    
    # Gọi service để lưu câu hỏi trả lời theo phiên
    handle_save_qa(phien_id, questions_answers)
    
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
