from typing import NamedTuple


class User(NamedTuple):
    usedId : int
    stocks : list[str]
    @staticmethod
    def from_dict(user_dict: dict):
        return User(user_dict["userId"], user_dict["stocks"])
            