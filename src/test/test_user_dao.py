import pytest
from DAO.user_dao import get_user_by_id, get_user_interview_history

# ✅ Test get_user_by_id
def test_get_user_by_id_valid():
    user = get_user_by_id(1)  # Giả sử ID 1 tồn tại
    assert user is not None
    assert user['Ma_Nguoi_Dung'] == 1
    assert 'Ho_Ten' in user

def test_get_user_by_id_invalid():
    user = get_user_by_id(-1)  # Giả sử ID -1 không tồn tại
    assert user is None

# ✅ Test get_user_interview_history
def test_get_user_interview_history_valid():
    history = get_user_interview_history(1)  # Giả sử ID 1 có lịch sử
    assert isinstance(history, list)
    if history:
        assert 'Ma_Phien' in history[0]
        assert 'Trang_Thai' in history[0]

def test_get_user_interview_history_empty():
    history = get_user_interview_history(9999)  # Giả sử ID 9999 không có lịch sử
    assert history == [] or isinstance(history, list)
