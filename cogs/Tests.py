from discord import Member
from discord.ext import commands

from typing import Literal

help_str = 'Contact @thefierywarrior  cause if this ain\'t working we are screwed'

cogs = Literal['cogs.Math', 'cogs.Tests', 'cogs.Responses', 'hypixel.Catacombs', 'cogs.Level', 'hypixel.Emoji', 'hypixel.Fishing']


class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_group(name='tests',
                           help=help_str,
                           )
    async def testers(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f'No subcommand used', ephemeral = True)

    @testers.command(name='latency')
    async def check_latency(self, ctx):
        latency = self.bot.latency
        await ctx.send(f'Pong! Latency: {latency * 1000:.2f} ms', ephemeral = True)

    @testers.command(name='reload')
    async def reload(self, ctx, cog_name: cogs):
        await self.bot.reload_extension(cog_name)
        await ctx.send(f'Reloaded {cog_name} successfully!', ephemeral = True)

    @testers.command(name='unload')
    async def unload(self, ctx, cog_name: cogs):
        await self.bot.unload_extension(cog_name)
        await ctx.send(f'Unloaded {cog_name} successfully!', ephemeral = True)

    @testers.command(name='load')
    async def load(self, ctx, cog_name: cogs):
        await self.bot.load_extension(cog_name)
        await ctx.send(f'Loaded {cog_name} successfully!', ephemeral = True)

    @testers.command(name='spam_ping')
    async def spam_ping(self, ctx, member: Member, amount: int):
        for i in range(amount): await ctx.send(member.mention)

    # Function to send the user a DM saying that they do not have the required permissions to use this command
    
    @testers.error
    async def testers_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('You do not have the required permissions to use this command, spread this command and you will be banned '
                           'from the server forever.')

        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(error)


async def setup(bot):
    await bot.add_cog(Tests(bot))
