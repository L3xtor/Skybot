import discord
import requests
from discord.ext import commands
from hypixel.catacombs.functions import returnProfileID
from hypixel.Emoji import EmoteFunctions

from typing import Tuple

class Fishing(commands.Cog):
	def get_fish_and_trophy_stage(self, playername: str, selected_profile: str = None) -> Tuple[dict, str]:

		# Searching Each Profile
		PID, _ = returnProfileID(selectedprofile=selected_profile, playername=playername)
		SkycryptProfileAPI: dict = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
		fish_data: dict= SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']
		catchedlist: dict = fish_data.get('fish')

		trophyStage = fish_data.get('stage') if not None else 'No Stage reached'

		# Creates a dictionary with all the fish name where " " gets replaced by '_' in fish names 
		# and the highest tier of the fish is the value
		fish_tier = {fish['display_name']: fish.get('highest_tier') for fish in catchedlist}

		return fish_tier.items(), trophyStage

	@commands.hybrid_command(name='trophy_stats')
	async def trophy(self, ctx, playername: str, selectedprofile: str = None):
		"""Sends a Trophyfish-Breakdown for a given Player"""
	  	
		fish_tiers ,trophyStage = self.get_fish_and_trophy_stage(playername, selectedprofile)
		embed = discord.Embed(
			color = discord.Color.dark_teal(),
			title = f"Trophyfish-Breakdown for {playername.title()}",
			description = f"Current Trophy-Level: {trophyStage}",
			)

		for fish_name, fish_stage in fish_tiers:
			fishname: str = ((fish_name.replace(" ", "_")).replace("-","_") + "_" + fish_stage).lower()
			emotji_markdown = (EmoteFunctions().getemote(fishname))

			embed.add_field(name=fishname.replace("_", " ").title(), value=f"{emotji_markdown}, {fish_stage.capitalize()}")
			
		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{playername}/100.png')
		await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
   await bot.add_cog(Fishing(bot))