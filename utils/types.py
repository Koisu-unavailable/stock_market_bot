from typing import Literal, get_args


type Consumable_ID_Type = Literal["priceis0"]
"""All consumable id's"""
def is_valid_consumable_id(id):
    return id in get_args(Consumable_ID_Type)
