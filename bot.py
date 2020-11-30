import os
from datetime import datetime
from discord.ext import commands
from config import PREFIX, TOKEN
from pyfiglet import Figlet

start_time = datetime.now().strftime('%d/%m/%Y | %H:%M')
client = commands.Bot(command_prefix=PREFIX, self_bot=True, case_insensitive=True)
# client.remove_command("help")


def cog_loader():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


def draw_ui():
    custom_fig = Figlet(font='basic')
    print(f"\033[1;34m=============================================================================\n\n\n"
          f"\033[1;36m{custom_fig.renderText('* SelfBot *')}"
          f"\033[1;34m=============================================================================\n\033"
          f"[0;0m\n")

def log(event, message, extra_info=""):
    time = datetime.now().strftime('%H:%M')
    print(f"\033[1;34m[\033[1;36m{time}\033[1;34m] "
          f"\033[1;36m{event}: "
          f"{message} "
          f"\033[1;34m[\033[1;36m{extra_info}\033[1;34m]\033[0m")


if __name__ == "__main__":
    cog_loader()
    draw_ui()
    client.run(TOKEN, bot=False)
