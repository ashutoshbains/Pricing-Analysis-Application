import re
import time
import requests
import pandas as pd
from app import config
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

PRODUCT_SUBCATEGORIES = ['Planters']
STORE_NAME = 'Artizan Made'

def get_url(subcategory):
    match subcategory:
        case 'Planters':
            return 'https://www.artizanmade.com/product-category/home-and-office/garden/planters/'
        

def scrape_data(subcategory):
    url_list = []
    output_df = pd.DataFrame(columns = config.DB_COLUMNS)
      
    url = get_url(subcategory)
    driver = webdriver.Edge(service=Service(config.WEBDRIVER_PATH),options=Options())
    driver.get(url)
    time.sleep(2.3)

    while True:
        current_height = driver.execute_script("return window.scrollY")
        page_length = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollBy(0, {page_length});")
        time.sleep(2)
        new_height = driver.execute_script("return window.scrollY")
        if current_height == new_height:
            break

    n=1
    product_grid = driver.find_element(By.CSS_SELECTOR,'#main > div > div.products-archive--products > div.products-loop.products-loop--fitrows')
    for product_element in product_grid.find_elements(By.TAG_NAME,'li'):
        try:
            element = product_element.find_element(By.CLASS_NAME, 'title-column')
            name = element.find_element(By.TAG_NAME, 'a').text
            url = element.find_element(By.TAG_NAME,'a').get_attribute('href')
            price = product_element.find_element(By.TAG_NAME,'bdi').text
            price = price.replace('$','')
            n+=1
            output_df.loc[len(output_df)] = [url,
                                                name,
                                                STORE_NAME,
                                                config.get_category(subcategory),
                                                subcategory,
                                                price,
                                                datetime.now()]
            url_list.append(url)
        except:
            continue

    return output_df

