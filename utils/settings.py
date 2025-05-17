import logging
import asyncio

from os import getenv
from dotenv import load_dotenv
from logging.config import dictConfig
from json import loads
import aiofiles
import aiofiles.os

load_dotenv()


async def load_config():
    async with aiofiles.open("utils/loggers.json", mode="r") as loggers:
        return loads(await loggers.read())


async def get_cogs(path: str, prefix: str):
    try:
        files = await aiofiles.os.listdir(path)
        return [
            f"{prefix}.{f[:-3]}"
            for f in files
            if f.endswith(".py") and f != "__init__.py"
        ]
    except FileNotFoundError:
        return []


async def return_cogs():
    logging_config = await load_config()
    dictConfig(logging_config)

    tasks = [
        get_cogs("cogs", "cogs"),
        get_cogs("hypixel", "hypixel"),
        get_cogs("hypixel/catacombs", "hypixel.catacombs"),
        get_cogs("hypixel/fishing", "hypixel.fishing"),
        get_cogs("hypixel/general", "hypixel.general"),
        get_cogs("hypixel/partyfinder", "hypixel.partyfinder"),
    ]

    (
        NORMAL_COGS,
        HYPIXEL_COGS,
        CATACOMBS_COGS,
        FISHING_COGS,
        GENERAL_COGS,
        PARTY_COGS,
    ) = await asyncio.gather(*tasks)

    COGS = (
        NORMAL_COGS
        + HYPIXEL_COGS
        + CATACOMBS_COGS
        + FISHING_COGS
        + GENERAL_COGS
        + PARTY_COGS
    )

    return COGS


def get_all_cogs():
    return asyncio.run(return_cogs())


COGS = get_all_cogs()
DISCORD_API_SECRET = getenv("DISCORD_API_TOKEN", default="1")
HYPIXEL_API_SECRET = getenv("HYPIXEL_API_TOKEN", default="1")
LOGGING_CHANNEL = getenv("LOGGING_CHANNEL", default="1")
