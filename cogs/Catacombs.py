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
		cataLevel, secretsfound, secretsperrun, catacompletions = 0, 0, 0, 0

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
		  description = f"""
						Cata-Level {cata_level} \n 
						Secrets found {secrets_found} (Per Run: {secrets_per_run}) \n 
						Networth: {networth}  \n 
						Has Hype: {has_hype}  
						Has Term: {has_term}  
						"""
		)

		await ctx.send(embed=embed) 


	@commands.hybrid_command()
	async def trophys(self, ctx, playername: str, selectedprofile: str = None):
		"""Sends a Trophyfish-Breakdown for a given Player"""
	  
		# Searching Each Profile
		PID, selectedprofile = returnProfileID(selectedprofile=selectedprofile, playername=playername)


		SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
		trophyStage = SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']['stage']
		fishlist = SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']['fish']
		
		emoji='https://cdn.discordapp.com/emojis//:Emoji:.png?v=1'

		embed = discord.Embed(
			color = discord.Color.dark_teal(),
			title = f"Stat-Breakdown for {playername.title()}",
			description = f"Current trophy-Level {trophyStage}"
			)
		await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
   await bot.add_cog(Catacombs(bot))