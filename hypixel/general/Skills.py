import discord
from discord.ext import commands
from hypixel.utils.Skillselection import Skillselection

class Skills(commands.Cog):
	
	@commands.hybrid_command()
	async def skills(self, ctx, playername: str):
		view = Skillselection(playername=playername)
		await ctx.send(view=view)
		await view.wait()


async def setup(bot: commands.Bot):
   await bot.add_cog(Skills(bot))