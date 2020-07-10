import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Game, Member
import aiohttp
from aiohttp import request
import json
import traceback
import requests
from utils import *
import time


class apiCommands(commands.Cog):
    #docstring for commands .

    def __init__(self, bot):
        self.bot = bot
        #super(commands, self).__init__()

    #Command 04: to generate random joke using API call
    @commands.command(name = 'joke', help = 'Tells you a joke! Huh, JOKE!')
    async def joke_api(self, ctx):
        URL = "https://official-joke-api.appspot.com/random_joke"
        async with ctx.channel.typing():
            async with request("GET", URL, headers = []) as response:
                if response.status == 200:
                    data = await response.json()
                    await ctx.send(data["setup"])
                    await ctx.send(f'```A: {data["punchline"]}```')
                else:
                    await ctx.send('Fuck, try after sometime!')

    #Command 05:
    @commands.command(name = 'tip', help = 'Gives you a live-saving advise. LOl!')
    async def advice_generator(self, ctx):
        URL = "https://api.adviceslip.com/advice"
        async with ctx.channel.typing():
            async with request("GET", URL, headers = []) as response:
                if response.status  == 200:
                    #print("response")
                    data = await response.json(content_type = 'text/html')
                    await ctx.send(f'```{data["slip"]["advice"]}```')
                else:
                    await ctx.send('Fuck, try after sometime!')


    #Synchornous function for Command 06: meme
    @commands.command(name = 'test', help = 'Gives you a live-saving advise. LOl!')
    async def meme_templates(self, ctx):

        with open(f'{DATA_DIR}\\templates.json', 'r') as f:
            data = json.load(f)
        data_str = json.dumps(data, indent = 2)
        print(data_str)




    #Command 06: Generate your own meme
    @commands.command(name = 'meme', help = 'You can create a meme on the go!')
    async def meme(self, ctx, txt0, txt1):
        URL =  "https://api.imgflip.com/caption_image"
        payload = {
            'template_id' : '181913649',
            'username' : 'walkytalky',
            'password' : 'Naveen21',
            'text0' : txt0,
            'text1' : txt1
        }
        r = requests.post(URL, data = payload)
        response = json.loads(r.text)
        meme_url= response["data"]["url"]
        embed = discord.Embed()
        embed.set_image(url = meme_url)
        await ctx.send(embed = embed)





def setup(bot):
    bot.add_cog(apiCommands(bot))
