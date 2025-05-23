import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Bỏ dòng này nếu muốn thấy trình duyệt
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_trangweb_content(driver):
    driver.get("http://localhost:5000/trangweb")
    wait = WebDriverWait(driver, 10)

    # 1. Kiểm tra tiêu đề trang
    assert "Giới thiệu" in driver.title
    print("✅ Tiêu đề trang hợp lệ:", driver.title)

    # 2. Kiểm tra phần tử chứa nội dung chính
    main_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "n-n-t-ng-AI-luy-n-t")))
    assert "Nền tảng AI" in main_title.text
    print("✅ Tiêu đề chính:", main_title.text.strip())

    # 3. Kiểm tra nút "Khám phá ngay"
    explore_btn = driver.find_element(By.CLASS_NAME, "text-wrapper-2")
    assert explore_btn.tag_name == "a"
    assert "Khám phá ngay" in explore_btn.text
    print("✅ Nút 'Khám phá ngay' tồn tại")

    # 4. Kiểm tra các section tiêu biểu như "Về chúng tôi"
    sections = driver.find_elements(By.CLASS_NAME, "scroll-animation")
    assert len(sections) > 0
    print(f"✅ Tìm thấy {len(sections)} phần tử có class 'scroll-animation'")

    # 5. Kiểm tra hình ảnh chính có tồn tại
    img = driver.find_element(By.CLASS_NAME, "bussinessman")
    assert img.get_attribute("src").startswith("http")
    print("✅ Ảnh chính hiển thị:", img.get_attribute("src"))
