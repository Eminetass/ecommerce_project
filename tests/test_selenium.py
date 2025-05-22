import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_home_page_title(chrome_driver, app):
    with app.test_server():
        chrome_driver.get('http://localhost:5000')
        assert 'E-Commerce' in chrome_driver.title

def test_login_form(chrome_driver, app):
    with app.test_server():
        chrome_driver.get('http://localhost:5000/login')
        try:
            # Wait for email input to be present
            email_input = WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_input = chrome_driver.find_element(By.NAME, "password")
            submit_button = chrome_driver.find_element(By.XPATH, "//button[@type='submit']")
            
            # Test form interaction
            email_input.send_keys("test@example.com")
            password_input.send_keys("testpassword")
            submit_button.click()
            
            # Wait for either success message or error message
            WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert"))
            )
            
        except TimeoutException:
            pytest.fail("Login form elements not found within timeout") 