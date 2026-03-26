"""
Experiment 002: pct_per_eps — random vs similar_subjective.
"""

import logging
from pathlib import Path

from keep_diverse.logger import configure_logger
from experiments.pct_per_eps_runner import run_pct_per_eps_experiment

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
RANDOM_DIR = DATA_DIR / "random"
SIMILAR_SUBJECTIVE_DIR = DATA_DIR / "similar_subjective"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

EPS_VALUES = [1e-5, 5e-4, 1e-4, 5e-3, 1e-3, 5e-2, 1e-2, 5e-1, 1e-1]

FILTER_ROUNDS = 50
SPLIT_BY = 50
MAX_TRIES = 10
MIN_INDICES_COUNT = 5

if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    run_pct_per_eps_experiment(
        dataset1_dir=RANDOM_DIR,
        dataset2_dir=SIMILAR_SUBJECTIVE_DIR,
        dataset1_label="Random 50",
        dataset2_label="Similar Subjective 50",
        output_dir=OUTPUT_DIR,
        eps_values=EPS_VALUES,
        filter_rounds=FILTER_ROUNDS,
        split_by=SPLIT_BY,
        max_tries=MAX_TRIES,
        min_indices_count=MIN_INDICES_COUNT,
    )
