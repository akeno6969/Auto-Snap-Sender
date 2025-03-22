from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_browser():
    """Configure and return a Selenium WebDriver."""
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver