import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def HTMLParse(url):
    # Opening up connection, grabbing the pages
    Req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    Client = uReq(Req)
    html = Client.read()
    Client.close()

    # HTML Parser
    page_soup = soup(html, "html.parser")
    return page_soup
