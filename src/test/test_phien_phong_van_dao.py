import sys
import os

# Thêm đường dẫn thư mục gốc (src) vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from DAO.phien_phong_van_dao import create_interview_session, end_interview_session, get_session_by_user
from DataBase.connectdb import create_connection, close_connection

print("Tạo phiên...")
ma_phien = create_interview_session(1)
print(f"Phiên mới: {ma_phien}")

print("Kết thúc...")
end_interview_session(ma_phien)

print("Lịch sử của người dùng:")
for p in get_session_by_user(1):
    print(p)
