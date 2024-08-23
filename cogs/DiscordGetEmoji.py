import requests

def gete(itemname, DISCORD_API_SECRET):

    applicationurl = ('https://discord.com/api/v10/applications/1264605196466651249/emojis')

    headers = {'Authorization':'Bot ' + DISCORD_API_SECRET}
    data = (requests.get(applicationurl, headers=headers)).json()
    
    for emote in data['items']:
        if emote['name'] == itemname:
            emoteid = (emote['id'])
            markdown = (f'<:{itemname}:{emoteid}>')
            print(markdown)
        break
    else:
        print ('not found')

