import discord
from discord import Color, Embed
from discord.ext import commands 
import random
import json
import textwrap
import os

from disputils import BotEmbedPaginator

wrapper = textwrap.TextWrapper(width=25)


class Read(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot=client

    @commands.command(hidden=True,aliases=['r'])
    @commands.is_owner()
    async def reloadall(self, ctx):
        """ Reloads all extensions. """
        error_collection = []
        for file in os.listdir("./Files/cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    await self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    await ctx.send(e)

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.message.add_reaction("<:CORRECT:790148954137821194>")



async def setup(client):
    await client.add_cog(Read(client))
