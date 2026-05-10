"""Experiment 002 (TSDm) — 150-file filtration with stability stop, knee plot.

Runs one TSDm filtration job over data_150/ (150 files), splitting by 50,
with stability-based early stop (Stop, pct=0.03) capped at FILTER_ROUNDS.
Re-renders the multi-panel knee figure after every round via LiveKneePlot.
"""

import logging
import shutil
import time
from pathlib import Path

from keep_diverse.logger import configure_logger
from keep_diverse.stop import Stop
from experiments.plot_knee import render_knee_figure
from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data" / "data_150"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

TAG = "data_150"
SPLIT_BY = 50
FILTER_ROUNDS = 200          # safety cap; Stop ends earlier when stable
STOP_PCT = 0.03
PROCESSES_COUNT = 1


class LiveKneePlot:
    """TsdmPlot-compatible hook that re-renders the multi-panel knee
    figure after each filtration round."""

    def __init__(self, output_path: Path):
        self.output_path = str(output_path)

    def draw(self, knee, knees_history, round_idx, ncd1_curves=None) -> None:
        files_count = len(knee.y_values)
        kept = files_count - knee.value
        title = (
            f"exp002 — round {round_idx}/{FILTER_ROUNDS}  |  "
            f"kept {kept}/{files_count}"
        )
        render_knee_figure(
            knee=knee,
            knees_history=knees_history,
            files_count=files_count,
            output_path=self.output_path,
            title=title,
        )


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    files_count = sum(1 for p in DATA_DIR.iterdir() if p.is_file())
    stop = Stop(files_count=files_count, pct=STOP_PCT)
    live_plot = LiveKneePlot(OUTPUT_DIR / "knee.svg")

    start = time.perf_counter()
    run_tsdm_filtration(
        directory=DATA_DIR,
        output_dir=OUTPUT_DIR,
        tag=TAG,
        filter_rounds=FILTER_ROUNDS,
        split_by=SPLIT_BY,
        processes_count=PROCESSES_COUNT,
        stop=stop,
        knee_plot=live_plot,
    )
    elapsed = time.perf_counter() - start

    logging.info(f"elapsed_seconds={elapsed:.3f}")
    print(f"elapsed_seconds={elapsed:.3f}")
