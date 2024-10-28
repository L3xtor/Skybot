import discord
from discord.ext import commands
from hypixel.utils.Skillselection import Skillselection
from ctypes import c_int, c_double, Structure, CDLL
import asyncio



class Skills(commands.Cog):
	

	@commands.hybrid_command()
	async def skills(self, ctx, playername: str):

		class SkillInfo(Structure):
			fields_ = [
        ("skill_level", c_int),
        ("remaining_xp", c_double),
        ("xp_required_to_level_up", c_double)
		]

		async def getskillxp(playername):
			view = Skillselection(playername=playername)
			await ctx.send(view=view)

			while not view.interaction_complete:
				await asyncio.sleep(1)  # Loop until the user has interacted
		
			return view.skill_data  # Return the selected skill data

		skilldata = await getskillxp(playername=playername)
		print(skilldata)

		embed = discord.Embed(
		  color = discord.Color.dark_teal(),
		  title = f"Stat-Breakdown for {playername.title()}",
		)


		lib = CDLL('hypixel/catacombs/skills.so')
		lib.getPlayerSkillInfo.restype = SkillInfo
		lib.getPlayerSkillInfo.argtypes = [c_double]

		
		playerInfo = lib.getPlayerSkillInfo(skilldata)
		skillLevel : int = playerInfo.skill_level
		current_xp : float = playerInfo.remaining_xp
		xp_to_reach_next_level : float = playerInfo.xp_required_to_level_up


		embed.add_field(name='**Skill Level**', value= skillLevel, inline=False)
		embed.add_field(name=f'Current xp: {current_xp}', inline=False)
		embed.add_field(name='xp to reach next Level:', value= xp_to_reach_next_level, inline=False)

		await ctx.send(embed=embed)



async def setup(bot: commands.Bot):
   await bot.add_cog(Skills(bot))