from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Literal


class Consumable(ABC):
    def __init__(self):
        self._id: str = type(self).__name__.lower()
        self._price: str
        self.display_name: str
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


class priceis0(Consumable):
    def __init__(self):
        super().__init__()
        self._price = 100
        self.display_name = "Freebie"

    def consume(self, transaction):
        transaction.price = 0
