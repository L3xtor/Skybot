import discord
from discord.ext import commands

from os import remove
from requests import get
from math import sqrt, floor
from random import randint
from sqlite3 import connect
from utils.settings import LOGGING_CHANNEL
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import Optional



database = connect('database.sqlite')
database.autocommit = True
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Level(user_id INT PRIMARY KEY, exp INT, last_level INT)""")


def fetch_user_info(message: discord.Message):
    cursor.execute(f"""
                    SELECT * FROM Level
                    WHERE user_id = {message.author.id}
                """)

    result = cursor.fetchone()

    if result is None:
        cursor.execute(f"""
                        INSERT INTO Level
                        VALUES({message.author.id}, 1, 1)
                    """)
        return
    return result[1], result[2]


def create_base_card():
    # Create a blank image with a solid background color
    base_width, base_height = 500, 300
    background_color = (50, 50, 50)  # Dark gray
    base = Image.new('RGBA', (base_width, base_height), background_color)

    # Adding sever icon to base image
    server_icon = Image.open('images/server_icon.png').convert("RGBA")
    server_icon = server_icon.resize((50,50))
    base.paste(server_icon, (400,20), server_icon)

    # Save the image
    base.save("images/base.png")



def create_rank_card(username, avatar_url, level, rank, exp) -> str:
    try:
        base = Image.open('images/base.png').convert("RGBA")
    except FileNotFoundError:
        create_base_card()
        base = Image.open('images/base.png').convert("RGBA")
    
    draw = ImageDraw.Draw(base)
    
    # Load avatar image
    response = get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert('RGBA')
    avatar = avatar.resize((120, 120))
    base.paste(avatar, (20, 20), avatar)

    # Define fonts
    font_path = "cogs/Fonts/OpenSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 24)
    small_font = ImageFont.truetype(font_path, 16)

    # Add text to image
    draw.text((150, 20), username, font=font, fill='white')
    draw.text((150, 60), f'LVL {level}', font=small_font, fill='white')
    draw.text((150, 100), f'Rank: #{rank}', font=small_font, fill='white')
    draw.text((150, 140), f'Total exp: {exp}', font=small_font, fill='white')

    # Save image to disk (will be deleted later)
    file_path = f"images/{username}_rank_card.png"
    base.save(file_path)

    return file_path


# Leveling system of the bot
class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.BOT_CMD_CHANNEL = bot.get_channel(LOGGING_CHANNEL)
    

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot : return
        exp, last_level =  fetch_user_info(message)

        if level > last_level:

            cursor.execute(f"""
                            UPDATE Level 
                            SET last_level = {level}
                            WHERE user_id = {message.author.id}
                        """)
            
            embed = discord.Embed(
                color= discord.Color.red(),
                timestamp= datetime.now(),
                description=f"{message.author.mention} has leveled up to *Level {floor(level)}*. GGS"
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)

        exp += randint(1,20)
        level = 0.1 * sqrt(exp)

        cursor.execute(
                        f"""
                        UPDATE Level
                        SET exp = {exp}
                        WHERE user_id = {message.author.id}
                    """
                    )

    @commands.hybrid_command(name='rank')
    async def rank(self, ctx, member: Optional[discord.Member]):
        user = member or ctx.author

        # User data
        username = user.name
        avatar_url = user.avatar.url

        cursor.execute(f"""
                        SELECT exp, level, RANK() OVER (ORDER BY exp DESC) AS rank
                        FROM Level
                        WHERE user_id = {user.id}
                       """)
        
        result = cursor.fetchone()
        exp, level, rank = result

        # Create rank card
        rank_card = create_rank_card(username, avatar_url, round(level), rank, exp)
        
        # Send rank card
        await ctx.send(file=discord.File(rank_card))

        # Delete the rank card
        remove(rank_card)

    
    @commands.hybrid_command(name='leaderboard')
    async def server_leaderboard(self, ctx):
        cursor.execute("""
                    SELECT user_id, exp, RANK() OVER (ORDER BY exp DESC) AS rank
                    FROM Level
                    LIMIT 25
                    """)
        
        rows = cursor.fetchall()
        embed = discord.Embed(title="🏆 Top 25 Users of the Server", color=discord.Color.gold())

        file = discord.File('images/server_icon.png' ,filename='server_icon.png')
        embed.set_thumbnail(url="attachment://server_icon.png")



        for row in rows:
            user_id, exp, rank = row
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{rank}. {user.name}", value=f"**Score**: {exp}", inline=False)

        # Send the embed message
        await ctx.send(file=file, embed=embed)


class Leveling_Debugger(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot :commands.Bot  = bot
        self.BOT_CMD_CHANNEL = self.bot.get_channel(LOGGING_CHANNEL) 


    @commands.hybrid_group(name="exp",
                           hidden = True)
    @commands.is_owner()
    async def exp_debugger(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.author.message("No subcommand used")
    

    @exp_debugger.command(name='add_exp')
    async def add_exp(self, ctx: discord.Message, exp_amount: Optional[int] | None, set_level: Optional[int] | None):
        if ctx.author.bot : return
        
        exp, level, last_level =  fetch_user_info(ctx)

        if exp_amount:
            exp += exp_amount
        elif set_level: 
            level = set_level
        else:
            level = 0.1 * sqrt(exp)
        
        if level > last_level:
            await self.BOT_CMD_CHANNEL.send(f'Fiery, you leveled up, ab exp hain {exp}')    

        cursor.execute(f"""
                        UPDATE Level
                        SET exp = {exp}, level = {level}, last_level = {floor(level)}
                        WHERE user_id = {ctx.author.id}
                    """)


    @exp_debugger.command(name='remove_exp')
    async def remove_exp(self, ctx, exp_amount: Optional[str], set_level: Optional[int]):
        if ctx.author.bot: return
        exp, level, last_level =  fetch_user_info(ctx)

        if exp_amount:
            if exp_amount == 'all':
                exp = 0

            else:
                exp -= int(exp_amount)
            level = 0.1 * sqrt(exp)

        if set_level:
            level = set_level

        if level < last_level:
            await self.BOT_CMD_CHANNEL.send(f'Fiery, you leveled down, ab exp hain {exp}')

        cursor.execute(f"""
                        UPDATE Level
                        SET exp = {exp}, level = {level}, last_level = {floor(level)}
                        WHERE user_id = {ctx.author.id}
                    """)


async def setup(bot):
    await bot.add_cog(Leveling(bot))
    await bot.add_cog(Leveling_Debugger(bot))
