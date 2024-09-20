import requests
from typing import Tuple
from numerize import numerize

from utils.settings import HYPIXEL_API_SECRET as API_KEY

class HypixelAPIError(Exception):
    pass


# Returns dungeon info of player
def dungeonsInfo(playername: str, selected_profile: str = None) -> Tuple[int, int, int, dict]:

	_, selected_profile = returnProfileID(playername=playername)
	SkycryptDungeonsAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/dungeons/{playername}/{selected_profile}').json()

	dungeons = SkycryptDungeonsAPI['dungeons']

	if dungeons['catacombs']['visited'] is True :
		cataLevel = dungeons['catacombs']['level']['level'] 
		catacompletions = dungeons['floor_completions']
		secretsfound = numerize.numerize(dungeons['secrets_found'])
		secretsperrun = round(int(dungeons['secrets_found']) / int(catacompletions), 2)

	else:
		cataLevel, secretsfound, secretsperrun = 0, 0, 0

	return cataLevel, secretsfound, secretsperrun, dungeons

# Returns profile ID based on cute name of player
def returnProfileID(playername: str, selectedprofile: str = None):
    hypixelProfiles = miscellaneous_data(playername=playername)

    # Searching Each Profile
    if selectedprofile:
        for profile in hypixelProfiles:
            if profile['cute_name'] == selectedprofile.capitalize():
                return profile['profile_id'], selectedprofile # Returns PID

    else:
        for profile in hypixelProfiles:
            if profile['selected']:
                return profile['profile_id'], profile['cute_name'] # Returns PID and cute name of profile


# Returns Miscellaneous data like Hypixel profiles data
def miscellaneous_data(playername):
	mojangData = requests.get('https://api.mojang.com/users/profiles/minecraft/' + playername).json()
	UUID = mojangData['id']
	hypixelProfileData = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={UUID}').json()

	if hypixelProfileData['success']: return hypixelProfileData['profiles']
	else: raise HypixelAPIError("INVALID HYPIXEL API KEY. PLEASE RENEW")