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

PRODUCT_SUBCATEGORIES = ['Planters','Earrings']
STORE_NAME = 'Ten Thousand Villages'

def get_url(subcategory):
    match subcategory:
        case 'Planters':
            return 'https://www.tenthousandvillages.com/collections/planters'
        case 'Earrings':
            return 'https://www.tenthousandvillages.com/collections/earrings'
        
def scrape_data(subcategory):
    url_list = []
    output_df = pd.DataFrame(columns = config.DB_COLUMNS)
      
    url = get_url(subcategory)
    driver = webdriver.Edge(service=Service(config.WEBDRIVER_PATH),options=Options())
    driver.get(url)

    while True:
        time.sleep(2.3)
        product_grid = driver.find_element(By.CSS_SELECTOR,'#shopify-section-template--22549394817327__main > div.productgrid--outer.layout--has-sidebar.productgrid-gridview > div.productgrid--wrapper > ul')
        for product_element in product_grid.find_elements(By.TAG_NAME,'li'):
            name = product_element.find_element(By.CLASS_NAME, 'productitem--title').text
            price = product_element.find_element(By.CLASS_NAME,'price__current  ')
            if '-' in price.text:
                price_limits = price.text.replace('$','').split('-')
                price_limits = [float(x) for x in price_limits]
                price = sum(price_limits)/len(price_limits)
            else:               
                price = float(re.findall('\d+\.\d+|\d+', product_element.find_element(By.CLASS_NAME, 'price__current  ').text)[0])
            url = product_element.find_element(By.CLASS_NAME,'productitem--title a').get_attribute('href')
            output_df.loc[len(output_df)] = [url,
                                             name,
                                             STORE_NAME,
                                             config.get_category(subcategory),
                                             subcategory,
                                             price,
                                             datetime.now()]
            url_list.append(url)

        try:
            next_button = driver.find_element(By.CLASS_NAME, 'pagination--next')
            ActionChains(driver).move_to_element(next_button).perform()
            next_button.click()
        except:
            break
    
    return output_df
