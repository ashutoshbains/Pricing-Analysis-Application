from app import config
import pyodbc
from sqlalchemy import create_engine

class DbHandler:
    def __init__(self):
        self.server = config.SERVER_NAME
        self.database = config.DATABASE_NAME
        self.conn = None
        self.connect()

    def connect(self):
        if not self.conn:
            self.conn = pyodbc.connect("Driver={SQL Server};"
                                        "Server="+self.server+';'
                                        "Database="+self.database+';')
            
    def add_to_database(self, data_frame):
        cursor = self.conn.cursor()
        # Get the last id in database
        cursor.execute('SELECT MAX(id) FROM fct_products')
        query_out = cursor.fetchone()
        id = 1
        if query_out[0] is not None:
            id = query_out[0] + 1   

        for row in range(0,len(data_frame)):
            cursor.execute('INSERT INTO fct_products VALUES (?, ?, ?, ?, ?, ?, ?)',
                   id,
                   data_frame.iloc[row, 0],
                   data_frame.iloc[row, 1],
                   data_frame.iloc[row, 2],
                   data_frame.iloc[row, 3],
                   data_frame.iloc[row, 4],
                   data_frame.iloc[row, 5])
            id += 1
            self.conn.commit()

    def clear_database(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM fct_products')
        self.conn.commit()

    def get_prices(self, store, subcategory):
        prices = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT price FROM fct_products WHERE store = ? AND subcategory = ?',store,subcategory)
        query_out = cursor.fetchall()
        for row in query_out:
            prices.append(row.price)
        return prices

    def get_product_count_by_subcategory(self,subcategory):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(id) FROM fct_products WHERE subcategory = ?',subcategory)
        count = int(cursor.fetchone()[0])
        print('Count in database ',count)
        return count
    
    # Outer join to find products in fct_products absent in scrape_df
    def find_deprecated_products(self, scraped_urls, store, subcategory):
        cursor = self.conn.cursor()
        db_urls_list = []

        cursor.execute('SELECT url FROM fct_products WHERE store = ? AND subcategory = ?', store, subcategory)
        query_out = cursor.fetchall()
        for row in query_out:
            db_urls_list.append(row.url)

        deprecated_products = [element for element in db_urls_list if element not in scraped_urls]
        return deprecated_products
        
    
    def update_subcategory(self, store, subcategory, scraped_df):
        engine = create_engine('mssql+pyodbc://@HP/CompetitorProductsDB?driver=SQL Server')
        print(type(engine))
        cursor = self.conn.cursor()

        # Remove existing entries for the specified store subcategory
        cursor.execute('DELETE FROM fct_products WHERE store = ? AND subcategory = ?',store,subcategory)
        self.conn.commit()

        # Write new scraped entries 
        scraped_df.to_sql('fct_products', engine, if_exists='append', index=False)



