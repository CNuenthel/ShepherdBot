from disnake.ext import commands
import os

# Prior to release, remove test_guilds as a kwarg
bot = commands.Bot(
    command_prefix="!",
    test_guilds=[870701146099044412],
    sync_commands_debug=True,
    sync_commands=False
)


@bot.slash_command(description="Loads a bot extension")
async def load(inter, extension: str):
    bot.load_extension(f"cogs.{extension}")


@bot.slash_command(description="Unloads a bot extension")
async def unload(inter, extension: str):
    bot.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("bot_token"))
# OTY3NzYwNjAxMDY3NzE2NjA4.YmU_Sw.5O8ILDNu9mze6X89eBdO3zFaE5E
