import json
from datetime import datetime
from json import JSONDecodeError

from discord.ext import commands
from bot import log
from config import PREFIX, WATCHED_SERVERS, LOGGING


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command(self, ctx):
        log("Command Executed", ctx.message.content.replace(PREFIX, ''))
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        log("Server Joined", guild.name)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log("Server Left", guild.name)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not LOGGING:
            return
        if message.content is not None and message.author != self.client.user:
            channel = str(message.channel.recipient.id) if message.guild is None else str(message.channel.id)
            with open("message_sniper.json", "r+") as f:
                try:
                    data = json.load(f)
                except JSONDecodeError:
                    data = {}
                try:
                    data["deleted_messages"][channel] = {
                        "author": str(message.author.id),
                        "message": message.content,
                        "time": datetime.now().strftime('%H:%M')
                    }
                except KeyError:
                    data["deleted_messages"] = {}
                    data["deleted_messages"][channel] = {
                        "author": str(message.author.id),
                        "message": message.content,
                        "time": datetime.now().strftime('%H:%M')
                    }
            with open("message_sniper.json", "w+") as f:
                json.dump(data, f, indent=4)
            if message.guild is None or int(message.guild.id) in WATCHED_SERVERS:
                channel = f"G: {message.guild.name} | #{message.channel.name}" if message.guild is not None else \
                    f"DM: {message.channel.recipient}"
                log("Message Deleted", message.content, channel)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not LOGGING:
            return
        old_message = before.content
        new_message = after.content
        if old_message == new_message or after.author == self.client.user:
            return
        if after.guild is None or int(after.guild.id) in WATCHED_SERVERS:
            log_message = f"{old_message} => {new_message}"
            if after.guild is None:
                channel = f"DM: {after.channel.recipient} | {after.author}"
            else:
                channel = f"{after.guild.name} | #{after.channel.name} | {after.author}"
            log("Message Edited", log_message, channel)
        channel = str(after.channel.recipient.id) if after.guild is None else str(after.channel.id)
        with open("message_sniper.json", "r+") as f:
            data = json.load(f)
            try:
                data["edited_messages"][channel] = {
                    "author": str(after.author.id),
                    "old_message": before.content,
                    "new_message": after.content,
                    "time": datetime.now().strftime('%H:%M')
                }
            except KeyError:
                data["edited_messages"] = {}
                data["edited_messages"][channel] = {
                    "author": str(after.author.id),
                    "old_message": before.content,
                    "new_message": after.content,
                    "time": datetime.now().strftime('%H:%M')
                }
        with open("message_sniper.json", "w+") as f:
            json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not LOGGING:
            return
        if self.client.user in message.mentions:
            log_message = message.content.replace(f"<@!{self.client.user.id}>", f"@{self.client.user.name}")
            if message.guild is not None:
                channel = f"{message.guild.name} | #{message.channel.name} | {message.author}"
            else:
                channel = f"DM: {message.channel.recipient} | {message.author}"
            log("You got mentioned", log_message, channel)


def setup(client):
    client.add_cog(Events(client))
