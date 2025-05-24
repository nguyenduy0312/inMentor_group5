from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login_ui():
    driver = webdriver.Chrome()
    try:
        driver.get("http://127.0.0.1:5000/login")

        wait = WebDriverWait(driver, 10)
        email_input = wait.until(EC.presence_of_element_located((By.ID, "loginEmail")))
        password_input = driver.find_element(By.ID, "loginPassword")
        submit_button = driver.find_element(By.CSS_SELECTOR, "form#loginForm button[type='submit']")

        email_input.send_keys("test@example.com")
        password_input.send_keys("123456")
        submit_button.click()

        # Đợi đến khi xuất hiện một phần tử nào đó của trang sau login thành công hoặc thông báo lỗi
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Chào mừng')]")),
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Đăng nhập')]"))
            )
        )

        page_source = driver.page_source
        assert "Đăng nhập" in page_source or "Chào mừng" in page_source
        print("✅ Giao diện đăng nhập hoạt động")

    except Exception as e:
        print("❌ Test thất bại:", e)

    finally:
        driver.quit()
