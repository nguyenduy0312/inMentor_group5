# dao/phien_phong_van_dao.py
from model.phien_phong_van import PhienPhongVan

class PhienPhongVanDAO:
    def __init__(self, connection):
        self.conn = connection

    def get_by_user(self, ma_nguoi_dung):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM phien_phong_van WHERE Ma_Nguoi_Dung = %s", (ma_nguoi_dung,))
        return cursor.fetchall()

    def insert(self, phien: PhienPhongVan):
        cursor = self.conn.cursor()
        sql = """INSERT INTO phien_phong_van (Ma_Nguoi_Dung, Thoi_Gian_Bat_Dau, 
                 Thoi_Gian_Ket_Thuc, Trang_Thai, Diem_Tong, Nhan_Xet, 
                 bao_cao_danh_gia_Ma_Bao_Cao)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (phien.Ma_Nguoi_Dung, phien.Thoi_Gian_Bat_Dau,
                             phien.Thoi_Gian_Ket_Thuc, phien.Trang_Thai,
                             phien.Diem_Tong, phien.Nhan_Xet,
                             phien.Ma_Bao_Cao))
        self.conn.commit()
