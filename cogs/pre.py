import discord
from discord.ext import commands


class PrebuiltClass(commands.Cog):

	@commands.hybrid_command()
	async def commandname(self, ctx, playername: str, selectedprofile: str = None):
		something = "something"
		await ctx.send(something) 


	@commands.hybrid_command()
	async def commandnametoo(self, ctx, playername: str, selectedprofile: str = None):
		somethingdifferent = "something different"
		await ctx.send(somethingdifferent)


async def setup(bot: commands.Bot):
   await bot.add_cog(PrebuiltClass(bot))