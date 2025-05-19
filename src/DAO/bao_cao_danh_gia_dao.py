# dao/bao_cao_danh_gia_dao.py
from model.bao_cao_danh_gia import BaoCaoDanhGia

class BaoCaoDanhGiaDAO:
    def __init__(self, connection):
        self.conn = connection

    def insert(self, bao_cao: BaoCaoDanhGia):
        cursor = self.conn.cursor()
        sql = """INSERT INTO bao_cao_danh_gia(Tong_Quan, Diem_Manh, Diem_Yeu, 
                 Goi_Y_Cai_Thien, Ngay_Tao)
                 VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (bao_cao.Tong_Quan, bao_cao.Diem_Manh,
                             bao_cao.Diem_Yeu, bao_cao.Goi_Y_Cai_Thien,
                             bao_cao.Ngay_Tao))
        self.conn.commit()
        return cursor.lastrowid

    def get_by_id(self, ma_bao_cao):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bao_cao_danh_gia WHERE Ma_Bao_Cao = %s", (ma_bao_cao,))
        row = cursor.fetchone()
        return BaoCaoDanhGia(*row) if row else None
