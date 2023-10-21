from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Hosttest(TestCase):

   
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()

    # def test_01_register_page(self):
    #     driver = self.driver
    #     driver.get(self.live_server_url)
    #     time.sleep(2)
    #     register_link = driver.find_element(By.CSS_SELECTOR, "#righ")
    #     register_link.click()
    #     time.sleep(2)
    #     username = driver.find_element(By.NAME, "username")
    #     email = driver.find_element(By.NAME, "email")
    #     password1 = driver.find_element(By.NAME, "password1")
    #     password2 = driver.find_element(By.NAME, "password2")
    #     username.send_keys("automated123")
    #     email.send_keys("automated@gmail.com")
    #     password1.send_keys("boringMATER@123")
    #     password2.send_keys("boringMATER@123")
    #     submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    #     time.sleep(2)
    #     submit_button.click()
    #     time.sleep(5)

    def test_02_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)
        theme=driver.find_element(By.CSS_SELECTOR,"button.dropdown-toggle[data-toggle='dropdown']")
        theme.click()
        time.sleep(3)
        theme=driver.find_element(By.CSS_SELECTOR,"button.dropdown-item > a[href='/login_user']")
        theme.click()
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("user17")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("User17@2023")
        time.sleep(2)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button#submit.submitbtn")
        submit_button.click()
        time.sleep(3)
        # driver.execute_script("window.scrollBy(0, 2900);")
        # time.sleep(5)
        browse=driver.find_element(By.CSS_SELECTOR,"div.custom-dropdownn")
        browse.click()
        time.sleep(3)
        browse=driver.find_element(By.CSS_SELECTOR,"a[href='/user_profile/']")
        browse.click()
        time.sleep(3)
        browse=driver.find_element(By.CSS_SELECTOR,"a#req_p.nav-link.collapsed > span")
        browse.click()
        time.sleep(3)
        # browse=driver.find_element(By.CSS_SELECTOR,"a[href='/add_subcategory/']")
        # browse.click()
        # time.sleep(5)
        select_element=Select(driver.find_element(By.NAME, "categ_id"))
        select_element.select_by_value("1")
        time.sleep(1)
    
        elem = driver.find_element(By.NAME, "sub_cat_name")
        elem.send_keys("Fishhh2")
        time.sleep(1)
        # elem = driver.find_element(By.NAME, "product_description")
        # elem.send_keys("good natural product")
        # time.sleep(2)

        # elem = driver.find_element(By.NAME, "product_price")
        # elem.send_keys("250")
        # time.sleep(2)

        # elem = driver.find_element(By.NAME, "product_stock")
        # elem.send_keys("20")
        # time.sleep(2)

        # select_element = Select(driver.find_element(By.NAME, "select_category"))
        # select_element.select_by_value("5")
        # time.sleep(2)

        file_path = r"C:\Users\asus\Downloads\nemo.jpg"
        elem = driver.find_element(By.NAME, "subcat_image")
        elem.send_keys(file_path)
        time.sleep(1)
        browse=driver.find_element(By.CSS_SELECTOR,"button#submitBtn")
        browse.click()
        time.sleep(2)
        browse=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-danger[href='/viewaddproduct']")
        browse.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 2900);")
        time.sleep(5)
        view=driver.find_element(By.CSS_SELECTOR,"a[href^='/book_event/']")
        view.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 2900);")
        time.sleep(4)
        elem = driver.find_element(By.NAME, "attendees")
        elem.send_keys("4")
        chap = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-register")
        chap.click()
        time.sleep(1)
        options = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-secondary.btn-back")
        options.click()
        time.sleep(1)
        select=driver.find_element(By.CSS_SELECTOR, "a.logo")
        select.click()
        time.sleep(3)
        options=driver.find_element(By.CSS_SELECTOR, "a[href='/user_profile_view']")
        options.click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2)
        options=driver.find_element(By.CSS_SELECTOR, "span.hide-menu")
        options.click()
        time.sleep(2)
        options=driver.find_element(By.CSS_SELECTOR, "a.btn.btn-warning")
        options.click()
        time.sleep(2)
        options=driver.find_element(By.CSS_SELECTOR, "select#fill_level")
        options.click()
        time.sleep(2)
        options=driver.find_element(By.CSS_SELECTOR, "option[value='50']")
        options.click()
        time.sleep(2)
        options = driver.find_element(By.CSS_SELECTOR, "img[src='/static/images/profile/flat-business-man-user-profile-avatar-in-suit-vector-4333496.jpg']")
        options.click()
        time.sleep(3)
        options = driver.find_element(By.CSS_SELECTOR, "a[href='/loggout']")
        options.click()
        time.sleep(1)
       

    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()