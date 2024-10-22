import discord
import requests

from utils.settings import HYPIXEL_API_SECRET
from hypixel.utils.functions import minecraft_uuid
from datetime import datetime


class Skillselection(discord.ui.View):
	def __init__(self, *, timeout: float | None = 180, playername: str):
		super().__init__(timeout=timeout)

		self.playername = playername

	@discord.ui.select(placeholder="Which Skill would you like to check?",      
		options=[
			discord.SelectOption(label="Catacombs", value="catacombs"),
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
		skill_name = select_item.values[0]
		hypixel_data = requests.get(f'https://api.hypixel.net/v2/skyblock/profiles?key={HYPIXEL_API_SECRET}&uuid={UUID}').json()

		for profiles in hypixel_data['profiles']:
			if profiles['selected']:
				profile_data = profiles
				break

		if skill_name == "catacombs":
			skill_data = profile_data['members'][UUID]['dungeons']['dungeon_types']['catacombs']['experience']
		else:
			skill_data = profile_data['members'][UUID]['player_data']['experience'][skill_name]
		
		embed = discord.Embed(
			color= discord.Color.red(),
			title=f"Test",
			timestamp=datetime.now()
		)
		embed.add_field(name='Testname',value=(skill_data), inline=False)

		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{self.playername}/100.png')
		await interaction.channel.send(embed=embed)