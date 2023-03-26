import os
import random
import sys
import json
import asyncio
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
from Helpers import config
import sqlite3

config_data = config.read_config()
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_ready():
    print("Hello there, I am ready to go")
    print("=================================")
    status.start()


@bot.slash_command(name="test", description="Test bot 023", guild_ids=config_data["GUILD_IDS"])
async def test(interaction: Interaction):
    await interaction.response.send_message("(╯°□°)╯︵ ┻━┻")


@tasks.loop(minutes=30.0)
async def status():
    statues = ["with Junior Devs", "with Devs", "with Humanity!", "with Python", "with Nextcord", "with Discord"]
    await bot.change_presence(activity=nextcord.Game(random.choice(statues)))


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


asyncio.run(load_cogs())
bot.run(config_data["DISCORD_TOKEN"])

#TODO: Use UI elements to make this look better
#TODO: Add a way to record a VM
