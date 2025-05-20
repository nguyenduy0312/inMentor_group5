import mysql.connector
from DataBase.connectdb import create_connection

def get_user_by_id(ma_nguoi_dung): # Lấy thông tin người dùng theo ID
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM user WHERE Ma_Nguoi_Dung = %s"
    cursor.execute(sql, (ma_nguoi_dung,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_interview_history(ma_nguoi_dung): # Lấy lịch sử phỏng vấn của người dùng
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT 
            p.Ma_Phien,
            p.Thoi_Gian_Bat_Dau,
            p.Thoi_Gian_Ket_Thuc,
            p.Trang_Thai,
            b.Diem_Tong,
            b.Nhan_Xet,
            b.Diem_Manh,
            b.Diem_Yeu,
            b.Goi_Y_Cai_Thien
        FROM phien_phong_van p
        LEFT JOIN bao_cao_danh_gia b ON p.Ma_Phien = b.Ma_Phien
        WHERE p.Ma_Nguoi_Dung = %s
        ORDER BY p.Thoi_Gian_Bat_Dau DESC
    """

    cursor.execute(sql, (ma_nguoi_dung,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()
    return history
