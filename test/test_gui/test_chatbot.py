import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chatbot_page(client):
    response = client.get('/chatbot')
    assert response.status_code == 200
    # Giả sử trong chatbot.html có <title>Chatbot</title>
    assert b'<title>chatbot</title>' in response.data.lower()

def test_summary_page_without_session(client):
    response = client.get('/summary')
    assert response.status_code == 200
    # Chuyển dữ liệu bytes sang chuỗi UTF-8 để check dấu tiếng Việt chính xác
    data_str = response.data.decode('utf-8').lower()
    assert 'chưa có' in data_str

def test_summary_page_with_session(client):
    with client.session_transaction() as sess:
        sess['score'] = '8.5'
        sess['strengths'] = 'Giao tiếp tốt'
        sess['weaknesses'] = 'Cần cải thiện kỹ thuật'

    response = client.get('/summary')
    assert response.status_code == 200
    data_str = response.data.decode('utf-8')
    assert '8.5' in data_str
    assert 'Giao tiếp tốt' in data_str
    assert 'Cần cải thiện kỹ thuật' in data_str
