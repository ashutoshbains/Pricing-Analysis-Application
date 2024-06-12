
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
    'Office': ['Journal'],
    'Decor': ('Frames','Statues','Door Mats'),
    'Garden': ['Planters'],
    'Accessories': ['Earrings']
}

def get_subcategories():
    subcategories = set()
    for values_tuple in CATEGORY_DICT.values():
        for value in values_tuple:
            subcategories.add(value)
    return subcategories

def get_category(subcategory):
        for cat, subcat in CATEGORY_DICT.items():
            if subcategory in subcat:
                return cat