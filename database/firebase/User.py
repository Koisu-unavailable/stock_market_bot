from recordclass import RecordClass


class User(RecordClass):
    userId : int
    stocks : dict[str, int]
    money: float
    @staticmethod
    def from_dict(user_dict: dict):
        user = User(user_dict["userId"], user_dict["stocks"], user_dict["money"])
        return user
    def to_dict(user):
        return_user = {}
        return_user["userId"] = user.userId
        return_user["stocks"] = user.stocks
        return_user["money"] = user.money
        return return_user

        
            