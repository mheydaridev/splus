from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from random import randint
from time import time, sleep

class First():
    mobile_list = []

    def __init__(self):
        self.cantact = []
        
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # مسدود کردن نوتیفیکیشن‌ها
        }
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=Service("./chromedriver"), options=chrome_options)

        self.driver.maximize_window()

        self.action = ActionChains(self.driver)

        self.driver.get('https://web.splus.ir/')
    
    
    def login(self):
        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/div[2]/button[2]')
                elem.click()
                break
            except:
                sleep(1)

        mobile = '09140999258' #input('Mobile: ')
        while True: 
            try:
                elem = self.driver.find_element(By.ID, 'sign-in-phone-number')
                elem.send_keys(mobile[1:])
                break
            except:
                sleep(1)                

        while True: 
            try:
                elem = self.driver.find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/form/button')
                elem.click()
                break
            except:
                sleep(1)

        time_start_check_new_contact = time()
        while time() - time_start_check_new_contact < 4:
            try:
                elem = self.driver.find_element(By.XPATH, '//*[@id="auth-code-form"]/div/div[3]/div')
                elem.click()
                break
            except:
                sleep(1)
        
        activation_code = input('Activation code: ')
        while True:
            try:
                elem = self.driver.find_element(By.ID, 'sign-in-code')
                elem.send_keys(activation_code)
                break
            except:
                sleep(1)
        
        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//*[@id="LeftColumn-main"]/div[4]/div[4]')
                elem.click()
                break
            except:
                sleep(1)


    def send_msg(self, mobile_prefix):

        def generate_mobile(mobile_prefix):
            generate_mobile_postfix = str(randint(1000000, 9999999))
            generate_mobile = mobile_prefix + generate_mobile_postfix
            while generate_mobile in self.mobile_list:
                generate_mobile_postfix = str(randint(1000000, 9999999))
                generate_mobile = mobile_prefix + generate_mobile_postfix
            
            self.mobile_list.append(generate_mobile)
            
            return generate_mobile

        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//button[@aria-label="مخاطب جدید"]')
                elem.click()
                break
            except:
                sleep(1)

        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//input[@aria-label="شماره تلفن"]')
                moblie_contact = generate_mobile(mobile_prefix)
                elem.send_keys(moblie_contact[1:])
                break
            except:
                sleep(1)

        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//input[@aria-label="نام (الزامی)"]')
                elem.send_keys(moblie_contact)
                break
            except:
                sleep(1)
                
        while True:
            try:
                elem = self.driver.find_element(By.XPATH, '//button[text()="تأیید"]')
                elem.click()
                break
            except:
                sleep(1)
        
        time_start_check_new_contact = time()
        while time() - time_start_check_new_contact < 4:
            try:
                self.driver.find_element("xpath", "//*[contains(text(), 'اول')]")
                self.driver.find_element("xpath", f"//*[contains(text(), '{moblie_contact}')]")
                self.cantact.append(moblie_contact)
                return True
            except:
                sleep(1)


    def extract(self):
        order = '/extract 0913 10'
        order = order.split(' ')
        mobile_prefix = order[1]
        
        self.cantact = []
        
        run_time = int(order[2])
        while len(self.cantact) < run_time:
            self.send_msg(mobile_prefix)

        with open('mobile_number.txt', 'w') as f:
            for item in self.cantact:
                f.write(item + "\n")


if __name__ == '__main__':
    bot = First()
    
    # کار هایی که کاربر بتواند انجام دهد
    bot.login()
    bot.extract()