import logging
import os


import discord
from discord import app_commands
from discord.ext import commands

import requests

import twelvedata

from dotenv import load_dotenv

load_dotenv(".env")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)


td = twelvedata.TDClient(apikey=os.environ["TD"])
@client.event
async def on_ready() -> None:
    logging.info("Bot is ready!!")
    await client.tree.sync()
    logging.info("Sync has run")
    
    
    
    
@client.tree.command(
    name="test",
    description="test"
)
async def test(interaction: discord.Interaction):
    
    await interaction.response.send_message("HAIII :3")
    
    

client.run(
    os.environ["TOKEN"],
    log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    root_logger=True,
)