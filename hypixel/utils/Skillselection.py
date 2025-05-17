import discord	

from utils.settings import HYPIXEL_API_SECRET
from hypixel.utils.functions import minecraft_uuid
import aiohttp


skill_emotes = {
    "Catacombs": "🪦",        
    "SKILL_FISHING": "🎣",    
    "SKILL_ALCHEMY": "⚗️",    
    "SKILL_MINING": "⛏️",     
    "SKILL_FARMING": "🌾",     
    "SKILL_ENCHANTING": "✨",  
    "SKILL_TAMING": "🐾",      
    "SKILL_FORAGING": "🪚",     
    "SKILL_CARPENTRY": "🔨",   
    "SKILL_COMBAT": "⚔️",     
}

class Skillselection(discord.ui.View):
	def __init__(self, *, timeout: float | None = 180, playername: str):
		super().__init__(timeout=timeout)

		self.playername = playername
		self.skill_data = 'Not filled yet'
		self.interaction_complete = False

	@discord.ui.select(placeholder="Which Skill would you like to check?",      
		options=[
			discord.SelectOption(label="Catacombs", value="Catacombs"),
			discord.SelectOption(label="Fishing", value="SKILL_FISHING"),
			discord.SelectOption(label="Alchemy", value="SKILL_ALCHEMY"),
			discord.SelectOption(label="Mining", value="SKILL_MINING"),
			discord.SelectOption(label="Farming", value="SKILL_FARMING"),
			discord.SelectOption(label="Enchanting", value="SKILL_ENCHANTING"),
			discord.SelectOption(label="Taming", value="SKILL_TAMING"),
			discord.SelectOption(label="Foraging", value="SKILL_FORGING"),
			discord.SelectOption(label="Carpentry", value="SKILL_CARPENTRY"),
			discord.SelectOption(label="Combat", value="SKILL_COMBAT"),
			]
	)
	async def select_skill(self, interaction: discord.Interaction, select_item: discord.ui.Select):
		UUID = minecraft_uuid(playername=self.playername)
		self.skill_name = select_item.values[0]

		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://api.hypixel.net/v2/skyblock/profiles?key={HYPIXEL_API_SECRET}&uuid={UUID}') as resp:
				hypixel_data = await resp.json()  

		for profiles in hypixel_data['profiles']:
			if profiles['selected']:
				profile_data = profiles
				break

		if self.skill_name == "Catacombs":
			self.skill_data = profile_data['members'][UUID]['dungeons']['dungeon_types']['catacombs']['experience']
		else:
			self.skill_data = profile_data['members'][UUID]['player_data']['experience'][self.skill_name]

		self.skill_emoji = skill_emotes.get(self.skill_name)

		self.interaction_complete = True
		await interaction.response.defer()
		return self.skill_data, self.skill_name, self.skill_emoji

