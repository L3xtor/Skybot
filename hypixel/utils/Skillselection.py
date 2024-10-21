import discord

import requests

from ...utils.settings import HYPIXEL_API_SECRET
from functions import minecraft_uuid

class skillselection(discord.ui.view):
	def __init__(self, *, timeout: float | None = 180, playername: str):
		super().__init__(timeout=timeout)
		self.playername = playername
		 
	@discord.ui.select(placeholder="Which Skill would you like to check",
		options=[
			discord.SelectOption(label="Catacombs", value="player_data"),
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
		skill_name = select_item.values
		hypixel_data = requests.get(f'https://api.hypixel.net/v2/skyblock/profiles?key={HYPIXEL_API_SECRET}&uuid={UUID}').json()

		for profiles in hypixel_data:
			if profiles['selected']:
				profile_data = profiles
				break
		
		if skill_name == 'player_data':
			skill_data = profile_data["player_data"]['experience'][skill_name]
		else:
			skill_data = profile_data[skill_data]['dungeon_types']['catacombs']['experience']