""" Initialization of an interactions discord bot """

import interactions
import os
import discord
import json
import toyhousescraper

test_id = 870701146099044412

with open("config.json", "r") as f:
    config = json.load(f)


class Bot(interactions.Client):
    """ Easy instantiation of a Discord Bot with on ready declaration """
    def __init__(self):
        super().__init__(config["bot_token"])

    async def on_ready(self):
        await self.wait_until_ready()
        print("✨ Shepherd Bot is in the Meadow! ✨")


# Initialize a bot
bot = Bot()

@bot.command(
    name="add_toys",
    description="Bind your Toyhou.se account!",
    scope=test_id,
    options=[
        interactions.Option(
            name="username",
            description="What is your Toyhou.se username?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def add_toys(ctx: interactions.CommandContext, username: str):
    ths = toyhousescraper.ToyHouseScraper(username)
    user_img = ths.scrape_user_image()
    embed = discord.Embed(
        title="Toyhou.se Username",
        url=user_img,
        description="Account Bound!",
        color=discord.Color.green()
        )
    await ctx.send(embed=embed)


bot.start()


