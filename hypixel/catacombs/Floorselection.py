import discord

from datetime import datetime,timedelta
from hypixel.catacombs.functions import dungeonsInfo

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
		embed.add_field(name='Best time for Entrance',value=timedelta(milliseconds=best_run_for_each_floor[0]), inline=False)
		embed.add_field(name='Best time for Floor 1',value=timedelta(milliseconds=best_run_for_each_floor[1]), inline=False)
		embed.add_field(name='Best time for Floor 2',value=timedelta(milliseconds=best_run_for_each_floor[2]), inline=False)
		embed.add_field(name='Best time for Floor 3',value=timedelta(milliseconds=best_run_for_each_floor[3]), inline=False)
		embed.add_field(name='Best time for Floor 4',value=timedelta(milliseconds=best_run_for_each_floor[4]), inline=False)
		embed.add_field(name='Best time for Floor 5',value=timedelta(milliseconds=best_run_for_each_floor[5]), inline=False)
		embed.add_field(name='Best time for Floor 6',value=timedelta(milliseconds=best_run_for_each_floor[5]), inline=False)
		embed.add_field(name='Best time for Floor 7',value=timedelta(milliseconds=best_run_for_each_floor[6]), inline=False)

		embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{self.playername}/100.png')
		await interaction.channel.send(embed=embed)