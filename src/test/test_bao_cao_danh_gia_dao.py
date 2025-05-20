import sys
import os

# Thêm đường dẫn thư mục src vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DAO.bao_cao_danh_gia_dao import create_report, get_report_by_session
from DAO.phien_phong_van_dao import create_interview_session
from DataBase.connectdb import create_connection, close_connection
# Kết nối tới database

print("Tạo phiên mới...")
ma_phien = create_interview_session(ma_nguoi_dung=1)
print(f"Mã phiên: {ma_phien}")

print("Thêm báo cáo...")
ma_bao_cao = create_report(
    ma_phien=ma_phien,
    diem_tong=8,
    nhan_xet="Ứng viên thể hiện tốt, cần cải thiện thêm về kỹ năng giải thích.",
    diem_manh="Tư duy logic, trả lời mạch lạc",
    diem_yeu="Thiếu ví dụ cụ thể",
    goi_y_cai_thien="Tập trung luyện kỹ năng coding và giải thích rõ hơn"
)
print(f"Mã báo cáo: {ma_bao_cao}")

print("Lấy báo cáo theo mã phiên...")
bao_cao = get_report_by_session(ma_phien)
print(bao_cao)
