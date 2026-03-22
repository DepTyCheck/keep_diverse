from collections import Counter
import json


class CounterReport:
    def __init__(self, counter_report_path: str, filter_args: dict | None = None):
        self.counter_report_path = counter_report_path
        self.filter_args = filter_args if filter_args is not None else {}

    def save(self, counter: Counter, rounds_completed: int) -> None:
        data = {
            "filter_args": self.filter_args,
            "rounds_completed": rounds_completed,
            "counter": dict(counter),
        }
        with open(self.counter_report_path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(path: str) -> dict:
        with open(path) as f:
            data = json.load(f)
        return data


class NoCounterReport(CounterReport):
    def __init__(self):
        pass

    def save(self, counter: Counter, rounds_completed: int) -> None:
        pass
