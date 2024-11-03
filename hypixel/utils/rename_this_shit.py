from ctypes import c_int, c_double, Structure, CDLL, c_char_p, create_string_buffer
from typing import Protocol

class SkillInfo(Structure):
	"""
		Structure to define te Skill level, current xp, xp required to reach the next level, to access these here is an example:-
		```
			playerInfo = lib.getPLayerSkillInfo(initial_xp : float)
		```

		To access Skill level, remaining xp and xp to reach next level, we can do this
		```
			skillLevel : int = playerInfo.skill_level
			current_xp : float = playerInfo.remaining_xp
			xp_to_reach_next_level : float = playerInfo.xp_required_to_level_up
		``` 
		
	"""
	_fields_ = [
		("skill_level", c_int),
		("remaining_xp", c_double),
		("xp_required_to_level_up", c_double)
		]
	
	skill_level: int
	remaining_xp: float
	xp_required_to_level_up: float

# Protocol defining that the function getPlayerSkillInfo exists
class SharedLibProtocol(Protocol):
	def getPlayerSkillInfo(self, skill_xp, skill_name) -> SkillInfo:
		...

lib: SharedLibProtocol = CDLL('hypixel/catacombs/skills.so')
lib.getPlayerSkillInfo.restype = SkillInfo
lib.getPlayerSkillInfo.argtypes = [c_double, c_char_p]

def getPlayerSkillLevel(skill_xp, skill_name: str):
	buffer = create_string_buffer(skill_name.encode('utf-08'), 15)
	playerInfo = lib.getPlayerSkillInfo(skill_xp, buffer)

	skillLevel : int = playerInfo.skill_level
	current_xp : float = playerInfo.remaining_xp
	xp_to_reach_next_level : float = playerInfo.xp_required_to_level_up

	return (skillLevel, float(f"{current_xp:.2f}"), float(f"{xp_to_reach_next_level:.2f}"))