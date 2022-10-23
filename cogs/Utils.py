
import discord
from discord import Color, Embed, File
from discord.ext import commands 
from discord.ext.commands import Cog
import os
import json
from async_timeout import timeout
import random
import string
import aiohttp
import asyncio
from cogs.lvl import human_format as hf
from typing import Optional
import nhentai as nh
from discord import utils
from typing import Union
import requests
from colorthief import ColorThief
from io import BytesIO


class MyHelpCommand(discord.ext.commands.MinimalHelpCommand):
    
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0x2F3136)
            await destination.send(embed=emby)

            



class Utils(Cog):
    def __init__(self, client):
        self.client = client
        self.bot=client
        self.client.help_command=MyHelpCommand()
        
    @commands.command(aliases=['w'])
    async def weather(self, ctx,*, location : str=None):
        """Find the weather of your location """
        if location == None:
            await ctx.send('You havent provided a location!')
        else:
            try:
                x = location
                x = x.lower()
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID=3e90b556a99e7fefb1fdaf14a3e4e69c'.format(x))
                x = r.json()
                country = x['sys']['country']
                city = x['name']
                cord1 = x['coord']['lon']
                cord2 = x['coord']['lat']
                main = x['weather'][0]['main']
                desc = x['weather'][0]['description']
                speed = x['wind']['speed']
                humid = x['main']['humidity']
                icon = x['weather'][0]['icon']
                pressure = x['main']['pressure']
                clouds = x['clouds']['all']
                
                
                temp = x['main']['temp']
                temp_f = x['main']['feels_like']
                zone = x['timezone']
                embed=discord.Embed(
                    title=f'Weather in **{city} ({country})**',
                    colour=discord.Color.blue())
                embed.add_field(name='**Wind**', value=f'{speed} MPH')
                embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{icon}@2x.png')
                embed.add_field(name='**Humidity**', value=f'{humid}%')
                embed.add_field(name='**Weather**', value=f'{main} ({desc})')
                embed.add_field(name='**Pressure**', value=f'{pressure}')
                embed.add_field(name='**Clouds**', value=f'{clouds}')
                embed.add_field(name='**Temperature**', value=f'{round(temp - 273.15)} °C')
                embed.add_field(name='**Feels Like**', value=f'{round(temp_f - 273.15)} °C')
                embed.add_field(name=f'**Time Zone**', value=f'{zone}')
                embed.add_field(name=f'**Min Temp**', value=str(round(x['main']['temp_min'] - 273.15)) + ' °C')
                embed.add_field(name=f'**Max Temp**', value=str(round(x['main']['temp_max'] - 273.15)) + ' °C')
                await ctx.send(embed=embed)
                
            except KeyError as e:
                print(e)
                await ctx.send('Location was invalid.')
    @commands.command(aliases=['cov', 'coronavirus'], brief="coronavirus statistics, you can also specify a country to see statistics for a given one.")
    async def covid(self, ctx, *, country: Optional[str]):
        if country is None:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://disease.sh/v3/covid-19/all?yesterday=true&twoDaysAgo=true') as r:
                    js = await r.json()
            covid_embed = discord.Embed(
                
                color=random.randint(0, 0xFFFFFF)
            ).set_author(name="Covid-19 World Stats",icon_url='https://media.discordapp.net/attachments/239446877953720321/691020838379716698/unknown.png').set_thumbnail(url="https://media.discordapp.net/attachments/787207148367118346/792335777874837544/image0.png")
            fields = [
                ('Total Cases', f"{hf(js['cases'])} ({js['cases']:,})"),
                ('Today Cases', f"{hf(js['todayCases'])} ({js['todayCases']:,})"),
                ('Deaths', f"{hf(js['deaths'])} ({js['deaths']:,})"),
                ('Today Deaths', f"{hf(js['todayDeaths'])} ({js['todayDeaths']:,})"),
                ('Recovered', f"{hf(js['recovered'])} ({js['recovered']:,})"),
                ('Today Recovered', f"{hf(js['todayRecovered'])} ({js['todayRecovered']:,})"),
                ('Active Cases', f"{hf(js['active'])} ({js['active']:,})"),
                ('Critical', f"{hf(js['critical'])} ({js['critical']:,}) "),
                ('Countries', f"({js['affectedCountries']:,}) ")
            ]
            for name, value in fields:
                covid_embed.add_field(name=name, value=value)
            await ctx.send(embed=covid_embed)
        else:
            country = country.replace(' ', '+')
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://disease.sh/v3/covid-19/countries/{country}?yesterday=true&twoDaysAgo=true&strict=true') as r:
                    js = await r.json()
            try:flag = f"{js['countryInfo']['flag']}"
            except:return await ctx.send("Country named '{}' is not found ".format(country))
            cases = js['cases']
            todayCases = js['todayCases']
            deaths = js['deaths']
            recovered = js['recovered']
            todayRecovered = js['todayRecovered']
            todayDeaths = js['todayDeaths']
            active = js['active']
            critical = js['critical']
            continent = js['continent']
            country_embed = discord.Embed(color=random.randint(0, 0xFFFFFF)).set_thumbnail(url=flag).set_author(icon_url='https://media.discordapp.net/attachments/239446877953720321/691020838379716698/unknown.png', name=f"Covid-19 Stats for {country}",)
            fields = [
                ('Continent', continent),
                ('Total Cases', f"{hf(int(cases))} ({cases:,})"),
                ('Today Cases', f"{hf(int(todayCases))} ({todayCases:,})"),
                ('Deaths', f"{hf(int(deaths))} ({deaths:,})"),
                ('Today Deaths', f"{hf(int(todayDeaths))} ({todayDeaths:,})"),
                ('Recovered', f"{hf(int(recovered))} ({recovered:,})"),
                ('Today Recovered', f"{hf(int(todayRecovered))} ({todayRecovered:,})"),
                ('Active Cases', f"{hf(int(active))} ({active:,})"),
                ('Critical', f"{hf(int(critical))} ({critical:,})")
            ]
            for name, value in fields:
                country_embed.add_field(name=name, value=value)
            await ctx.send(embed=country_embed)
                       




    @commands.command(
        name='anime',
        brief='search for some anime'
    )
    async def anime_command(self, ctx, *, anime: str):
        anime = anime.replace(' ', '+')
        async with ctx.channel.typing():
            # Data from API
            cs = aiohttp.ClientSession()
            r = await cs.get(f'https://kitsu.io/api/edge/anime?filter[text]={anime}')
            js = await r.json()
            _id = js['data'][0]['id']
            g = await cs.get(f'https://kitsu.io/api/edge/anime/{_id}/genres')
            gs = await g.json()
            attributes = js['data'][0]['attributes']
            # Collecting Genres List
            genres_list = []
            for i in range(0, len(gs['data'])):
                genres_list.append(gs['data'][i]['attributes']['name'])
            fields = [
                ('Type', f"{js['data'][0]['type']} | {attributes['status']}", True),
                ('Rating', f"{attributes['averageRating']}/100⭐", True),
                ('Aired', f"from **{attributes['startDate']}** to **{attributes['endDate']}**", True),
                ('NSFW', attributes['nsfw'], True),
                ('Episodes', attributes['episodeCount'], True),
                ('Duration', attributes['episodeLength'], True),
                ('Rank', attributes['ratingRank'], True),
                ('Age Rating', attributes['ageRatingGuide'], True),
                ('Genres', 'Not specified.' if not genres_list else ' • '.join(genres_list), True)
            ]
            embed = Embed(color=self.bot.color,title=f"{attributes['titles']['en_jp']} ({attributes['titles']['ja_jp']})",
                description=attributes['description'],
                url=f'https://kitsu.io/anime/{_id}'
            ).set_thumbnail(url=attributes['posterImage']['small'])
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)
    @commands.command(aliases=["av", "pfp"])
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author

        avatars_list = []

        def target_avatar_formats(target):
            formats = ["JPEG", "PNG", "WebP"]
            if target.is_animated():
                formats.append("GIF")
            return formats

        if not user.avatar and not user.guild_avatar:
            return await ctx.send(f"**{user}** has no avatar")

        if user.avatar:
            avatars_list.append("**Avatar Formats:** " + " **|** ".join(
                f"[{img_format}]({user.avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.avatar)
            ))

        embed = discord.Embed(colour=self.bot.color)

        if user.guild_avatar:
            avatars_list.append("**Server avatar:** " + " **-** ".join(
                f"[{img_format}]({user.guild_avatar.replace(format=img_format.lower(), size=1024)})"
                for img_format in target_avatar_formats(user.guild_avatar)
            ))
            embed.set_thumbnail(url=user.avatar.replace(format="png"))

        embed.set_image(url=f"{user.display_avatar.with_size(1024).with_static_format('jpeg')}")
        embed.description = "\n".join(avatars_list)

        await ctx.send(f"Avatar of **{user}**", embed=embed)

            

async def setup(client):
    await client.add_cog(Utils(client))