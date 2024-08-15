from asyncio import sleep
from datetime import datetime
from random import choice, randint

import discord
from discord.ext import commands


class Responses(commands.Cog):
    @commands.hybrid_command(name="about")
    async def about(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.red(),
            title="About me",
            description="Hi! I'm a bot that was created my TheFieryWarrior purely in python!. I am just his coding project and I hope that I can help"
                        " with my geeky things my creator coded for you"
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/731143503530164374/7ac170c9e25e3cf308d3af80ab961234.webp?size=80')
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='8ball')
    async def _8ball_command(self, ctx):
        """Returns random 8ball question"""
        ball_responses = ['The same response as every boy/girl gave you when you asked them out, no.',
                            'You wanna hear no in German? NEIN.',
                            'As one wise man said, just go with the flow.',
                            'The one in a million, a YES.',
                            'True, yea, I am listening.',
                            'Yes, couldn\'t be more obvious.',
                            'You good?, cause all I see is a no',
                            'yeet',
                            'baldiest bald of baller, baller bald than intrests'
                            ]
        await ctx.send(choice(ball_responses))


    @commands.hybrid_command(aliases=['pong', 'p'],
                             name="ping",
                             description='Returns pong',
                             brief='Returns Pong'
                             )
    async def ping(self, ctx):
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'Pong! {discord.Member.mention}',
            timestamp=datetime.now()
        )

        embed.set_author(name=str(ctx.author).title(), url='https://github.com/CodingWithPython?tab=repositories')
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='say')
    async def say(self, ctx, user_message):
        if not user_message:
            await ctx.send('WHAT DO YOU WANT FROM ME')
        else:
            await ctx.send(type(user_message))


    @commands.hybrid_command(name='hello',
                             aliases=['hi', 'hi_bot'],
                             description='Just pings the user who used this command',
                             brief='Returns Hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}!')


    @commands.hybrid_command(name='slap', description='Slaps a member')
    async def slap_command(self, ctx, member: discord.Member, reason: str):
        randint_1 = randint(1, 10)
        randint_2 = randint(1, 10)

        await ctx.send(f'{ctx.author.mention} slapped {member.mention} with reason {reason}')

        if randint_1 == randint_2:
            await ctx.send(f'***CRITICAL HIT*** {member.mention} is now muted for 5 minutes as they are unconscious from the slap')
            await member.add_roles(discord.utils.get(member.guild.roles, name='Muted'))
            await sleep(300)
            await ctx.send(f'{member.mention} welcome back! You were slapped unconscious from the slap given by {ctx.author.mention}')
            await member.remove_roles(discord.utils.get(member.guild.roles, name='Muted'))


    @commands.Cog.listener()
    async def on_message(self, ctx):
        random_number = randint(1,100)
        if ctx.author.bot: return

        if random_number <= 2:
            file = discord.File("images/rick_roll.gif")
            await ctx.reply(file=file)

            await ctx.reply("GET RICK ROLLED SON")

async def setup(bot):
    await bot.add_cog(Responses(bot))
