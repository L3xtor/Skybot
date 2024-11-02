import discord
from discord.ext import commands
from sqlite3 import connect
from hypixel.utils.functions import minecraft_uuid as get_uuid
from hypixel.utils.functions import connect_linkdb 

class Accountslinks(commands.Cog):
	
    @commands.hybrid_command()
    async def link(self, ctx, playername: str):
        
        database = connect('accounts.sqlite')
        database.isolation_level = None  # Enables autocommit mode
        cursor = database.cursor()
        is_linked = None
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

        embed = discord.Embed(
            color= discord.Color.dark_teal(),
            )


        interactionUser = ctx.message.author.mention
        interactionUserID = ctx.message.author.id

        result = cursor.execute(f"SELECT discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked FROM accountlinks WHERE discord_name = '{interactionUser}'").fetchone()

        if result:
            discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked = result


        if is_linked is not None:
            embed.add_field(name= "Already linked!",value=f"This Account is already linked with user {discord_name}")
        

        else:
            discordUUID = interactionUserID
            minecraftUUID = get_uuid(playername)
            discordName = interactionUser
            minecraftName = playername
            is_linked = True

            cursor.execute("""
            INSERT INTO accountlinks (discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked)
            VALUES (?, ?, ?, ?, ?)
            """, (discordUUID, minecraftUUID, discordName, minecraftName, is_linked))

            embed.add_field(name= "Thank you!",value=f"Thanks for veryfing *{interactionUser}*")
            await ctx.send(embed=embed)




    @commands.hybrid_command()
    async def whois(self, ctx, playername: str, ):

        embed = discord.Embed(
            color= discord.Color.dark_teal(),
            )

        cursor = connect_linkdb()

        result = cursor.execute(f"SELECT discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked FROM accountlinks WHERE minecraft_name = '{playername}'").fetchone()

        if result:
            discord_uuid, minecraft_uuid, discord_name, minecraft_name, is_linked = result

            if is_linked == 1: 
                is_linked = '<a:checkmark:1302394407231815740>'
                
            fields = (
                f"**Discord UUID:** {discord_uuid}\n"
                f"**Minecraft UUID:** {minecraft_uuid}\n"
                f"**Discord Name:** {discord_name}\n"
                f"**Minecraft Name:** {minecraft_name}\n"
                f"**Link Status:** {is_linked}"
            )

            embed.add_field(name="Following Data was found for user", value=fields)

        else:
            embed.add_field(name="No Data Found", value=f"Account '{playername}' has no linked Discord")


        await ctx.send(embed=embed)



		
async def setup(bot: commands.Bot):
   await bot.add_cog(Accountslinks(bot))