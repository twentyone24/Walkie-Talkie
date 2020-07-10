import os
import random
import discord
import asyncio
import aiohttp
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Game

class EventHandlers(commands.Cog):
    #docstring for commands .

    def __init__(self, bot):
        self.bot = bot
        #super(commands, self).__init__()

    #Greeting when a member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hey {member.name}, Have a great day!'
        )
        print(f'Hey {member.name}, has joined {member.guild}')

    #@command.Cog.listener()
    #async def on_message(self, message):




def setup(bot):
    bot.add_cog(EventHandlers(bot))
