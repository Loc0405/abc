import time
import pytest
import mysql.connector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Cấu hình Database và URL
MY_DB = {
    "host": "localhost",
    "user": "root",
    "password": "", 
}
DB_NAME = "db_test_cau3"
URL = "https://www.demoblaze.com"

@pytest.fixture(scope="module")
def db():
    """Khởi tạo Database MySQL và bảng kết quả"""
    conn = mysql.connector.connect(**MY_DB)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_result (
            stt INTEGER PRIMARY KEY AUTO_INCREMENT,
            TenBai TEXT,
            Link TEXT
        )
    """)
    conn.commit()

    yield conn, cursor

    cursor.close()
    conn.close()

@pytest.fixture(scope="module")
def driver():
    """Khởi tạo trình duyệt Edge"""
    drv = webdriver.Edge()  
    drv.maximize_window()
    yield drv
    drv.quit()

def find_product_link(drv, ten_sp, max_pages=10):
    """
    Tìm sản phẩm theo tên trên demoblaze bằng cách duyệt nhiều trang (Next).
    Trả về link nếu thấy, ngược lại trả về None.
    """
    wait = WebDriverWait(drv, 10)
    drv.get(URL)

    for _ in range(max_pages):
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))

        cards = drv.find_elements(By.CLASS_NAME, "card-title")
        for sp in cards:
            a_tag = sp.find_element(By.TAG_NAME, "a")
            if ten_sp.lower() in sp.text.lower():
                return a_tag.get_attribute("href")
        try:
            # Nhấn nút Next để sang trang tiếp theo
            next_btn = wait.until(EC.element_to_be_clickable((By.ID, "next2")))
            drv.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            drv.execute_script("arguments[0].click();", next_btn)
            time.sleep(1.2)
        except TimeoutException:
            return None

    return None

def test_tim_kiem(driver, db):
    """Bài test chính: Tìm kiếm sản phẩm và lưu vào Database"""
    conn, cursor = db
    ds = ["Samsung galaxy s6", "Nokia lumia 1520", "Sony xperia z5"]

    for TenBai in ds:
        Link = find_product_link(driver, TenBai, max_pages=10)
        print(f"{TenBai} -> {Link}")

        assert Link is not None, f"Không tìm thấy sản phẩm chứa: {TenBai}"

        cursor.execute(
            "INSERT INTO test_result (TenBai, Link) VALUES (%s, %s)",
            (TenBai, Link)
        )
        conn.commit()
if __name__ == "__main__":
    print("\n--- Đang bắt đầu chạy kiểm thử Selenium & MySQL (Câu 3)... ---")
    pytest.main([__file__])