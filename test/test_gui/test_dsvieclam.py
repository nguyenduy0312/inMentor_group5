from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_job_list_and_interview_button():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/dsvieclam")  # URL trang danh sách việc làm
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        # Đợi trang tải và kiểm tra tiêu đề
        wait.until(EC.title_contains("inMentor - Việc làm"))

        # Kiểm tra có ít nhất 1 job card
        jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#jobList > div")))
        assert len(jobs) > 0
        print(f"✅ Tìm thấy {len(jobs)} việc làm hiển thị.")

        # Test filter: chọn location "Hà Nội"
        location_filter = Select(driver.find_element(By.ID, "locationFilter"))
        location_filter.select_by_visible_text("Hà Nội")
        time.sleep(1)  # chờ JS render lại
        filtered_jobs = driver.find_elements(By.CSS_SELECTOR, "#jobList > div")
        assert all("Hà Nội" in job.text for job in filtered_jobs)
        print("✅ Bộ lọc địa điểm hoạt động đúng.")

        # Test filter: chọn ngành nghề "Frontend"
        industry_filter = Select(driver.find_element(By.ID, "industryFilter"))
        industry_filter.select_by_visible_text("Frontend")
        time.sleep(1)
        filtered_jobs = driver.find_elements(By.CSS_SELECTOR, "#jobList > div")
        assert all("Frontend" in job.text for job in filtered_jobs)
        print("✅ Bộ lọc ngành nghề hoạt động đúng.")

        # Test nút "Phỏng vấn ảo" khi chưa đăng nhập: phải alert và chuyển tới /login
        interview_btn = driver.find_element(By.CSS_SELECTOR, ".interview-btn")
        interview_btn.click()

        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        assert "Vui lòng đăng nhập" in alert_text
        alert.accept()

        wait.until(EC.url_contains("/login"))
        print("✅ Chưa đăng nhập, click Phỏng vấn ảo chuyển tới /login và cảnh báo hiện đúng.")

        # Giả lập đăng nhập bằng localStorage (ví dụ username = testuser)
        driver.execute_script("window.localStorage.setItem('username', 'testuser');")
        driver.get("http://127.0.0.1:5000/dsvieclam")
        time.sleep(1)

        # Click nút "Phỏng vấn ảo" khi đã đăng nhập: chuyển tới /chatbot
        interview_btn = driver.find_element(By.CSS_SELECTOR, ".interview-btn")
        interview_btn.click()
        wait.until(EC.url_contains("/chatbot"))
        print("✅ Đã đăng nhập, click Phỏng vấn ảo chuyển tới trang chatbot thành công.")

        print("🎉 Test hoàn tất thành công!")

    except Exception as e:
        print("❌ Test lỗi:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_job_list_and_interview_button()
    
    import pytest

if __name__ == "__main__":
    pytest.main()

