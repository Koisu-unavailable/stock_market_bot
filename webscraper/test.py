from bs4 import BeautifulSoup
import requests


# import http.client
# http.client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

GOOLGLE_SEARCH_LINK_TEMPLATE = "https://finance.yahoo.com/quote/AAPL/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "From": "youremail@domain.example",  # This is another valid field
}


html_doc = requests.get(GOOLGLE_SEARCH_LINK_TEMPLATE, headers=headers)
print("dj")

soup = BeautifulSoup(html_doc.text, "html.parser")
with open("response.html", "w", encoding="UTF-8") as f:
    f.write(int(soup.find(name="span", attrs={"data-testid": "qsp-price"}).contents[0]))
