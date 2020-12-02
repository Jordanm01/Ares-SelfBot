import io
import discord
from discord.ext import commands

from config import PASSWORD
from utils.avatar import generate_pfp


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx, bg_colour=None, icon_colour=None):
        try:
            img_bytes = await generate_pfp(bg_colour, icon_colour)
            img = discord.File(io.BytesIO(img_bytes), filename="generated_avatar.png")
            await ctx.send(file=img)
        except ValueError:
            await ctx.send("The colours you specified were not valid!")

    @commands.command()
    async def setavatar(self, ctx, bg_colour=None, icon_colour=None):
        try:
            img_bytes = await generate_pfp(bg_colour, icon_colour)
            await self.client.user.edit(avatar=img_bytes, password=PASSWORD)
        except ValueError:
            await ctx.send("The colours you specified were not valid!")

def setup(client):
    client.add_cog(Avatar(client))
