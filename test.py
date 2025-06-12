from json import load


class SkyblockProfile:
    def __init__(self, profiles, index):
        self.data = profiles[index]  # Assume it's a list of profile dicts

    @property
    def fishing_data(self):
        return self.data.get("fishing", {})


class SkyblockData:
    def __init__(self, all_profiles):
        self.profiles = all_profiles

    def profile(self, index):
        return SkyblockProfile(self.profiles, index)


def get_skyblock_data():
    # Normally you'd fetch this from an API
    mock_profiles = [
        {"fishing": {"level": 12, "exp": 34500}},
        {"fishing": {"level": 17, "exp": 78900}},
    ]
    return SkyblockData(mock_profiles)


profiles = {}

with open("response.json") as file:
    profiles = load(file)

for profile in profiles.get("profiles", []):
    if profile.get("selected"):
        print(profile.get("profile_id"))
