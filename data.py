import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import urllib.parse
import datetime

class priceVolumeHistory:
    def __init__(self):
        self.conn = sqlite3.connect('priceVolume.db')
        self.cursor = self.conn.cursor()
        self.stocks = []
    
    def fill_stocks(self):
        with open('stocks', 'r') as f:
            for line in f:
                self.stocks.append(line.strip())
    
        print("Stocks Filled")

    #Create all the tables to be monitored
    def create_tables(self):
        for stock in self.stocks:
            stock_encoded = urllib.parse.quote(stock)
            query = f"CREATE TABLE if not exists '{stock_encoded}' (date DATE, price INTEGER, volume INTEGER)"
            self.cursor.execute(query)
            self.conn.commit()

    def get_data_from_NSE(self, stock):
        headers = {'User-Agent': 'Mozilla/5.0'}
     
        main_url = "https://www.nseindia.com/"
        response = requests.get(main_url, headers=headers)
        cookies = response.cookies
    
        url = f"https://www.nseindia.com/api/quote-equity?symbol={stock}&section=trade_info"
        page = requests.get(url,headers=headers, cookies=cookies)
        dajs = json.loads(page.content)
        volume = dajs["marketDeptOrderBook"]["tradeInfo"]["totalTradedVolume"]

        url = f"https://www.nseindia.com/api/quote-equity?symbol={stock}"
        page = requests.get(url,headers=headers, cookies=cookies)
        dajs = json.loads(page.content)
        price = dajs["priceInfo"]["lastPrice"]
        return volume,price

    def fill_data_from_NSE(self):
        for stock in self.stocks:
            try:
                stock_encoded = urllib.parse.quote(stock)
                print(stock_encoded)
                [volume, price] = self.get_data_from_NSE(stock_encoded)
                today = datetime.date.today()
                todayDate = today.strftime('%Y-%m-%d')
                query = f"SELECT COUNT(*) FROM {stock_encoded} WHERE date = {todayDate}"
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                if count <= 0:
                    query = f"INSERT INTO {stock_encoded} (date,price,volume) VALUES ({todayDate},{price},{volume})"
                    self.cursor.execute(query)
                    self.conn.commit()
                else:
                    query = f"UPDATE {stock_encoded} SET date = {todayDate}, price = {price}, volume = {volume} WHERE date = {todayDate}"
                    self.cursor.execute(query)
                    self.conn.commit()

                print(count, volume,price)
            except Exception as e:
                print(f"Error occured for {stock}, {e}")

def main():
    pvObj = priceVolumeHistory()
    pvObj.fill_stocks()
    pvObj.create_tables()
    pvObj.fill_data_from_NSE()

if __name__ == '__main__':
    main()
    exit()
