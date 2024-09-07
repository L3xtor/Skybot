import discord
import requests
from discord.ext import commands
from cogs.Catacombs import returnProfileID
from cogs.Emoji import EmoteFunctions



class Fishing(commands.Cog):

	@commands.hybrid_command()
	async def trophy(self, ctx, playername: str, selectedprofile: str = None):
		"""Sends a Trophyfish-Breakdown for a given Player"""
	  	
		# Searching Each Profile
		PID, selectedprofile = returnProfileID(selectedprofile=selectedprofile, playername=playername)
		SkycryptProfileAPI: dict = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
		fish_data: dict= SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']

		def getfishstage(fishname):
			catchedlist: dict = fish_data.get('fish')
			for fish in catchedlist:
				if fish['display_name'] == fishname :
					return (fish.get('highest_tier')) if not None else 'Undiscovered'


		trophyStage = fish_data.get('stage') if not None else 'No Stage reached'


		embed = discord.Embed(
			color = discord.Color.dark_teal(),
			title = f"Trophyfish-Breakdown for {playername.title()}",
			description = f"Current Trophy-Level: {trophyStage}",
			)
		  
		trophyfishnames = ['Blobfish', 'Flyfish', 'Golden Fish', 'Gusher', 'Karate Fish', 'Lavahorse', 'Mana Ray', 'Moldfin', 'Skeleton Fish', 'Slugfish', 'Soul Fish', 'Steaming-Hot Flounder', 'Sulphur Skitter', 'Vanille', 'Volcanic Stonefish', 'Obfuscated 1','Obfuscated 2', 'Obfuscated 3']
 
		for fish in trophyfishnames:
			formatedfishname = fish.title()
			currentemotename = (f'{fish.replace(' ', '_')}_{getfishstage(fish)}').lower()
			embed.add_field(name=formatedfishname, value=f"{EmoteFunctions().getemote(currentemotename)},{getfishstage(fish).capitalize()}")
		
		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{playername}/100.png')
		await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
   await bot.add_cog(Fishing(bot))