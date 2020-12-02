import re
import requests
from datetime import datetime
from discord.ext import commands

from bot import log
from config import TOKEN


class Sniper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gift/' in message.content:
            code = re.search("discord.gift/(.*)", message.content).group(1)
            headers = {'Authorization': TOKEN}
            r = requests.post(
                f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem",
                headers=headers
            ).json()
            response = r['message']
            if "Unknown Gift Code" in response:
                discord_response = "Invalid Code"
            elif "subscription_plan" in response:
                discord_response = "Successfully Sniped Nitro!"
            elif "This gift has been redeemed already." in response:
                discord_response = "Code Already Redeemed"
            else:
                discord_response = f"Unknown Response: {response}"
            log("Nitro Sniper", discord_response, f"{message.guild.name} | {message.author}")

def setup(client):
    client.add_cog(Sniper(client))
