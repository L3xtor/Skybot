from ctypes import c_int, c_double, Structure, CDLL
from typing import Protocol

class SkillInfo(Structure):
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
	def getPlayerSkillInfo(self, skill_data) -> SkillInfo:
		...

lib: SharedLibProtocol = CDLL('hypixel/catacombs/skills.so')
lib.getPlayerSkillInfo.restype = SkillInfo
lib.getPlayerSkillInfo.argtypes = [c_double]

def getPlayerSkillLevel(skill_data):
	playerInfo = lib.getPlayerSkillInfo(skill_data)

	skillLevel : int = playerInfo.skill_level
	current_xp : float = playerInfo.remaining_xp
	xp_to_reach_next_level : float = playerInfo.xp_required_to_level_up

	return (skillLevel, current_xp, xp_to_reach_next_level)