from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import traceback

def test_chatbot_flow():
    driver = webdriver.Chrome()  # Đảm bảo đã cài ChromeDriver và đúng version
    driver.get("http://127.0.0.1:5000/chatbot")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Chọn lĩnh vực nghề nghiệp
        career_select = wait.until(EC.presence_of_element_located((By.ID, "career-select")))
        Select(career_select).select_by_visible_text("Frontend")

        # 2. Nhập tin nhắn đầu tiên
        user_input = wait.until(EC.presence_of_element_located((By.ID, "user-input")))
        send_button = wait.until(EC.element_to_be_clickable((By.ID, "send-button")))
        user_input.send_keys("Xin chào")
        send_button.click()

        # 3. Đợi phản hồi từ AI
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ai")))

        # 4. Gửi tin nhắn thứ hai
        user_input = wait.until(EC.presence_of_element_located((By.ID, "user-input")))
        user_input.send_keys("Tôi có 2 năm kinh nghiệm ReactJS")
        send_button.click()

        # 5. Đợi phản hồi từ AI lần nữa
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ai")))

        # 6. Kiểm tra nút 'Kết thúc'
        end_button = wait.until(EC.visibility_of_element_located((By.ID, "end-button")))
        driver.execute_script("arguments[0].scrollIntoView();", end_button)
        wait.until(EC.element_to_be_clickable((By.ID, "end-button")))

        if end_button.is_displayed():
            print("✅ Nút 'Kết thúc' đã hiển thị.")
        else:
            print("⚠️ Nút 'Kết thúc' chưa hiển thị.")

        # 7. Click nút 'Kết thúc' và kiểm tra điều hướng về trang chủ
        end_button.click()
        wait.until(EC.url_contains("trangchu"))
        print("✅ Điều hướng về trang chủ thành công.")

        print("🎉 TEST PASSED!")

    except Exception as e:
        print(f"❌ Lỗi khi chạy test: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    test_chatbot_flow()
