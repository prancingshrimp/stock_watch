from bs4 import BeautifulSoup as html
# import openpyxl
# import os
# import pandas
import requests
# import shutil
import time
# import urllib
# import xlrd

# from pprint import pprint


class Stock():

    URL_DATA = "https://www.tradegate.de"
    URL_QUERY = URL_DATA + "/orderbuch.php?isin="


    def __init__(self, id, ticker):
        self._id = id
        self._ticker = ticker
        self._query = Stock.URL_QUERY + id
        self._data = {}
        self.scrapWeb()
        self.fetchData()


    def scrapWeb(self):
        proof = True
        while proof:
            try:
                self._html = html(requests.get(self._query).content, "html.parser")
                proof = False
            except:
                print("Error... keep going!")
                time.sleep(2)


    def fetchData(self):
        stock_data = {}
        stock_name = self._html.find("div", {"id": "col1_content"}).find("h2").text
        stock_data.update({"name": stock_name})
        tag_parent = self._html.find_all("td", class_="longprice")
        for item in tag_parent:
            if "id" in item.attrs:
                key = item.attrs.get("id")
                value = item.text.replace(" ", "").replace(",", ".").replace("\xa0", "").replace("TEUR", " TEUR")
                stock_data.update({key: value})
            else:
                tag_child = item.find("strong")
                key = tag_child.attrs.get("id")
                value = item.text.replace(" ", "").replace(",", ".").replace("\xa0", "").replace("TEUR", " TEUR")
                stock_data.update({key: value})
        self._data = stock_data
        # pprint(self._data["delta"])
        # pprint(self._data)


    def getData(self, key="all"):
        if (key == "all"):
            return self._data
        else:
            return self._data[key]
