
from discord.ext import commands
from utils.settings import DISCORD_API_SECRET
from functions.DiscordRequests import getemote as gete
from functions .GetItemJPG import getjpg as getj
from functions.DiscordPosts import postdiscordemote as postde

class Emotes(commands.Cog):

	@commands.hybrid_command()
	async def gete(self, ctx, itemname: str):
		markdown = gete(itemname, DISCORD_API_SECRET)
		await ctx.send(f'The Emoji: {markdown}') 
          

	@commands.hybrid_command()
	async def createe(self, ctx, itemname: str):
		getj(itemname)
		jpg = f'Emoji_Images/{itemname}.jpg'
		post = postde(jpg, itemname, DISCORD_API_SECRET)
		markdown = gete(itemname, DISCORD_API_SECRET)
        
		await ctx.send(f'The Emoji: {markdown}')


async def setup(bot: commands.Bot):
   await bot.add_cog(Emotes(bot))
