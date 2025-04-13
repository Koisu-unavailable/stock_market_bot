import requests


def get_all_symbols() -> list[str]:
    list_of_stocks = requests.get(
        "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
    ).text

    with open("list_of_stocks.txt", "w") as f:
        f.write(list_of_stocks)
    with open("list_of_stocks.txt", "r") as f:
        lines = f.readlines()
        symbols = [("")] * len(lines)
        for i, line in enumerate(lines):
            if lines.index(line) == 0:
                continue

            for char in line:
                if char != "|":
                    if char != "\n":
                        symbols[i] += char
                else:
                    break
        for symbol in symbols:
            if symbol == "":
                symbols.remove(symbol)
                continue

        # DON'T CHANGE THE ORDER
        symbols.pop(len(symbols) - 2)
        symbols.pop(len(symbols) - 1)
        # remove last  2 elements
    return symbols
