from typing import Literal
from database.stock_obj import Stock

STOCK_CACHE : dict[str, Stock] = {}

broker_obj = dict[Literal["name"] | Literal["image_url"] | Literal["rarity"], str]

BROKERS: dict[str, dict[Literal["name"] | Literal["image_url"], str]] = {}


CURRENT_BROKERS_IN_SHOP = ["Test", "Test1"]

