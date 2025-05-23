from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os

def test_trangchu_workflow():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/trangchu")  # Sửa lại URL nếu khác

    # 1. Kiểm tra tiêu đề trang
    assert "inMentor" in driver.title

    # 2. Chọn lĩnh vực và chế độ
    select_linhvuc = Select(driver.find_element(By.ID, "linhvuc"))
    select_linhvuc.select_by_visible_text("Phân tích dữ liệu")

    select_chedo = Select(driver.find_element(By.ID, "chedo"))
    select_chedo.select_by_visible_text("Văn bản")

    # 3. Nhấn nút "Bắt đầu phỏng vấn"
    start_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Bắt đầu phỏng vấn')]")
    start_btn.click()
    time.sleep(1)

    assert "chatbot" in driver.current_url

    # 4. Quay lại trang chính
    driver.get("http://localhost:5000/trangchu")

    # 5. Upload CV
    upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
    fake_cv_path = os.path.abspath("tests/sample_cv.pdf")
    upload_input.send_keys(fake_cv_path)

    upload_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Tải CV lên')]")
    upload_btn.click()
    time.sleep(1)

    # 6. Làm bài kiểm tra kỹ năng
    select_kynang = Select(driver.find_element(By.ID, "kynang"))
    select_kynang.select_by_visible_text("Python")

    test_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Bắt đầu kiểm tra')]")
    test_btn.click()
    time.sleep(1)

    # 7. Xem tiến độ
    xem_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Xem chi tiết')]")
    xem_btn.click()
    time.sleep(1)

    driver.quit()
