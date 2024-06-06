import time
from app import config
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

PRODUCT_SUBCATEGORIES = ['Planters','Door Mats']
STORE_NAME = 'Rural Handmade'

def get_url(subcategory):
    if subcategory == 'Tic Tac Toe':
        return 'https://ruralhandmade.com/search/tic-tac'
    elif subcategory == 'Planters':
        return 'https://ruralhandmade.com/product/garden-and-outdoors/planters-1'
    elif subcategory == 'Door mats':
        return 'https://ruralhandmade.com/product/rugs/door-mats-1'
    else:
        return f'https://ruralhandmade.com/search/{subcategory.lower().replace(" ", "-")}'

def scrape_data(subcategory):
    url_list = []
    output_df = pd.DataFrame(columns = config.DB_COLUMNS)

    url = get_url(subcategory)

    driver = webdriver.Edge(service=Service(config.WEBDRIVER_PATH), options=Options())
    driver.get(url)

    # Close the Cookies overlay
    try:
        i_understand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "accept")))
        i_understand_button.click()
    except:
        print('I understand button not present, proceeding without clicking.')

    n=1
    # Press the next button
    while True:
        
        try:
            products = driver.find_elements(By.CLASS_NAME, 'jprodut-listing-details')
            # url_list.extend([product.find_element(By.TAG_NAME, 'a').get_attribute('href') for product in products])
            for product in products:
                if n > 100:
                    return output_df
                name = product.find_element(By.TAG_NAME,'p').text
                price = product.find_element(By.CLASS_NAME,'jpd-price').text.split(' - ')[0].split('\n')[1]
                price = float(price.replace('$',''))
                url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                output_df.loc[len(output_df)] = [url,
                                             name,
                                             STORE_NAME,
                                             config.get_category(subcategory),
                                             subcategory,
                                             price,
                                             datetime.now()]
                url_list.append(product.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                print(n)
                n+=1
        except StaleElementReferenceException:
        # If a StaleElementReferenceException is raised, wait for a short time and then retry
            time.sleep(1)
            continue

        try:
            next_button = driver.find_element(By.XPATH, '//ul[@id="pagingidshow"]/li/a[contains(text(), "Next") and not(@style="display:none;")]')
            parent_li = next_button.find_element(By.XPATH, './parent::li')
            if "display: none;" in parent_li.get_attribute("style"):
                break
        except:
            if "display: none;" in parent_li.get_attribute("style"):
                break

        ActionChains(driver).move_to_element(next_button).perform()
        next_button.click()
        time.sleep(2)
    
    return output_df

def get_product_details(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'html.parser')

    product_title = page.find('div', class_='jpd-right-title').text.strip()
    product_price = page.find('span', id='price_div').text.strip()
    product_price = product_price.split('-')
    lower_price = float(product_price[0].replace('$',''))
    upper_price = float(product_price[1].replace('$',''))
    material = '-'
    material_elements = page.findAll('div', class_='jpd-right-value-block-group')
    for material_element in material_elements:
        if 'title' in material_element.attrs:
            material = material_element['title']
    return product_title,upper_price,material
