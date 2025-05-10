from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Literal
from transaction import Transaction, BuyStock, BuyConsumable
import errors
class Consumable(ABC):
    def __init__(self):
        self._id: str = type(self).__name__.lower()
        self._price: str
        self.display_name: str
        self.description : str
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
        self.description = "Next transaction cost $0 dollars!"

    def consume(self, transaction):
        transaction.price = 0
        
class seeingDouble(Consumable):
    def __init__(self):
        super().__init__()
        self._price = 50
        self.display_name = "Seeing Double"
        self.description = "If using this to buy a consumable or stock, get double the amount you requested fo the same price!"
    def consume(self, transaction:Transaction ):
        if not (isinstance(transaction, BuyStock ) | isinstance(transaction, BuyConsumable)):
            raise errors.WrongTransaction("This consumable may only be used when buy stocks or powerups")
        transaction.amount *= 2
        return
    
