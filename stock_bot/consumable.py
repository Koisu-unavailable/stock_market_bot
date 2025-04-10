from __future__ import annotations
from abc import ABC, abstractmethod

VALID_BUFFS = [
    "PriceIs0",
]


class Consumable(ABC):
    def __init__(self):
        self._id: str
        self._price: str
        pass

    @property
    def id(self):
        return self._id

    @property
    def price(self):
        return self._price

    @abstractmethod
    def consume(self, transaction: Transaction):  # type: ignore # noqa: F821
        pass


class PriceIs0(Consumable):
    def __init__(self):
        super().__init__()
        self._id = "priceIs0"

    def consume(self, transaction):
        transaction.price = 0
