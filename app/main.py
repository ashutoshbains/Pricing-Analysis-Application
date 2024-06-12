from app.databasehandler import DbHandler

# ------------------- [IMPORT SCRAPERS HERE]------------------------------

from app.scrapers import rhscraper
from app.scrapers import ttvscraper
from app.scrapers import ivscraper
SCRAPERS = [rhscraper,ttvscraper,ivscraper] # Add scrapers to this list

db_handler = DbHandler()

def get_scrapers_for_subcategory(subcategory,get_names=False):
    scrapers = []
    for scraper in SCRAPERS:
        if subcategory in scraper.PRODUCT_SUBCATEGORIES:
            scrapers.append(scraper)
    if get_names:
        store_names = [scraper.STORE_NAME for scraper in scrapers]
        return store_names
    else:
        return scrapers


def update_data(subcategory):
    scrapers = get_scrapers_for_subcategory(subcategory)

    for scraper in scrapers:
        print('ACTIVE SCRAPER:',scraper)
        scraped_df = scraper.scrape_data(subcategory)
        print('SUCCESSFULLY SCRAPED:',scraper.STORE_NAME,subcategory)

        deprecated_products = db_handler.find_deprecated_products(scraped_df['url'],scraper.STORE_NAME,subcategory)
        # Deprecated products are removed here
        for url in deprecated_products:
            db_handler.remove_product_by_url('fct_price_history',url)
            db_handler.remove_product_by_url('fct_products',url)

        # Update fct_products and add new price (if changed) to fct_price_history    
        db_handler.update_subcategory(scraped_df)
        for index in range(0,len(scraped_df)):
            db_handler.change_price_if_updated(scraped_df.iloc[[index]])