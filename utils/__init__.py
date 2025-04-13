def trim_at_char(target: str, char: str) -> str:
    return target.split(char)[0]


def is_greater_than_zero(num):
    return num > 0


class PassByReference:
    def __setattr__(self, name, value):
        setattr(self, name, value)
