import requests
import json


def getemote(itemname, apikey):
    applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')
    headers = {'Authorization':'Bot ' + apikey}
    request = requests.get(applicationurl, headers=headers)
    data = (request).json()


# Iterate through the items and print the "name"
    if data['items'][0]['name'] == itemname:
       emote_name = data['items'][0]['name']
       print('here')
       emote_id = emote_name['id'] 
       markdown= f'<:{itemname}:{emote_id}>'
       return markdown

   
 
    

    

