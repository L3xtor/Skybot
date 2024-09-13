import logging

from json import load
from os import getenv, listdir
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

with open('utils/loggers.json') as loggers:
    logging_config = load(loggers)

DISCORD_API_SECRET = getenv("DISCORD_API_TOKEN")
HYPIXEL_API_SECRET = getenv("HYPIXEL_API_TOKEN")
LOGGING_CHANNEL = getenv('LOGGING_CHANNEL')

NORMAL_COGS_DIR = listdir('cogs')
HYPIXEL_COGS_DIR = listdir('hypixel')

# Adds ever cog into the list without '.py' and also ignores the file if its a '__init__.py' file
NORMAL_COGS = [f'cogs.{cogs[:-3]}' for cogs in NORMAL_COGS_DIR if cogs != '__init__.py' and cogs.endswith('.py') ]
HYPIXEL_COGS = [f'hypixel.{cogs[:-3]}' for cogs in HYPIXEL_COGS_DIR if cogs != '__init__.py' and cogs.endswith('.py') ]

COGS = NORMAL_COGS + HYPIXEL_COGS

dictConfig(logging_config)