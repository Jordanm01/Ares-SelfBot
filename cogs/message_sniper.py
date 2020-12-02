import discord
import json
from discord.ext import commands
from config import EMBED_COLOUR


class MessageSnipe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        guild = ctx.message.guild
        if guild is None:
            channel = str(ctx.channel.recipient.id)
        else:
            channel = str(ctx.channel.id) if channel is None else str(channel.id)
        sniped_message = None
        with open("message_sniper.json") as data:
            data = json.load(data)
            try:
                sniped_message = data["deleted_messages"][channel]
                author = await self.client.fetch_user(int(sniped_message["author"]))
            except KeyError:
                pass
        if sniped_message is not None:
            emb = discord.Embed(colour=int(EMBED_COLOUR, 16))
            emb.description = sniped_message["message"]
            emb.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            emb.set_footer(text=f"Deleted at {sniped_message['time']}")
            await ctx.send(embed=emb, delete_after=10)

    @commands.command(aliases=['esnipe'])
    async def edit_snipe(self, ctx, channel: discord.TextChannel = None):
        guild = ctx.message.guild
        if guild is None:
            channel = str(ctx.channel.recipient.id)
        else:
            channel = str(ctx.channel.id) if channel is None else str(channel.id)
        sniped_message = None
        with open("message_sniper.json") as data:
            data = json.load(data)
            try:
                sniped_message = data["edited_messages"][channel]
                author = await self.client.fetch_user(int(sniped_message["author"]))
            except KeyError:
                pass
        if sniped_message is not None:
            emb = discord.Embed(colour=int(EMBED_COLOUR, 16))
            emb.description = f"**Before**: {sniped_message['old_message']}\n\n" \
                              f"**After**: {sniped_message['new_message']}"
            emb.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            emb.set_footer(text=f"Edited at {sniped_message['time']}")
            await ctx.send(embed=emb, delete_after=10)

def setup(client):
    client.add_cog(MessageSnipe(client))
