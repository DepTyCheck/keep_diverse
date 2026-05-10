"""Experiment 001 (TSDm) — NCD1 curve: similar_subjective vs different_subjective.

One filtration round per dataset; all 50 files in one chunk so the greedy
sequence produces a single NCD1 curve.  Plots both curves on one figure,
with three cutoff markers (pct_drop, argmax, kneedle) per dataset.

Expected: similar files → lower NCD1, curve rises then peaks early (more
redundancy to remove); different files → higher NCD1, peak stays right
(set already diverse, little to remove).
"""

import logging
import shutil
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from keep_diverse.logger import configure_logger
from keep_diverse.save_plot_safely import save_plot_safely
from tsdm_src.cutoff import cutoff_pct_drop, cutoff_argmax, cutoff_kneedle
from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

CUTOFFS = [
    ("pct_drop", cutoff_pct_drop, "o"),
    ("argmax",   cutoff_argmax,   "^"),
    ("kneedle",  cutoff_kneedle,  "s"),
]

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

DATASETS = {
    "similar_subjective":   DATA_DIR / "similar_subjective",
    "different_subjective": DATA_DIR / "different_subjective",
}

FILTER_ROUNDS = 1
SPLIT_BY = 50
PROCESSES_COUNT = 1

COLORS = {"similar_subjective": "steelblue", "different_subjective": "darkorange"}


class RecordingTsdmPlot:
    def __init__(self):
        self.rounds: list[list[list[float]]] = []

    def draw(self, knee, knees_history, round_idx, ncd1_curves=None):
        if ncd1_curves is None:
            return
        self.rounds.append([list(c) for c in ncd1_curves])


def run_one_round(data_dir: Path, tag: str) -> list[float]:
    recorder = RecordingTsdmPlot()
    run_tsdm_filtration(
        directory=data_dir,
        output_dir=OUTPUT_DIR,
        tag=tag,
        filter_rounds=FILTER_ROUNDS,
        split_by=SPLIT_BY,
        processes_count=PROCESSES_COUNT,
        knee_plot=recorder,
    )
    return recorder.rounds[0][0] if recorder.rounds and recorder.rounds[0] else []


def plot_curves(curves: dict[str, list[float]], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))

    for label, curve in curves.items():
        if not curve:
            continue
        color = COLORS[label]
        n_start = len(curve) + 2
        x = list(range(n_start, 2, -1))

        ax.plot(x, curve, color=color, linewidth=1.8, label=label)
        for name, fn, marker in CUTOFFS:
            cut = fn(curve)
            ax.plot(
                x[cut],
                curve[cut],
                marker=marker,
                color=color,
                markersize=9,
                markeredgecolor="black",
                markeredgewidth=0.8,
                zorder=5,
                label=f"{label} — {name} @ {x[cut]} files",
            )

    ax.invert_xaxis()
    ax.set_xlabel("files remaining")
    ax.set_ylabel("NCD1")
    ax.set_title("NCD1 vs files remaining — similar vs different subjective datasets")
    ax.legend(loc="best", fontsize=9, ncol=2)
    fig.tight_layout()
    save_plot_safely(fig, str(output_path))
    plt.close(fig)


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    curves: dict[str, list[float]] = {}
    start = time.perf_counter()

    for label, data_dir in DATASETS.items():
        logging.info(f"Running: {label}")
        curves[label] = run_one_round(data_dir, label)

    elapsed = time.perf_counter() - start

    plot_path = OUTPUT_DIR / "ncd1_curves.svg"
    plot_curves(curves, plot_path)
    logging.info(f"Plot saved to {plot_path}")

    logging.info(f"elapsed_seconds={elapsed:.3f}")
    print(f"elapsed_seconds={elapsed:.3f}")
