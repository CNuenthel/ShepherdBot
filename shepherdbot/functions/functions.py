import discord
from discord.ext import commands
import os
from img import img_path

""" Type Checking Vars"""
CTX = commands.context.Context
RCN = discord.reaction.Reaction
MEM = discord.member.Member
MSG = discord.message.Message


def base_embed(title: str,
               text: str,
               color: discord.Color = discord.Color.blurple(),
               footer: str = None):
    """ Creates a standard basic Embed to maintain consistency between routine embeds """
    base = discord.Embed(
        title=title,
        description=text,
        color=color,
    )
    base.set_author(name="Shepherd Bot",
                    icon_url="https://f2.toyhou.se/file/f2-toyhou-se/images/44459180_Tf52gq8HEKmh0sD.png")
    base.set_thumbnail(url="https://f2.toyhou.se/file/f2-toyhou-se/images/44459180_Tf52gq8HEKmh0sD.png")
    if footer:
        base.set_footer(text=footer)
    return base


def user_confirm_embed(user_page: str, user_name: str, color: discord.Color = discord.Color.blurple()):
    base = discord.Embed(title=user_name,
                         color=color)
    base.set_author(name="Shepherd Bot",
                    icon_url="https://f2.toyhou.se/file/f2-toyhou-se/images/44459180_Tf52gq8HEKmh0sD.png")
    base.add_field(name="Toyhou.se Page",
                   value=f"[This you?]({user_page})",
                   inline=False)
    return base


def random_img_embed(msg_author: str, caption: str, color: discord.Color = discord.Color.blurple()):
    """ Return Embed base and attachment protocol for local image file """
    base = discord.Embed(title=caption, color=color)
    base.set_author(name=msg_author,
                    icon_url="https://f2.toyhou.se/file/f2-toyhou-se/images/44459180_Tf52gq8HEKmh0sD.png")
    base.set_image(url="attachment://image.png")
    return base


def basic_msg_check(context: CTX, msg: MSG) -> bool:
    return msg.author == context.author and msg.channel == context.channel


def basic_reaction_check(context: CTX, reaction: RCN, user: MEM) -> bool:
    return context.author == user and str(reaction.emoji) in ["✅", "❌"]

