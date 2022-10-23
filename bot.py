import discord
import random 
import asyncio
import time
import os , aiohttp
import sys
import json
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
from PIL import Image,ImageDraw
from math import floor, pow

async def getprefix(bot,message):
    if int(message.author.id)==732298101351645184:
        return commands.when_mentioned_or("?","!","")(bot, message)
    if message.guild.id==730882708452016130:
        return commands.when_mentioned_or("?")(bot, message)
    else:
        return commands.when_mentioned_or("!")(bot, message)
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=getprefix,intents=intents)


path = os.path.realpath(__file__)
path = path.replace('\\', '/')
path = path.replace('bot.py', 'cogs')
initial_extensions = os.listdir(path)
try:
    initial_extensions.remove("__pycache__")
except:
    pass
print(initial_extensions)
initial_extensions3 = []
for initial_extensions2 in initial_extensions:
    initial_extensions2 = "cogs." + initial_extensions2
    initial_extensions2 = initial_extensions2.replace(".py", "")
    initial_extensions3.append(initial_extensions2)



@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    
    for extension in initial_extensions3:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.\n{e}', file=sys.stderr)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"your mom"))
    for g in bot.guilds:
        n=random.choice(["Neko","Daisuki", "最後ちゃん","Saigo","Sempai","amongus","baka","urmom","yamete kudasai","🗿","Omae Wa Mou Shinderu","sui","Tsundere","Nani","Yandere","onichan","waifu","chibi"])
        try:
            await g.get_member(bot.user.id).edit(nick=f"{n}")
        except:
            pass
    

        
bot.color=0x2F3136


@bot.command()
async def cat(ctx):
    s=aiohttp.ClientSession()
    async with s.get(f"https://some-random-api.ml/img/cat") as res:
        res = await res.json()
    image= res.get("link")
    e=discord.Embed(title="Neko!",color=bot.color)
    e.set_image(url=image)
    await ctx.reply(embed=e)
    
    

    

# ------------------------ RUN ------------------------ # 

bot.run()
