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



    #Command 06: Generate your own meme
    @commands.command(name = 'meme', help = 'You can create a meme on the go!', pass_context=True)
    async def meme(self, ctx):
        meme_json()
        def templateSelectCheck(message):
            return message.author == ctx.message.author and message.channel == ctx.message.channel and message.content.startswith('-')

        def boxCheck(message):
            return message.author == ctx.message.author and message.channel == ctx.message.channel and len(message.content) <= 100

        URL =  "https://api.imgflip.com/caption_image"
        toDel = [ctx.message]
        txt = []; i = 1;
        results = json.loads(template_list())
        templateE = discord.Embed(title='List of Templates', color=discord.Colour.blue())
        for templ in results:
            i = i + 1
            tempid = templ['id']; tempnam = templ['name']
            templateE.add_field(name=tempnam ,value = f'type -{chr(95+i)} to select this template',inline=True)
            if templ['id'] == 26:
                break
        templateE.set_footer(text='Type (Eg: ```-a ```) to select a template!')
        message = await ctx.channel.send(embed=templateE)

        #13/07 to return a template id based on a messageText
        try:
            arg = await self.bot.wait_for('message', check = templateSelectCheck, timeout = 60.0 )
            param = arg.clean_content
            input = param[::-1]
            templateID, box = returnTemplate(input[:1])
            #templateID = str(templateID)

        except asyncio.TimeoutError:
            timeoutE=discord.Embed(title="Session Timeout", description="Hmm, You should have typed something to make the meme you wanted to. Try Again. Yo, Have a great day!", color=0xf24242)
            timeoutE.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed = timeoutE)
            templateID = '181913649'
        i=1
        print(templateID, box)
        #We got TemplateID
        #22:32 & I'm doing this rynow

        #I wrote this to get the text
        #tellME Embed
        tellMeE = discord.Embed(title='Meme creator', description=f'Enter the text {i} of the meme or \nmake `-b` to abort',
        color=0x00ff00)
        tellMeE.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        tellMeE.set_footer(text=f'-meme command requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        #TEXT BOX embed
        argumentsE=discord.Embed(title="Meme Creator", description="Text Boxes: List of Parameters", color=0xffffff)
        argumentsE.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)

        await ctx.send(f'`You should enter {box} texts...`')
        while i <= box:
            await ctx.send(f'`{i}/{box}: `')
            try:
                arg = await self.bot.wait_for('message', check = boxCheck, timeout = 30.0 )
                await ctx.channel.purge(limit=2)
                argumentsE.add_field(name=f"Text {i}:", value=arg.clean_content, inline=True)
                i = i+1

            except asyncio.TimeoutError:
                timeoutE=discord.Embed(title="Session Timeout", description="Hmm, You should have typed something to make the meme you wanted to. Try Again. Yo, Have a great day!", color=0xf24242)
                timeoutE.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed = timeoutE)
                break


            if arg.clean_content.startswith('-z'):
                timeoutE=discord.Embed(title="Request Abort", description="Hmm, You aborted the request to make the meme you wanted to. Yo, Have a great day!", color=0xf24242)
                timeoutE.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed = timeoutE)
                break

            txt.append(arg.clean_content)
            toDel.append(await ctx.send(embed=argumentsE))
            await ctx.channel.purge(limit=1)
            toDel.append(arg.clean_content)


        if not arg.clean_content.startswith('-z'):
            #await ctx.channel.purge(limit=box*2+2)
            payload = {
                'template_id' : templateID,
                'username' : 'walkytalky',
                'password' : 'Naveen21',
                'text0' : txt[0],
                'text1' : txt[1]
            }

            r = requests.post(URL, data = payload)
            response = json.loads(r.text)
            meme_url= response["data"]["url"]
            embed = discord.Embed()
            embed.set_image(url = meme_url)
            await ctx.send(embed = embed)



def setup(bot):
    bot.add_cog(apiCommands(bot))
