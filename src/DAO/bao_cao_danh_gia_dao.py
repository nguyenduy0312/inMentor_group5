import mysql.connector
from DataBase.connectdb import create_connection

# Thêm báo cáo đánh giá mới
def create_report(ma_phien, diem_tong, nhan_xet, diem_manh, diem_yeu, goi_y_cai_thien):
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Bao_Cao_Danh_Gia (
            Ma_Phien, Diem_Tong, Nhan_Xet, Diem_Manh, Diem_Yeu, Goi_Y_Cai_Thien
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (ma_phien, diem_tong, nhan_xet, diem_manh, diem_yeu, goi_y_cai_thien))
    conn.commit()
    ma_bao_cao = cursor.lastrowid

    cursor.close()
    conn.close()
    return ma_bao_cao


# Lấy báo cáo theo mã phiên
def get_report_by_session(ma_phien):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM Bao_Cao_Danh_Gia WHERE Ma_Phien = %s"
    cursor.execute(sql, (ma_phien,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result
