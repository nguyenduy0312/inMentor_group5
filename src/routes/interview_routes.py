from flask import Blueprint, request, jsonify, session
from services.interview_service import handle_create_session, handle_save_qa, handle_save_evaluation
from DAO.cau_hoi_tra_loi_dao import add_question_answer
interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/phongvan', methods=['POST'])
def create_session():
    # Mặc định sử dụng user_id = 1
    user_id = 1
    phien_id = handle_create_session(user_id)
    # 👉 Lưu phien_id vào session để sử dụng sau
    session["phien_id"] = phien_id
    return jsonify({'ma_phien': phien_id}), 201

@interview_bp.route('/luu_cau_tra_loi', methods=['POST'])
def luu_cau_tra_loi():
    data = request.json
    phien_id = data.get('phien_id')
    cau_hoi = data.get('cau_hoi')
    cau_tra_loi = data.get('cau_tra_loi')
    print("Giá trị cau_hoi nhận được:", repr(cau_hoi))
    if not phien_id or not cau_hoi or not cau_tra_loi:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
    print("DEBUG cau_hoi:", repr(cau_hoi), "strip:", repr(cau_hoi.strip().lower()))
    if cau_hoi and cau_hoi.strip().lower() == "bắt đầu":
        print("Không lưu vào DB vì là 'bắt đầu'")
        return jsonify({"message": "Không lưu câu bắt đầu"}), 200
    add_question_answer(phien_id, cau_hoi, None)      # Lưu câu hỏi của AI
    add_question_answer(phien_id, None, cau_tra_loi)  # Lưu trả lời của người dùng
    return jsonify({"message": "Đã lưu thành công"}), 200

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