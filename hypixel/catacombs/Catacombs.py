import discord
from discord.ext import commands

import requests
import logging
from numerize.numerize import numerize
from ctypes import c_int, c_double, Structure, CDLL

from hypixel.utils.Floorselection import floorselection
from hypixel.utils.functions import *

loggers = logging.getLogger('console2')

# Load the shared library (adjust the path if needed)
# Use 'libcata.dll' for Windows or './libcata.so' for Linux/macOS
lib = CDLL('hypixel/catacombs/skills.so')

# Define the SkillsInfo structure in Python to match the C++ struct
class SkillInfo(Structure):
	"""
		Structure to define te Skill level, current xp, xp required to reach the next level, to access these here is an example:-
		```
			playerInfo = lib.getPLayerSkillInfo(initial_xp : float)
		```

		To access Skill level, remaining xp and xp to reach next level, we can do this
		```
			skillLevel : int = playerInfo.skill_level
			current_xp : float = playerInfo.remaining_xp
			xp_to_reach_next_level : float = playerInfo.xp_required_to_level_up
		``` 
		
	"""
	_fields_ = [
        ("skill_level", c_int),
        ("remaining_xp", c_double),
        ("xp_required_to_level_up", c_double)
    ]

# Specify the return type for the getPlayerSkillInfo function (SkillInfo structure)
lib.getPlayerSkillInfo.restype = SkillInfo

# Specify the argument type for the getPlayerSkillInfo function (takes a double)
lib.getPlayerSkillInfo.argtypes = [c_double]


class Catacombs(commands.Cog):

	# Returns profile info of player 
	@staticmethod
	def profileInfo(playername: str, PID):
		SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
		networth = numerize(SkycryptProfileAPI['profiles'][PID]['data']['networth']['networth'])

		has_hype = ':x:'
		has_term = ':x:'

		for weapon in SkycryptProfileAPI['profiles'][PID]['data']['items']['weapons']['weapons']:
			if 'Hyperion' in weapon['display_name']:  
				has_hype = ':white_check_mark:'

		for weapon in SkycryptProfileAPI['profiles'][PID]['data']['items']['weapons']['weapons']:
			if 'Terminator' in weapon['display_name']:  
				has_term = ':white_check_mark:'

		return networth, has_hype, has_term

			
	@commands.hybrid_command()
	async def cata(self, ctx, playername: str, selectedprofile: str = None):
		"""Sends a Stat-Breakdown for a given Player"""
	  
		PID, selectedprofile = returnProfileID(selectedprofile=selectedprofile, playername=playername)

		networth, has_hype, has_term = self.profileInfo(playername=playername, PID=PID)
		cata_level, secrets_found, secrets_per_run, _ = dungeonsInfo(playername=playername, selected_profile=selectedprofile)


		embed = discord.Embed(
		  color = discord.Color.dark_teal(),
		  title = f"Stat-Breakdown for {playername.title()}",
		)

		embed.add_field(name='**Cata-Level**', value= cata_level, inline=False)
		embed.add_field(name=f'Secrets found {secrets_found}', value= f'(Per Run: {secrets_per_run})', inline=False)
		embed.add_field(name='Networth:', value= networth, inline=False)
		embed.add_field(name='Has Hype:', value= has_hype, inline=False)
		embed.add_field(name='Has Term:', value= has_term, inline=False)

		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{playername}/100.png')
		await ctx.send(embed=embed) 


	@commands.hybrid_command()
	async def times(self, ctx, playername: str):
		view = floorselection(playername=playername)
		await ctx.send(view=view)
		await view.wait()




async def setup(bot: commands.Bot):
   await bot.add_cog(Catacombs(bot))