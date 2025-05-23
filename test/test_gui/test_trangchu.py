from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def test_trangchu_workflow():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)  # đợi tối đa 10s

    driver.get("http://localhost:5000/trangchu")

    # 1. Kiểm tra tiêu đề trang
    assert "inMentor" in driver.title

    # 2. Chọn lĩnh vực và chế độ
    select_linhvuc = wait.until(EC.presence_of_element_located((By.ID, "linhvuc")))
    Select(select_linhvuc).select_by_visible_text("Phân tích dữ liệu")

    select_chedo = wait.until(EC.presence_of_element_located((By.ID, "chedo")))
    Select(select_chedo).select_by_visible_text("Văn bản")

    # 3. Nhấn nút "Bắt đầu phỏng vấn"
    start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Bắt đầu phỏng vấn')]")))
    start_btn.click()

    wait.until(EC.url_contains("chatbot"))
    assert "chatbot" in driver.current_url

    # 4. Quay lại trang chính
    driver.get("http://localhost:5000/trangchu")

    # 5. Upload CV
    upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    fake_cv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_cv.pdf"))
    print("Đường dẫn file CV:", fake_cv_path)
    print("File tồn tại:", os.path.exists(fake_cv_path))
    upload_input.send_keys(fake_cv_path)

    upload_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tải CV lên')]")))
    upload_btn.click()

    # 6. Làm bài kiểm tra kỹ năng
    select_kynang = wait.until(EC.presence_of_element_located((By.ID, "kynang")))
    Select(select_kynang).select_by_visible_text("Python")

    test_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Bắt đầu kiểm tra')]")))
    test_btn.click()

    # 7. Xem tiến độ
    xem_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Xem chi tiết')]")))
    xem_btn.click()

    driver.quit()
