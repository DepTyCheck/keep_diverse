from collections import Counter
import json


class CounterReport:
    def __init__(self, counter_report_path: str):
        self.counter_report_path = counter_report_path

    def save(self, counter: Counter):
        with open(self.counter_report_path, "w") as f:
            json.dump(dict(counter), f, indent=2)


class NoCounterReport(CounterReport):
    def __init__(self):
        pass

    def save(self, counter: Counter):
        pass
