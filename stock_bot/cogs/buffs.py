import discord
import discord.types
from discord import app_commands
from discord.ext import commands
import logging
from utils.database import get_user_from_interaction
from database.firebase.databse_user import add_or_update_user
import stock_bot.consumable
from stock_bot.consumable import PriceIs0, Consumable, VALID_BUFFS
from stock_bot.ui import broker_shop_factory, ChangeBrokerInBrokerShop, Shop_State


logger = logging.getLogger("BuffsCog")


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

    group = app_commands.Group(name="buffs", description="all buff related commands")

    @group.command(name="view", description="view all your buffs")
    async def view_buffs(self, interaction: discord.Interaction):
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
            await interaction.followup.send("Invalid buff")
        user = await get_user_from_interaction(interaction)
        try:
            user.consumables[buff.id] += 1
        except KeyError:
            user.consumables[buff.id] = 1

        add_or_update_user(user)

    @group.command(name="buy_broker", description="buy a broker from the shop")
    @app_commands.describe(
        private="Whether you want everyone to see the shop, or just you."
    )
    async def show_broker_shop(
        self, interaction: discord.Interaction, private: bool = True
    ):
        # implent broker cycling
        await interaction.response.defer(thinking=True, ephemeral=private)
        embeds = [broker_shop_factory("Test"), broker_shop_factory("Test2")]
        view = discord.ui.View()
        state = Shop_State(current_broker =0 )
        view.add_item(
            ChangeBrokerInBrokerShop(
                label="Back",
                owner=interaction.user,
                back=True,
                embeds=embeds,
                shop_interaction=interaction,
                style=discord.ButtonStyle.red,
                shop_state=state,
            )
        )
        view.add_item(
            ChangeBrokerInBrokerShop(
                label="Next",
                owner=interaction.user,
                back=False,
                embeds=embeds,
                shop_interaction=interaction,
                style=discord.ButtonStyle.green,
                shop_state=state,
            )
        )

        await interaction.followup.send(embed=embeds[0], view=view)
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Buffs_Cog(bot))
    logger.info("Buffs cog loaded")
