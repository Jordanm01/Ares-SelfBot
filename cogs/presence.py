from discord.ext import commands


class Presence(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def afk(self, ctx):
        await self.client.change_presence(afk=True)


def setup(client):
    client.add_cog(Presence(client))
