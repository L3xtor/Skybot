import json
import requests


from discord.ext import commands
from utils.settings import DISCORD_API_SECRET
from base64 import b64encode
from os import remove


class EmoteFunctions:
	def __init__(self) -> None:
		
		self.applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')
		self.headers = {
						'Authorization':'Bot ' + DISCORD_API_SECRET
						}
	
	def postdiscordemote(self, itemname: str):
		filepath = f'Emoji_Images/{itemname}.jpg'

		binary_fc       = open(filepath, 'rb').read()  # fc aka file_content
		base64_utf8_str = b64encode(binary_fc).decode('utf-8')

		ext     = filepath.split('.')[-1]
		dataurl = f'data:image/{ext};base64,{base64_utf8_str}'
		itemname = itemname.lower()

		data = {
			'name': itemname,
			'image': dataurl
		}
		response = requests.post(self.applicationurl, headers=self.headers, json=data)

		print(response.text)
		remove(filepath)


	@staticmethod
	def getjpg(itemname):
		picpath = f'Emoji_Images/{itemname}.jpg'
		# Get Itemhash of the Skyblock item saved in variable itemname
		with open("Skyblock-Item-Emojis/v3/itemHash.json") as itemHash:
			data = json.load(itemHash)
			itemhash = (data[itemname])

		# Get emoji discord ID with  help of the itemhash
		with open("Skyblock-Item-Emojis/v3/emojis.json") as emojis:
			data = json.load(emojis)
			emojiid = (data[itemhash]["normal"]["id"])

		# Download and save the emoji with its itemname 
		url = (f'https://cdn.discordapp.com/emojis/{emojiid}.png')
		data = requests.get(url).content 
		f = open(picpath,'wb')
		f.write(data) 
		f.close() 

		with open(picpath, 'rb') as pic:
			data = pic.read()
		return picpath

	
	def getemote(self, itemname):
		request = requests.get(self.applicationurl, headers=self.headers)
		if request.ok: 
			data = request.json()
		
		else:
			raise ValueError('Request is not ok, verify key', request.content)


		# Iterate through the items and print the "name"
<<<<<<< HEAD
		items = data['items']
		for item in items:
			if item['name'] == itemname:
				emote_id = item['id'] 
				markdown= f'<:{itemname}:{emote_id}>'
				return markdown
		
=======
		item = data['items'][0]
		if any(item['name'] == itemname for item in data['items']):
			emote_id = item['id'] 
			markdown= f'<:{itemname}:{emote_id}>'
			return markdown if not None else 'Emote wasnt found'
		
		

>>>>>>> 825fc77 (Changed the getjpg function to return the path to the picture)

			
class Emotes(commands.Cog):
	@commands.hybrid_command(name='get_emoji')
	async def _get(self, ctx, itemname: str):
		markdown= EmoteFunctions().getemote(itemname)
		await ctx.send(f'The Emoji: {markdown}') 
          

	@commands.hybrid_command(name='create_emoji')
	async def _create(self, ctx, itemname: str):
		EmoteFunctions().getjpg(itemname)

		EmoteFunctions().postdiscordemote(itemname)
		markdown = EmoteFunctions().getemote(itemname)
        
		await ctx.send(f'The Emoji: {markdown}')


async def setup(bot: commands.Bot):
   await bot.add_cog(Emotes(bot))

# EmoteFunctions().getemote("blobfish_silver")