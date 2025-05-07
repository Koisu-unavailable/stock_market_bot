from __future__ import annotations
import typing

from recordclass import RecordClass  # mutable named tuple
from typing import List
from utils.types import Consumable_ID_Type
from typing import get_origin, Dict
from utils import trim_at_char


class User(RecordClass):
    userId: int
    stocks: dict[str, int]
    money: float
    consumables: dict[Consumable_ID_Type, int]
    brokers: list[Broker]  # type: ignore  # noqa: F821
    active_consumables: list[Consumable_ID_Type]
    active_brokers: list[Broker]  # type: ignore  # noqa: F821

    @staticmethod
    def from_dict(user_dict: dict):
        user_dict = normalise_user(user_dict)
        user = User(
            user_dict["userId"],
            user_dict["stocks"],
            user_dict["money"],
            user_dict["consumables"],
            user_dict["brokers"],
            user_dict["active_consumables"],
            user_dict["active_brokers"]
        )
        return user

    def to_dict(user):
        return_user = {}
        return_user["userId"] = user.userId
        return_user["stocks"] = user.stocks
        return_user["money"] = user.money
        return_user["consumables"] = user.consumables
        return_user["brokers"] = user.brokers
        return_user["active_consumables"] = user.active_consumables
        return_user["active_brokers"] = user.active_brokers
        return return_user


def normalise_user(user_dict: dict):
    """If any values are missing from a user dictionary, add the empty versions of the values.
    This function ensures that all attributes of the User class are present in the dictionary,
    even if they weren't explicitly set."""
    for (
        key,
        var_type,
    ) in User.__annotations__.items():  # get all the annotated variables
        if key not in user_dict.keys():
            true_type = trim_at_char(var_type, "[")
                
            
            if true_type == "dict":
                user_dict[key] = {}
            elif true_type ==  "list":
                user_dict[key] = []
            elif true_type ==  "str":
                user_dict[key] = ""
            elif true_type ==  "int":
                user_dict[key] = 0
            elif true_type == "float":
                user_dict[key] = 0
    return user_dict

if __name__ == "__main__":
    
    print(normalise_user({}))