import re
import json
import asyncio
import datetime
from PIL import Image, ImageDraw, ImageFont
from math import floor, ceil
import os
import aiohttp
from io import BytesIO
import functools
import textwrap
from discord.ext import commands
import discord
from PIL import ImageChops,ImageFilter
import random
from random import randint
from datetime import datetime, timedelta
from colorthief import ColorThief

def key_search(dict,value):
    list_of_keys = list(dict.keys())
    list_of_value = list(dict.values())
    position = list_of_value.index(value)
    return list_of_keys[position]


def value_sort(dict,type=False):
    d={}
    values=sorted(dict.values(),reverse=type)
    for i in values:
        d[key_search(dict,i)]=i
    return d



def reverse(dict,key,type=False):
    d={}
    for i in dict:
        d[i]=dict[i][key]
    d=value_sort(d,type)
    d2={}
    for i in d:
        d2[i]=dict[i]
    return d2

def openfile(file):
    with open(file) as f:
        data = json.load(f)
    return data

def savefile(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)
        
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T','Qd','Qn'][magnitude])

class test(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        
        self._session = aiohttp.ClientSession()
    async def process_xp(self, message):
        data=openfile('level.json')
        if str(message.author.id) in data:
            pass
        else:
            data[str(message.author.id)]={}
            data[str(message.author.id)]["level"]=0
            data[str(message.author.id)]["xp"]=0
            data[str(message.author.id)]["user_id"]=str(message.author.id)
            data[str(message.author.id)]["xplock"]=(datetime.utcnow()+timedelta(seconds=60)).isoformat()
            
            savefile(data,'level.json')
            
        xp=data[str(message.author.id)]["xp"]
        xplock=data[str(message.author.id)]["xplock"]
        lvl=data[str(message.author.id)]["level"]
        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)
            
            
    async def add_xp(self, message, xp, lvl):
        
        data=openfile('level.json')
        lebel=data[str(message.author.id)]["level"]
        xp_to_add = randint(10, 25)
        lev=0
        xp=xp+xp_to_add
        exp=xp
        while True:
            if xp < ((50*(lev**2))+(50*lev)):
                
                break
            lev+=1
        exp-= ((50*((lev-1)**2))+(50*(lev-1)))
        
        
        if lebel<lev:
            await message.channel.send(f" GG  {message.author.mention}! you reached level **{lev:,}**!")

        #new_lvl = int((xp + xp_to_add) / 200)
        #if new_lvl > lvl:
            #new_lvl = new_lvl
        #else:
            #new_lvl = lvl
        
        data[str(message.author.id)]["level"]=lev
        data[str(message.author.id)]["xp"]=xp
        data[str(message.author.id)]["user_id"]=str(message.author.id)
        rate=60+((5*lev)-5)
        data[str(message.author.id)]["xplock"]=(datetime.utcnow()+timedelta(seconds=rate)).isoformat()
        
        savefile(data,'level.json')
			
    async def get_avatar(self, user):
        try:
            res = BytesIO()
            await user.avatar.replace(format="png")
            return res
        except:
            async with self._session.get(str(user.avatar.replace(format="png"))) as r:
                img = await r.content.read()
                return BytesIO(img)

    async def get_background(self, url):
        async with self._session.get(url) as f:
            data = await f.read()
            
            return Image.open(BytesIO(data))

    def round_corner(self, radius):
        """Draw a round corner"""
        corner = Image.new("L", (radius, radius), 0)
        draw = ImageDraw.Draw(corner)
        draw.pieslice((0, 0, radius *2, radius * 2), 180, 270, fill=255)
        return corner

    def add_corners(self, im, rad=100):
        
        width, height = im.size
        alpha = Image.new("L", im.size, 255)
        origCorner = self.round_corner(rad)
        corner = origCorner
        alpha.paste(corner, (0, 0))
        corner = origCorner.rotate(90)
        alpha.paste(corner, (0, height - rad))
        corner = origCorner.rotate(180)
        alpha.paste(corner, (width - rad, height - rad))
        corner = origCorner.rotate(270)
        alpha.paste(corner, (width - rad, 0))
        im.putalpha(alpha)
        return im

    async def make_full_profile(self, avatar_data, user, xp, nxp, lvl,rank,bg=None,color=None):
        img = Image.new("RGBA",(934,282))
        if bg is not None:
            bg_width, bg_height = bg.size
            ratio = bg_height/282
            bg = bg.resize((int(bg_width / (ratio)), int(bg_height / ratio)))
            if bg.size[0] < 934:
                ratio = bg_width / 934
                bg = bg.resize((int(bg_width / (ratio)), int(bg_height / ratio)))
            bg = bg.convert("RGBA")
            bg.putalpha(128)
            offset = 0
            if bg.size[0] >= 934:
                offset = (int((-(bg.size[0] - 934) / 2)), 0)
            if bg.size[0] < 934:
                offset = (0, int((-(bg.size[1] - 282) / 2)))

            img.paste(bg, offset, bg)
        img = self.add_corners(img, 10)
        draw = ImageDraw.Draw(img)
        usercolor = "white"
        
        xptot = self.add_corners(Image.new("RGBA", (600, 40), (40,40,40)), 22)
        
        img.paste(xptot, (300, 170), xptot)
        avatar = Image.open(avatar_data).resize((180,180),Image.LANCZOS).convert("RGB")
        c=Image.open("./Files/imgs/Circle.PNG").resize((180,180)).convert("RGBA")
        
        
        img.paste(avatar, (65, 70),c)

        fontpath = "./Files/imgs/Ms.ttf"

        font1 = ImageFont.truetype(fontpath, 18)
        font2 = ImageFont.truetype(fontpath, 22)
        font3 = ImageFont.truetype(fontpath, 32)
        font_50 =ImageFont.truetype(fontpath, 50)
    
        lxp = xp 
        lnxp = nxp 
        lprc = ceil(lxp / (lnxp / 200))
        #lprc = int((nxp / 100) * xp)
        b_offset = floor(lprc * 3.1)
        clrs=[(55, 202, 115),(3, 255, 254),(138, 43, 224),(235, 3, 0),(254, 6, 255)]
        rarity=[40,40,5,5,10]
        if color==None:
            clr=random.choices(clrs,rarity)[0]
        else:
            clr=color
        
        xpbar = self.add_corners(Image.new("RGBA", (b_offset, 40), clr), 22)
        #xpbar = self.add_corners(Image.new("RGBA", (lprc, 40), "cyan"), 22)
        img.paste(xpbar, (300, 170), xpbar)
        

        
        
        draw.text((700,208), (f" {human_format(xp)}/{human_format(nxp)} XP"), fill=usercolor, font=font3)
        
        usern=(f"{user.name}#{user.discriminator}")
        f=40
        userns=int(len(usern))
        if userns>10:
        	f=40
        fn =ImageFont.truetype(fontpath, f)
        draw.text((280,90),usern,fill=usercolor,font=fn)
        if int(rank)==1:
            usercolor="#FFD700"
        if int(rank)==2:
            usercolor='#C0C0C0'
        if int(rank)==3:
            usercolor='#CD7F32'
        draw.text((700,15),(f"Level {lvl}"),fill=clr,font=font_50)

        draw.text((50,15),(f"Rank "),font=font_50)
        draw.text((200,15),(f"#{rank}"),fill=usercolor,font=font_50)
        temp = BytesIO()
        img.save(temp, format="PNG")
        temp.name = "profile.png"
        temp.seek(0)
        return temp
    
    @commands.command(hidden=True)
    async def rank(self,ctx,user:discord.Member=None):
        await ctx.channel.typing()
        if user==None:
            user=ctx.author
        else:
            user=user
        if ctx.guild.id!=927523123488763924:
            return
        data=openfile('level.json')
        try:
            xp=int(data[str(user.id)]["xp"])
            
            lv=0
            while True:
                if xp < ((50 * (lv**2)) + (50 * lv)):
                    break
                lv += 1
            xp -= ((50 * ((lv- 1)**2)) + (50 * (lv - 1)))
            nxp=int(200*((1/2)*lv))
            record=reverse(data,'xp',True)
            rank=0
            for x in record:
                rank+=1
                if record[x]['user_id']==str(user.id):
                    break
            
                
           
        except Exception as e:
            await ctx.send(e)
            return await ctx.send("You hav no XP\nChat then you will gain XP and try this command again")
        
        
        try:
            bgr=data[str(user.id)]["bg"]
        except:
            bgr=random.choice(["https://i.imgur.com/UM0icxL.jpg","https://i.imgur.com/M1SEbiF.jpg","https://media.discordapp.net/attachments/784063480672157736/928256609480769576/IMG_7516.jpg","https://media.discordapp.net/attachments/784063480672157736/928257226890678292/image0.jpg","https://media.discordapp.net/attachments/784063480672157736/928257871777529866/image0.jpg","https://media.discordapp.net/attachments/784063480672157736/928258270383198238/image0.jpg","https://media.discordapp.net/attachments/784063480672157736/928258640304046101/IMG_7519.jpg","https://media.discordapp.net/attachments/784063480672157736/929048727438651423/IMG_7542.jpg","https://media.discordapp.net/attachments/784063480672157736/929052575418945648/IMG_7552.jpg","https://media.discordapp.net/attachments/784063480672157736/929052586575798333/IMG_7551.jpg","https://media.discordapp.net/attachments/784063480672157736/929052596038172803/IMG_7550.jpg","https://media.discordapp.net/attachments/784063480672157736/929052609594150932/IMG_7549.jpg","https://media.discordapp.net/attachments/784063480672157736/929052609854201936/IMG_7548.jpg","https://media.discordapp.net/attachments/784063480672157736/929052622940409886/IMG_7547.jpg","https://media.discordapp.net/attachments/784063480672157736/929052635460431973/IMG_7546.jpg","https://media.discordapp.net/attachments/784063480672157736/929052635858878495/IMG_7545.jpg","https://media.discordapp.net/attachments/784063480672157736/929052649070923866/IMG_7544.jpg","https://media.discordapp.net/attachments/784063480672157736/929052667047727104/IMG_7543.jpg","https://i.pinimg.com/564x/23/81/1c/23811c170a7ea67f365237d375919258.jpg"])
        try:
            color=data[str(user.id)]["clr"]
        except:
            color=None
        bg=await self.get_background(bgr)
        av= await self.get_avatar(user)

            
          #  i=BytesIO()
         #   ef.save(i, format="PNG")
          #  i.name = "bg.png"
         #   i.seek(0)
          #  bg=Image.open(ef)
         #   await ctx.send(file=discord.File(i))
        temp=await self.make_full_profile(av,user,int(xp),int(nxp),int(lv),rank,bg,color)
        await ctx.send(file=discord.File(temp))
        
    @commands.command(hidden=True,aliases=['bg','setbg'])
    async def background(self,ctx,bg=None):
        await ctx.channel.typing()
        if ctx.guild.id!=927523123488763924:
            return
        data=openfile('level.json')
        if bg==None :
            try :
                bg=ctx.message.attachments[0].url.replace(".webp", ".png")
            except:
                pass
        
        
        if bg ==None:
            try:
                data[str(ctx.author.id)].pop("bg")
                
                savefile(data,"level.json")
                return await ctx.send("Done! Set background to default random")
            except Exception as e:
                
                return await ctx.send(f"You have not set any background  image\n")
        if not re.search(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',bg):
            return await ctx.send("You're only allowed to give an URL or an attachment")

        data[str(ctx.author.id)]["bg"]=bg
        savefile(data,"level.json")
        await ctx.send(embed=discord.Embed(title=f"Successfully set the rank card bg to the image provided",color=self.bot.color).set_image(url=bg))
        
        
        
        
    @commands.command(hidden=True,aliases=['rc','rankcolour'])
    async def rankcolor(self,ctx,color=None):
        await ctx.channel.typing()
        if ctx.guild.id!=927523123488763924:
            return
        data=openfile('level.json')
        
        if color ==None:
            try:
                data[str(ctx.author.id)].pop("clr")
                
                savefile(data,"level.json")
                return await ctx.send("Done! Set color to default random")
            except Exception as e:
                
                return await ctx.send(f"You have not set any rank color\n")
            
            
        if color[:1] == "#":
            cl = color[1:]
        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', cl):
            return await ctx.send("You're only allowed to enter HEX (0-9 & A-F)")
        data[str(ctx.author.id)]["clr"]=color
        savefile(data,"level.json")
        await ctx.send(embed=discord.Embed(title=f"Successfully set the rank card bar color to {color}",color=self.bot.color))
        

        em=discord.Embed(title="Leaderboard",color=self.bot.color)
        
    @commands.command(hidden=True,aliases=['lb'])
    async def leaderboard(self,ctx):
        await ctx.channel.typing()
        if ctx.guild.id!=927523123488763924:
            return
        data=openfile('level.json')
        record=reverse(data,'xp',True)
        em=discord.Embed(title="Leaderboard",color=self.bot.color)
        img=Image.open("./Files/imgs/lb.png")
        fp= "./Files/imgs/Ms.ttf"
        font = ImageFont.truetype(fp, 32)
        fn=ImageFont.truetype(fp, 24)
        draw = ImageDraw.Draw(img)
        
        y=10
        i=0
        yy=15

        for x in record:
            try:
                user=ctx.guild.get_member(int(record[x]['user_id']))
                av=await self.get_avatar(user)
                avatar = Image.open(av).resize((55,55),Image.LANCZOS).convert("RGB")
                c=Image.open("./Files/imgs/Circle.PNG").resize((55,55)).convert("RGBA")
                img.paste(avatar, (80,y),c)
                
                
                tempxp=human_format(record[x]['xp'])
                
                draw.text((135,y), (f"{user.name or member.nick }"), fill="white", font=font)
                draw.text((545,yy), (f"{tempxp}"), fill="white", font=fn)
                
                y+=74
                yy+=74
                i+=1
                
            except Exception as e:
                
                pass
            if i==10:
                break
        temp=BytesIO()
        
        img.save(temp, format="PNG")
        temp.name = "leaderboard.png"
        temp.seek(0)
        file=discord.File(temp)
        em.set_image(url="attachment://leaderboard.png")
        em.set_footer(icon_url=ctx.author.avatar,text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=em,file=file)

                
        
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.guild.id==927523123488763924:
                await self.process_xp(message)
        #await self.bot.process_commands(message)
async def setup(bot):
	await bot.add_cog(test(bot))