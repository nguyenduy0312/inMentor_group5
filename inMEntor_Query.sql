
-- Table `inmentor`.`bao_cao_danh_gia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `inmentor`.`bao_cao_danh_gia` (
  `Ma_Bao_Cao` INT NOT NULL AUTO_INCREMENT,
  `Diem_Tong` INT NULL DEFAULT '0',
  `Nhan_Xet` TEXT NULL DEFAULT NULL,
  `Diem_Manh` TEXT NULL DEFAULT NULL,
  `Diem_Yeu` TEXT NULL DEFAULT NULL,
  `Goi_Y_Cai_Thien` TEXT NULL DEFAULT NULL,
  `Ngay_Tao` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Ma_Bao_Cao`));



-- -----------------------------------------------------
-- Table `inmentor`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `inmentor`.`user` (
  `Ma_Nguoi_Dung` INT NOT NULL AUTO_INCREMENT,
  `Ho_Ten` VARCHAR(255) NOT NULL,
  `NgaySinh` DATE NOT NULL,
  `GioiTinh` VARCHAR(50) NOT NULL,
  `Email` VARCHAR(255) NOT NULL,
  `SoDienThoai` VARCHAR(15) NULL DEFAULT NULL,
  `TenDangNhap` VARCHAR(50) NOT NULL,
  `Mat_Khau` VARCHAR(255) NOT NULL,
  `Picture` MEDIUMBLOB NULL DEFAULT NULL,
  `Hoan_Thanh_Ho_So` TINYINT NULL DEFAULT '0',
  PRIMARY KEY (`Ma_Nguoi_Dung`),
  UNIQUE INDEX `Email` (`Email` ASC) VISIBLE,
  UNIQUE INDEX `TenDangNhap` (`TenDangNhap` ASC) VISIBLE);



-- -----------------------------------------------------
-- Table `inmentor`.`phien_phong_van`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `inmentor`.`phien_phong_van` (
  `Ma_Phien` INT NOT NULL AUTO_INCREMENT,
  `Thoi_Gian_Bat_Dau` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `Thoi_Gian_Ket_Thuc` TIMESTAMP NULL DEFAULT NULL,
  `Trang_Thai` ENUM('dang_dien_ra', 'da_hoan_thanh', 'that_bai') NULL DEFAULT 'dang_dien_ra',
  `user_Ma_Nguoi_Dung` INT NOT NULL,
  `bao_cao_danh_gia_Ma_Bao_Cao` INT NOT NULL,
  PRIMARY KEY (`Ma_Phien`, `user_Ma_Nguoi_Dung`, `bao_cao_danh_gia_Ma_Bao_Cao`),
  INDEX `fk_phien_phong_van_user1_idx` (`user_Ma_Nguoi_Dung` ASC) VISIBLE,
  INDEX `fk_phien_phong_van_bao_cao_danh_gia1_idx` (`bao_cao_danh_gia_Ma_Bao_Cao` ASC) VISIBLE,
  CONSTRAINT `fk_phien_phong_van_user1`
    FOREIGN KEY (`user_Ma_Nguoi_Dung`)
    REFERENCES `inmentor`.`user` (`Ma_Nguoi_Dung`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_phien_phong_van_bao_cao_danh_gia1`
    FOREIGN KEY (`bao_cao_danh_gia_Ma_Bao_Cao`)
    REFERENCES `inmentor`.`bao_cao_danh_gia` (`Ma_Bao_Cao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE phien_phong_van
ADD COLUMN Ma_Linh_Vuc INT;

-- Tạo ràng buộc khóa ngoại
ALTER TABLE phien_phong_van
ADD CONSTRAINT fk_phien_linhvuc
FOREIGN KEY (Ma_Linh_Vuc)
REFERENCES linh_vuc_ky_nang(Ma_Linh_Vuc)
ON DELETE SET NULL
ON UPDATE CASCADE;


-- -----------------------------------------------------
-- Table `inmentor`.`cau_hoi_tra_loi`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `inmentor`.`cau_hoi_tra_loi` (
  `Ma_Cau_Tra_Loi` INT NOT NULL AUTO_INCREMENT,
  `Cau_Hoi` TEXT NOT NULL,
  `Tra_Loi` TEXT NOT NULL,
  `phien_phong_van_Ma_Phien` INT NOT NULL,
  `phien_phong_van_user_Ma_Nguoi_Dung` INT NOT NULL,
  `phien_phong_van_bao_cao_danh_gia_Ma_Bao_Cao` INT NOT NULL,
  PRIMARY KEY (`Ma_Cau_Tra_Loi`, `phien_phong_van_Ma_Phien`, `phien_phong_van_user_Ma_Nguoi_Dung`, `phien_phong_van_bao_cao_danh_gia_Ma_Bao_Cao`),
  INDEX `fk_cau_hoi_tra_loi_phien_phong_van1_idx` (`phien_phong_van_Ma_Phien` ASC, `phien_phong_van_user_Ma_Nguoi_Dung` ASC, `phien_phong_van_bao_cao_danh_gia_Ma_Bao_Cao` ASC) VISIBLE,
  CONSTRAINT `fk_cau_hoi_tra_loi_phien_phong_van1`
    FOREIGN KEY (`phien_phong_van_Ma_Phien` , `phien_phong_van_user_Ma_Nguoi_Dung` , `phien_phong_van_bao_cao_danh_gia_Ma_Bao_Cao`)
    REFERENCES `inmentor`.`phien_phong_van` (`Ma_Phien` , `user_Ma_Nguoi_Dung` , `bao_cao_danh_gia_Ma_Bao_Cao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE cau_hoi_tra_loi
ADD COLUMN Ma_Phien INT;

-- Tạo ràng buộc khóa ngoại
ALTER TABLE cau_hoi_tra_loi
ADD CONSTRAINT fk_cauhoi_phien
FOREIGN KEY (Ma_Phien)
REFERENCES phien_phong_van(Ma_Phien)
ON DELETE CASCADE
ON UPDATE CASCADE;


-- -----------------------------------------------------
-- Table `inmentor`.`linh_vuc_ky_nang`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `inmentor`.`linh_vuc_ky_nang` (
  `Ma_Linh_Vuc` INT NOT NULL AUTO_INCREMENT,
  `Ten_Linh_Vuc` VARCHAR(255) NOT NULL,
  `Mo_Ta` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`Ma_Linh_Vuc`))

