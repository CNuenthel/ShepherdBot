""" Main discord bot """

import os
import discord
from discord.ext import commands
import json

test_id = 870701146099044412
bot = commands.Bot(command_prefix=".")


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


