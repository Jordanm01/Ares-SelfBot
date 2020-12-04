import re
import time
import httpx
from discord.ext import commands
from bot import log
from config import TOKEN, REDEEM_TOKEN, NOTIFICATION_WEBHOOK, EMBED_COLOUR, NITRO_SNIPER


class Sniper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not NITRO_SNIPER:
            return
        if 'discord.gift/' in message.content:
            nitro_regex = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
            if nitro_regex.search(message.content):
                code = nitro_regex.search(message.content).group(2)
                start = time.time()
                if len(code) != 16 and len(code) != 24:
                    discord_response = "Fake Code Sent"
                    delay = time.time() - start
                else:
                    async with httpx.AsyncClient() as client:
                        token = REDEEM_TOKEN if REDEEM_TOKEN != "TOKEN" else TOKEN
                        response = await client.post(
                            f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem",
                            json={'channel_id': str(message.channel.id)},
                            headers={'authorization': token, 'user-agent': 'Mozilla/5.0'}
                        )
                        delay = time.time() - start
                        log("Nitro Sniper", f"Attempted to Snipe Code: {code}")
                    response = str(response.content)
                    if "Unknown Gift Code" in response:
                        discord_response = "Invalid Code"
                    elif "subscription_plan" in response:
                        discord_response = "Successfully Sniped Nitro!"
                        if NOTIFICATION_WEBHOOK != "WEBHOOK URL":
                            try:
                                data = {
                                    "embeds": [{
                                        "title": "Ares has sniped a nitro gift!",
                                        "description": f"Look at your Discord inventory to view it!:\n"
                                                       f"Server: {message.guild.name}\n"
                                                       f"Channel: {message.channel.name}\n"
                                                       f"Sender: {message.author}\n"
                                                       f"Delay: {round(delay, 3)}s",
                                        "color": int(EMBED_COLOUR, 16)
                                    }]
                                }
                                await client.post(NOTIFICATION_WEBHOOK, json=data)
                            except:
                                pass
                    elif "This gift has been redeemed already." in response:
                        discord_response = "Code Already Redeemed"
                    else:
                        discord_response = f"Unknown Response: {response}"
                log(f"Nitro Sniper [%.3fs]" % delay, f"{discord_response} ({code})", f"{message.guild.name} | "
                                                                                    f"#{message.channel.name} | "
                                                                                    f"{message.author}")

def setup(client):
    client.add_cog(Sniper(client))
