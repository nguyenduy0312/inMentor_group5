# dao/api_khoa_dao.py
from model.api_khoa import APIKhoa # type: ignore

class APIKhoaDAO:
    def __init__(self, connection):
        self.conn = connection

    def get_by_user(self, ma_nguoi_dung):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM api_khoa WHERE Ma_Nguoi_Dung = %s", (ma_nguoi_dung,))
        row = cursor.fetchone()
        return APIKhoa(*row) if row else None

    def validate_api_key(self, api_key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM api_khoa WHERE API_Khoa = %s AND Trang_Thai = 'ACTIVE'", (api_key,))
        return cursor.fetchone() is not None
