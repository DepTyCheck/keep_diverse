"""
Experiment 005: box plot of kept-files % — otk (random dataset).

For each (dataset, eps) pair, filtration is run ITERATIONS_NUMBER times so
that each box on the plot shows the spread of pct_kept across those iterations.
"""

import logging
import shutil
from pathlib import Path

from keep_diverse.logger import configure_logger
from experiments.filtration_runner import run_filtration
from experiments.plot_box_pct import plot_box_pct, pct_kept_from_report

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
OTK_DIR = DATA_DIR / "otk"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

EPS_VALUES = [1e-5, 5e-4, 1e-4, 5e-3, 1e-3, 5e-2, 1e-2, 5e-1, 1e-1]

FILTER_ROUNDS = 50
ITERATIONS_NUMBER = 10
SPLIT_BY = 50
MAX_TRIES = 10
MIN_INDICES_COUNT = 5

DATASETS = [
    (OTK_DIR, "OTK"),
]

if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    plot_path = str(OUTPUT_DIR / "box_pct.png")
    # {label: {eps: [pct_kept_iter0, pct_kept_iter1, ...]}}
    dataset_pcts: dict[str, dict[float, list[float]]] = {label: {} for _, label in DATASETS}

    for eps in sorted(EPS_VALUES):
        for directory, label in DATASETS:
            pcts: list[float] = []
            for iteration in range(ITERATIONS_NUMBER):
                logging.info(f"Filtering {label} eps={eps:.0e} iteration {iteration + 1}/{ITERATIONS_NUMBER}")
                report = run_filtration(
                    directory=directory,
                    eps=eps,
                    output_dir=OUTPUT_DIR,
                    tag=f"{directory.name}_iter{iteration}",
                    filter_rounds=FILTER_ROUNDS,
                    split_by=SPLIT_BY,
                    max_tries=MAX_TRIES,
                    min_indices_count=MIN_INDICES_COUNT,
                )
                pcts.append(pct_kept_from_report(str(report)))
            dataset_pcts[label][eps] = pcts

        plot_box_pct(datasets=dataset_pcts, output_path=plot_path)
        logging.info(f"Plot updated -> {plot_path}")
