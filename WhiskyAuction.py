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

# -*- coding: utf8mb4 -*-



import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import pymysql

mysql_host = "db4free.net"
mysql_user = "whiskydb"
mysql_pass = "seandy29"
mysql_db = "whisky"
db = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass, db=mysql_db, use_unicode=True, charset="utf8mb4")
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


def WALotLinkScrape(WApage_soup):
    """Scrape all active Whisky Lot URLs from whiskyauction.com"""

    page = 0
    LotLinks = []

    while WApage_soup.find("li", {"class":"pager-next"}) or WApage_soup.find("li", {"class":"pager-current last"}):

        for link in WApage_soup.findAll('a', attrs={'href': re.compile('/lot/')}):
            LotLinks.append('https://www.whiskyauctioneer.com' + link.get('href'))

        if WApage_soup.find("li", {"class":"pager-current last"}):
            break

        page += 1
        WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction' + '?page=' + str(page)
        WApage_soup = HTMLParse(WAurl)
        print('Scraping WA Links on Page : ' + page)

    return LotLinks


def WAScrape(LotLinks, WAurl):
    """Scrape all Whisky Lots from whiskyauction.com"""

    itemcounter = 0

    for url in LotLinks:

        itemcounter += 1
        print('Scraping WA Data. Item ' + itemcounter + ' of ' + len(LotLinks))
        Lot = HTMLParse(url)

        try:
            WALotNo = (Lot.find("div", {"class": "lot"})).text.strip()[4:]
            WATitle = (Lot.find("div", {"class": "ptitle"})).text.strip()
            WADistilery = (Lot.find("div", {"class": "distillery"})).text.strip()
            WAAge = re.split(" year old", (Lot.find("div", {"class": "age"})).text.strip(), flags=re.IGNORECASE)[0]
            WAVintage = (Lot.find("div", {"class": "right"}).find("div", {"class":"topvbn"}).find("div", {"class": "region"})).text.strip()
            WARegion = (Lot.find("div", {"class": "right"}).find("div", {"class":"topvbn"}).find("div", {"class": "region"}).next_sibling.next_sibling).text.strip()
            WABottler = (Lot.find("div", {"class": "casktype"})).text.strip()
            WACaskType = (Lot.find("div", {"class": "casktype"}).next_sibling.next_sibling).text.strip()
            WAStrength = (Lot.find("div", {"class": "strength"})).text.strip()
            WAVolume = (Lot.find("div", {"class": "bottlesize"})).text.strip()
            WADistilleryStatus = (Lot.find("div", {"class": "bottlestatus"})).text.strip()
            WAPrice = (Lot.find("span", {"class": "uc-price"})).text.strip()
            WAURLBottle = url
            WAURLAuction = WAurl
        except:
            continue

        cursor.execute('INSERT INTO WACurrent(Title, LotNo, Distillery, Age, Vintage, Region, Bottler, CaskType, Strength, Volume, DistilleryStatus, Price, URLBottle, URLAuction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (WATitle, WALotNo, WADistilery, WAAge, WAVintage, WARegion, WABottler, WACaskType, WAStrength, WAVolume, WADistilleryStatus, WAPrice, WAURLBottle, WAURLAuction))
        db.commit()

    print('WA Scrape Complete')


def WEProductLinkScrape(WEurls):
    """Scrape all Whisky Product Links from whiskyexchange.come"""

    WEProductLinks = []

    for WEurl in WEurls:
        WEpage_soup = HTMLParse(WEurl)
        whisky = WEurl.split('/')[5].split('?')[0]
        page = 1

        while True:
            print('Scraping ' + whisky + ' Links on Page : ' + str(page))
            for link in WEpage_soup.findAll('a', attrs={'href': re.compile('/p/')}):
                 WEProductLinks.append('https://www.thewhiskyexchange.com' + link.get('href'))
            if WEpage_soup.find("a", {"class": "page-link active"}).find_next_sibling("a") is None:
                break
            page += 1
            WEurl = 'https://www.thewhiskyexchange.com/c' + WEurl.split('/c')[1].split('?')[0] + '?filter=true&rfdata=&pg=' + str(page) + '#productlist-filter'
            WEpage_soup = HTMLParse(WEurl)

        print(WEProductLinks)

    return WEProductLinks


def WEScrape(WEProductLinks):
    """Scrape all Whisky Product data from whiskyexchange.com"""

    itemcounter = 0

    for url in WEProductLinks:

        itemcounter += 1
        print('Scraping WE Data. Item ' + str(itemcounter) + ' of ' + str(len(WEProductLinks)))
        Bottle = HTMLParse(url)

        try:
            WETitle = (Bottle.find("h1", {"itemprop": "name"})).text.strip()
        except:
            WETitle = 'NULL'
        print(WETitle)
        try:
            WEDistilery = (Bottle.find("div", {"class": "distillery"})).text.strip()
        except:
           WEDistilery = 'Null'
        try:
            WAAge = re.split(" year old", (Bottle.find("div", {"class": "age"})).text.strip(), flags=re.IGNORECASE)[0]
        except:
           WEAge = 'Null'
        try:
            WAVintage = (Bottle.find("div", {"class": "right"}).find("div", {"class": "topvbn"}).find("div", {"class": "region"})).text.strip()
        except:
            WAVintage = 'Null'
        try:
            WERegion = (Bottle.find("div", {"class": "right"}).find("div", {"class": "topvbn"}).find("div", {"class": "region"}).next_sibling.next_sibling).text.strip()
        except:
            WERegion = 'Null'
        try:
            WACaskType = (Bottle.find("div", {"class": "casktype"}).next_sibling.next_sibling).text.strip()
        except:
            WACaskType = 'NULL'
        try:
            WEStrength = (Bottle.find("div", {"class": "strength"})).text.strip()
        except:
            WEStrength = 'NULL'
        try:
            WEVolume = (Bottle.find("div", {"class": "bottlesize"})).text.strip()
        except:
            WEVolume = 'NULL'
        try:
            WEDistilleryStatus = (Bottle.find("div", {"class": "bottlestatus"})).text.strip()
        except:
            WEDistilleryStatus = 'NULL'
        try:
            WEPrice = (Bottle.find("span", {"class": "uc-price"})).text.strip()
        except:
            WEPrice = 'NULL'
        try:
            WEURLBottle = url
        except:
            WEURLBottle = 'NULL'
        try:
            WEBottler = (Bottle.find("dt", string='Bottler').find_next_sibling("dd")).text.strip()
        except:
            WEBottler = 'NULL'
        print(WEBottler)

        cursor.execute('INSERT INTO WEShop(Title, Bottler) VALUES (%s, %s)', (WETitle, WEBottler))
        db.commit()

    print('WE Scrape Complete')




# Whisky Auctioneer URL
WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction'

# Whisky Exchange URLs
WESingleMaltScotchurl = 'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?filter=true&rfdata=#productlist-filter'
WEBlendedScotchurl = 'https://www.thewhiskyexchange.com/c/304/blended-scotch-whisky?filter=true&rfdata=#productlist-filter'
WEBlendedMalturl = 'https://www.thewhiskyexchange.com/c/309/blended-malt-scotch-whisky?filter=true&rfdata=#productlist-filter'
WEGrainScotchurl = 'https://www.thewhiskyexchange.com/c/310/grain-scotch-whisky?filter=true&rfdata=#productlist-filter'
WEIrishurl = 'https://www.thewhiskyexchange.com/c/32/irish-whiskey?filter=true&rfdata=#productlist-filter'
WEAmericanurl = 'https://www.thewhiskyexchange.com/c/33/american-whiskey?filter=true&rfdata=#productlist-filter'
WEJapaneseurl = 'https://www.thewhiskyexchange.com/c/35/japanese-whisky?filter=true&rfdata=#productlist-filter'
WECanadianurl = 'https://www.thewhiskyexchange.com/c/34/canadian-whisky?filter=true&rfdata=#productlist-filter'
WERestofWorldurl = 'https://www.thewhiskyexchange.com/c/305/rest-of-the-world-whisky?filter=true&rfdata=#productlist-filter'
#WEurls = [WESingleMaltScotchurl, WEBlendedScotchurl, WEBlendedMalturl, WEGrainScotchurl, WEIrishurl, WEAmericanurl, WEJapaneseurl, WECanadianurl, WERestofWorldurl]
WEurls = [WEBlendedMalturl]

# Grab the Whiskey Auction HTML
#WApage_soup = HTMLParse(WAurl)

# Scrape Lot Numbers, Description and Price of all items and return as a numpy array
#LotLinks = WALotLinkScrape(WApage_soup)
#WAScrape(LotLinks, WAurl)

# Scrape WE
WEProductLinks = WEProductLinkScrape(WEurls)
WEScrape(WEProductLinks)
db.close()

# Grabs Web Price of Whiskey and find cheapest

#MoMWebPrice = (MoMpage_soup.find("div", {"class":"priceDiv"})).text
#WSWebPrice = (WSpage_soup.find("span", {"class":"price"})).text.strip()
#MinWebPrice = min(WEWebPrice, MoMWebPrice, WSWebPrice)