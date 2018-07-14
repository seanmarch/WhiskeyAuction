## Development Whiskeys
# Johnnie Walker Black label
# SUNTORY YAMAZAKI DISTILLER'S RESERVE
# MACALLAN 12

## Whiskey Auction Sites
# https://www.whiskyauctioneer.com/

## Whiskey Shops
# https://www.thewhiskyexchange.com/tweagegate-home.aspx?gclid=EAIaIQobChMI64K6_5_T2QIV4ZztCh0WDAnsEAAYASAAEgLw8_D_BwE
# https://www.masterofmalt.com/
# https://www.whiskyshop.com/

## Whisky Shops Search Format

# https://www.masterofmalt.com/search/#search=FIRSTWORD%20SECONDWORD
# https://www.whiskyshop.com/catalogsearch/result/?q=FIRSTWORD+SECONDWORD&order=relevance&dir=desc

#!/usr/bin/env python3

import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import pymysql

mysql_host = ""
mysql_user = ""
mysql_pass = ""
mysql_db = ""
db = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass, db=mysql_db)
cursor = db.cursor()

def HTMLParse(url):
    # Opening up connection, grabbing the pages
    Req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    Client = uReq(Req)
    html = Client.read()
    Client.close()

    # HTML Parser
    page_soup = soup(html, "html.parser")
    return page_soup


def WAScrape(WApage_soup):
    page = 0
    tempLot = []

    # while WApage_soup.find("li", {"class":"pager-next"}) or WApage_soup.find("li", {"class":"pager-current last"}):
    while page != 3:
        WAContainers = WApage_soup.findAll("div", {"class": re.compile("views-row views-row-")})
        for WAContainer in WAContainers:

            try:
                WALotNo = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                WATitle = (WAContainer.find("span", {"class": "protitle"})).text.strip()
                #WADistilery = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAAge = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAVintage = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WARegion = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WABottler = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WACaskType = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAStrength = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAVolume = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WADistileryStatus = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAPrice = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAURLBottle = (WAContainer.find("span", {"class": "lotnumber"})).text.strip()
                #WAURLAuction = (WAContainer.find("span", {"class":"uc-price"})).text.strip()

            except:
                continue

            print(WATitle)
            print(WALotNo)

            #cursor.execute("INSERT INTO `WACurrent`(`Title`, `LotNo`, `Distillery`, `Age`, `Vintage`, `Region`, `Bottler`, `CaskType`, `Strength`, `Volume`, `DistilleryStatus`, `Price`, `URLBottle`, `URLAuction`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #               , (WALotNo, WATitle, WADistilery, WAAge, WAVintage, WARegion, WABottler, WACaskType, WAStrength, WAVolume, WADistileryStatus, WAPrice, WAURLBottle, WAURLAuction))

            cursor.execute("INSERT INTO `WACurrent`(`Title`, `LotNo`) VALUES (%s,%s)", (WALotNo, WATitle))

            db.commit()

            # temp = [WAWebLot, WADescription, WAWebPrice, '']
            # tempLot.append(temp)
            # print(WADescription)
            # WEPrice = WEPriceSearch(WADescription)
            # if WEPrice is not None:
            #   print(WAWebLot, WADescription, WEPrice)

        # if WApage_soup.find("li", {"class":"pager-current last"}):
        #     break
        #
        page += 1
        WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction' + '?page=' + str(page)
        WApage_soup = HTMLParse(WAurl)

        # BrandsListing = (cursor.fetchall())
        # print(BrandsListing)


WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction'

# Grab the Whiskey Auction HTML
WApage_soup = HTMLParse(WAurl)

# Scrape Lot Numbers, Description and Price of all items and return as a numpy array
AuctionLots = WAScrape(WApage_soup)
print(AuctionLots)
db.close()

# Grabs Web Price of Whiskey and find cheapest

#MoMWebPrice = (MoMpage_soup.find("div", {"class":"priceDiv"})).text
#WSWebPrice = (WSpage_soup.find("span", {"class":"price"})).text.strip()
#MinWebPrice = min(WEWebPrice, MoMWebPrice, WSWebPrice)





