"""
    This file is part of Pugsy Malone.

    Pugsy Malone is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Pugsy Malone is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pugsy Malone.  If not, see <https://www.gnu.org/licenses/>.
"""
import discord
import os
import requests as req
import urllib.request
import io, aiohttp
import mysql.connector
from discord.ext import commands
from dotenv import load_dotenv
from random import randint
from listdogs import listdogs

load_dotenv()
# Global Var
TOKEN = os.environ.get("TOKEN")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DIS_OWNER = str(os.environ.get("DIS_OWNER"))
CE_API = os.environ.get("CE_API")
CAT_API = os.environ.get("CAT_API")
API_URL = os.environ.get("API_URL")
DOG_URL = os.environ.get("DOG_URL")

dbq = mysql.connector.connect(user='pugsy@localhost', password=DB_PASSWORD, host='127.0.0.1', database='pugsy')

client = discord.Client()

bot = commands.Bot(command_prefix=".")

@bot.command()
async def bull(message):
    await homeapi('bulldog', message.channel.id)

@bot.command()
async def pug(message):
    await dogceo("pug", message.channel.id)
    
@bot.command()
async def husky(message):
    await dogceo("husky", message.channel.id)
    
@bot.command()
async def golden(message):
    await dogceo("retriever/golden", message.channel.id)
    
@bot.command()
async def lab(message):
    await dogceo("labrador", message.channel.id)
    
@bot.command()
async def rot(message):
    await dogceo("rottweiler", message.channel.id)
    
@bot.command()
async def corgi(message):
    await dogceo("corgi", message.channel.id)

@bot.command()
async def cloud(message):
    await dogceo("samoyed", message.channel.id)
    
@bot.command()
async def hotdog(message):
    await dogceo("dachshund", message.channel.id)
    
@bot.command()
async def boxer(message):
    await dogceo("boxer", message.channel.id)
    
@bot.command()
async def bagel(message):
    await dogceo("beagle", message.channel.id)
    
@bot.command()
async def dob(message):
    await dogceo("doberman", message.channel.id)
    
@bot.command()
async def germany(message):
    await dogceo("germanshepherd", message.channel.id)
    
@bot.command()
async def biscuit(message):
    await dogceo("frise/bichon", message.channel.id)
    
@bot.command()
async def oodle(message):
    await dogceo("poodle", message.channel.id)

@bot.command()
async def tucker(message):
    tucker = randint(1, 31)
    tuckerfile = 'tucker' + str(randint(1, 31)) + '.jpg'
    await message.channel.send(file=discord.File(tuckerfile, "tucker.jpg"))

@bot.command()
async def cat(message):
    cat_pic = req.get('https://api.thecatapi.com/v1/images/search')
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    cat_file = cat_pic.json()[0]['url']
    cat_req = urllib.request.Request(cat_file, headers=hdr)
    url = urllib.request.urlopen(cat_req)
    await message.channel.send(file=discord.File(io.BytesIO(url.read()), "cool_cat.png"))

@bot.command()
async def register(message):
    if message.author.id == int(DIS_OWNER):
        cr = dbq.cursor(buffered=True)
        try:
            is_private_dm = 0
            throw_away_var = message.guild.name
        except:
            is_private_dm = 1
        
        if not is_private_dm:
            cr.execute('select * from dailydog where channel_id = %s', (message.channel.id,))
            if not cr.rowcount:
                cr.execute("insert into dailydog (channel_id, channel_name, user_id, user_name, guild_name) VALUES(%s, %s, %s, %s, %s)", 
                           (message.channel.id, message.channel.name, message.author.id, message.author.nick, message.guild.name,))
                dbq.commit()
                cr.close()
                await message.channel.send('Registered for a daily dog!')
                return
            else:
                for (channel_id, channel_name, user_id, user_name, guild_name) in cr:
                    await message.channel.send('Channel has already been registered by <@%s>' % user_id)
                    cr.close()
                    return
        
        cr.close()
        await message.channel.send('Pugsy was unable to register channel')

async def homeapi(dog_type, channel_id):
    try:
        dog_req = req.get(API_URL % str(dog_type))
        dog_url = urllib.request.urlopen(DOG_URL % str(dog_type) + '/' + dog_req.json()['hash'] + '.' + dog_req.json()['format'])
        channel = bot.get_channel(int(channel_id))
        await channel.send(file=discord.File(io.BytesIO(dog_url.read()), (dog_req.json()['hash'] + '.' + dog_req.json()['format'])))
    except:
        await channel.send('Error all the dogs have gotten out!')

async def dogceo(msg, channel_id):
    channel = bot.get_channel(int(channel_id))
    try:
        dog = req.get("https://dog.ceo/api/breed/%s/images/random" % msg)
        url = urllib.request.urlopen(dog.json()['message'])
        await channel.send(file=discord.File(io.BytesIO(url.read()), '%s.jpg' % msg))
    except:
        await channel.send('Error all the dogs have gotten out!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)

