from disnake.ext import commands


class ToyHouseSheep(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The Toyhou.se Sheep are being herded!")


def setup(bot):
    bot.add_cog(ToyHouseSheep(bot))