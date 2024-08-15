import requests
import base64

filepath = '/home/dcadmin/Documents/Skybot/Emoji_Images/img.jpg'

binary_fc       = open(filepath, 'rb').read()  # fc aka file_content
base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')

ext     = filepath.split('.')[-1]
dataurl = f'data:image/{ext};base64,{base64_utf8_str}'


url = 'https://discord.com/api/v10/applications/1264605196466651249/emojis'

data = {
    'name': 'test',
    'image': dataurl
}


headers = {'Authorization':'Bot TOKENHERE'}


response = requests.post(url, headers=headers, json=data)

print(response.text)

