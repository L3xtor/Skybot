import os
from discord.ext import commands
from utils.settings import DISCORD_API_SECRET
from base64 import b64encode


class EmoteFunctions:
	def __init__(self) -> None:
		self.applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')
		self.headers = {
			'Authorization':'Bot ' + DISCORD_API_SECRET
			}


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


	def getemote(self, itemname):
		request = requests.get(self.applicationurl, headers=self.headers)
		if request.ok: 
			data = request.json()
		
		else:
			raise ValueError('Request is not ok, verify key', request.content)


		# Iterate through the items and print the "name"
		item = data['items'][0]

		if item['name'] == itemname:
			emote_id = item['id'] 
			markdown= f'<:{itemname}:{emote_id}>'
			return markdown


	def postdiscordemote(self, filepath, itemname):

		binary_fc       = open(filepath, 'rb').read()  # fc aka file_content
		base64_utf8_str = b64encode(binary_fc).decode('utf-8')

		ext     = filepath.split('.')[-1]
		dataurl = f'data:image/{ext};base64,{base64_utf8_str}'

		data = {
			'name': itemname,
			'image': dataurl
		}
		response = requests.post(self.applicationurl, headers=self.headers, json=data)

		print(response.text)



class Emotes(commands.Cog):
	functions = EmoteFunctions()


	@commands.hybrid_command(name='get_emoji')
	async def _get(self, ctx, itemname: str):
		markdown = self.functions.getemote(itemname)
		await ctx.send(f'The Emoji: {markdown}') 
          

	@commands.hybrid_command(name='create_emoji')
	async def _create(self, ctx, itemname: str):
		self.functions.getjpg(itemname)
		jpg = f'Emoji_Images/{itemname}.jpg'
		f_itemname = postde(jpg, itemname, k)
		markdown = gete(f_itemname, k)
		os.remove(jpg)
		await ctx.send(f'The Emoji: {markdown}')


async def setup(bot: commands.Bot):
   await bot.add_cog(Emotes(bot))
