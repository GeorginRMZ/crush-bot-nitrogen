import discord
import string
import random
import requests
from discord.ext import commands
from cfg import bot_data
from logs import Logging

session = requests.Session()
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=f"{bot_data['prefix']}", help_command=None, intents=intents, reconnect=False)
log = Logging()


def generate(codes: int):
    for _ in range(codes):
        code = "discord.gift/" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        req = session.get(
            f"https://discordapp.com/api/entitlements/gift-codes/{code}",
            timeout=10,
        ).status_code

        if req == 200:
            code = f"[VALID] [{code}](https://{code})"
        elif req == 404:
            code = f"[INVALID] [{code}](https://{code})"
        elif req == 429:
            code = f"[CAN'T CHECK] [{code}](https://{code})"

        yield code
