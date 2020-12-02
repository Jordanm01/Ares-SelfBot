from discord.ext import commands


class CogManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reload(self, ctx, *, cog):
        self.client.unload_extension(f'cogs.{cog}')
        self.client.load_extension(f'cogs.{cog}')
        await ctx.send(f"{cog} has been reloaded!")

    @commands.command()
    async def load(self, ctx, *, cog):
        self.client.load_extension(f'cogs.{cog}')
        await ctx.send(f"{cog} has been loaded!")

def setup(client):
    client.add_cog(CogManager(client))
