import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Địa chỉ server DB, thường là localhost
            user='root',            # Tên user MySQL của bạn
            password='123456789',  # Mật khẩu MySQL của bạn
            database='inmentor'     # Tên database bạn đã tạo
        )
        if connection.is_connected():
            print("Kết nối MySQL thành công")
            return connection
    except Error as e:
        print(f"Lỗi khi kết nối MySQL: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Đã đóng kết nối MySQL")

