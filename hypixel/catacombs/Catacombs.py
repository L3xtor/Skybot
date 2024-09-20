import discord
from discord.ext import commands

import requests
import logging
from numerize import numerize

from hypixel.catacombs.Floorselection import floorselection
from hypixel.catacombs.functions import *

loggers = logging.getLogger('console2')


class Catacombs(commands.Cog):

	# Returns profile info of player 
	@staticmethod
	def profileInfo(playername: str, PID):
		SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
		networth = numerize.numerize(SkycryptProfileAPI['profiles'][PID]['data']['networth']['networth'])

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
	  
		PID, selectedprofile = self.returnProfileID(selectedprofile=selectedprofile, playername=playername)

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