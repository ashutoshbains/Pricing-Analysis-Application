from app import config
from app import app
import pandas as pd
from app.databasehandler import DbHandler

# ------------------- [IMPORT SCRAPERS HERE]------------------------------

from app.scrapers import rhscraper
from app.scrapers import ttvscraper

db_handler = DbHandler()

# -------------------[ADD SCRAPERS TO THIS LIST]--------------------------

def update_all_data():
    scrapers = (ttvscraper,rhscraper)

    for scraper in scrapers:
        for subcat in scraper.PRODUCT_SUBCATEGORIES:

            print('ACTIVE SCRAPER: ',scraper)
            scraped_df = scraper.scrape_data(subcat)

            deprecated_products = db_handler.find_deprecated_products(scraped_df['url'],scraper.STORE_NAME,subcat)
            # Deprecated products are removed here
            for url in deprecated_products:
                db_handler.remove_product_by_url('fct_price_history',url)
                db_handler.remove_product_by_url('fct_products',url)

            # Update fct_products and add new price (if changed) to fct_price_history    
            db_handler.update_subcategory(scraped_df)
            for index in range(0,len(scraped_df)):
                db_handler.change_price_if_updated(scraped_df.iloc[[index]])