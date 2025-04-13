from typing import NamedTuple


class Stock(NamedTuple):
    symbol: str
    price: float
    exchange: str
    display_name: str
    __tablename__ = "stock"
