# ignore ts btw <3 ( unless u need ts idk )
# dont execute this btw

import time
from selenium.webdriver.common.by import By

def wait_for_element(driver, by, value, timeout=10):
    for _ in range(timeout):
        try:
            driver.find_element(by, value)
            return True
        except:
            time.sleep(1)
    return False

def click_element(driver, by, value):
    element = driver.find_element(by, value)
    element.click()