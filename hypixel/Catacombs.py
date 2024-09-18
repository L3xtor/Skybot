import discord
from discord.ext import commands

import requests
from numerize import numerize
from typing import Tuple
from datetime import datetime, timedelta

from utils.settings import HYPIXEL_API_SECRET as API_KEY, logging

loggers = logging.getLogger('console2')


# Returns dungeon info of player
def dungeonsInfo(playername: str, selected_profile: str = None) -> Tuple[int, int, int, dict]:

	_, selected_profile = returnProfileID(playername=playername)
	SkycryptDungeonsAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/dungeons/{playername}/{selected_profile}').json()

	dungeons = SkycryptDungeonsAPI['dungeons']

	if dungeons['catacombs']['visited'] is True :
		cataLevel = dungeons['catacombs']['level']['level'] 
		catacompletions = dungeons['floor_completions']
		secretsfound = numerize.numerize(dungeons['secrets_found'])
		secretsperrun = round(int(dungeons['secrets_found']) / int(catacompletions), 2)

	else:
		cataLevel, secretsfound, secretsperrun = 0, 0, 0

	return cataLevel, secretsfound, secretsperrun, dungeons


# Returns profile ID based on cute name of player
def returnProfileID(playername: str, selectedprofile: str = None):
	hypixelProfiles = Catacombs().miscellaneous_data(playername=playername)

	# Searching Each Profile
	if selectedprofile:
		for profile in hypixelProfiles:
			if profile['cute_name'] == selectedprofile.capitalize():
				return profile['profile_id'], selectedprofile # Returns PID

	else:
		for profile in hypixelProfiles:
			if profile['selected']:
				return profile['profile_id'], profile['cute_name'] # Returns PID and cute name of profile



class floorselection(discord.ui.View):
	def __init__(self, *, timeout: float | None = 180, playername: str):
		super().__init__(timeout=timeout)

		self.playername = playername

	@discord.ui.select(placeholder="Which Dungeon-Type would you like to check?",      
		options=[
			discord.SelectOption(label="Normal Floors", value="catacombs"), 
			discord.SelectOption(label="Master Mode", value="master_catacombs") 
			]
	)
	async def select_floortype(self, interaction: discord.Interaction, select_item: discord.ui.Select):
		_, _, _, dungeons = dungeonsInfo(self.playername)

		# Adds best run of each floor from entrance to floor 7
		best_run_for_each_floor = [dungeons[select_item.values[0]]['floors'][str(i)]['best_runs'][0]['elapsed_time'] for i in range(8)]

		embed = discord.Embed(
			color= discord.Color.red(),
			title=f"Best time for each floor for {self.playername}",
			timestamp=datetime.now()
		)
		embed.add_field(name='Best time for Entrance',value=timedelta(seconds=best_run_for_each_floor[0]), inline=False)
		embed.add_field(name='Best time for Floor 1',value=timedelta(seconds=best_run_for_each_floor[1]), inline=False)
		embed.add_field(name='Best time for Floor 2',value=timedelta(seconds=best_run_for_each_floor[2]), inline=False)
		embed.add_field(name='Best time for Floor 3',value=timedelta(seconds=best_run_for_each_floor[3]), inline=False)
		embed.add_field(name='Best time for Floor 4',value=timedelta(seconds=best_run_for_each_floor[4]), inline=False)
		embed.add_field(name='Best time for Floor 5',value=timedelta(seconds=best_run_for_each_floor[5]), inline=False)
		embed.add_field(name='Best time for Floor 6',value=timedelta(seconds=best_run_for_each_floor[5]), inline=False)
		embed.add_field(name='Best time for Floor 7',value=timedelta(seconds=best_run_for_each_floor[6]), inline=False)

		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{self.playername}/100.png')
		await interaction.channel.send(embed=embed)


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
	

	# Returns Miscellaneous data like Hypixel profiles data
	@staticmethod
	def miscellaneous_data(playername):
		mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/' + playername).json()
		UUID = mojangData['id']
		hypixelProfileData = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={UUID}').json()

		if hypixelProfileData['success']: return hypixelProfileData['profiles']
		else: raise Exception("INVALID HYPIXEL API KEY. PLEASE RENEW")
				

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