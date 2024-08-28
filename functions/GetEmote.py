import requests
import json


itemname = "WARDEN_HELMET"

def getemote(itemname):
# Get Itemhash of the Skyblock item saved in variable itemname
 with open("Skyblock-Item-Emojis/v3/itemHash.json", "r") as f:
    data = json.load(f)
    itemhash = (data[itemname])

# Get emoji discord ID with  help of the itemhash
 with open("Skyblock-Item-Emojis/v3/emojis.json", "r") as f:
    data = json.load(f)
    emojiid = (data[itemhash]["normal"]["id"])
    
#download and save the emoji with its itemname 
 url = (f'https://cdn.discordapp.com/emojis/{emojiid}.png')
 data = requests.get(url).content 
 f = open(f'Emoji_Images/{itemname}.jpg','wb') 
 f.write(data) 
 f.close() 
 with open(f'Emoji_Images/{itemname}.jpg', 'rb') as pic:
  data = pic.read()

