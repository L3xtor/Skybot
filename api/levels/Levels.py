from ctypes import c_int, c_double, Structure, CDLL, c_char_p, create_string_buffer
from typing import Dict, Protocol
from os import path

SHARED_FILE_PATH = path.join(path.dirname(__file__), "levels.so")
JSON_PATH = path.abspath(path.join(path.dirname(__file__), "json", "levels.json"))


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
        ("xp_required_to_level_up", c_double),
    ]

    skill_level: int
    remaining_xp: float
    xp_required_to_level_up: float


# Protocol defining that the function getPlayerSkillInfo exists
class SharedLibProtocol(Protocol):
    def getPlayerSkillInfo(self, skill_xp, skill_name, json_path) -> SkillInfo: ...


lib: SharedLibProtocol = CDLL(SHARED_FILE_PATH)
lib.getPlayerSkillInfo.argtypes = [c_double, c_char_p, c_char_p]
lib.getPlayerSkillInfo.restype = SkillInfo


def getSkillLevel(skill_xp: float, is_catacombs=False) -> Dict[str, int | float]:
    skill_type = "Catacombs" if is_catacombs else "Skills"

    skill_buffer = create_string_buffer(skill_type.encode("utf-8"), 15)
    path_buffer = create_string_buffer(JSON_PATH.encode("utf-8"), 256)

    info = lib.getPlayerSkillInfo(skill_xp, skill_buffer, path_buffer)

    return {
        "level": info.skill_level,
        "leftover_xp": round(info.remaining_xp, 2),
        "xp_required_to_level_up": round(info.xp_required_to_level_up, 2),
    }
