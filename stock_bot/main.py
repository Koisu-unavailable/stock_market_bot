import json
import logging
import os

import discord
import discord.context_managers
import discord.ext
import discord.ext.commands
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import cache
import stock_bot.cogs.buffs
import stock_bot.cogs.stock

assert load_dotenv("./.env")  # make sure it loads
intents = discord.Intents.all()
client = commands.Bot(
    intents=intents, command_prefix="!"
)  # command prefix doesn't really matter as this bot uses slash commands because they're cooler 😀

with open("./brokers.json", "r") as f:
    cache.BROKERS = json.load(f)

@client.event
async def on_ready() -> None:
    logging.info("Sync has run")
    await stock_bot.cogs.stock.setup(client)
    await stock_bot.cogs.buffs.setup(client)
    await client.tree.sync(guild=discord.Object(1337277734480642109))
    logging.info("Bot is ready!!")
    
    
@client.tree.error
async def on_command_error(interaction: discord.Interaction, error):
    if not interaction.response.is_done:
        await interaction.response.send_message("An error occured, please try again later.")
    else:
        await interaction.followup.send("An error occured, please try again later.")
    logging.error("Error occured: ", exc_info=error)
client.run(
    os.environ["TOKEN"],
    log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),  
    root_logger=True,
)
