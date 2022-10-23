import discord
from discord.ext import commands
import sys
import sqlite3

class Tags(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.t = sqlite3.connect('tags.db')
        self.c = self.t.cursor()
        
        
#    @commands.command(aliases=['t'])
 #   async def tag(self, ctx,*, location : str=None):
        
        
async def setup(bot):
    await bot.add_cog(Tags(bot))