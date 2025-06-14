from typing import Any, Dict
from concurrent.futures import ThreadPoolExecutor

trophy_tiers = ["diamond", "gold", "silver", "bronze", None]

# Define the suffix→tier-name mapping (empty suffix is "normal")
tier_suffixes = {
    "": "normal",
    "_bronze": "bronze",
    "_silver": "silver",
    "_gold": "gold",
    "_diamond": "diamond",
}


class Fishing:
    def __init__(self, skyblock_data: Dict[str, Any]):
        self._data = skyblock_data
        self._trophy_fishes: Dict[str, int] = skyblock_data.get("trophy_fish", {})

        # Remove unwanted data
        self._extra_data = {
            "last_caught": self._trophy_fishes.get("last_caught"),
            "rewards": self._trophy_fishes.get("rewards"),
            "total_caught": self._trophy_fishes.get("total_caught"),
        }

    def _get_highest_trophies(self) -> Dict[str, int]:
        # Checks if {} was assigned to trophy_fishes or not
        if not self._trophy_fishes:
            raise ValueError("User has no trophy fishes")

        all_keys = set(self._trophy_fishes)

        # Collect all base fish names
        base_names = set()
        for key in all_keys:
            parts = key.rsplit("_", 1)
            if parts[-1] in {"diamond", "gold", "silver", "bronze"}:
                base_names.add(parts[0])
            else:
                base_names.add(key)

        def _best(name):
            for tier in trophy_tiers:
                k = f"{name}_{tier}" if tier else name
                if k in all_keys:
                    return name, {"count": self._trophy_fishes[k], "rank": tier}
            return name, {"count": 0, "rank": None}

        highest = {}
        with ThreadPoolExecutor() as pool:
            for name, result in pool.map(_best, base_names):
                highest[name] = result

        highest.update(self._extra_data)
        return highest

    def _get_trophies(self) -> Dict[str, Dict[str, int]]:
        # collect every base fish name
        base_names = set()
        for key in self._trophy_fishes:
            for suffix in tier_suffixes:
                if key.endswith(suffix):
                    base_names.add(key[: len(key) - len(suffix)])
                    break

        # build result in one pass per base
        result = {}
        for name in base_names:
            # start with zeros for all tiers
            breakdown = {tier: 0 for tier in tier_suffixes.values()}
            # fill in whatever exists
            for suffix, tier in tier_suffixes.items():
                full_key = name + suffix
                if full_key in self._trophy_fishes:
                    breakdown[tier] = self._trophy_fishes[full_key]
            result[name] = breakdown

        result.update(self._extra_data)

        return result

    @property
    def highest_trophies(self):
        return self._get_highest_trophies()

    @property
    def trophies(self):
        return self._get_trophies()
