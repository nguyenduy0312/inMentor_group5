import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app  # app chính, đã đăng ký blueprint routes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

from unittest.mock import patch

@patch('routes.interview_routes.create_session')
def test_create_session(mock_create_session, client):
    mock_create_session.return_value = 123
    response = client.post('/api/phongvan')
    data = response.get_json()
    assert response.status_code == 201
    assert data['ma_phien'] == 123

@patch('routes.interview_routes.luu_cau_tra_loi')
def test_luu_cau_tra_loi_thanh_cong(mock_add, client):
    payload = {
        "phien_id": 1,
        "cau_hoi": "Hãy giới thiệu bản thân",
        "cau_tra_loi": "Tôi là sinh viên IT"
    }
    response = client.post('/api/luu_cau_tra_loi', json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == "Đã lưu thành công"
    assert mock_add.call_count == 2

@patch('routes.interview_routes.luu_cau_tra_loi')
def test_luu_cau_tra_loi_thieu_du_lieu(mock_add, client):
    response = client.post('/api/luu_cau_tra_loi', json={"phien_id": 1})
    assert response.status_code == 400
    assert "Thiếu dữ liệu" in response.data.decode('utf-8')

@patch('routes.interview_routes.luu_cau_tra_loi')
def test_luu_cau_tra_loi_cau_hoi_bat_dau(mock_add, client):
    payload = {
        "phien_id": 1,
        "cau_hoi": "  Bắt đầu  ",
        "cau_tra_loi": "OK"
    }
    response = client.post('/api/luu_cau_tra_loi', json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == "Không lưu câu bắt đầu"
    mock_add.assert_not_called()

@patch('routes.interview_routes.save_evaluation')
def test_save_evaluation_thanh_cong(mock_save_eval, client):
    payload = {
        "phien_id": 1,
        "danhgia": "Rất tốt",
        "diemso": 9.5
    }
    response = client.post('/api/danhgia', json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == "Đã lưu đánh giá"
    mock_save_eval.assert_called_once_with(1, "Rất tốt", 9.5)

@patch('routes.interview_routes.save_evaluation')
def test_save_evaluation_thieu_du_lieu(mock_save_eval, client):
    response = client.post('/api/danhgia', json={"phien_id": 1})
    assert response.status_code == 400
    assert "Thiếu dữ liệu đánh giá" in response.data.decode('utf-8')
    mock_save_eval.assert_not_called()
