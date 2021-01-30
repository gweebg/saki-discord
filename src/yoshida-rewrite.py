import os
import discord
from discord.ext import commands
import discord_keys
import time

client = commands.Bot(command_prefix = ".")
client.remove_command('help')
token = discord_keys._keys

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f"cog.{extension} loaded.")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f"cog.{extension} unloaded.")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    time.sleep(1)
    client.load_extension(f'cogs.{extension}')
    print(f"cog.{extension} reloaded.")
    
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f"cog.{file[:-3]} loaded.")

client.run(token)