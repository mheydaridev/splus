import telebot
import pyperclip
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time, sleep

TOKEN = '7872666597:AAEc-x2dev_2k297XZo1rFTdsXbwLmhEYqc'
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "پیام را که می‌خواهید به مخاطبین بفرستید ارسال کنید.")
    user_data[message.chat.id] = {"step": "get_msg"}
    
@bot.message_handler(content_types=['document'])
def handle_mobile_file(message):
    # تابع برای خواندن شماره‌ها از فایل
    def read_numbers_from_file(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    chat_id = message.chat.id

    if chat_id in user_data and user_data[chat_id]["step"] == "get_mobile":
        if message.document:
            user_data[chat_id]["mobile"] = []
            
            # دریافت فایل از کاربر
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # ذخیره فایل به صورت موقت
            file_name = message.document.file_name
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)

            # خواندن شماره‌ها از فایل و ذخیره در user_data
            user_data[chat_id]["mobile"] = read_numbers_from_file(file_name)

            # حذف فایل موقت
            os.remove(file_name)
            
            user_data[chat_id]["step"] = "get_phone"
            bot.reply_to(message, "شماره تلفنی که می‌خواهید با آن لاگین کنید را وارد کنید.")
        else:
            bot.reply_to(message, "ورودی باید یک فایل حاوی شماره ها باشد...\nفایل را مجددا ارسال کنید")

    

@bot.message_handler(func=lambda message: True)
def handle_input(message):    
    chat_id = message.chat.id
    user_input = message.text.strip()

    if chat_id in user_data and user_data[chat_id]["step"] == "get_msg":
        if user_input != '':
            user_data[chat_id]["msg"] = user_input
            user_data[chat_id]["step"] = "get_mobile"
            bot.reply_to(message, "فایل حاوی شماره‌هایی که می‌خواهید به ان ها  پیام ارسال کنید را بفرستید.")
        else:
            bot.reply_to(message, "پیام نمیتواند خالی باشد. پیام مورد نظر را ارسال کنید.")
    
    elif chat_id in user_data and user_data[chat_id]["step"] == "get_phone":
        if user_input.isdigit() and len(user_input) == 11:
            user_data[chat_id]["phone"] = user_input
            user_data[chat_id]["step"] = "get_code"
            one_step_selenium(user_data, chat_id, message)
            bot.reply_to(message, "کد فعال سازی را وارد کنید:")
        else:
            bot.reply_to(message, "شماره تلفن اشتباه است. لطفاً یک شماره ۱۱ رقمی وارد کنید.")

    elif chat_id in user_data and user_data[chat_id]["step"] == "get_code":
        if user_input.isdigit() and len(user_input) == 5:
            user_data[chat_id]["code"] = user_input
            user_data[chat_id]["step"] = "done"
            two_step_selenium(user_data, chat_id, message)
        else:
            bot.reply_to(message, "کد فعال سازی اشتباه است. لطفا کد فعال سازی ۵ رقمی وارد کنید:")

def one_step_selenium(user_data, chat_id, message):
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
    }
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    user_data[chat_id]["driver"] = webdriver.Chrome(service=Service("./chromedriver"), options=chrome_options)
    user_data[chat_id]["driver"].maximize_window()
    user_data[chat_id]["action"] = ActionChains(user_data[chat_id]["driver"])
    user_data[chat_id]["driver"].get('https://web.splus.ir/')

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/div[2]/button[2]')
            elem.click()
            break
        except:
            sleep(1)

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.ID, 'sign-in-phone-number')
            elem.send_keys(user_data[chat_id]["phone"][1:])
            break
        except:
            sleep(1)

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/form/button')
            elem.click()
            break
        except:
            sleep(1)

    time_start_check_new_contact = time()
    while time() - time_start_check_new_contact < 4:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="auth-code-form"]/div/div[3]/div')
            elem.click()
            break
        except:
            sleep(1)

def two_step_selenium(user_data, chat_id, message):
    user_data[chat_id]["contact"] = []
    
    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.ID, 'sign-in-code')
            elem.send_keys(user_data[chat_id]["code"])
            break
        except:
            sleep(1)
    
    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="LeftColumn-main"]/div[4]/div[4]')
            elem.click()
            break
        except:
            sleep(1)
            
    for moblie_contact in user_data[chat_id]['mobile']:
        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//button[@aria-label="مخاطب جدید"]')
                elem.click()
                break
            except:
                sleep(1)

        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//input[@aria-label="شماره تلفن"]')
                elem.send_keys(moblie_contact[1:])
                break
            except:
                sleep(1)

        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//input[@aria-label="نام (الزامی)"]')
                elem.send_keys(moblie_contact)
                break
            except:
                sleep(1)
                
        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//button[text()="تأیید"]')
                elem.click()
                break
            except:
                sleep(1)
        
        while True:
            try:
                pyperclip.copy(user_data[chat_id]["msg"])
                user_data[chat_id]["action"].key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
                
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//button[@aria-label="ارسال پیام"]')
                elem.click()
                
                user_data[chat_id]["contact"].append(moblie_contact)            
                
                break
            except:
                sleep(1)
                
    user_data[chat_id]["driver"].close()

bot.polling()
