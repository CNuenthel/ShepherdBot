""" Main discord bot """

import os
import discord
import json
import logging

from discord.ext import commands
from pretty_help import PrettyHelp

# Error and Debug logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Discord Bot instantiation
bot = commands.Bot(command_prefix=".")
bot.help_command = PrettyHelp(no_category="Base", sort_commands=True)


@bot.event
async def on_ready():
    """ Called when bot is activated """
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Game("Herding Bots"))
    print("✨ Shepherd Bot is in the Meadow! ✨")


@bot.command()
async def load(ctx, extension):
    """ Load a cog extension """
    if ctx.message.author.guild_permissions.administrator:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"```{extension} loaded! 🚀 ```")


@bot.command()
async def unload(ctx, extension):
    """ Unload a cog extension """
    if ctx.message.author.guild_permissions.administrator:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"```{extension} unloaded! 😱 ```")

# Initial load of all cogs in the cogs folder
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


with open("config.json", "r") as f:
    config = json.load(f)

bot.run(config["bot_token"])


