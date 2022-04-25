"""
Track the stock performance on the stock market and store price development.
Trigger notifications to the user in case of high market volatility.
"""

import argparse
import colorama
import datetime
import sqlite3

from matplotlib.pyplot import table

# from pprint import pprint

from stock import Stock
from termcolor import colored

colorama.init()


class Portfolio():

    def __init__(self, df, dbName, dbPath):
        self.df = df
        self.dbName = dbName
        self.dbPath = dbPath
        print(dbName)
        print(dbPath)
        self.stocks = {}
        self.get_stocks_from_df()
        self.get_stock_instances()
        self.write_database()


    def get_date_string(self):
        now = datetime.datetime.now()
        nowDay = now.day
        if now.month < 10:
            dateStr = str(now.year) + '0' + str(now.month)
        else:
            dateStr = str(now.year) + str(now.month)
        if nowDay < 10:
            dateStr = dateStr + '0' + str(nowDay)
        else:
            dateStr = dateStr + str(nowDay)
        return dateStr


    def check_data_quality(self, stockData):
        for key in stockData:
            if stockData[key] == './.':
                print(stockData[key])
                stockData[key] = 'NULL'
        return stockData


    def write_database(self):
        connection = sqlite3.connect(self.dbPath)
        dateStr = self.get_date_string()
        for stockKey in self.stocks:
            tableName = '_' + dateStr + '_' + stockKey
            stockData = self.stocks[stockKey][2].getData()
            cursor = connection.cursor()
            try:
                cursor.execute("CREATE TABLE " + tableName + " (name TEXT, bid REAL, ask REAL, bidsize REAL, asksize REAL," + 
                                                              " high REAL, low REAL, last REAL, delta TEXT, umsatz TEXT" + 
                                                              ", stueck INTEGER, preis REAL, hour INTEGER, minute INTEGER" + 
                                                              ", second INTEGER, hourmin INTEGER)")
            except:
                pass

            self.check_data_quality(stockData)

            now = datetime.datetime.now()
            sql = "INSERT INTO " + tableName + " VALUES ('" + stockData['name'] + "'," + stockData['bid'] + "," + stockData['ask']
            sql = sql + "," + stockData['bidsize'] + "," + stockData['asksize'] + "," + stockData['high']
            sql = sql + "," + stockData['low'] + "," + stockData['last'] + "," + "'" + stockData['delta'] + "'"
            sql = sql + "," + "'" + stockData['umsatz'] + "'" + "," + stockData['stueck'] + "," + stockData['preis']
            sql = sql + "," + str(now.hour) + "," + str(now.minute) + "," + str(now.second)
            if now.minute < 10:
                sql = sql + "," + str(now.hour) + "0" + str(now.minute) + ")"
            else:
                sql = sql + "," + str(now.hour) + str(now.minute) + ")"
            cursor.execute(sql)
            connection.commit()


    def get_stocks_from_df(self):
        for row in self.df['Stock']:
            selectedRow = self.df.loc[self.df['Stock'] == row]
            ticker = selectedRow['Ticker'].iloc[0]
            isin   = selectedRow['ISIN'].iloc[0]
            self.stocks[row] = [isin, ticker]


    def get_stock_instances(self):
        for stockKey in self.stocks:
            newStock = Stock(self.stocks[stockKey][0], self.stocks[stockKey][1])
            self.stocks[stockKey].append(newStock)


    def display_stocks(self):
        print()
        print()
        time_str = ('--- ' +
                    str(datetime.datetime.now().hour)   + ':' +
                    str(datetime.datetime.now().minute) + ':' +
                    str(datetime.datetime.now().second)
                    + ' ---')
        print(time_str)

        for stockKey in self.stocks:
            stock = self.stocks[stockKey][2]
            if stock.getData('delta')[0] == '+':
                print('{:<7}'.format(stock._ticker) + '  ' + colored(stock.getData('delta'), 'green') + '  ' + stock.getData('ask'))
            else:
                print('{:<7}'.format(stock._ticker) + '  ' + colored(stock.getData('delta'), 'red') + '  ' + stock.getData('ask'))


    def refresh_stocks(self):
        for stockKey in self.stocks:
            self.stocks[stockKey][2].scrapWeb()
            self.stocks[stockKey][2].fetchData()