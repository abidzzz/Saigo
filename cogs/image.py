from discord.ext import commands
import discord, random, aiohttp
import json
from cogs.lvl import openfile,savefile

def create_embed(ctx,n):
    x=openfile('waifu.json')
    if str(ctx.author.id) not in x:
        return False
    data=x[str(ctx.author.id)]
    em=discord.Embed()
    em.color=ctx.bot.color
    em.title=f'{ctx.author.name.title()}\'s collections '
    em.set_footer(text=f"Page {n+1}/{len(data)}")
    em.description=f"[Sauce]({data[n]['s']})"
    em.set_image(url=data[n]['url'])
    return em


	
class ListButton(discord.ui.View):
    def __init__(self,ctx,timeout=60):
        super().__init__(timeout=timeout)
        self.ctx=ctx
        self.num=0
        self.data=openfile('waifu.json')[str(self.ctx.author.id)]
		

    async def on_timeout(self):
        self.clear_items()
        try:
            await self.message.edit(view=self)
        except :
            pass
    @property
    def b(self):
        buttons = {child.label: child for child in self.children}
        return buttons		


    @discord.ui.button(label="Previous page",emoji='◀️',style=discord.ButtonStyle.blurple,disabled=True)
    async def previous_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.num-=1
        B=self.num==0
        button.disabled=B
        
        if self.num==len(self.data)-2:
            self.b['Next page'].disabled=False
        em=create_embed(self.ctx,self.num)
        
        await interaction.response.edit_message(view=self,embed=em)
		
	
    @discord.ui.button(label="Next page",emoji='▶️',style=discord.ButtonStyle.blurple) 
    async def next_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.num+=1
        if self.num==1:
            self.b['Previous page'].disabled=False
        if (self.num)+1==len(self.data):
            button.disabled=True
        em=create_embed(self.ctx,self.num)
        
        await interaction.response.edit_message(view=self,embed=em)
    @discord.ui.button(label="❌ Stop",style=discord.ButtonStyle.red) 
    async def red_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(view=self)

class AddToList(discord.ui.View):
    def __init__(self,url,sauce,userid,timeout=180):
        self.url=url
        self.sauce=sauce
        self.userid=userid
        super().__init__(timeout=timeout)
        
    async def on_timeout(self):
        self.clear_items()
        try:
            await self.message.edit(view=self)
        except :
            pass
    
    @discord.ui.button(label="Add to list",emoji='➕',style=discord.ButtonStyle.blurple)
    async def add_to_list_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        x=openfile('waifu.json')
        if str(self.userid) in x:
            pass
        else:
            x[str(self.userid)]=[]
            savefile(x,'waifu.json')
        z=openfile('waifu.json')
        z[str(self.userid)].append({"url":self.url,"s":self.sauce})
        savefile(z,'waifu.json')
        x=self.message.embeds[0]._footer['text']
        m=x+" | Added to list ✅ use `list` command to view your collection"
        y=self.message.embeds[0].set_footer(text=m)
        self.clear_items()
        await interaction.response.edit_message(view=self,embed=y)        

class Image(commands.Cog):
    """ Image commands"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.api_list=['uniform','maid','waifu','marin-kitagawa','mori-calliope','raiden-shogun','oppai','selfies','ass','hentai','milf','oral','paizuri','ecchi','ero']
        for commands in self.api_list:
            self.make_command(commands)
            
            
    @commands.command()
    async def list(self,ctx):
        """View list of images you saved using any images command"""
        if not ctx.message.channel.is_nsfw():
                return await ctx.reply(embed=discord.Embed(title=f"<:WRONG:790156704322289715> | **Error!**",description="`Sorry but u need to be in a NSFW channel to view it :(`",color=discord.Colour.red()))
        e=create_embed(ctx,0)
        if e==False:
            em=discord.Embed(title="No list found",description=f"You dont have a list \nTo create one use any images command and click 'Add button'\nUse {ctx.prefix}help to see various kind of image commands",color=discord.Color.red())
            return await ctx.reply(embed=em)
        if e._footer['text']=='Page 1/1':
            v=None
        else:
            v=ListButton(ctx)
        try:
            v.message=await ctx.reply(embed=e,view=v)
        except:
            pass
            

    def make_command(self,name):
        @commands.command(name=name,help=f"Gives you random {name.title()} image")
        async def _command(ctx):
            
            if not ctx.message.channel.is_nsfw():
                await ctx.reply(embed=discord.Embed(title=f"<:WRONG:790156704322289715> | **Error!**",description="`Sorry but u need to be in a NSFW channel to view it :(`",color=discord.Colour.red()))
                return
            async with self.session.get(f"https://api.waifu.im/random/?selected_tags={name}") as res:
                res = await res.json()
            image= res.get("images")[0]["url"]
            tag=res.get("images")[0]["tags"]
            tags=[]
            for t in tag:
                tags.append(t['name'])
            c=res.get("images")[0]["dominant_color"]
            
            em = discord.Embed(title=name.title(),url=res.get("images")[0]["source"],color=self.bot.color)
            s=res.get("images")[0]["source"]
            v=AddToList(image,s,ctx.author.id)
            if tags!=[]:
                g=' • '.join(tags)
                em.add_field(name="Tags" , value=g,inline =False)
            em.set_footer(icon_url=ctx.author.avatar,text=f"Requested by {ctx.author.name}")
            em.set_image(url=image)
            v.message=e=await ctx.reply(embed=em,view=v)
         
       # _command.cog = self
        #self.__cog_commands__ += (_command,)
        
        self.bot.add_command(_command)
        

    
async def setup(bot):
    await bot.add_cog(Image(bot))