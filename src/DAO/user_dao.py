# dao/user_dao.py
from model.user import User

class UserDAO:
    def __init__(self, connection):
        self.conn = connection

    def get_by_id(self, ma_nguoi_dung):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE Ma_Nguoi_Dung = %s", (ma_nguoi_dung,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def insert(self, user: User):
        cursor = self.conn.cursor()
        sql = """INSERT INTO user(Ho_Ten, NgaySinh, GioiTinh, Email, SoDienThoai, 
                                  TenDangNhap, Mat_Khau, Picture, Hoan_Thanh_Ho_So)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (user.Ho_Ten, user.NgaySinh, user.GioiTinh, user.Email,
                             user.SoDienThoai, user.TenDangNhap, user.Mat_Khau,
                             user.Picture, user.Hoan_Thanh_Ho_So))
        self.conn.commit()
