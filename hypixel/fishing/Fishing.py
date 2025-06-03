import discord
import requests
import asyncio
from discord.ext import commands
from hypixel.utils.functions import returnProfileID
from hypixel.utils.Emoji import EmoteFunctions

from typing import Optional, Tuple, List


class Fishing(commands.Cog):
    def get_fish_and_trophy_stage(
        self, playername: str, selected_profile: Optional[str]
    ) -> Tuple[List[Tuple[str, str]], str]:
        """Fetches the player's trophy fish data and current trophy stage."""

        result = returnProfileID(
            selectedprofile=selected_profile, playername=playername
        )
        if result is None:
            raise ValueError("No profile ID found for that player/profile.")
        profile_id, profile_name = result

        # Fetch SkyCrypt profile data
        try:
            response = requests.get(
                f"https://sky.shiiyu.moe/api/v2/profile/{playername}/{profile_name}"
            )
            response.raise_for_status()
            profile_data = response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch SkyCrypt data: {e}")

        # Extract trophy fish data safely
        try:
            trophy_info = profile_data["profiles"][profile_id]["data"]["crimson_isle"][
                "trophy_fish"
            ]
        except KeyError:
            raise ValueError("Trophy fish data not found for this profile.")

        caught_fish = trophy_info.get("fish", [])
        trophy_stage = trophy_info.get("stage") or "No Stage reached"

        # Build a list of (fish name, highest tier) pairs
        fish_tiers = [
            (fish["display_name"], fish.get("highest_tier", "bronze"))
            for fish in caught_fish
        ]

        return fish_tiers, trophy_stage

    @commands.hybrid_command(name="trophy_stats")
    async def trophy(self, ctx, playername: str, selectedprofile: Optional[str]):
        """Sends a Trophyfish-Breakdown for a given Player"""

        fish_tiers, trophyStage = self.get_fish_and_trophy_stage(
            playername, selectedprofile
        )
        embed = discord.Embed(
            color=discord.Color.dark_teal(),
            title=f"Trophyfish-Breakdown for {playername.title()}",
            description=f"Current Trophy-Level: {trophyStage}",
        )

        async def process_fish(fish_name, fish_stage):
            fish_and_stage = (
                (fish_name.replace(" ", "_")).replace("-", "_")
                + f"_{fish_stage or 'bronze'}"
            ).lower()
            emoji_markdown = await EmoteFunctions().getemote(fish_and_stage)

            if fish_stage == "bronze":
                fish_stage_emote = ":brown_circle: Bronze"
            elif fish_stage == "silver":
                fish_stage_emote = ":white_circle: Silver"
            elif fish_stage == "gold":
                fish_stage_emote = ":yellow_circle: Gold"
            elif fish_stage == "diamond":
                fish_stage_emote = ":small_blue_diamond: Diamond"
            else:
                fish_stage_emote = "Not found yet!"

            embed.add_field(
                name=f"{emoji_markdown} {fish_name.title()}",
                value=f"{fish_stage_emote}",
            )

        await asyncio.gather(
            *(
                process_fish(fish_name, fish_stage)
                for fish_name, fish_stage in fish_tiers
            )
        )

        embed.set_thumbnail(url=f"https://mineskin.eu/headhelm/{playername}/100.png")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fishing(bot))
