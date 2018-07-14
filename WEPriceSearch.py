# Search Whisky Exchange Price
# Search format https://www.thewhiskyexchange.com/search?q=FIRSTWORD+SECONDWORD

from HTMLParse import HTMLParse
from bs4 import BeautifulSoup as soup

def WEPriceSearch(WADescription):
    
    WEurl = 'https://www.thewhiskyexchange.com/search?q=' + WADescription.replace(' ', '+')
    if '&' in WEurl:
        WEurl = WEurl.replace('&', '')
    WEpage_soup = HTMLParse(WEurl)

    # Grab containers of all search results
    WEResultsContainers = WEpage_soup.findAll("div", {"class":"item"})

    for WEContainer in WEResultsContainers:
        WEDescription = WEContainer.find("div", {"class":"name"}).text.strip()

        if WEDescription == WADescription:
            WEWebPrice = (WEpage_soup.find("span", {"class":"price"})).text.strip()
            return WEWebPrice
    
