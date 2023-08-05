from cfg import bot_data
from functions import client
from logs import write_log


@client.event
async def on_ready():
    await write_log(f"Bot is starting...")

    for cog in bot_data['cogs']:
        await client.load_extension(f"cogs.{cog}")
        await write_log(f'Loaded extension "{cog}"')


client.run(bot_data['token'])
