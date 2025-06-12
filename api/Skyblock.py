import requests
from typing import Any, Dict, Optional, Literal
from logging import getLogger

from utils.settings import HYPIXEL_API_SECRET as API_KEY
from .utils.utils import minecraft_uuid
from .exceptions.exceptions import HypixelSuccessError, ExpiredAPIKey

logger = getLogger(__name__)

SelectedProfile = Literal[
    "Apple",
    "Banana",
    "Blueberry",
    "Coconut",
    "Cucumber",
    "Grapes",
    "Kiwi",
    "Lemon",
    "Lime",
    "Mango",
    "Orange",
    "Papaya",
    "Peach",
    "Pear",
    "Pineapple",
    "Pomegranate",
    "Raspberry",
    "Strawberry",
    "Tomato",
    "Watermelon",
    "Zucchini",
]


class Skyblock:
    _auth_header = {"API-Key": API_KEY}
    _base_url = "https://api.hypixel.net/v2/skyblock"

    def __init__(
        self,
        player_name: Optional[str] = None,
        uuid: Optional[str] = None,
        selected_profile: Optional[SelectedProfile] = None,
    ) -> None:
        #

        self.uuid = self._resolve_uuid(player_name, uuid)
        self.selected_profile = selected_profile
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self) -> Optional[str]:
        """Return profile ID based on selected_profile or default one."""
        profiles = self.skyblock_data

        if self.selected_profile:
            for profile in profiles.get("profiles", []):
                if (
                    profile.get("cute_name", "").lower()
                    == self.selected_profile.lower()
                ):
                    return profile.get("profile_id")
        else:
            for profile in profiles.get("profiles", []):
                if profile.get("selected"):
                    return profile.get("profile_id")
        raise ValueError("No matching profile found.")

    def _resolve_uuid(self, player_name: Optional[str], uuid: Optional[str]) -> str:
        """Ensure exactly one of player_name or uuid is provided, and return a resolved uuid."""
        if (player_name is None) == (uuid is None):  # XOR check
            raise ValueError(
                "Provide either 'uuid' or 'player_name', not both or none."
            )

        if player_name:
            return minecraft_uuid(player_name)

        return uuid  # type: ignore (we know at this point it's not None)

    @property
    def skyblock_data(self) -> Dict[str, Any]:
        """Fetch the Skyblock profiles data for the player."""
        url = f"{self._base_url}/profiles"
        response = requests.get(
            url, headers=self._auth_header, params={"uuid": self.uuid}
        )

        data: Dict[str, Any] = response.json()

        if not data["success"]:
            if response.status_code == 403:
                raise ExpiredAPIKey("API Key is either expired or invalid")

            raise HypixelSuccessError(
                f"Response was not successfull due to {data.get('cause')}"
            )

        return response.json().get("profiles", [])
