
# Scraping related variables
WEBDRIVER_PATH = r'C:\Users\ash24\OneDrive\Desktop\edgeDriver\msedgedriver.exe'

# Database related variables
SERVER_NAME = 'HP'
DATABASE_NAME = 'CompetitorProductsDB'
DB_COLUMNS = ['url',
               'name',
                 'store',
                     'category',
                       'subcategory',
                         'price',
                           'last_updated']

# Product related variables
CATEGORY_DICT = {
    'Office': ('Journal'),
    'Decor': ('Frames', 'Statues'),
    'Garden': ('Planters')
}

def get_category(subcategory):
        for cat, subcat in CATEGORY_DICT.items():
            if subcategory in subcat:
                return cat