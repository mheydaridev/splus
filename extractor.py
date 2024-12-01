import telebot
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time, sleep
from random import randint

TOKEN = '7808150414:AAFNXvEsyoO5uz19FvHYbYScl4bOihuFbo0'
bot = telebot.TeleBot(TOKEN)

user_data = {}
mobile_list = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "پیش شماره چهار رقمی برای استخراج شماره تلفن ارسال کنید.")
    user_data[message.chat.id] = {"step": "get_prefix"}

@bot.message_handler(func=lambda message: True)
def handle_input(message):
    chat_id = message.chat.id
    user_input = message.text.strip()

    if chat_id in user_data and user_data[chat_id]["step"] == "get_prefix":
        if user_input.isdigit() and len(user_input) == 4:
            user_data[chat_id]["prefix"] = user_input
            user_data[chat_id]["step"] = "get_count"
            bot.reply_to(message, "تعداد شماره‌هایی که می‌خواهید استخراج کنید را وارد کنید.")
        else:
            bot.reply_to(message, "پیش شماره اشتباه است. لطفاً یک پیش شماره چهار رقمی ارسال کنید.")
    
    elif chat_id in user_data and user_data[chat_id]["step"] == "get_count":
        if user_input.isdigit():
            user_data[chat_id]["count"] = int(user_input)
            user_data[chat_id]["step"] = "get_phone"
            bot.reply_to(message, "شماره تلفنی که می‌خواهید با آن لاگین کنید را وارد کنید.")
        else:
            bot.reply_to(message, "تعداد باید عدد باشد. لطفاً یک عدد وارد کنید.")

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
            sleep(1.25)

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.ID, 'sign-in-phone-number')
            elem.send_keys(user_data[chat_id]["phone"][1:])
            break
        except:
            sleep(1.25)

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/form/button')
            elem.click()
            break
        except:
            sleep(1.25)

    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="auth-code-form"]/div/div[3]/div')
            elem.click()
            break
        except:
            sleep(1.25)

def two_step_selenium(user_data, chat_id, message):
    user_data[chat_id]["contact"] = []
    
    def generate_mobile(user_data, chat_id):
        generate_mobile_postfix = str(randint(1000000, 9999999))
        generate_mobile = user_data[chat_id]["prefix"] + generate_mobile_postfix
        while generate_mobile in mobile_list:
            generate_mobile_postfix = str(randint(1000000, 9999999))
            generate_mobile = user_data[chat_id]["prefix"] + generate_mobile_postfix
        
        mobile_list.append(generate_mobile)
        
        return generate_mobile
    
    while True:
        try:
            elem = user_data[chat_id]["driver"].find_element(By.ID, 'sign-in-code')
            elem.send_keys(user_data[chat_id]["code"])
            break
        except:
            sleep(1.25)
            
    while len(user_data[chat_id]['contact']) < user_data[chat_id]["count"]:
        while True: 
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//*[@id="LeftColumn-main"]/div[4]/div[4]')
                elem.click()
                break
            except:
                sleep(1.25)

        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//button[@aria-label="مخاطب جدید"]')
                elem.click()
                break
            except:
                sleep(1.25)

        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//input[@aria-label="شماره تلفن"]')
                moblie_contact = generate_mobile(user_data, chat_id)
                elem.send_keys(moblie_contact[1:])
                break
            except:
                sleep(1.25)

        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//input[@aria-label="نام (الزامی)"]')
                elem.send_keys(moblie_contact)
                break
            except:
                sleep(1.25)
                
        while True:
            try:
                elem = user_data[chat_id]["driver"].find_element(By.XPATH, '//button[text()="تأیید"]')
                elem.click()
                break
            except:
                sleep(1.25)
        
        time_start_check_new_contact = time()
        while time() - time_start_check_new_contact < 20:
            try:
                user_data[chat_id]["driver"].find_element(By.XPATH, "//*[contains(text(), 'اول')]")
                user_data[chat_id]["driver"].find_element(By.XPATH, f"//*[contains(text(), '{moblie_contact}')]")
                user_data[chat_id]["contact"].append(moblie_contact)
                break
            except:
                sleep(1.25)
                
    user_data[chat_id]["driver"].close()
                
    with open(f'mobile_number{chat_id}.txt', 'wb') as f:
        for item in user_data[chat_id]["contact"]:
            f.write(item + "\n")
            
    with open(f'mobile_number{chat_id}.txt', 'rb') as file:
        bot.send_document(chat_id, file)


bot.polling()