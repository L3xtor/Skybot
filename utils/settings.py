from os import getenv, listdir
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = getenv("DISCORD_API_TOKEN")
HYPIXEL_API_SECRET = getenv("HYPIXEL_API_TOKEN")

COGS_DIR = listdir('cogs')

# Adds ever cog into the list without '.py' and also ignores the file if its a '__init__.py' file
COGS = [f'cogs.{cogs[:-3]}' for cogs in COGS_DIR if cogs != '__init__.py' and cogs.endswith('.py') ]