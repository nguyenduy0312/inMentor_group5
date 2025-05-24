import pytest
from DAO.phien_phong_van_dao import (
    create_interview_session,
    end_interview_session,
    get_session_by_user
)
from DataBase.connectdb import create_connection

# ✅ Test tạo phiên phỏng vấn
def test_create_interview_session():
    # Giả sử người dùng có ID = 1 tồn tại
    ma_phien = create_interview_session(1)
    assert isinstance(ma_phien, int)
    assert ma_phien > 0

# ✅ Test tạo phiên phỏng vấn với người dùng KHÔNG tồn tại
def test_create_session_invalid_user():
    invalid_user_id = -1  # Giả sử ID này không tồn tại

    # Kiểm tra người dùng có tồn tại không
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user WHERE Ma_Nguoi_Dung = %s", (invalid_user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert count == 0, "User không hợp lệ nhưng lại tồn tại trong bảng người_dung!"

    with pytest.raises(Exception):
        create_interview_session(invalid_user_id)

# ✅ Test kết thúc phiên phỏng vấn
def test_end_interview_session():
    # Tạo trước một phiên để đảm bảo có Ma_Phien hợp lệ
    ma_phien = create_interview_session(1)
    end_interview_session(ma_phien)

    # Lấy lại thông tin để kiểm tra
    sessions = get_session_by_user(1)
    found = False
    for session in sessions:
        if session['Ma_Phien'] == ma_phien:
            found = True
            assert session['Trang_Thai'] == 'hoan_thanh'
            assert session['Thoi_Gian_Ket_Thuc'] is not None
    assert found  # Đảm bảo phiên vừa tạo và kết thúc tồn tại

# ✅ Test kết thúc phiên phỏng vấn KHÔNG tồn tại
def test_end_session_invalid_id():
    invalid_session_id = -1  # Giả sử phiên này chưa từng được tạo

    # Không lỗi, nhưng không thay đổi gì nếu phiên không tồn tại
    try:
        end_interview_session(invalid_session_id)
        assert True
    except Exception:
        assert False, "Không nên raise lỗi khi kết thúc phiên không tồn tại"

# ✅ Test lấy danh sách phiên theo người dùng có lịch sử
def test_get_session_by_user_with_sessions():
    # Giả sử người dùng 1 đã có phiên
    sessions = get_session_by_user(1)
    assert isinstance(sessions, list)
    if sessions:
        assert 'Ma_Phien' in sessions[0]
        assert 'Trang_Thai' in sessions[0]

# ✅ Test lấy danh sách phiên theo người dùng không có lịch sử
def test_get_session_by_user_no_sessions():
    # Giả sử người dùng ID 9999 chưa từng phỏng vấn
    sessions = get_session_by_user(9999)
    assert isinstance(sessions, list)
    assert len(sessions) == 0
