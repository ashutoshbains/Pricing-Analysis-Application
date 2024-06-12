import pyodbc
import numpy as np
from app import config
from datetime import datetime

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
            

    def clear_database(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM fct_price_history')
        cursor.execute('DELETE FROM fct_products')
        self.conn.commit()

    def get_prices(self, store, subcategory):
        """Return a dictionary of product urls with their prices as value.

        Args:
            store (str): The store for which to fetch the prices
            subcategory (str): The subcategory to fetch

        Returns:
            dict: Key: Product URL Value: Price
        """
        product_price_dict = {}
        cursor = self.conn.cursor()
        cursor.execute('SELECT url,price FROM fct_products WHERE store = ? AND subcategory = ?',store,subcategory)
        query_out = cursor.fetchall()
        for row in query_out:
            product_price_dict[row.url] = row.price
        return product_price_dict
    
    def change_price_if_updated(self, scraped_row):
        """Compares the most recent stored prices in fct_price_history with scraped data and add new entry if price has changed.

        Args:
            scraped_row (dataframe): Single row from a scraped_df.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT price,timestamp from fct_price_history where url = ? ORDER BY timestamp DESC", scraped_row['url'].values[0])
        query_out = cursor.fetchall()
        if len(query_out) == 0:
            dt_str = np.datetime_as_string(scraped_row['last_updated'].values[0])
            last_updated = datetime.fromisoformat(dt_str)
            cursor.execute('INSERT INTO fct_price_history VALUES ( ?, ?, ?)',
                           scraped_row['url'].values[0],
                           scraped_row['price'].values[0],
                           last_updated)
            self.conn.commit()
        else:
            last_updated_price = query_out[0].price
            scraped_price =  scraped_row['price'].values[0]
            if scraped_price != last_updated_price:
                dt_str = np.datetime_as_string(scraped_row['last_updated'].values[0])
                last_updated = datetime.fromisoformat(dt_str)
                cursor.execute('INSERT INTO fct_price_history VALUES ( ?, ?, ?)',
                           scraped_row['url'].values[0],
                           scraped_price,
                           last_updated)
                self.conn.commit()
                print('UPDATED PRICE FOR',scraped_row['url'].values[0]) 


    def get_product_count_by_subcategory(self,subcategory):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(id) FROM fct_products WHERE subcategory = ?',subcategory)
        count = int(cursor.fetchone()[0])
        print('Count in database ',count)
        return count
    

    def find_deprecated_products(self, scraped_urls, store, subcategory):
        cursor = self.conn.cursor()
        db_urls_list = []

        cursor.execute('SELECT url FROM fct_products WHERE store = ? AND subcategory = ?', store, subcategory)
        query_out = cursor.fetchall()
        for row in query_out:
            db_urls_list.append(row.url)

        deprecated_products = [element for element in db_urls_list if element not in scraped_urls.values]
        print(f'FOUND {len(deprecated_products)} DEPRECATED PRODUCTS')
        return deprecated_products
        
    def remove_product_by_url(self,table,url):
        cursor = self.conn.cursor()
        cursor.execute( f"DELETE FROM {table} WHERE URL = '{url}'")
        self.conn.commit()

    def update_subcategory(self, scraped_df):
        cursor = self.conn.cursor()

        for index in range(0,len(scraped_df)):
            cursor.execute('SELECT * from fct_products WHERE url = ?',scraped_df['url'].iloc[index])
            query_out = cursor.fetchall()
            if len(query_out) == 0:
                cursor.execute('INSERT INTO fct_products VALUES (?, ?, ?, ?, ?, ?, ?)',
                    scraped_df.iloc[index, 0],
                    scraped_df.iloc[index, 1],
                    scraped_df.iloc[index, 2],
                    scraped_df.iloc[index, 3],
                    scraped_df.iloc[index, 4],
                    scraped_df.iloc[index, 5],
                    scraped_df.iloc[index, 6])
                self.conn.commit()
            else:
                cursor.execute('UPDATE fct_products SET price = ?, last_updated = ? WHERE url = ?',
                               scraped_df.iloc[index, 5],
                               scraped_df.iloc[index, 6],
                               scraped_df.iloc[index, 0])
                self.conn.commit()


# --------------------------[DEPRECATED FUNCTIONS]------------------------------

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