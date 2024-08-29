import requests
from base64 import b64encode



def postdiscordemote(filepath,itemname, apikey):
 applicationurl = (f'https://discord.com/api/v10/applications/1264605196466651249/emojis')

 binary_fc       = open(filepath, 'rb').read()  # fc aka file_content
 base64_utf8_str = b64encode(binary_fc).decode('utf-8')

 ext     = filepath.split('.')[-1]
 dataurl = f'data:image/{ext};base64,{base64_utf8_str}'

 data = {
    'name': itemname,
    'image': dataurl
 }

 headers = {'Authorization':'Bot ' + apikey}
 response = requests.post(applicationurl, headers=headers, json=data)

 print(response.text)
