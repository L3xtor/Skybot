import discord
from discord.ext import commands
from PIL import Image
import requests



class testing(commands.Cog):

 @commands.hybrid_command()
 async def ping(self, ctx):
    guild = ctx.guild
    url = (f'https://cdn.discordapp.com/emojis/945325276085252156.png')
    data = requests.get(url).content 
    f = open('Emoji_Images\img.jpg','wb') 
    f.write(data) 
    f.close() 
    with open('img.jpg', 'rb') as pic:
     data = pic.read()
     await guild.create_custom_emoji(name='Raccoon', image=data)



	#@commands.hybrid_command()
	#async def hello(self, ctx):
	#	await ctx.send("Hello user :)")


async def setup(bot: commands.Bot):
   await bot.add_cog(testing(bot))

