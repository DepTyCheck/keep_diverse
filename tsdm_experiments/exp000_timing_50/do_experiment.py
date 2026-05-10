"""Experiment 000 — NCD1 curve comparison across three 50-file datasets.

One filtration round per dataset; all 50 files in one chunk so the greedy
sequence produces a single NCD1 curve per dataset.  Plots the three curves on
one figure: NCD1 (Y) vs files remaining (X), with three cutoff markers (pct_drop, argmax, kneedle) per dataset.
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
OUTPUT_DIR = EXPERIMENT_DIR / "output"

DATASETS = [
    ("otk (exp005)", EXPERIMENT_DIR / "data_otk", "otk"),
    ("sv (tests/data_50)", EXPERIMENT_DIR / "data", "sv"),
    ("algos5x10 (exp006)", EXPERIMENT_DIR / "data_algos", "algos"),
    ("sv duplicate", EXPERIMENT_DIR / "data_copy", "sv-dup"),
]

FILTER_ROUNDS = 1
SPLIT_BY = 50
PROCESSES_COUNT = 1

COLORS = ["steelblue", "darkorange", "seagreen", "crimson"]


class RecordingTsdmPlot:
    """Captures per-round NCD1 curves for post-run plotting."""

    def __init__(self):
        self.rounds: list[list[list[float]]] = []

    def draw(self, knee, knees_history, round_idx, ncd1_curves=None):
        if ncd1_curves is None:
            return
        self.rounds.append([list(c) for c in ncd1_curves])


def run_one_round(data_dir: Path, tag: str) -> list[float]:
    """Run one filtration round; return the single chunk's NCD1 curve."""
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
    # split_by=50 and 50 files → one chunk → one curve
    return recorder.rounds[0][0] if recorder.rounds and recorder.rounds[0] else []


def plot_curves(curves: dict[str, list[float]], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))

    for (label, curve), color in zip(curves.items(), COLORS):
        if not curve:
            continue
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
    ax.set_title("NCD1 vs files remaining — one greedy round per dataset")
    ax.legend(loc="best", fontsize=8, ncol=2)
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

    for label, data_dir, tag in DATASETS:
        logging.info(f"Running dataset: {label}")
        round_start = time.perf_counter()
        curves[label] = run_one_round(data_dir, tag)
        round_elapsed = time.perf_counter() - round_start
        logging.info(f"{label} elapsed_seconds={round_elapsed:.3f}")
        print(f"{label} elapsed_seconds={round_elapsed:.3f}")

    elapsed = time.perf_counter() - start

    plot_path = OUTPUT_DIR / "ncd1_curves.svg"
    plot_curves(curves, plot_path)
    logging.info(f"Plot saved to {plot_path}")

    logging.info(f"elapsed_seconds={elapsed:.3f}")
    print(f"elapsed_seconds={elapsed:.3f}")
