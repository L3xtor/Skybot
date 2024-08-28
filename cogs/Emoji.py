import requests
from discord.ext import commands
from utils.settings import DISCORD_API_SECRET as k

def gete(itemname, apikey):
    applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')
    headers = {'Authorization':'Bot ' + apikey}
    request = requests.get(applicationurl, headers=headers)

    data = (request).json()
    
    for emote in data['items']:
        if emote['name'] == itemname:
            emoteid = (emote['id'])
            markdown = (f'<:{itemname}:{emoteid}>')
            return markdown
        break
    else:
        markdown = ('not found')
        return markdown

class emotes(commands.Cog):

	@commands.hybrid_command()
	async def gete(self, ctx, itemname: str):
		markdown = gete(itemname, k)
		await ctx.send(f'The Emoji: {markdown}') 


async def setup(bot: commands.Bot):
   await bot.add_cog(emotes(bot))