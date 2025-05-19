import sys
import os

# Thêm đường dẫn thư mục gốc (src) vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DAO.user_dao import get_user_by_id, get_user_interview_history

print("📌 Test lấy người dùng theo mã:")
user = get_user_by_id(1)
print(user)

print("\n📌 Test truy xuất lịch sử phỏng vấn:")
history = get_user_interview_history(1)
for item in history:
    print(item)
