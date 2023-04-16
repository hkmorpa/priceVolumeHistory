import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import urllib.parse
import datetime
import argparse

class priceVolumeHistory:
    def __init__(self):
        self.conn = sqlite3.connect('priceVolume.db')
        self.cursor = self.conn.cursor()
        self.stocks = []
        self.fill_stocks()
        self.create_tables()
    
    def fill_stocks(self):
        with open('stocks', 'r') as f:
            for line in f:
                self.stocks.append(line.strip())
    
        print("Stocks Filled")

    def get_table_name(self,stock):
        if '-' in stock:
            stock = stock.replace("-", "_")
        if '&' in stock:
            stock = stock.replace("&", "_")
        return stock

    #Create all the tables to be monitored
    def create_tables(self):
        for stock in self.stocks:
            table_name = self.get_table_name(stock)
            query = f"CREATE TABLE if not exists '{table_name}' (date DATE, price INTEGER, volume INTEGER)"
            self.cursor.execute(query)
            self.conn.commit()
            print (f"created table for {table_name}")

    def get_data_from_NSE(self, stock):
        stock_encoded = urllib.parse.quote(stock)
        stock = stock_encoded
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
                [volume, price] = self.get_data_from_NSE(stock)
                table_name =  self.get_table_name(stock)

                today = datetime.date.today()
                if today.weekday() == 5 or today.weekday() == 6:  # Saturday has a weekday index of 5
                    last_working_day = today - datetime.timedelta(days=today.weekday()-4)
                todayDate = last_working_day.strftime('%Y-%m-%d')

                query = f"SELECT COUNT(*) FROM {table_name} WHERE date = {todayDate}"
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                if count <= 0:
                    query = f"INSERT INTO {table_name} (date,price,volume) VALUES ({todayDate},{price},{volume})"
                    self.cursor.execute(query)
                    self.conn.commit()
                else:
                    query = f"UPDATE {table_name} SET date = {todayDate}, price = {price}, volume = {volume} WHERE date = {todayDate}"
                    self.cursor.execute(query)
                    self.conn.commit()

                print(table_name, count, volume,price)
            except Exception as e:
                print(f"Error occured for {stock}, {e}")

def main():
    global args


    parser = argparse.ArgumentParser()
    parser.add_argument("-show", action="store_true", help="Show the tables")

    pvObj = priceVolumeHistory()
    pvObj.fill_data_from_NSE()

if __name__ == '__main__':
    main()
    exit()
