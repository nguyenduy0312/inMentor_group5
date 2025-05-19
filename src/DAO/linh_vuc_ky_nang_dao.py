# dao/linh_vuc_ky_nang_dao.py
from model.linh_vuc_ky_nang import LinhVucKyNang

class LinhVucKyNangDAO:
    def __init__(self, connection):
        self.conn = connection

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM linh_vuc_ky_nang")
        return [LinhVucKyNang(*row) for row in cursor.fetchall()]
