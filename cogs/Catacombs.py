import discord
from discord.ext import commands


from numerize import numerize
import requests

from utils.settings import HYPIXEL_API_SECRET as API_KEY


# Returns profile info of player 
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


# Returns dungeon info of player
def dungeonsInfo(playername: str, selected_profile):
	SkycryptDungeonsAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/dungeons/{playername}/{selected_profile}').json()


	dungeons = SkycryptDungeonsAPI['dungeons']

	if dungeons['catacombs']['visited'] is True :
		cataLevel = dungeons['catacombs']['level']['level'] 
		catacompletions = dungeons['floor_completions']
		secretsfound = numerize.numerize(dungeons['secrets_found'])
		secretsperrun = round(int(dungeons['secrets_found']) / int(catacompletions), 2)

	else:
		cataLevel, secretsfound, secretsperrun = 0, 0, 0

	return cataLevel, secretsfound, secretsperrun


# Returns Miscellaneous data like Hypixel profiles data
def miscellaneous_data(playername):
	mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/' + playername).json()
	UUID = mojangData['id']
	hypixelProfileData = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={UUID}').json()

	return hypixelProfileData


# Returns profile ID based on cute name of player
def returnProfileID(selectedprofile: str, playername: str):
	hypixelProfileData = miscellaneous_data(playername=playername)

	# Searching Each Profile
	if selectedprofile:
		for profile in hypixelProfileData['profiles']:
			if profile['cute_name'] == selectedprofile.capitalize():
				return profile['profile_id'], selectedprofile # Returns PID

	else:
		for profile in hypixelProfileData['profiles']:
			if profile['selected'] == True:
				return profile['profile_id'], profile['cute_name'] # Returns PID and cute name of profile


class Catacombs(commands.Cog):

	@commands.hybrid_command()
	async def cata(self, ctx, playername: str, selectedprofile: str = None):
		"""Sends a Stat-Breakdown for a given Player"""
	  
		PID, selectedprofile = returnProfileID(selectedprofile=selectedprofile, playername=playername)

		networth, has_hype, has_term = profileInfo(playername=playername, PID=PID)
		cata_level, secrets_found, secrets_per_run = dungeonsInfo(playername=playername, selected_profile=selectedprofile)


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


async def setup(bot: commands.Bot):
   await bot.add_cog(Catacombs(bot))