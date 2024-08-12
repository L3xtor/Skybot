from os import getenv, listdir
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = getenv("DISCORD_API_TOKEN")
HYPIXEL_API_SECRET = getenv("HYPIXEL_API_TOKEN")

CATA_COGS = ['cata.Catacombs']