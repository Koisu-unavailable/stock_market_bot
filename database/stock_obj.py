from typing import NamedTuple

class Stock(NamedTuple):
    symbol : str
    price: float
    exchange: str
    __tablename__  = "stock"