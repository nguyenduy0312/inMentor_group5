from datetime import datetime
from DAO.phien_phong_van_dao import create_interview_session
from DAO.cau_hoi_tra_loi_dao import add_question_answer
from DAO.bao_cao_danh_gia_dao import create_report

# Hàm xử lý tạo phiên phỏng vấn mới cho người dùng
def handle_create_session(user_id):
    user_id = 1  # Mặc định sử dụng user_id = 1
    phien_id = create_interview_session(user_id)  # Gọi DAO để lưu vào DB
    return phien_id  # Trả về ID của phiên phỏng vấn vừa tạo

# Hàm xử lý lưu danh sách câu hỏi và câu trả lời vào DB
def handle_save_qa(phien_id, qa_list):
    # Nếu qa_list là list các dict {question:..., answer:...}
    for qa in qa_list:
        cau_hoi = qa.get('question')
        tra_loi = qa.get('answer')
        print("Lưu AI hỏi:", cau_hoi)
        print("Lưu User trả lời:", tra_loi)
        add_question_answer(phien_id, cau_hoi, None)      # Lưu câu hỏi của AI
        add_question_answer(phien_id, None, tra_loi)

# Hàm xử lý lưu đánh giá và điểm số AI vào DB
def handle_save_evaluation(phien_id, danhgia, diemso):
    create_report(phien_id, danhgia, diemso)  # Gọi DAO để lưu đánh giá