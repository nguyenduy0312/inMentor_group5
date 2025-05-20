import pytest
from DAO.bao_cao_danh_gia_dao import create_report, get_report_by_session
from DataBase.connectdb import create_connection

# ✅ Test thêm báo cáo đánh giá vào một phiên hợp lệ
def test_create_report_valid_session():
    # Tạo phiên mới
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau)
        VALUES (1, 'dang_dien_ra', NOW())
    """)
    conn.commit()
    ma_phien = cursor.lastrowid

    # Gọi hàm để thêm báo cáo
    ma_bao_cao = create_report(
        ma_phien=ma_phien,
        diem_tong=8.5,
        nhan_xet="Ứng viên khá tốt.",
        diem_manh="Kỹ năng giao tiếp",
        diem_yeu="Thiếu kiến thức chuyên sâu",
        goi_y_cai_thien="Nên học thêm về hệ điều hành"
    )

    # Kiểm tra tồn tại trong DB
    cursor.execute("SELECT * FROM Bao_Cao_Danh_Gia WHERE Ma_Bao_Cao = %s", (ma_bao_cao,))
    result = cursor.fetchone()
    assert result is not None

    # Dọn dẹp
    cursor.execute("DELETE FROM Bao_Cao_Danh_Gia WHERE Ma_Bao_Cao = %s", (ma_bao_cao,))
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test thêm báo cáo với phiên KHÔNG tồn tại
def test_create_report_invalid_session():
    invalid_session_id = -1  # Giả định không tồn tại
    with pytest.raises(Exception):
        create_report(
            ma_phien=invalid_session_id,
            diem_tong=7.0,
            nhan_xet="Không hợp lệ",
            diem_manh="Không có",
            diem_yeu="Không có",
            goi_y_cai_thien="Không có"
        )

# ✅ Test lấy báo cáo theo mã phiên có dữ liệu
def test_get_report_by_session_with_data():
    # Tạo phiên mới
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau)
        VALUES (1, 'da_hoan_thanh', NOW())
    """)
    conn.commit()
    ma_phien = cursor.lastrowid

    # Thêm báo cáo cho phiên đó
    ma_bao_cao = create_report(
        ma_phien=ma_phien,
        diem_tong=9.0,
        nhan_xet="Xuất sắc",
        diem_manh="Phân tích tốt",
        diem_yeu="Không rõ",
        goi_y_cai_thien="Nên giữ phong độ"
    )

    # Gọi hàm lấy báo cáo
    result = get_report_by_session(ma_phien)
    assert isinstance(result, dict)
    assert result['Ma_Phien'] == ma_phien
    assert result['Diem_Tong'] == 9.0

    # Dọn dẹp
    cursor.execute("DELETE FROM Bao_Cao_Danh_Gia WHERE Ma_Bao_Cao = %s", (ma_bao_cao,))
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test lấy báo cáo khi phiên có nhưng KHÔNG có báo cáo
def test_get_report_by_session_no_report():
    # Tạo phiên mới nhưng không tạo báo cáo
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Trang_Thai, Thoi_Gian_Bat_Dau)
        VALUES (1, 'dang_dien_ra', NOW())
    """)
    conn.commit()
    ma_phien = cursor.lastrowid

    result = get_report_by_session(ma_phien)
    assert result is None

    # Dọn dẹp
    cursor.execute("DELETE FROM phien_phong_van WHERE Ma_Phien = %s", (ma_phien,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Test lấy báo cáo khi phiên KHÔNG tồn tại
def test_get_report_by_session_invalid():
    invalid_session_id = -1  # Không tồn tại
    result = get_report_by_session(invalid_session_id)
    assert result is None
