from __future__ import annotations

from typing import List, Self
from database.firebase.User import User
from database.firebase.databse_user import add_or_update_user, get_user_by_id


from enum import Enum
from abc import ABC, abstractmethod


class TransactionResult(Enum):
    Success = 0
    Poor = 1

class SellTransactionResult(Enum):
    Success = 0
    NotEnoughStock = 1
    
    
    
class Transaction(ABC):
    '''U must verify transaction validty yourself.
    '''
    def __init__(self, price: float, user: User, consumables: list[Consumable], amount: int): # type: ignore  # noqa: F821
        self.price = price * amount
        self.user = user
        self.consumables = consumables
        self.amount = amount
        if not self.amount >= 0:
            raise ValueError("Amount must be greater than 0")
        self.not_enough_value = TransactionResult.Poor
        self.result_enum  =  TransactionResult
    def _check_if_enough(self):
        self.enough = True if self.user.money >= self.price else False # Consumables made modify this varirable
        
    @abstractmethod
    def _update_user(self):
        pass
    
    def complete(self) -> TransactionResult:
        self._check_if_enough()
        self.result = self.result_enum.Success
        for consumable in self.consumables:
            consumable.consume(self)
        if not self.enough:
            self.result = self.not_enough_value
            return self.result # poor
        self._update_user()

        return self.result
    

    
class BuyStock(Transaction):
    def __init__(self, price_of_stock, user: User, consumables, amount, symbol):
        super().__init__(price_of_stock, user, consumables, amount)
        self.symbol = symbol
    def _update_user(self):
        self.user.money -= self.price
        try:
            self.user.stocks[self.symbol] += 1 * self.amount
        except KeyError:
            self.user.stocks[self.symbol] = 1 * self.amount

        add_or_update_user(self.user)
        

        
class SellStock(BuyStock): # almost exactley the same functionality just with a few signs flipped or at least the inits the same
    def __init__(self, price_of_stock, user, consumables, amount, symbol):
        super().__init__(price_of_stock, user, consumables, amount, symbol)
        self.not_enough_value = SellTransactionResult.NotEnoughStock
        self.result_enum = SellTransactionResult
    def _check_if_enough(self) -> None:
        """Changes `self.enough`
        """
        if self.symbol not in list(self.user.stocks.keys()):
            self.enough = False
            return
        self.enough = True if (self.user.stocks[self.symbol] >= self.amount) else False
    def _update_user(self):
        self.user.money += self.price
        self.user.stocks[self.symbol] -= 1 * self.amount
        if self.user.stocks[self.symbol] == 0:
            self.user.stocks.pop(self.symbol)
        add_or_update_user(self.user)

if __name__ == "__main__":
    # bootleg unit test
    test = BuyStock(200, get_user_by_id(713130676387315772), [], 29929, 'aapl' )
    result = test.complete()
    match result:
        case TransactionResult.Poor:
            print("poor")
        case TransactionResult.Success:
            print("success")
    
    
