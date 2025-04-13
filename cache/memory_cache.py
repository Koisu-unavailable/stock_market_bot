from __future__ import annotations

from typing import Literal


STOCK_CACHE: dict[str, Stock] = {}  # type: ignore  # noqa: F821

broker_obj = dict[
    Literal["name"] | Literal["image_url"] | Literal["rarity"] | Literal["price"],
    str | float,
]

BROKERS: dict[str, broker_obj] = {}


CURRENT_BROKERS_IN_SHOP = []

BROKER_RARITIES = ["Common", "Cool", "Rare", "Legendary"]
