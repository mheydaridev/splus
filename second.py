import pyperclip

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from time import time, sleep

class Second():
    mobile_list = list()
    msg = ''
    
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

        
    def set_msg(self):
        self.msg = '''من برنامه نویسم و یک ربات نوشتم که به صورت خودکار به کاربران سروش پیام میده :)\nبرای خرید این ربات به ایدی تلگرام زیر پیام بدید:\n\n@mheydaridev\n\nاین ربات خوراکه تبلیغاته! حواست باشه از دستش ندی یه وقت... :)\n
        ''' #input('message: ')
        

    def send_msg(self, moblie_contact):
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
                
        while True:
            try:
                pyperclip.copy(self.msg)
                self.action.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
                
                elem = self.driver.find_element(By.XPATH, '//button[@aria-label="ارسال پیام"]')
                elem.click()
                
                break
            except:
                pass
                sleep(1)
                                    
    
    def auto(self):
        order = '/auto'        
        
        file_name = 'mobile_number.txt' #input('file: ')
        with open(file_name, 'r') as f:
            lines = f.readlines()
        self.contact = [line.strip() for line in lines]
        
        for moblie_contact in self.contact:
            self.send_msg(moblie_contact)


if __name__ == '__main__':
    bot = Second()
    
    # کار هایی که کاربر بتواند انجام دهد
    bot.login()
    bot.set_msg()
    bot.auto()