import logging
import os


import discord
from discord import app_commands
from discord.ext import commands

import requests


import stock_bot.cogs.stock

from dotenv import load_dotenv

assert load_dotenv("./.env")
intents = discord.Intents.all()
client =   commands.Bot(intents=intents, command_prefix="!")



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
    log_level=os.environ.get("LOG_LEVEL", "INFO").upper(), # type: ignore
    root_logger=True,
)