import requests
from typing import Any, Dict, Optional, Tuple
from numerize import numerize
from sqlite3 import connect

from utils.settings import HYPIXEL_API_SECRET as API_KEY


class HypixelAPIError(Exception):
    pass


# Returns dungeon info of player
def dungeonsInfo(
    playername: str, selected_profile: str | None
) -> Tuple[int, int, float, Dict[Any, Any]]:
    _, selected_profile = returnProfileID(playername=playername)
    SkycryptDungeonsAPI = requests.get(
        f"https://sky.shiiyu.moe/api/v2/dungeons/{playername}/{selected_profile}"
    ).json()

    dungeons = SkycryptDungeonsAPI["dungeons"]

    if dungeons["catacombs"]["visited"] is True:
        cataLevel: int = dungeons["catacombs"]["level"]["level"]
        catacompletions: int = dungeons["floor_completions"]
        secretsfound: int = int(numerize.numerize(dungeons["secrets_found"]))
        secretsperrun: float = round(
            int(dungeons["secrets_found"]) / int(catacompletions), 2
        )

    else:
        cataLevel, secretsfound, secretsperrun = 0, 0, 0

    return cataLevel, secretsfound, secretsperrun, dungeons


# Returns profile ID based on cute name of player
def returnProfileID(playername: str, selectedprofile: Optional[str] = None):
    hypixelProfiles = miscellaneous_data(playername=playername)

    # Searching Each Profile
    if selectedprofile:
        for profile in hypixelProfiles:
            if profile["cute_name"] == selectedprofile.capitalize():
                return profile["profile_id"], selectedprofile  # Returns PID

    else:
        for profile in hypixelProfiles:
            if profile["selected"]:
                return profile["profile_id"], profile[
                    "cute_name"
                ]  # Returns PID and cute name of profile


# Returns Miscellaneous data like Hypixel profiles data
def miscellaneous_data(playername):
    UUID = minecraft_uuid(playername=playername)
    hypixelProfileData = requests.get(
        f"https://api.hypixel.net/v2/skyblock/profiles?key={API_KEY}&uuid={UUID}"
    ).json()

    if hypixelProfileData["success"]:
        return hypixelProfileData["profiles"]
    else:
        raise HypixelAPIError(hypixelProfileData["cause"])


def player_data(playername):
    UUID = minecraft_uuid(playername=playername)
    hypixelProfileData = requests.get(
        f"https://api.hypixel.net/v2/player?key={API_KEY}&uuid={UUID}"
    ).json()

    if hypixelProfileData["success"]:
        return hypixelProfileData["player"]
    else:
        raise HypixelAPIError(hypixelProfileData["cause"])


def minecraft_uuid(playername: str):
    return (
        requests.get(
            "https://api.mojang.com/users/profiles/minecraft/" + playername
        ).json()
    )["id"]


def connect_linkdb():
    database = connect("accounts.sqlite")
    database.isolation_level = None  # Enables autocommit mode
    cursor = database.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS accountlinks (
                        discord_uuid VARCHAR(255) PRIMARY KEY,
                        minecraft_uuid VARCHAR(255),
                        discord_name VARCHAR(255),
                        minecraft_name VARCHAR(255),
                        is_linked BOOLEAN
                        )     
        """)
    return cursor


def whodis(dcname):
    cursor = connect_linkdb()
    result = cursor.execute(
        f"SELECT discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked FROM accountlinks WHERE discord_name = '{dcname}'"
    ).fetchone()

    if result:
        discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked = result

    class player:
        def __init__(
            self, discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked
        ):
            self.discordid = discord_uuid
            self.minecraftid = minecraft_uuid
            self.discordname = discord_name
            self.minecraftname = minecraft_name
            self.linked = is_linked

    return player(discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked)


skill_emotes = {
    "Catacombs": "🪦",  # Example emoji for Catacombs
    "SKILL_FISHING": "🎣",  # Emoji for Fishing
    "SKILL_ALCHEMY": "⚗️",  # Emoji for Alchemy
    "SKILL_MINING": "⛏️",  # Emoji for Mining
    "SKILL_FARMING": "🌾",  # Emoji for Farming
    "SKILL_ENCHANTING": "✨",  # Emoji for Enchanting
    "SKILL_TAMING": "🐾",  # Emoji for Taming
    "SKILL_FORGING": "🔨",  # Emoji for Foraging
    "SKILL_CARPENTRY": "🪚",  # Emoji for Carpentry
    "SKILL_COMBAT": "⚔️",  # Emoji for Combat
}


def get_skill_emote(skill_name):
    return skill_emotes.get(skill_name, "❓")


get_skill_emote("SKILL_FISHING")

