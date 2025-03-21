import logging
import os

import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import stock_bot.cogs.stock

assert load_dotenv("./.env")  # make sure it loads
intents = discord.Intents.all()
client = commands.Bot(
    intents=intents, command_prefix="!"
)  # command prefix doesn't really matter as this bot uses slash commands because they're cooler 😀


@client.event
async def on_ready() -> None:
    logging.info("Sync has run")
    await stock_bot.cogs.stock.setup(client)
    await client.tree.sync()
    logging.info("Bot is ready!!")


# group = app_commands.Group(name="stock", description="all stock related commands")
# @group.command(
#     name="test",
#     description="test"
# )
# async def test(interaction: discord.Interaction):
#     await interaction.response.send_message("HAIII :3")


client.run(
    os.environ["TOKEN"],
    log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),  
    root_logger=True,
)
