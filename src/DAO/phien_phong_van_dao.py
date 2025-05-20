import mysql.connector
from datetime import datetime
from DataBase.connectdb import create_connection  # Hàm kết nối DB

def create_interview_session(ma_nguoi_dung):
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Thoi_Gian_Bat_Dau, Trang_Thai)
        VALUES (%s, %s, %s)
    """
    thoi_gian_bat_dau = datetime.now()
    cursor.execute(sql, (ma_nguoi_dung, thoi_gian_bat_dau, 'dang_dien_ra'))
    conn.commit()

    ma_phien = cursor.lastrowid
    cursor.close()
    conn.close()
    return ma_phien

def end_interview_session(ma_phien):
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE phien_phong_van
        SET Thoi_Gian_Ket_Thuc = %s, Trang_Thai = %s
        WHERE Ma_Phien = %s
    """
    thoi_gian_ket_thuc = datetime.now()
    cursor.execute(sql, (thoi_gian_ket_thuc, 'hoan_thanh', ma_phien))
    conn.commit()

    cursor.close()
    conn.close()

def get_session_by_user(ma_nguoi_dung):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM phien_phong_van
        WHERE Ma_Nguoi_Dung = %s
        ORDER BY Thoi_Gian_Bat_Dau DESC
    """
    cursor.execute(sql, (ma_nguoi_dung,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result
