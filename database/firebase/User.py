from __future__ import annotations

from recordclass import RecordClass  # mutable named tuple
from typing import List

class User(RecordClass):
    userId: int
    stocks: dict[str, int]
    money: float
    consumables: dict[Consumable] # type: ignore  # noqa: F821
    @staticmethod
    def from_dict(user_dict: dict):
        user = User(user_dict["userId"], user_dict["stocks"], user_dict["money"], user_dict["consumables"])
        return user

    def to_dict(user):
        return_user = {}
        return_user["userId"] = user.userId
        return_user["stocks"] = user.stocks
        return_user["money"] = user.money
        return_user["consumables"] = user.consumables
        return return_user
