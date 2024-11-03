import discord
import asyncio
from discord.ext import commands
from hypixel.utils.Skillselection import Skillselection
from hypixel.utils.rename_this_shit import getPlayerSkillLevel

class Skills(commands.Cog):
	@commands.hybrid_command()
	async def skills(self, ctx, playername: str):
		async def getskillxp(playername):
			view = Skillselection(playername=playername)
			await ctx.send(view=view)

			while not view.interaction_complete: await asyncio.sleep(1)  # Loop until the user has interacted

			return view.skill_data, view.skill_name   # Return the selected skill data

		skilldata, skillname = await getskillxp(playername=playername)  
		
		if skillname == "Catacombs":
			skilltype = skillname
		else:
			skilltype = "Skill"

		embed = discord.Embed(
		  color = discord.Color.dark_teal(),
		  title = f"Stat-Breakdown for {playername.title()}",
		)

		skillLevel, current_xp, xp_to_reach_next_level = getPlayerSkillLevel(skilldata, skilltype)
		embed.add_field(name='**Skill Name**', value= skillname, inline=False)
		embed.add_field(name='**Skill Level**', value= skillLevel, inline=False)
		embed.add_field(name=f'Current xp: {current_xp}', inline=False)
		embed.add_field(name='xp to reach next Level:', value= xp_to_reach_next_level, inline=False)

		await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
   await bot.add_cog(Skills(bot))