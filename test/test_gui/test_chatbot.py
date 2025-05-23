from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


def test_chatbot_flow():
    # 1. Khởi tạo trình duyệt
    driver = webdriver.Chrome()  # Hoặc Firefox() nếu dùng Firefox
    driver.get("http://127.0.0.1:5000/chatbot")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    try:
        # 2. Chọn lĩnh vực nghề nghiệp
        career_select = wait.until(EC.presence_of_element_located((By.ID, "career-select")))
        Select(career_select).select_by_visible_text("Frontend")
        time.sleep(1)

        # 3. Nhập tin nhắn đầu tiên
        user_input = driver.find_element(By.ID, "user-input")
        user_input.send_keys("Xin chào")

        send_button = driver.find_element(By.ID, "send-button")
        send_button.click()

        # 4. Đợi phản hồi của AI
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ai")))

        # 5. Gửi thêm tin nhắn
        user_input.send_keys("Tôi có 2 năm kinh nghiệm ReactJS")
        send_button.click()

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ai")))

        # 6. Kiểm tra hiển thị nút "Kết thúc"
        try:
            end_button = driver.find_element(By.ID, "end-button")
            if end_button.is_displayed():
                print("✅ Nút 'Kết thúc' đã hiển thị.")
            else:
                print("⚠️ Nút 'Kết thúc' chưa hiển thị.")
        except:
            print("❌ Không tìm thấy nút 'Kết thúc'.")

        # 7. (Tùy chọn) Click nút kết thúc để quay về trang chủ
        end_button.click()
        time.sleep(1)
        assert "trangchu" in driver.current_url.lower()
        print("✅ Điều hướng về trang chủ thành công.")

        print("🎉 TEST PASSED!")

    except Exception as e:
        print(f"❌ Lỗi khi chạy test: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_chatbot_flow()
