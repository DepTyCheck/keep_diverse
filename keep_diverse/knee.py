from collections import Counter

from kneefinder import KneeFinder


class Knee:
    def __init__(self, counter: Counter):
        self.counter = counter
        sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        self.file_names, self.y_values = zip(*sorted_items)
        self.x_values = list(range(len(self.y_values)))

        kf = KneeFinder(self.x_values, self.y_values)
        knee_x, _ = kf.find_knee()
        self.value = int(knee_x)

    def good_files(self) -> list[str]:
        return self.file_names[self.value :]
