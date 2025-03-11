import os

from bs4 import BeautifulSoup
import requests

import logging

from database.sqlite.database_stock import add_stock_or_edit, get_all_stocks
from database.stock_obj import Stock
from utils.get_all_stock_symbols import get_all_symbols
from utils import trim_at_char

from fake_useragent import UserAgent
logging.basicConfig(level=logging.NOTSET)


SEARCH_LINK_TEMPLATE = "https://finance.yahoo.com/quote/{symbol}"

ua = UserAgent()
logger = logging.getLogger("Webscraper")

headers = {
    "User-Agent": ua.random,
    "From": os.environ["email"],
}




def get_price_from_yahoo_finance(symbol: str):
    html_doc = requests.get(SEARCH_LINK_TEMPLATE.format(symbol=symbol), headers=headers)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    price_element = soup.find(name="span", attrs={"data-testid": "qsp-price"})
    logger.debug("Found price element: " + str(price_element))
    exchange_element = soup.find("span", class_="exchange")
    logger.debug("Found exchange element: " + str(exchange_element))
    if exchange_element is None:
        return None
    exchange = exchange_element.contents[0].contents[0]
    exchange = trim_at_char(exchange, " ")
    
    if price_element is None:
        return None
    stock_price = float(
        str(
            price_element.contents[0]
        ).strip(" ")
    )
    return Stock(symbol, stock_price, exchange)
    
def _add_stock(symbol: str):
    add_stock_or_edit(symbol, get_price_from_yahoo_finance(symbol))
    
# def update_database(): <-- THIS IS A DEATH FUNCTION DON'T RUN IT
#     for stock in STOCKS:
#         _add_stock(stock)
        
        
        
if __name__ == "__main__":
    print(get_price_from_yahoo_finance("goog"))
