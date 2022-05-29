""" Toyhou.se scraper cog, adds interactive commands with Toyhou.se website """
import functions
import discord
import userdb
import asyncio
import os

from discord.ext import commands
from functions import functions
from toyhousescraper import ToyHouseScraper
from functools import partial


class ToyHouse(commands.Cog):
    """
    Discord Bot Cog, adds user interaction with images on Toyhou.se website
    """

    def __init__(self, bot):
        self.bot = bot
        self.scraper = ToyHouseScraper()
        self.db = userdb.UserDBService()
        self.img_count = 10

    @commands.Cog.listener()
    async def on_ready(self):
        """ Confirms cog load """
        print("✨ Toyhou.se is being herded! ✨")

    @commands.command()
    async def link(self, ctx):
        """
        Links a discord user to a toyhouse user account

        Toyhouse user profile must be set to visible to guests or these bot features
        will be unavailable.
        """
        await ctx.send(embed=functions.base_embed(
            title="Link Account",
            text="Tell me your Toyhou.se username and I'll link it!"
        ))

        # Message retrieval and verification
        try:
            msg = await self.bot.wait_for("message", check=partial(functions.basic_msg_check, ctx), timeout=45)
            self.scraper.set_route(msg.content)
            user_page_exists = self.scraper.verify_user_found()

        # Timeout command
        except asyncio.TimeoutError:
            await ctx.send(embed=functions.base_embed(
                title="Ok",
                text=f"Times up! Call me back if you'd like to link accounts ⏰"
            ))
            return

        # Confirm page accuracy
        if user_page_exists:
            verify_msg = await ctx.send(embed=functions.user_confirm_embed(
                user_page=self.scraper.route,
                user_name=msg.content.title()
            ))
        else:
            await ctx.send(embed=functions.base_embed(
                title="Link Account",
                text="Well this is awkward... that profile was either not found on Toyhou.se "
                     "or the user is not visible to guests 😬"
            ))
            return

        # Confirm reaction set
        await verify_msg.add_reaction("✅")
        await verify_msg.add_reaction("❌")

        # Wait for user reaction
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=partial(functions.basic_reaction_check, ctx),
                timeout=35)

        except asyncio.TimeoutError:
            await ctx.send(embed=functions.base_embed(
                title="Link Account",
                text="Times up! Call me back if you'd like to link accounts ⏰"
            ))
            return

        if str(reaction) == "❌":
            await verify_msg.delete()
            await ctx.send(embed=functions.base_embed(
                title="Link Account",
                text="Shoot, I missed! Make sure you gave me your correct username! 😅"
            ))
            return

        await verify_msg.delete()
        # Save user ID and Toyhou.se account name
        # If user is not in the DB, insert and advise, else update and advise
        if not self.db.query_id(ctx.author.id):
            self.db.insert(ctx.author.id, ctx.author.name, msg.content.title())
            await ctx.send(embed=functions.base_embed(
                title="Account Link",
                text="🌠 Successfuly Linked! Welcome to the meadow 🌠",
                footer=f"{ctx.author.name} linked to {msg.content}."
            ))
        else:
            self.db.update_th_account(ctx.author.id, msg.content.title())
            await ctx.send(embed=functions.base_embed(
                title="Account Link",
                text="🌠 Welcome back! I updated your link! 🌠",
                footer=f"{ctx.author.name} linked to {msg.content}."
            ))

    @commands.command()
    async def random(self, ctx):
        """ Display a random file image of a character from your linked Toyhouse account """
        user = self.db.query_id(ctx.message.author.id)
        if user:
            self.scraper.set_route(user.th_account)
            path, caption = self.scraper.scrape_random_image()
            file = discord.File(path, filename="image.png")
            await ctx.send(embed=functions.random_img_embed(
                caption=caption, msg_author=user.th_account), file=file)
            os.remove(path)

        else:
            await ctx.send(embed=functions.base_embed(
                title="No Linked Account",
                text="You need to link your Toyhou.se account before using this command!"))


def setup(bot):
    """ Required setup function for cog """
    bot.add_cog(ToyHouse(bot))
