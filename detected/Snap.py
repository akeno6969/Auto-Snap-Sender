# this script uses Selenium WebDriver for snapchat web browser 
#supported browsers (google chrome), (firefox), (opera), (microsoft edge), (safari for MacOS),


### WEB DRIVERS USED (IMPORTANT MUST READ BELOW)

# ChromeDriver (Google Chrome) Headless Mode: Supported

# GeckoDriver (Mozilla Firefox) Headless Mode: Supported

# EdgeDriver (Microsoft Edge) Headless Mode: Supported

# OperaDriver (Opera) Headless Mode: Supported (through ChromeDriver)

# SafariDriver (Safari for MacOS) Headless Mode: Limited (Safari headless mode is supported in Safari 13 and later on macOS).
	

import time
import os
import pyautogui
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

SNAPCHAT_USERNAME = "your_username"
SNAPCHAT_PASSWORD = "your_password"
RECIPIENT_USERNAME = "recipient_username"
CHROME_DRIVER_PATH = "path/to/your/chromedriver"  

def initialize_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_to_snapchat(driver):
    driver.get('https://web.snapchat.com/')
    time.sleep(5)
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys(SNAPCHAT_USERNAME)
    password_field.send_keys(SNAPCHAT_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

def take_photo(driver):
    camera_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/div[1]/div[2]/div/button')
    camera_button.click()
    time.sleep(3)

def send_snap(driver):
    send_to_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]')
    send_to_button.click()
    time.sleep(2)

    search_field = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/input')
    search_field.send_keys(RECIPIENT_USERNAME)
    time.sleep(2)

    first_result = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]')
    first_result.click()
    time.sleep(1)

    send_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[4]/button')
    send_button.click()
    time.sleep(2)

def send_multiple_snaps(count):
    driver = initialize_browser()
    login_to_snapchat(driver)

    for i in range(count):
        print(f"Sending Snap #{i + 1}")
        take_photo(driver)
        send_snap(driver)
        time.sleep(5)

    driver.quit()

def ask_for_snap_count():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_input = input("Import how many snaps to send: ")

        if user_input.isdigit():  
            return int(user_input)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Not a valid number.")
            time.sleep(3)

def main():
    snap_count = ask_for_snap_count()
    send_multiple_snaps(snap_count)

if __name__ == '__main__':
    main()