from flask import Flask, request, jsonify
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# Hàm kết nối DB
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database"
    )

@app.route('/api/create_interview', methods=['POST'])
def create_interview():
    data = request.get_json()
    ma_nguoi_dung = data.get("ma_nguoi_dung")

    if not ma_nguoi_dung:
        return jsonify({"error": "Thiếu mã người dùng"}), 400

    try:
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify({"ma_phien": ma_phien}), 201

