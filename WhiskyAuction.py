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

import numpy as np
import re
from HTMLParse import HTMLParse
from WAScrape import WAScrape

WAurl = 'https://www.whiskyauctioneer.com/january-2018-auction'

# Grab the Whiskey Auction HTML
WApage_soup = HTMLParse(WAurl)

# Scrape Lot Numbers, Description and Price of all items and return as a numpy array
AuctionLots = WAScrape(WApage_soup)
print(AuctionLots)

# Grabs Web Price of Whiskey and find cheapest

#MoMWebPrice = (MoMpage_soup.find("div", {"class":"priceDiv"})).text
#WSWebPrice = (WSpage_soup.find("span", {"class":"price"})).text.strip()
#MinWebPrice = min(WEWebPrice, MoMWebPrice, WSWebPrice)



