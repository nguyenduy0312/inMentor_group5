# File này sẽ trung gian kết nối logic giữa các DAO và ai_service
from src.DAO.phien_phong_van_dao import create_interview_session, end_interview_session
from src.DAO.cau_hoi_tra_loi_dao import add_question_answer, get_qas_by_session
from src.DAO.bao_cao_danh_gia_dao import save_report
from src.services.ai_service import generate_question, evaluate_answer, generate_final_report

# Tạo mới một phiên phỏng vấn cho người dùng
def start_interview_session(user_id: int) -> int:
    return create_interview_session(user_id)

# Kết thúc một phiên phỏng vấn
def finish_interview_session(ma_phien: int) -> dict:
    qas = get_qas_by_session(ma_phien)
    report = generate_final_report(qas)
    save_report(ma_phien, report)
    end_interview_session(ma_phien)
    return report

# Xử lý một vòng hỏi - trả lời
def handle_question_answer(ma_phien: int, topic: str, user_answer: str = None, last_question: str = None) -> dict:
    if last_question and user_answer:
        # Đánh giá và lưu lại cặp Q&A
        eval_result = evaluate_answer(last_question, user_answer)
        add_question_answer(ma_phien, last_question, user_answer)
    else:
        eval_result = None

    # Sinh câu hỏi tiếp theo
    next_question = generate_question(topic)
    return {
        "question": next_question,
        "evaluation": eval_result
    }
