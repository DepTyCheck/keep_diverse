from dataclasses import dataclass
import numpy as np
import textwrap
from scipy.stats import sem

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.cbook import boxplot_stats

from .save_plot_safely import save_plot_safely
from .knee import Knee


@dataclass
class DisplayKneeArgs:
    total_files_count: int
    split_by: int
    relative_eps: float
    max_tries: int
    min_indices_count: int
    filter_rounds: int | None

    def to_string(self) -> str:
        fr_prefix = (
            f"/{self.filter_rounds} rounds."
            if self.filter_rounds is not None
            else " rounds."
        )
        return f"{fr_prefix} Total files count: {self.total_files_count}. Split by: {self.split_by}. Relative eps: {self.relative_eps}. Max tries: {self.max_tries}. Min indices count: {self.min_indices_count}."


def knee_plot(ax, knee: Knee):
    ax.clear()
    ax.plot(
        knee.x_values,
        knee.y_values,
        "b-",
        linewidth=2,
        label="File's removal frequency",
    )

    pct = knee.value / len(knee.y_values) * 100

    ax.axvline(
        x=knee.value,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Knee point: {knee.value} ({pct:.1f}%)",
    )

    ax.set_xlabel("Files count")
    ax.set_ylabel("Times to remove")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def sems_plot(ax, sems_history: list[tuple[int, float]]):
    if len(sems_history) == 0:
        return
    ax.clear()
    rounds = [x for x, y in sems_history]
    sems = [y for x, y in sems_history]
    ax.plot(rounds, sems, "g-", linewidth=2)
    ax.set_xlabel("Round")
    ax.set_ylabel("SEM of knee point")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


def fill_between_plot(ax, knees_history: list[tuple[int, int]], files_count: int):
    if len(knees_history) == 0:
        return

    knees_values = [y for x, y in knees_history]
    rounds = [x for x, y in knees_history]

    knees_per_round: list[list[int]] = []

    files_len_05_pct = files_count * 0.03
    files_len_5_pct = files_count * 0.05

    for i in range(1, len(knees_values) + 1):
        knees_per_round.append(knees_values[0:i])

    means = []
    medians = []
    lower_whiskers = []
    q1_list = []
    q3_list = []
    upper_whiskers = []
    plus_05_pct = []
    minus_05_pct = []
    plus_5_pct = []
    minus_5_pct = []

    stats = boxplot_stats(knees_per_round)

    for i, stat in enumerate(stats):
        means.append(np.mean(knees_per_round[i]))
        medians.append(stat["med"])
        lower_whiskers.append(stat["whislo"])
        upper_whiskers.append(stat["whishi"])
        q1_list.append(stat["q1"])
        q3_list.append(stat["q3"])

        last_median = medians[-1]

        plus_05_pct.append(last_median + files_len_05_pct)
        minus_05_pct.append(last_median - files_len_05_pct)

        plus_5_pct.append(last_median + files_len_5_pct)
        minus_5_pct.append(last_median - files_len_5_pct)

    ax.clear()

    ax.plot(rounds, medians, "b-", linewidth=2, label="Median knee")
    ax.plot(rounds, lower_whiskers, "r-", linewidth=2, label="Q1-1.5IQR")
    ax.plot(rounds, upper_whiskers, "r-", linewidth=2, label="Q3+1.5IQR")
    ax.plot(rounds, q1_list, "g-", linewidth=2, label="Q1")
    ax.plot(rounds, q3_list, "g-", linewidth=2, label="Q3")
    ax.fill_between(
        rounds,
        plus_05_pct,
        minus_05_pct,
        color="b",
        alpha=0.4,
        label="+/- 3% of files",
    )
    ax.fill_between(
        rounds,
        plus_5_pct,
        minus_5_pct,
        color="b",
        alpha=0.2,
        label="+/- 5% of files",
    )

    ax.set_xlabel("Round")
    ax.set_ylabel("Knee point statistics")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()


class Plot:
    def __init__(self, output_file: str, display_knee_args: DisplayKneeArgs):
        self.output_file = output_file
        self.display_knee_args = display_knee_args
        self.knees_history: list[tuple[int, int]] = []
        self.sems_history: list[tuple[int, float]] = []

    def draw(
        self,
        knee: Knee,
        round_number: int,
        files_count: int,
    ):
        if knee.value < files_count - 1:
            self.knees_history.append((round_number, knee.value))

            knees_values = [v for r, v in self.knees_history]
            sem_value = sem(knees_values) if len(knees_values) > 1 else 0.0
            self.sems_history.append((round_number, sem_value))

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        plt.subplots_adjust(bottom=0.1)

        knee_plot(ax1, knee)
        ax2.set_axis_off()
        fill_between_plot(ax3, self.knees_history, files_count)
        sems_plot(ax4, self.sems_history)

        t = f"{round_number}" + self.display_knee_args.to_string()
        tt = textwrap.fill(t, width=70)
        fig.text(
            0.5,
            0.02,
            tt,
            ha="center",
            va="bottom",
            fontsize=8,
            style="italic",
        )

        plt.suptitle("Knee Detection Plot")
        save_plot_safely(fig, self.output_file)


class NoOutputKneePlot(Plot):
    def __init__(self):
        pass

    def draw(
        self,
        knee: Knee,
        round_number: int,
        files_count: int,
    ):
        pass
