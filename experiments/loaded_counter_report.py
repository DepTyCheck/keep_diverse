import json


class LoadedCounterReport:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self) -> dict:
        with open(self.file_path, "r") as f:
            content = f.read().strip()
            return json.loads(content)

    def sorted_values(self) -> list[int]:
        return list(sorted(self.data.values(), reverse=True))
