import sys
import os

# Thêm đường dẫn thư mục src vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DAO.cau_hoi_tra_loi_dao import add_question_answer, get_questions_answers_by_session

print("Thêm câu hỏi & trả lời...")
ma_phien = 2  # Giả sử đã tồn tại phiên phỏng vấn này
add_question_answer(ma_phien, "Hãy giới thiệu về bản thân bạn.", "Tôi là một lập trình viên Java.")

print("Lấy danh sách câu hỏi & trả lời...")
ds = get_questions_answers_by_session(ma_phien)
for item in ds:
    print(item)
