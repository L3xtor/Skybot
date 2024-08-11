import settings
import discord
from discord.ext import commands
from numerize import numerize
import requests

#HypixelAPI Key
API_KEY = settings.HYPIXEL_API_SECRET


class floorselection(discord.ui.View):
   answer1 = None
   answer2 = None

   @discord.ui.select(placeholder=("Which Dungeon-Type would you like to check?"),      
        options=[discord.SelectOption(label="Normal Floors", value="Normal Floors"), discord.SelectOption(label="Master Mode", value="Master Mode") ]
    )
   
   async def select_floortype(self, interaction:discord.Interaction, select_item:discord.ui.Select):
        self.answer1 = select_item.values 

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event  
    async def on_ready():
        print ("Bot is Up and ready!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e: 
            print(e)


    @bot.hybrid_command()
    async def cata(ctx, playername: str, selectedprofile: str = None):

      """Sends a Stat-Breakdown for a given Player"""
      
      mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/' + playername).json()
      UUID = mojangData['id']
      hypixelProfileData = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={UUID}').json()

      # Searching Each Profile

      if selectedprofile:
         for profile in hypixelProfileData['profiles']:
            if profile['cute_name'] == selectedprofile.capitalize():
             PID = (profile['profile_id']) # Returns the profile ID based on cute name

      else:
         for profile in hypixelProfileData['profiles']:
            if profile['selected'] == True:
             PID = (profile['profile_id']) # Returns the profile ID based on cute name
             selectedprofile = (profile['cute_name'])

      SkycryptDungeonsAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/dungeons/{playername}/{selectedprofile}').json()
      SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()

      networth = numerize.numerize(SkycryptProfileAPI['profiles'][PID]['data']['networth']['networth'])
      dungeons = SkycryptDungeonsAPI['dungeons']
      cataLevel = (dungeons['catacombs']['level']['level'])
      catacompletions = (dungeons['floor_completions'])
      secretsfound = numerize.numerize(dungeons['secrets_found'])
      secretsperrun = round(int(dungeons['secrets_found']) / int(catacompletions), 2)

      hashype = ':x:'
      hasterm = ':x:'

      for weapon in SkycryptProfileAPI['profiles'][PID]['data']['items']['weapons']['weapons']:
            if 'Hyperion' in weapon['display_name']:  
             hashype = ':white_check_mark:'



      for weapon in SkycryptProfileAPI['profiles'][PID]['data']['items']['weapons']['weapons']:
            if 'Terminator' in weapon['display_name']:  
             hasterm = ':white_check_mark:'



      embed = discord.Embed(
          color = discord.Color.dark_teal(),
          title = f"Stat-Breakdown for {playername}",
          description = f"Cata-Level {cataLevel} \n Secrets found {secretsfound} (Per Run: {secretsperrun})\n Networth: {networth}  \n Has Hype: {hashype}  Has Term: {hasterm}  "
        )
      

      await ctx.send(embed=embed) 


    @bot.hybrid_command()
    async def trophys(ctx, playername: str, selectedprofile: str = None):

      """Sends a Trophyfish-Breakdown for a given Player"""
      
      mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/' + playername).json()
      UUID = mojangData['id']
      hypixelProfileData = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={UUID}').json()

      # Searching Each Profile

      if selectedprofile:
         for profile in hypixelProfileData['profiles']:
            if profile['cute_name'] == selectedprofile.capitalize():
             PID = (profile['profile_id']) # Returns the profile ID based on cute name

      else:
         for profile in hypixelProfileData['profiles']:
            if profile['selected'] == True:
             PID = (profile['profile_id']) # Returns the profile ID based on cute name
             selectedprofile = (profile['cute_name'])

      SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()
      trophyStage = SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']['stage']
      fishlist = SkycryptProfileAPI['profiles'][PID]['data']['crimson_isle']['trophy_fish']['fish']
      
      emoji='https://cdn.discordapp.com/emojis//:Emoji:.png?v=1'

      embed = discord.Embed(
          color = discord.Color.dark_teal(),
          title = f"Stat-Breakdown for {playername}",
          description = f"Current trophy-Level {trophyStage}"
        )
      await ctx.send(embed=embed)






          

    @bot.hybrid_command()
    async def times(ctx):
    
        view = floorselection()

        await ctx.send(view=view)
        
        await view.wait()

             



    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()