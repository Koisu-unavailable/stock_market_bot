import os

from bs4 import BeautifulSoup
import requests

import requests
import logging
from database.sqlite.stock import add_stock_or_edit

logging.basicConfig(level=logging.NOTSET)

STOCKS = [
    # https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt <-- LIST OF ALL NASDAQ STOCKS!!!
    'goog',
    'ssss'
]
SEARCH_LINK_TEMPLATE = "https://finance.yahoo.com/quote/{symbol}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "From": os.environ["email"],
}


html_doc = requests.get(SEARCH_LINK_TEMPLATE, headers=headers)
print("dj")


def _get_price_from_yahoo_finance(symbol: str) -> int:
    html_doc = requests.get(SEARCH_LINK_TEMPLATE.format(symbol=symbol), headers=headers)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    price_element = soup.find(name="span", attrs={"data-testid": "qsp-price"})
    if price_element is None:
        return None
    return float(
        str(
            price_element.contents[0]
        ).strip(" ")
    )
    
def _add_stock(symbol: str, price: float):
    add_stock_or_edit(symbol, _get_price_from_yahoo_finance(symbol))
    
def update_database():
    for stock in STOCKS:
        _add_stock(stock, 99)
        
