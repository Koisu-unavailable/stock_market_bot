import logging
from random import choice, shuffle
from typing import Literal, Union

import discord
import discord.types
from discord import app_commands
from discord.ext import commands, tasks

import cache
import cache.constants
import stock_bot.consumable
from stock_bot.consumable import VALID_BUFFS, Consumable
from stock_bot.ui import ChangeBrokerInBrokerShop, Shop_View, broker_shop_embed_factory
from utils.database import get_user_from_interaction
from stock_bot.transaction import BuyConsumable, TransactionResult

logger = logging.getLogger("BuffsCog")
cycle_broker_logger = logging.Logger("cycle_broker_task", logging.INFO)


class ConsumableTransformer(app_commands.Transformer):
    async def transform(
        self, interaction: discord.Interaction, value: str
    ) -> Consumable:
        if value not in VALID_BUFFS:
            return None
        consumable = getattr(stock_bot.consumable, value)
        return consumable()


class Buffs_Cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cycle_brokers.start()
        cycle_broker_logger.info("I have been started")

    group = app_commands.Group(name="buffs", description="all buff related commands")

    @group.command(name="view", description="view all your buffs and brokers")
    @app_commands.describe(
        what='What you wanna view'
    )
    async def view_buffs(self, interaction: discord.Interaction, what: Literal["BROKERS", "BUFFS"]):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user = await get_user_from_interaction(interaction)
        await interaction.followup.send(user.consumables)

    @group.command(name="buy_consumable", description="test")
    async def buy_consumable(
        self,
        interaction: discord.Interaction,
        buff: app_commands.Transform[Consumable, ConsumableTransformer],
    ):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if buff is None:
            await interaction.followup.send("Invalid buff requested")
            return

        transaction = BuyConsumable(
            buff.price, await get_user_from_interaction(interaction.user), [], buff.id
        )
        result = transaction.complete()
        user = await get_user_from_interaction(interaction.user)
        match result:
            case TransactionResult.Success:
                await interaction.followup.send(
                    f"You now have {user.consumables[buff.id]}, {buff.display_name}"
                )
            case TransactionResult.Poor:
                await interaction.followup.send("You're too poor!")

    @group.command(name="buy_broker", description="buy a broker from the shop")
    @app_commands.describe(
        private="Whether you want everyone to see the shop, or just you."
    )
    async def show_broker_shop(
        self, interaction: discord.Interaction, private: bool = False
    ):
        # implent broker cycling
        await interaction.response.defer(thinking=True, ephemeral=private)
        brokers = [broker_id for broker_id in cache.CURRENT_BROKERS_IN_SHOP]
        embeds = [broker_shop_embed_factory(broker_id) for broker_id in brokers]
        if len(embeds) == 0:
            pass  # <-- add default brokers
        print(len(embeds))
        view = Shop_View(owner=interaction.user, brokers=brokers)

        view.add_item(
            ChangeBrokerInBrokerShop(
                label="Back",
                back=True,
                embeds=embeds,
                shop_interaction=interaction,
                style=discord.ButtonStyle.red,
            )
        )
        view.add_item(
            ChangeBrokerInBrokerShop(
                label="Next",
                back=False,
                embeds=embeds,
                shop_interaction=interaction,
                style=discord.ButtonStyle.green,
            )
        )

        await interaction.followup.send(embed=embeds[0], view=view, ephemeral=private)
        return
    @tasks.loop(minutes=5.0)
    async def cycle_brokers(self):
        """Changes brokers in shop."""
        list_of_brokers = []
        for id in cache.BROKERS.keys():
            match cache.BROKERS[id]["rarity"]:
                case 0:
                    list_of_brokers.extend([id] * 25)
                case 1:
                    list_of_brokers.extend([id] * 12)
                case 2:
                    list_of_brokers.extend([id] * 6)
                case 3:
                    list_of_brokers.extend([id] * 3)
        cache.CURRENT_BROKERS_IN_SHOP = []
        while (
            len(cache.CURRENT_BROKERS_IN_SHOP)
            < cache.constants.BROKERS_IN_SHOP_AT_A_TIME
        ):  # continue until populated
            selection = choice(list_of_brokers)

            list_of_brokers = [
                broker_id
                for broker_id in list_of_brokers
                if broker_id != selection  # <-- remove all occurances of selection
            ]

            cache.CURRENT_BROKERS_IN_SHOP.append(selection)
        cache.CURRENT_BROKERS_IN_SHOP = list(
            set(cache.CURRENT_BROKERS_IN_SHOP)
        )  # <-- remove dupes
        shuffle(cache.CURRENT_BROKERS_IN_SHOP)
        cycle_broker_logger.error(f"Cycled Jokers to: {cache.CURRENT_BROKERS_IN_SHOP}")
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Buffs_Cog(bot))
    logger.info("Buffs cog loaded")
