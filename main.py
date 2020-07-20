import os
import random
import discord
import asyncio
import aiohttp
from discord.ext import commands
from discord import Game
import sys, traceback
from settings import *



#Load env file to retrive token & guild id
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_GUILD')

#Variable Customized prfix for the commands
def get_prefix(bot, message):

    prefixes = ['-', 'Wt ', 'wt ']

    # On DM, ? is only allowed
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')

#Defining func to load & unload Extensions
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'Cogs.{extension}')
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'Cogs.{extension}')
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')



#Event handler; Event: When bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game("| wt help"))


bot.run(TOKEN)
