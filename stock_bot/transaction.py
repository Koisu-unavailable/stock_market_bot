from database.firebase.User import User
from database.firebase.databse_user import add_or_update_user
from stock_bot.consumable import Consumable

from enum import Enum
from abc import ABC, abstractmethod


class TransactionResult(Enum):
    Success = 0
    Poor = 1
    InvalidAmount = 1
    
    
    
class Transaction(ABC):
    def __init__(self, price: float, user: User, consumables: list[Consumable], amount: int):
        self.price = price * amount
        self.user = user
        self.consumables = consumables
        self.amount = amount
    def _check_if_enough(self):
        self.enough = True if self.user.money >= self.amount else False
        
    @abstractmethod
    def _update_user(self):
        pass
    
    def complete(self) -> TransactionResult:
        self._check_if_enough()
        self.result = TransactionResult.Success
        if self.amount <= 0:
            self.result = TransactionResult.InvalidAmount
            return self.result # may not continue with an invalid amount
        for consumable in self.consumables:
            consumable.consume(self)
        if not self.enough:
            self.result = TransactionResult.Poor
            return self.result
        self._update_user()

        return TransactionResult.Poor
    

    
class BuyStock(Transaction):
    def __init__(self, price, user: User, consumables, amount, symbol):
        super().__init__(price, user, consumables, amount, symbol)
        self.symbol = symbol
    def _update_user(self):
        self.user.money -= self.price
        try:
            self.user.stocks[self.symbol] += 1 * self.amount
        except KeyError:
            self.user.stocks[self.symbol] = 1 * self.amount

        add_or_update_user(self.user)
        

if __name__ == "__main__":
    test = BuyStock(999, )
        
    
    
