import discord
from discord.ext import commands
from datetime import datetime
from src.functions import generate, log


class NitroCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gen_nitro'])
    @commands.check(log.logging)
    async def _gen_nitro(self, ctx, amount: int):
        if amount > 10:
            message = ""
            for code in generate(amount):
                message = message + code + "\n"
            await ctx.send(
                embed=discord.Embed(title=f"Generated {amount} discord nitro codes!", description=message,
                                    color=0xdd2e44,
                                    timestamp=datetime.now()))
        else:
            await ctx.send(
                embed=discord.Embed(title=f"Error", description="Fewer generations required",
                                    color=0xdd2e44,
                                    timestamp=datetime.now()))


async def setup(client):
    await client.add_cog(NitroCog(client))
