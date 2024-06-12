import re
import time
# from app import config
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

PRODUCT_SUBCATEGORIES = ['Frames','Statues','Journal']
STORE_NAME = 'Indie Vibe'

def get_url(subcategory):
    match subcategory:
        case 'Frames':
            return 'https://www.indievibe.co/category/home-and-living-decor-photo-frames'

def get_subcategory_urls(subcategory):
    url_list = []
      
    # REMEMBER TO CHANGE WEBDRIVER PATH TO REFER TO CONFIG INSTEAD OF HARD WRITTEN PATH HERE
    url = get_url(subcategory)
    driver = webdriver.Edge(service=Service(r'C:\Users\ash24\OneDrive\Desktop\edgeDriver\msedgedriver.exe'),options=Options())
    driver.get(url)

    while True:
        time.sleep(2.3)
        product_grid = driver.find_element(By.CLASS_NAME,'css-111rnvc')
        url_list.extend([a.get_attribute('href') for a in product_grid.find_elements(By.TAG_NAME, 'a')])
        try:
            next_button = driver.find_element(By.XPATH, "//div[@class='css-33rkaa' and contains(text(), 'Next')]")
            ActionChains(driver).move_to_element(next_button).perform()
            next_button.click()
        except:
            print('IndieVibe next button not found')
            break
    
    return url_list

# CHANGE WEBDRIVER PATH FROM HARD WRITTEN TO A REFERENCE FROM CONFIG.PY
def get_product_details(url):
    driver = webdriver.Edge(service=Service(r'C:\Users\ash24\OneDrive\Desktop\edgeDriver\msedgedriver.exe'), options=Options())
    driver.get(url)

    name = driver.find_element(By.CLASS_NAME,'css-1er4t18')
    time.sleep(50)
    price_list = driver.find_element(By.CLASS_NAME,'px-3 pb-3 pt-2 css-1u00h7y')
    child_divs = price_list.find_elements(By.TAG_NAME, "div")
    last_div = child_divs[-1]


def scrape_data(subcategory):
    for subcategory in PRODUCT_SUBCATEGORIES:
        product_urls = get_subcategory_urls(subcategory)

        for url in product_urls:
            details = get_product_details(url)
