from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

def create_driver():

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')

    chromedriver_autoinstaller.install()
    service = Service()
    return webdriver.Chrome(service=service, options=options)

def test_successful_auth():
    driver = create_driver()
    try:
        driver.get("https://localhost:2443")
        wait = WebDriverWait(driver, 5)
        time.sleep(2)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("root")
        password = driver.find_element(By.ID, "password")
        password.send_keys("0penBmc")

        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
        login_btn.click()
        time.sleep(5)
        print("[v] Тест 'Успешная авторизация' пройден")
    finally:
        driver.quit()

def test_invalid_login():
    driver = create_driver()
    try:
        driver.get("https://localhost:2443")
        wait = WebDriverWait(driver, 5)
        time.sleep(2)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("rota_подъем")
        password = driver.find_element(By.ID, "password")
        password.send_keys("xdxdxd")

        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
        login_btn.click()
        time.sleep(3)
        error_msg = wait.until(EC.presence_of_element_located((By.ID, "username")))
        time.sleep(3)
        print("[v] Тест 'Неверные данные' пройден", error_msg.text)
    finally:
        driver.quit()

def test_power_control():
    driver = create_driver()
    try:
        driver.get("https://localhost:2443")
        wait = WebDriverWait(driver, 5)
        time.sleep(2)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("root")
        password = driver.find_element(By.ID, "password")
        password.send_keys("0penBmc")

        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
        login_btn.click()

        time.sleep(3)
        power_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Power')]")
        power_link.click()
        power_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Power on')]")))
        power_btn.click()

        time.sleep(3)
        print("[v] Тест 'Управление питанием' пройден")

    finally:
        driver.quit()

def test_resources_display():
    driver = create_driver()
    try:
        driver.get("https://localhost:2443")
        wait = WebDriverWait(driver, 5)
        time.sleep(2)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("root")
        password = driver.find_element(By.ID, "password")
        password.send_keys("0penBmc")

        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]")))
        login_btn.click()

        time.sleep(3)
        menu_trigger_btn = wait.until(EC.element_to_be_clickable((By.ID, "app-header-trigger")))
        menu_trigger_btn.click()

        hardware = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Hardware status')]")))
        hardware.click()

        invbutton = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Inventory and LEDs')]")))
        invbutton.click()

        time.sleep(5)
        print("[v] Тест 'Инвентаризация' пройден")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_successful_auth()
    test_invalid_login()
    time.sleep(5)
    test_power_control()
    test_resources_display()
    print("\n[v] Все тесты завершены!")
