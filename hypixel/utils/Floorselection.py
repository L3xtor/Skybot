import discord
from datetime import datetime, timedelta
from typing import Optional
from hypixel.utils.functions import dungeonsInfo

class FloorSelection(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180, playername: str):
        super().__init__(timeout=timeout)
        self.playername = playername

    @discord.ui.select(
        placeholder="Which Dungeon-Type would you like to check?",
        options=[
            discord.SelectOption(label="Normal Floors", value="catacombs"),
            discord.SelectOption(label="Master Mode", value="master_catacombs")
        ]
    )
    async def select_floortype(
        self,
        interaction: discord.Interaction,
        select_item: discord.ui.Select
    ):
        _, _, _, dungeons = dungeonsInfo(self.playername)
        selected_floor_type = select_item.values[0]

        try:
            floor_data = dungeons[selected_floor_type]["floors"]
        except KeyError:
            await interaction.response.send_message(
                "Dungeon data not found for the selected type.", ephemeral=True
            )
            return

        best_runs = []
        for i in range(8):
            floor_key = str(i)
            try:
                if i == 0 and selected_floor_type == "master_catacombs":
                    best_runs.append(None)
                else:
                    best_time = floor_data[floor_key]["best_runs"][0]["elapsed_time"]
                    best_runs.append(best_time)
            except (KeyError, IndexError, TypeError):
                best_runs.append(None)

        embed = discord.Embed(
            color=discord.Color.red(),
            title=f"Best time for each floor for {self.playername}",
            timestamp=datetime.now()
        )

        for i, run_time in enumerate(best_runs):
            floor_label = "Entrance" if i == 0 else f"Floor {i}"
            display_time = (
                str(timedelta(milliseconds=run_time))
                if run_time is not None
                else "No run data"
            )
            embed.add_field(name=f"Best time for {floor_label}", value=display_time, inline=False)

        embed.set_thumbnail(url=f'https://mineskin.eu/headhelm/{self.playername}/100.png')
        await interaction.response.send_message(embed=embed)
