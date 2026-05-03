from matplotlib.cbook import boxplot_stats


class Stop:
    def __init__(
        self,
        files_count: int,
        pct: float,
        min_rounds: int = 20,
    ) -> None:
        self.eps = files_count * pct
        self.min_rounds = min_rounds

    def should_stop(self, knees_list: list[int]):
        if len(knees_list) < self.min_rounds:
            return False

        stat = boxplot_stats(knees_list)
        q1 = stat[0]["q1"]
        q3 = stat[0]["q3"]
        med = stat[0]["med"]

        print(f"q1: {q1}")
        print(f"q3: {q3}")
        print(f"med: {med}")
        print(f"eps: {self.eps}")

        # q1 and q3 are inside med +/- eps range

        if q1 + self.eps > med > q3 - self.eps:
            return True


class DontStop(Stop):
    def __init__(self) -> None:
        pass

    def should_stop(self, knees_list: list[int]):
        pass
