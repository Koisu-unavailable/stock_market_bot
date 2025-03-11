import discord
from discord import app_commands
from discord.ext import commands

import logging
from webscraper.get_stock import get_price_from_yahoo_finance
from database.sqlite.database_stock import add_stock_or_edit, get_all_stocks

from cache import STOCK_CACHE
from database.stock_obj import Stock
from stock_bot.errors import StockIsNoneException

logger = logging.getLogger("SetUp")


class Stock_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="stock", description="all stock related commands")

    def _get_stock_and_cache(self, symbol: str, stock_is_there: bool):
        if stock_is_there:
            return STOCK_CACHE[symbol]

        stock = get_price_from_yahoo_finance(symbol)
        if stock is None:
            raise StockIsNoneException(
                f"{symbol} returned None from get_syjmbol_from_yahoo_finance"
            )
        add_stock_or_edit(symbol, stock.price, stock.exchange)
        STOCK_CACHE[symbol] = stock
        return stock

    @group.command(
        name="price", description="Get the price of a stock with it's symbol"
    )
    async def get_price(self, interaction: discord.Interaction, symbol: str) -> None:
        """Get the prrice of a stock, prefer the memory cache for retreiving"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        all_symbols = STOCK_CACHE.keys()
        stock_is_there = False
        for stock_symbol in all_symbols:
            if stock_symbol == symbol:
                stock_is_there = True
                break
        try:
            stock = self._get_stock_and_cache(symbol, stock_is_there)
        except StockIsNoneException as e:
            logger.error(e)
            await interaction.followup.send(
                "Something went wrong. Perhaps you've entered an invalid symbol.",
                ephemeral=True,
            )
            return
        price = stock.price
        exchange = stock.exchange
        await interaction.followup.send(str(price) + str(exchange), ephemeral=True)
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Stock_Cog(bot))
