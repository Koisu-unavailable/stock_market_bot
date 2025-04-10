import logging
from typing import List

import discord
import discord.types
from discord import app_commands
from discord.ext import commands

from cache import STOCK_CACHE
from functools import cache
from database.firebase.databse_user import add_or_update_user, get_user_by_id
from database.firebase.User import User
from database.stock_obj import Stock
from stock_bot.errors import StockIsNoneException, StockNotFound
from webscraper.get_stock import get_price_from_yahoo_finance
from stock_bot.transaction import (
    BuyStock,
    SellStock,
    TransactionResult,
    SellTransactionResult,
)

logger = logging.getLogger("StockCog")


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
        # add_stock_or_edit(symbol, stock.price, stock.exchange)
        STOCK_CACHE[symbol] = stock
        return stock

    @group.command(
        name="price", description="Get the price of a stock with it's symbol"
    )
    async def get_price(self, interaction: discord.Interaction, symbol: str) -> None:
        """Get the prrice of a stock, prefer the memory cache for retreiving"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            stock = await self._get_stock(symbol)
        except StockNotFound as e:
            await self._stock_not_found(interaction, e)
            return
        price = stock.price
        exchange = stock.exchange
        await interaction.followup.send(str(price) + str(exchange), ephemeral=True)
        return

    @group.command(name="buy", description="buy a stock")
    async def buy_stock(
        self, interaction: discord.Interaction, symbol: str, amount: int
    ):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user = await self._get_user_from_interaction(interaction)
        try:
            stock = await self._get_stock(symbol)
        except StockNotFound as e:
            await self._stock_not_found(interaction, e)
            return
        try:
            transaction = BuyStock(stock.price, user, user, amount, symbol)
        except ValueError:
            await interaction.followup.send(f"{amount} is not a valid amount.")
            return
        result = transaction.complete()
        match result:
            case TransactionResult.Poor:
                await interaction.followup.send(
                    "You're too poor the the requested stock."
                )
            case TransactionResult.Success:
                await interaction.followup.send(
                    f"You now have {user.stocks[symbol]} {stock.display_name} stock"
                )
        return

    @group.command(name="sell", description="sell a stock with for profit (hopefully)")
    async def sell_stock(
        self, interaction: discord.Interaction, symbol: str, amount: int
    ):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user: User = await self._get_user_from_interaction(interaction)

        try:
            stock = await self._get_stock(symbol)
        except StockNotFound as e:
            await self._stock_not_found(interaction, e)

        try:
            transaction = SellStock(stock.price, user, [], amount, symbol)
        except ValueError:
            await interaction.followup.send(f"{amount} is not a valid amount.")
            return

        result = transaction.complete()
        match result:
            case SellTransactionResult.Success:
                await interaction.followup.send(
                    f"Successfully sold {amount} of {stock.display_name} stock(s)"
                )
            case SellTransactionResult.NotEnoughStock:
                await interaction.followup.send(f"You don't have enough of the requested stock {stock.display_name}.")
        return

    @sell_stock.autocomplete("symbol")
    async def sell_stock_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        data = []
        user = get_user_by_id(interaction.user.id)
        for symbol in user.stocks.keys():
            if symbol != "None" and current.lower() in symbol:
                data.append(app_commands.Choice(name=symbol, value=symbol))
        return data

    async def _get_stock(self, symbol: str) -> Stock:
        all_symbols = STOCK_CACHE.keys()
        stock_is_there = False
        for stock_symbol in all_symbols:
            if stock_symbol == symbol:
                stock_is_there = True
                break
        try:
            stock = self._get_stock_and_cache(symbol, stock_is_there)
            return stock
        except StockIsNoneException:
            raise StockNotFound(f"Stock: {symbol} was not found")

    async def _stock_not_found(self, interaction: discord.Interaction, e: Exception):
        logger.error(e)
        await interaction.followup.send(
            "Something went wrong. Perhaps you've entered an invalid symbol.",
            ephemeral=True,
        )

    async def _get_user_from_interaction(
        self, interaction: discord.Interaction
    ) -> User:
        """Gets the user from the reaction, if they don't exist, create them and give them the starting amount of money."""
        userId = interaction.user.id
        user = get_user_by_id(userId)

        if user is None:
            user = User(userId, {}, 10**5)  # $10000 to start
            add_or_update_user(user)
        return user


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Stock_Cog(bot))
    logger.info("Stock cog loaded")
