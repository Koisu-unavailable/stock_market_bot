import discord
from discord import app_commands
from discord.ext import commands

import logging
from webscraper.get_stock import get_price_from_yahoo_finance

logger = logging.getLogger("SetUp")


class MyCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  group = app_commands.Group(name="stock", description="all stock related commands")
  # Above, we declare a command Group, in discord terms this is a parent command
  # We define it within the class scope (not an instance scope) so we can use it as a decorator.
  # This does have namespace caveats but i don't believe they're worth outlining in our needs.

  @group.command(name="price")    # we use the declared group to make a command.
  async def get_price(self, interaction: discord.Interaction, symbol: str) -> None:
    """ /price sub-command """
    await interaction.response.defer(ephemeral=True, thinking=True)
    price = get_price_from_yahoo_finance(symbol)
    if price is None:
      await interaction.followup.send("Something went wrong. You likely entered an invalid symbol.", ephemeral=True)
      return
    await interaction.followup.send(str(price), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
  
