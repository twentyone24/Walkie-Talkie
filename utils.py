import json
import os
import random
from bs4 import BeautifulSoup
import requests
import re
import discord
from discord.ext import commands
from settings import *
import codecs


async def notify_user(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)


def mods_or_owner():
    #Check that the user has the correct role to execute a command
    def predicate(ctx):
        return commands.check_any(commands.is_owner(), commands.has_role(MODERATOR_ROLE_NAME))
    return commands.check(predicate)


async def get_compliments():
    with codecs.open(f'{DATA_DIR}\\compliment.json', 'r','utf-8') as f:
        jokes = json.load(f)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult


vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

#Helper func for Command 03
def filterOnlyOnlineMembers(member):
    return member.status != discord.Status.offline and not member.bot



def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format(
                'Y' if v.isupper() else 'y', v))

    return text




def meme_json():
    URL = "https://api.imgflip.com/get_memes"
    data = requests.get(URl)
    data = response.json()
    meme_templates = data["data"]["memes"]
    results = []
    i = 1

    for templ in meme_templates:
        template_id = templ['id']
        template_name = templ['name']
        template_box = templ['box_count']
        data = {
            'uuid' : i,
            'id' : template_id,
            'name' : template_name,
            'box' : template_box
        }
        results.append(data)
        i = i+1
        print(f'Parsed {template_name} template!')

    with open('templates.json', 'w') as f:
        json.dump(results, f, indent = 2)
