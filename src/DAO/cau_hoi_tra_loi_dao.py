import mysql.connector
from DataBase.connectdb import create_connection

# Thêm câu hỏi và trả lời vào một phiên
def add_question_answer(ma_phien, cau_hoi, tra_loi):
    print(f"[LOG] Thêm vào DB: Ma_Phiên={ma_phien}, Cau_Hoi={cau_hoi}, Tra_Loi={tra_loi}")
    conn = create_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO cau_hoi_tra_loi (Ma_Phiên, Cau_Hoi, Tra_Loi)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (ma_phien, cau_hoi, tra_loi))
    conn.commit()

    cursor.close()
    conn.close()

# Lấy tất cả câu hỏi-trả lời của một phiên
def get_questions_answers_by_session(ma_phien):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM cau_hoi_tra_loi
        WHERE Ma_Phiên = %s
        ORDER BY Ma_Cau_Tra_Loi ASC
    """
    cursor.execute(sql, (ma_phien,))
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result