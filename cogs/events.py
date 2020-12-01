from discord.ext import commands
from bot import log
from config import PREFIX, WATCHED_SERVERS


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log("Command Executed", ctx.message.content.replace(PREFIX, ''))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log("Server Joined", guild.name)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log("Server Left", guild.name)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        guild = payload.guild_id
        channel_id = payload.channel_id
        message = payload.cached_message
        if guild is not None or guild in WATCHED_SERVERS:
            channel_name = await self.client.fetch_channel(channel_id)
            if guild is not None:
                channel = f"{(await self.client.fetch_guild(guild)).name} | #{channel_name.name}"
            else:
                channel = f"DM" + f": {channel_name.recipient}" if channel_name.recipient is not None else ""

            if message is None:
                log_message = f"Couldn't fetch message!"
            else:
                log_message = f"'{message.content}'"
                channel = f"{channel} | @{message.author}"
            log("Message Deleted", log_message, channel)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        old_message = before.content
        new_message = after.content
        if after.guild is None or after.guild.id in WATCHED_SERVERS:
            log_message = f"{old_message} => {new_message}"
            if after.guild is None:
                channel = f"DM: {after.channel.recipient} | {after.author}"
            else:
                channel = f"{after.guild.name} | #{after.channel.name} | {after.author}"
            log("Message Edited", log_message, channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user in message.mentions:
            log_message = message.content.replace(f"<@!{self.client.user.id}>", f"@{self.client.user.name}")
            if message.guild is not None:
                channel = f"{message.guild.name} | #{message.channel.name} | {message.author}"
            else:
                channel = f"DM: {message.channel.recipient} | {message.author}"
            log("You got mentioned", log_message, channel)


def setup(client):
    client.add_cog(Events(client))
