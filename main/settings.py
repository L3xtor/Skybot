import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
HYPIXEL_API_SECRET = os.getenv("HYPIXEL_API_TOKEN")
