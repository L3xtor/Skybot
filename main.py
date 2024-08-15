# Default modules
from typing import Any, Iterable, Callable, Awaitable


# Discord modules
import discord
from discord.app_commands.tree import CommandTree
from discord.ext import commands


# Modules from different files
import utils.settings as settings


#HypixelAPI Key
API_KEY = settings.HYPIXEL_API_SECRET

# Logger
logger = settings.logging.getLogger('bot')


class floorselection(discord.ui.View):
   answer1 = None
   answer2 = None

   @discord.ui.select(placeholder=("Which Dungeon-Type would you like to check?"),      
        options=[
           discord.SelectOption(label="Normal Floors", value="Normal Floors"), 
           discord.SelectOption(label="Master Mode", value="Master Mode") 
           ]
    )

   async def select_floortype(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values 
        await interaction.response.send_message(self.answer1)
        

# Main class to make a bot
class Bot(commands.Bot):
    # Bot initializer class, auto generated by VSC so no idea whats going on but do not disturb it
    def __init__(
            self, 
            command_prefix: Iterable[str] | str | Callable[[commands.Bot, discord.Message], Iterable[str] | str | Awaitable[Iterable[str] | str]],
            *, 
            tree_cls: CommandTree[Any] = CommandTree, 
            description: str | None = None, 
            intents: discord.Intents, 
            **options: Any
            ) -> None:
        

        super().__init__(
            		command_prefix, 
            		tree_cls=tree_cls, 
        			description=description, 
            		intents=intents, 
            		**options
            )
        
        self.initial_extensions = settings.COGS


	# Loads every cog in the cata directory
    async def setup_hook(self):
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                logger.error(f'Error loading extension {extension}: {e}')
                
        

    async def on_ready(self):
        logger.info("Bot is Up and ready!")
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")

        except Exception as e: 
            print(e)

        self.change_presence(activity=discord.Game(name='Hypixel API shitting'), status=discord.Status.dnd)


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix='!', intents=intents)


    @bot.hybrid_command()
    async def times(ctx):
        view = floorselection()
        await ctx.send(view=view)
        await view.wait()

    bot.run(settings.DISCORD_API_SECRET)