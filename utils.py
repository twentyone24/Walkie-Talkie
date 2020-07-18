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


def template_list():
    with open(f'{DATA_DIR}\\templatestw.json', 'r') as f:
        data = json.load(f)
    data_str = json.dumps(data, indent = 2)
    results = []
    for templ in data:
         data = {
            'id' : templ['uuid'],
            'name' : templ['name'],
            'tid' : templ['id'],
            'box' : templ['box']
        }
         results.append(data)
    results = json.dumps(results, indent = 1)
    return results


    #for templ in data:
#        print(templ['uuid'], templ['name'])


def strip_command(ctx):
    '''Takes a Discord.py ctx object and return the message content with the first word (command name) removed.'''
    s = ctx.message.content.split(' ', 1)
    return s[1] if len(s) > 1 else ''

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
    data = requests.get(URL)
    data = data.json()
    meme_templates = data["data"]["memes"]
    results = []
    i = 1

    for templ in meme_templates:
        if templ['box_count'] == 2:

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

    with open('templatestw.json', 'w') as f:
        json.dump(results, f, indent = 2)


def returnTemplate(asc):
    id = ord(asc) - 96
    print(id)
    results = template_list()
    results = json.loads(results)
    for templ in results:
        if templ['id'] == id:
            return str(templ['tid']), templ['box']
    return '181913649', 2

    # Find a way to return the template id from the totalResults
    # # IDEA:



# Returns a youtube link using the message text
def getYoutubeLink(messageText):
    # Ignore 'play '
    linkText = messageText[5:]
    if len(linkText.split()) > 1:
        # Search for video if more than one word after !play
        return searchYoutube(linkText)

    else:
        # If the standard beginnings of the link aren't there, just search youtube with the text
        if linkText[:4] != 'www.' and linkText[:11] != 'http://www.' and linkText[:12] != 'https://':
            return searchYoutube(linkText)

        # Otherwise, append http:// and try the youtube link
        else:
            linkText = 'http://' + linkText

            testLink = requests.get(linkText)
            if testLink.status_code == 200:
                return testLink

            else:
                return ('404 page not found. Usage: !play cantina theme or '
                + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')

# Will return the link to youtube's first result
def searchYoutube(searchText):
    searchUrl = ('https://www.googleapis.com/youtube/v3/search?order=relevance'
                + '&part=snippet&type=video&searchmaxResults=1&key=GOOGLE_API_KEY_HERE'
                + searchText)

    searchPage = requests.get(searchUrl)

    if searchPage.status_code == 200:
        searchPage = searchPage.json()

        # Check number of search results using search parameters
        if searchPage['pageInfo']['totalResults'] != 0:
            videoId = searchPage['items'][0]['id']['videoId']
            return 'http://www.youtube.com/watch?v=' + videoId

        # If no results, return error message
        else:
            return ('No results found. Usage: !play cantina theme or '
                    + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')

    else:
        return ('404 Page not found. Usage: !play cantina theme or '
                + '!play http://www.youtube.com/watch?v=FWO5Ai_a80M')
