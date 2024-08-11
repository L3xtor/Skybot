import requests
import datetime
playername = 'xnuggeto'
PID = "01f09df7-62db-4a69-b799-287c5f38188a"

SkycryptProfileAPI = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{playername}').json()


selectedfloor = None

number = 196604
dt = datetime.datetime.fromtimestamp(number / 1000.0, tz=datetime.timezone.utc)
formattedtime=('%02d:%02d.%d'%(dt.minute,dt.second,dt.microsecond))[:-4]


print(formattedtime)

