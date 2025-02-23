from os import link
import discord
from discord.ext import commands
from sqlite3 import connect
from hypixel.utils.functions import minecraft_uuid as get_uuid
from hypixel.utils.functions import *

database = connect('accounts.sqlite')
database.autocommit = True  # Enables autocommit mode
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

class Accountslinks(commands.Cog):
	
    @commands.hybrid_command()
    async def link(self, ctx: commands.Context, playername: str):
    
        is_linked, linked_discord = None, None

        embed = discord.Embed(
            color= discord.Color.dark_teal(),
            )

        message_author = ctx.message.author
        interactionUser, interactionUserName, interactionUserID = message_author.mention, message_author.name, message_author.id

        result = cursor.execute(f"SELECT is_linked FROM accountlinks WHERE discord_name = '{interactionUserName}'").fetchone()

        if result:
            is_linked = result[0]

        
            try:
                playerdata = player_data(playername=playername)
                linked_discord = playerdata['socialMedia']['links']['DISCORD']


            except KeyError as e:
                if str(e) == "'id'":
                    embed.add_field(name="No Minecraft Account found!", value=f"User {playername} wasn't found in the Hypixel API")
                elif str(e) == "'socialMedia'":
                    embed.add_field(name="No Discord Account found!", value=f"User {playername} currently isn't linked with any Discord account")

            if linked_discord is not None and linked_discord == interactionUserName:
                (discordUUID, minecraftUUID, discordName, minecraftName, is_linked) = (interactionUserID, get_uuid(playername), interactionUserName, playername, True)

                cursor.execute("""
                                INSERT INTO accountlinks (discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked)
                                VALUES (?, ?, ?, ?, ?)
                                """, (discordUUID, minecraftUUID, discordName, minecraftName, is_linked))
                
                file = discord.File(fp='images/rick_roll.gif', filename='rick_roll.gif')
                embed.set_thumbnail(url='attachment://rick_roll.gif')
                embed.add_field(name= "Thank you!",value=f"Thanks for veryfing *{interactionUser}*", file = file)

            else:
                embed.add_field(name= "Wrong Account linked!",value=f"User '{playername}' has the discord name '{linked_discord}' linked")


        await ctx.send(embed=embed)




    @commands.hybrid_command()
    async def whois(self, ctx, playername: str, ):
        """Displays info about a linked player"""
        embed = discord.Embed(
            color= discord.Color.dark_teal(),
            )

        cursor = connect_linkdb()

        result = cursor.execute(f"""
                                SELECT discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked FROM accountlinks 
                                WHERE minecraft_name = '{playername}'""").fetchone()

        if result:
            discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked = result
            discord_lnk = f"<@{discord_uuid}>"

            if is_linked: 
                is_linked = '<a:checkmark:1302394407231815740>'
                
            fields = (
                f"**Discord UUID:** {discord_uuid}\n"
                f"**Minecraft UUID:** {minecraft_uuid}\n"
                f"**Discord:** {discord_lnk}\n"
                f"**Minecraft Name:** {minecraft_name}\n"
                f"**Link Status:** {is_linked}"
            )

            embed.add_field(name="Following Data was found for user", value=fields)

        else:
            embed.add_field(name="No Data Found", value=f"Account '{playername}' has no linked Discord")


        await ctx.send(embed=embed)



		
async def setup(bot: commands.Bot):
   await bot.add_cog(Accountslinks(bot))