import pytest
from DAO.cau_hoi_tra_loi_dao import (
    add_question_answer,
    get_questions_answers_by_session
)
from DataBase.connectdb import create_connection

# ✅ Test thêm câu hỏi - trả lời vào một phiên hợp lệ
def test_add_question_answer_valid():
    # Tạo một phiên mới cho người dùng ID = 1
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau) VALUES (1, 'dang_dien_ra', NOW())")
    conn.commit()
    ma_phien = cursor.lastrowid

    # Gọi hàm thêm câu hỏi - trả lời
    add_question_answer(ma_phien, "Bạn có kinh nghiệm gì với Python?", "Tôi đã dùng Python 2 năm.")
    
    # Kiểm tra lại trong DB
    cursor.execute("SELECT * FROM cau_hoi_tra_loi WHERE Ma_Phiên = %s", (ma_phien,))
    rows = cursor.fetchall()
    assert len(rows) >= 1

    # Dọn dẹp dữ liệu
    cursor.execute("DELETE FROM cau_hoi_tra_loi WHERE Ma_Phiên = %s", (ma_phien,))
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test thêm câu hỏi - trả lời vào phiên KHÔNG tồn tại (gây lỗi do khóa ngoại)
def test_add_question_answer_invalid_session():
    invalid_session_id = -1  # Giả sử không tồn tại
    with pytest.raises(Exception):
        add_question_answer(invalid_session_id, "Câu hỏi?", "Câu trả lời.")

# ✅ Test lấy danh sách câu hỏi - trả lời của một phiên có dữ liệu
def test_get_questions_answers_by_session_with_data():
    # Tạo phiên và thêm dữ liệu
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau) VALUES (1, 'dang_dien_ra', NOW())")
    conn.commit()
    ma_phien = cursor.lastrowid

    add_question_answer(ma_phien, "Bạn biết gì về OOP?", "Tôi biết 4 tính chất OOP.")
    add_question_answer(ma_phien, "Từng dùng MySQL chưa?", "Rồi, tôi đã làm vài project.")

    # Gọi hàm lấy danh sách câu hỏi - trả lời
    results = get_questions_answers_by_session(ma_phien)
    assert isinstance(results, list)
    assert len(results) >= 2
    assert 'Cau_Hoi' in results[0]
    assert 'Tra_Loi' in results[0]

    # Dọn dẹp
    cursor.execute("DELETE FROM cau_hoi_tra_loi WHERE Ma_Phiên = %s", (ma_phien,))
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test lấy danh sách câu hỏi - trả lời của phiên KHÔNG có dữ liệu
def test_get_questions_answers_by_session_no_data():
    # Tạo phiên mới không thêm câu hỏi
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau) VALUES (1, 'dang_dien_ra', NOW())")
    conn.commit()
    ma_phien = cursor.lastrowid

    # Gọi hàm lấy dữ liệu
    results = get_questions_answers_by_session(ma_phien)
    assert isinstance(results, list)
    assert len(results) == 0

    # Dọn dẹp
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test lấy danh sách câu hỏi - trả lời từ phiên KHÔNG tồn tại
def test_get_questions_answers_by_session_invalid():
    invalid_session_id = -1  # Không tồn tại
    results = get_questions_answers_by_session(invalid_session_id)
    assert isinstance(results, list)
    assert len(results) == 0
