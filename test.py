from api import Skyblock, Fishing
from api.utils import json_readable

skyblock_data = Skyblock("L3Xtor").skyblock_data
fishing_data = Fishing(skyblock_data).trophies

print(json_readable(fishing_data))
