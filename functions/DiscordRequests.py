import requests
from ..utils.settings import DISCORD_API_SECRET


def getemote(itemname, apikey = DISCORD_API_SECRET):
    applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')
    headers = {'Authorization':'Bot ' + apikey}
    request = requests.get(applicationurl, headers=headers)
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

print(getemote('End_Sword'))