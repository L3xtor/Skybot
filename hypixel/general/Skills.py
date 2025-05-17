import discord
import asyncio
from discord.ext import commands
from hypixel.utils.Skillselection import Skillselection
from hypixel.utils.GetSkillInfo import getPlayerSkillLevel
from numerize.numerize import numerize


class Skills(commands.Cog):
	@commands.hybrid_command()
	async def skills(self, ctx, playername: str):
		"""Shows Skill Level, current xp and xp to next lvl"""
		async def getskillxp(playername):
			view = Skillselection(playername=playername)
			await ctx.send(view=view)

			while not view.interaction_complete: await asyncio.sleep(1)  # Loop until the user has interacted

			return view.skill_data, view.skill_name, view.skill_emoji   # Return the selected skill data

		skilldata, skillname, skillemote = await getskillxp(playername=playername)  
		
		SkillnameFormated = skillname.capitalize() if skillname == 'Catacombs' else skillname.replace("SKILL_", "").capitalize()

		embed = discord.Embed(
		  color = discord.Color.dark_teal(),
		  title = f"Skill-Breakdown for {playername.title()}",
		)

		skillLevel, current_xp, xp_to_reach_next_level = getPlayerSkillLevel(skilldata, skillname)

		embed.add_field(name='**Selected Skill**', value= f'[{skillemote}] {SkillnameFormated}', inline=False) 
		embed.add_field(name='**Skill Level**', value= skillLevel, inline=False)
		embed.add_field(name=f'Current xp:', value=numerize(current_xp), inline=False)
		embed.add_field(name='xp to reach next Level:', value= numerize(xp_to_reach_next_level), inline=False)

		await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
   await bot.add_cog(Skills(bot))