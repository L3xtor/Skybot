import requests
from base64 import b64encode
from ..utils.settings import DISCORD_API_SECRET

print(DISCORD_API_SECRET)

'''
filepath = '~/Skybot/Emoji_Images/img.jpg'

def postdiscordemote(filepath,itemname):
 applicationurl = 'https://discord.com/api/v10/applications/1264605196466651249/emojis'
 binary_fc       = open(filepath, 'rb').read()  # fc aka file_content
 base64_utf8_str = b64encode(binary_fc).decode('utf-8')

 ext     = filepath.split('.')[-1]
 dataurl = f'data:image/{ext};base64,{base64_utf8_str}'

 data = {
    'name': itemname,
    'image': dataurl
 }

 headers = {'Authorization':'Bot' + DISCORD_API_SECRET}
 response = requests.post(applicationurl, headers=headers, json=data)

 print(response.text)


applicationurl = 'https://discord.com/api/v10/applications/1264605196466651249/emojis'
headers = {'Authorization':'Bot' + DISCORD_API_SECRET}
response = requests.get(applicationurl, headers=headers)

print(response.text)
'''
