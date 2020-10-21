import discord
import os
import json
from discord.ext import commands

client = commands.Bot(command_prefix='!!')

# @client.command(hidden=True)
# async def load(ctx, extension):
#     client.load_extension(f"cogs.{extension}")
#     await ctx.send("Extension loaded")
#
#
# @client.command(hidden=True)
# async def unload(ctx, extension):
#     client.unload_extension(f"cogs.{extension}")
#     await ctx.send("Extension unloaded")
#
#
# @client.command(hidden=True)
# async def reload(ctx, extension):
#     client.unload_extension(f"cogs.{extension}")
#     client.load_extension(f"cogs.{extension}")
#     await ctx.send("Extension reloaded")
#
#
# @client.command()
# async def clear(ctx, amount=5):
#     await ctx.channel.purge(limit=amount)


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

with open("./lists/credentials.json", "r") as f:
    credentials = json.load(f)

# Run the Discord Client
client.run(credentials["discord_token"])
