import discord
import os
import requests as req
import urllib.request
import io, aiohttp
import mysql.connector
from dotenv import load_dotenv
from random import randint
from listdogs import listdogs

load_dotenv()
# Global Var
TOKEN = os.environ.get("TOKEN")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DIS_OWNER = os.environ.get("DIS_OWNER")
CE_API = os.environ.get("CE_API")
CAT_API = os.environ.get("CAT_API")
API_URL = os.environ.get("API_URL")
DOG_URL = os.environ.get("DOG_URL")
checkdd = ('select * from dailydog where req_id = %s')

dbq = mysql.connector.connect(user='pugsy@localhost', password=DB_PASSWORD, host='127.0.0.1', database='pugsy')

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if (message.content.startswith('.register') and message.author.id == DIS_OWNER):
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
    
    if (message.content.startswith('.testpugapi') and message.author.id == DIS_OWNER):
        await homeapi('pug', message.channel.id)
    
    if message.content.startswith('.listdog'):
        await listdogs(message)
    
    if message.content.startswith('.dogs'):
        await listdogs(message)

    if message.content.startswith('.pug'):
        pug_pic = req.get('https://dog.ceo/api/breed/pug/images/random')
        pug_file = pug_pic.json()
        url = urllib.request.urlopen(pug_file['message'])
        channel = message.channel
        await channel.send(file=discord.File(io.BytesIO(url.read()), "cool_pug.png"))
    
    if message.content.startswith('.bull'):
        await homeapi('bulldog', message.channel.id)

    if message.content.startswith('.husky'):
        husky = req.get('https://dog.ceo/api/breed/husky/images/random')
        url = urllib.request.urlopen(husky.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), "cool_husky.png"))

    if message.content.startswith('.golden'):
        golden = req.get('https://dog.ceo/api/breed/retriever/golden/images/random')
        url = urllib.request.urlopen(golden.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_golden.png'))

    if message.content.startswith('.lab'):
        lab = req.get('https://dog.ceo/api/breed/labrador/images/random')
        url = urllib.request.urlopen(lab.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_lab.png'))
    
    if message.content.startswith('.rot'):
        rot = req.get('https://dog.ceo/api/breed/rottweiler/images/random')
        url = urllib.request.urlopen(rot.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_rot.png'))

    if message.content.startswith('.corgi'):
        corgi = req.get('https://dog.ceo/api/breed/corgi/images/random')
        url = urllib.request.urlopen(corgi.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_corgi.png'))

    if message.content.startswith('.cloud'):
        cloud = req.get('https://dog.ceo/api/breed/samoyed/images/random')
        url = urllib.request.urlopen(cloud.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_cloud.png'))
    
    if message.content.startswith('.hotdog'):
        hotdog = req.get('https://dog.ceo/api/breed/dachshund/images/random')
        url = urllib.request.urlopen(hotdog.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_hotdog.png'))

    if message.content.startswith('.boxer'):
        boxer = req.get('https://dog.ceo/api/breed/boxer/images/random')
        url = urllib.request.urlopen(boxer.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_boxer.png'))

    if message.content.startswith('.bagel'):
        bagel = req.get('https://dog.ceo/api/breed/beagle/images/random')
        url = urllib.request.urlopen(bagel.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_bagel.png'))

    if message.content.startswith('.dob'):
        dob = req.get('https://dog.ceo/api/breed/doberman/images/random')
        url = urllib.request.urlopen(dob.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_dob.png'))

    if message.content.startswith('.germany'):
        germany = req.get('https://dog.ceo/api/breed/germanshepherd/images/random')
        url = urllib.request.urlopen(germany.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_germany.png'))
    
    if message.content.startswith('.biscuit'):
        biscuit = req.get('https://dog.ceo/api/breed/frise/bichon/images/random')
        url = urllib.request.urlopen(biscuit.json()['message'])
        await message.channel.send(file=discord.File(io.BytesIO(url.read()), 'cool_biscuit.png'))

    if message.content.startswith('.oodle'):
        await dogceo("poodle", message.channel.id)

    if message.content.startswith('.tucker'):
        tucker = randint(1, 31)
        tuckerfile = 'tucker' + str(randint(1, 31)) + '.jpg'
        await message.channel.send(file=discord.File(tuckerfile, "tucker.jpg"))

    if message.content.startswith('.cat'):
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

async def homeapi(dog_type, channel_id):
    try:
        dog_req = req.get(API_URL % str(dog_type))
        dog_url = urllib.request.urlopen(DOG_URL % str(dog_type) + '/' + dog_req.json()['hash'] + '.' + dog_req.json()['format'])
        channel = client.get_channel(int(channel_id))
        await channel.send(file=discord.File(io.BytesIO(dog_url.read()), (dog_req.json()['hash'] + '.' + dog_req.json()['format'])))
    except:
        await channel.send('Error all the dogs have gotten out!')

async def dogceo(msg, channel_id):
    channel = client.get_channel(int(channel_id))
    try:
        dog = req.get("https://dog.ceo/api/breed/%s/images/random" % msg)
        url = urllib.request.urlopen(dog.json()['message'])
        await channel.send(file=discord.File(io.BytesIO(url.read()), '%s.jpg' % msg))
    except:
        await channel.send('Error all the dogs have gotten out!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
