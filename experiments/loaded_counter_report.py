import json


class LoadedCounterReport:
    def __init__(self, file_path: str):
        self.file_path = file_path
        raw = self._load_raw()
        self.data: dict = raw["counter"]
        self.filter_args: dict = raw.get("filter_args", {})
        self.rounds_completed: int = raw.get("rounds_completed", 0)
        self.knees_history: list[int] = raw.get("knees_history", [])

    def _load_raw(self) -> dict:
        with open(self.file_path, "r") as f:
            content = f.read().strip()
            return json.loads(content)

    def sorted_values(self) -> list[int]:
        return list(sorted(self.data.values(), reverse=True))
