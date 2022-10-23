import discord
from discord.ext import commands
import sys
class example(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    async def embed(self,ctx,desc):
        embed=discord.Embed(title=f"<:ERROR:793376449855750175> | **Error!**",description=desc,color=discord.Colour.red())
        await ctx.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        err=error
    
  	
        if isinstance(error, commands.CommandNotFound):
            return
   # if ctx.author.id==732298101351645184:return await ctx.send(err)
        elif isinstance(error,commands.NotOwner):
            return
        await ctx.message.add_reaction("<:WRONG:790156704322289715>")
        if isinstance(err, discord.HTTPException):
            await self.embed(ctx,"An error occurred while I was trying to execute a task. Are you sure I have the correct permissions?")

        elif isinstance(error,commands.MissingPermissions):
    	  	
    	    await self.embed(ctx,'You need **{}** permission to run this command.'.format(' '.join(error.missing_perms[0].split('_'))).title())
  
    	    
        elif isinstance(error,commands.MemberNotFound):
            await self.embed(ctx,f'Not Found')
            
    	
        elif isinstance(error, commands.BotMissingPermissions):
            await self.embed(ctx,f"I need  **{error.missing_perms[0].replace('_', ' ')}` **permission to run this command*")
            
        elif isinstance(error, commands.MaxConcurrencyReached):
        
            await self.embed(ctx,"This command is already being used ")
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            d,h=divmod(h,24)
            if int(h) is 0 and int(m) is 0:
                await self.embed(ctx,f'This Command is on Cooldown . \n You must wait {int(s)} seconds to use this command!')
            elif int(h) is 0 and int(m) is not 0:
                await self.embed(ctx,f'This command is on Cooldown .\n You must wait {int(m)} minutes to use this command!')
                
            else:
                await self.embed(ctx,f'This command is on Cooldown .\nYou must wait {int(h)} hours , {int(m)} minutes to use this command!')
                

          
        elif isinstance(error,commands.MissingRequiredArgument):
            value = f'```{ctx.prefix}\u200b{ctx.command.name} {" ".join([f"<{x}>" for x in ctx.command.clean_params])}```'
            await self.embed(ctx,f"**{error.param.name.title()}** is a required argument which is missing\n{value}\nDo `{ctx.prefix}help {ctx.command.name}` for more  info")#f"{' '.join(error.args)}")
          
        
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"**:no_entry: `{ctx.command}` can not be used in Private Messages/DM's. **")
            except:
                pass  
        else:

            embed = discord.Embed(colour=discord.Color.red())
            embed.title = f"Error on `{ctx.command}`"
            embed.description = f"`{error.__class__.__name__}`\n[Jump!]({ctx.message.jump_url})\n"
            embed.description += f"```py\n{str(error)}\n```"
            embed.description = embed.description[:2048]
            embed.add_field(name="Server",value=f"{ctx.guild.name}")
            #exc_type, exc_obj, exc_tb = sys.exc_info()
           # embed.add_field(name="Line number",vaule=exc_tb.tb_lineno)
            embed.add_field(name="User",value=f"{ctx.author.name}#{ctx.author.discriminator}")       
        
            ch=self.bot.get_channel(787207148367118346)
            await ch.send(embed=embed)
            print(error)

  
   
    
    
    
async def setup(bot):
    await bot.add_cog(example(bot))