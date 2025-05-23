from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_trang_web(driver):
    driver.get("http://localhost:5000/trangweb")  # đổi thành URL của bạn
    wait = WebDriverWait(driver, 10)

    # 1. Kiểm tra username hiển thị đúng
    username_elem = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    username_text = username_elem.text
    assert username_text != ""

    # 2. Kiểm tra click menu nav active đúng
    nav_links = driver.find_elements(By.CLASS_NAME, "nav-link")
    nav_links[0].click()
    time.sleep(1)
    assert "active" in nav_links[0].get_attribute("class")

    nav_links[-1].click()
    time.sleep(1)
    assert "active" in nav_links[-1].get_attribute("class")

    # 3. Kiểm tra scroll animation
    scroll_element = driver.find_element(By.CLASS_NAME, "scroll-animation")
    classes_before = scroll_element.get_attribute("class")
    assert "animate" not in classes_before

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    classes_after = scroll_element.get_attribute("class")
    assert "animate" in classes_after

    # 4. Kiểm tra dropdown skill chuyển trang đúng
    skill_select = Select(driver.find_element(By.ID, "skill-select"))
    skill_select.select_by_value("https://example.com/page2")  # chọn giá trị đúng của bạn

    wait.until(EC.url_contains("page2"))
    assert "page2" in driver.current_url
