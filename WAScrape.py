import re
from bs4 import BeautifulSoup as soup
from WEPriceSearch import WEPriceSearch
from HTMLParse import HTMLParse
import numpy as np
import sys
import pymysql

# Grabs auction container of whiskey and then lot number and current auction price


#!/usr/bin/env python3

mysql_host = "db4free.net"
mysql_user = "whiskydb"
mysql_pass = "seandy29"
mysql_db = "whisky"
db = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass, db=mysql_db)
cursor = db.cursor()

def WAScrape(WApage_soup):
    page = 0
    tempLot = []
    
    while WApage_soup.find("li", {"class":"pager-next"}) or WApage_soup.find("li", {"class":"pager-current last"}):
        WAContainers = WApage_soup.findAll("div", {"class":re.compile("views-row views-row-")})
        for WAContainer in WAContainers:
            try:
                WALotNo = (WAContainer.find("span", {"class":"lotnumber"})).text.strip()
                WATitle = (WAContainer.find("span", {"class":"protitle"})).text
                WAWebPrice = (WAContainer.find("span", {"class":"uc-price"})).text
                WADistilery = (WAContainer.find("span", {"class":"lotnumber"})).text.strip()
            except:
                continue

            sql = "INSERT INTO `WACurrent`(`Title`, `LotNo`, `Distillery`, `Age`, `Vintage`, `Region`,`Bottler`, `CaskType`, `Strength`, `Volume`, `DistilleryStatus`, `Price`, `URLBottle`, `URLAuction`) VALUES (WATitle, WALotNo,[value-3],[value-4],[value-5],[value-6],[value-7],[value-8],[value-9],[value-10],[value-11],[value-12],[value-13],[value-14])"
            cursor.execute(sql)

            #temp = [WAWebLot, WADescription, WAWebPrice, '']
            #tempLot.append(temp)
            #print(WADescription)
            #WEPrice = WEPriceSearch(WADescription)
            #if WEPrice is not None:
            #   print(WAWebLot, WADescription, WEPrice)
            
        if WApage_soup.find("li", {"class":"pager-current last"}):
            break
        
        page = page + 1
        WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction' + '?page=' + str(page)
        WApage_soup = HTMLParse(WAurl)


BrandsListing = (cursor.fetchall())
print(BrandsListing)	
db.close()
