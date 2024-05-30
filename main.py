import config
import rhscraper
import pandas as pd
from databasehandler import DbHandler

db_handler = DbHandler()

for subcat in rhscraper.PRODUCT_SUBCATEGORIES:
    scraped_df = rhscraper.scrape_data(subcat)
    deprecated_products = db_handler.find_deprecated_products(scraped_df['url'],'Rural Handmade',subcat)
    db_handler.update_subcategory('Rural Handmade',subcat,scraped_df)