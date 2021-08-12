import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Game, Member
from aiohttp import request
from utils import *
import json
from frinkiac import simpsons, futurama

class commandsList(commands.Cog):
    #docstring for commands.

    def __init__(self, bot):
        self.bot = bot
        #super(commands, self).__init__()

    @commands.command(name='t')
    async def test(self, ctx, ars):
        tellMeE = discord.Embed(title='template',
            description=f'{name} `-p` to publish the poll or\n`-c` to cancel the poll',
            color=0x00ff00)
        tellMeE.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        tellMeE.set_footer(text=f'-poll command requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(link)

    #Command 01: to roll a dice
    @commands.command(name='dice', aliases=['roll', 'roll dice'], help = 'Roll a dice')
    async def roll(self, ctx, number_of_dice: int = 1, number_of_sides: int = 6):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]

        await ctx.send(', '.join(dice))

    #Command 02: to flip a coin
    @commands.command(name = 'flip', aliases = ['coin', 'coinflip'], help = 'Flip a coin')
    async def flip(self, ctx):
        coin =  ['heads','tails']
        flipped = random.choice(coin)
        await ctx.send(flipped)


    #Command 03: to number of online members
    @commands.command(name = 'online', aliases = ['buddies'], help = 'List online members')
    async def listOnlineMembers(self, ctx):
        membersInServer = ctx.guild.members
        channel = ctx.channel
        onlineMembersInServer = list(filter(filterOnlyOnlineMembers,membersInServer ))
        onlineMembersCount = len(onlineMembersInServer)
        await ctx.channel.send(f"```Online: {onlineMembersCount}```")

    #Command 04: Text to OwO
    @commands.command(name = 'owo', help = 'Converts your text to OwO')
    async def TextToOwo(self, ctx):
        await ctx.send(text_to_owo(ctx.message.content))


    #Command 04: to mock someone you mentioned
    #URL = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    @commands.command(name = 'insult', help = 'insults him! Huh, JK!')
    async def insult_api(self, ctx, member: discord.Member = None):
        insult = await get_compliments()
        if member is not None:
            await ctx.send(f"```{member.display_name}{insult}```")
        else:
            await ctx.send(f"```He{insult}```")

    #Command 05: Clear Command
    @commands.command(name = 'cls',brief='!clear [x]', aliases=['delete', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit: int = 1):
        limit = int(limit) + 1
        await ctx.channel.purge(limit=limit)

    @commands.command()
    async def simpsons(self, ctx):
        '''Search for a Simpsons screencap and caption matching a query (or a random one if no query is given).'''
        query = strip_command(ctx)
        if query == '':
            im, cap = simpsons.random()
        else:
            im, cap = simpsons.search(query)
        await ctx.send(im)
        await ctx.send(cap)

    #To be redesigned again, & to be placed in main.py
'''    @commands.command(brief='!help')
    async def help(self, ctx):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(color=discord.Color.blue(), title='Listes des commandes')
        for cog in self.bot.cogs:
            if self.bot.get_cog(cog).get_commands():
                temp = []
                for cmd in self.bot.get_cog(cog).get_commands():
                    if not cmd.hidden:
                        temp.append(f"{cmd.name}\n")
                embed.add_field(name=f'**{cog} :**', value=f"{''.join(temp)}", inline=True)
        await ctx.send(embed=embed)
'''

def setup(bot):
    bot.add_cog(commandsList(bot))
