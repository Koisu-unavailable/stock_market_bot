import discord
import discord.types
from discord import app_commands
from discord.ext import commands, tasks

from utils.database import get_user_from_interaction
import logging

logger = logging.Logger("MiselleneousCog")


class Miselleneous_Cog(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="money", description="View how much money you have")
    async def view_money(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        user = await get_user_from_interaction(interaction)
        await interaction.followup.send(f"{interaction.user.mention} has ${user.money}")


async def setup(client: commands.Bot):
    await client.add_cog(Miselleneous_Cog(client))
    logger.info("MisellenousCog loaded")
