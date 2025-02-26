import os

from bs4 import BeautifulSoup
import requests

import requests
import logging


SEARCH_LINK_TEMPLATE = "https://finance.yahoo.com/quote/{symbol}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "From": os.environ["email"],
}


html_doc = requests.get(SEARCH_LINK_TEMPLATE, headers=headers)
print("dj")


def get_price_from_yahoo_finance(symbol: str) -> int:
    html_doc = requests.get(SEARCH_LINK_TEMPLATE.format(symbol=symbol), headers=headers)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    return float(
        str(
            soup.find(name="span", attrs={"data-testid": "qsp-price"}).contents[0]
        ).strip(" ")
    )
