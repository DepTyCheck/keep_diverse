"""
Experiment 000: pct_per_eps — random_50 vs equivalent_50 (Caesar cipher).

Run from project root:
    python -m experiments.exp000_pct_per_eps_random_vs_equivalent.do_experiment
"""

import logging
import shutil
from pathlib import Path

from keep_diverse.logger import configure_logger
from experiments.exp000_pct_per_eps_random_vs_equivalent.caesar_cipher import apply_caesar_to_dir
from experiments.pct_per_eps_runner import run_pct_per_eps_experiment

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
RANDOM_50_DIR = DATA_DIR / "random_50"
EQUIVALENT_50_DIR = DATA_DIR / "equivalent_50"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

EPS_VALUES = [1e-5, 5e-4, 1e-4, 5e-3, 1e-3, 5e-2, 1e-2, 5e-1, 1e-1]

FILTER_ROUNDS = 5
SPLIT_BY = 50
MAX_TRIES = 10
MIN_INDICES_COUNT = 5
CAESAR_SHIFT = 3

if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if EQUIVALENT_50_DIR.exists():
        shutil.rmtree(EQUIVALENT_50_DIR)
    EQUIVALENT_50_DIR.mkdir(parents=True)
    logging.info(f"Applying Caesar cipher (shift={CAESAR_SHIFT}): {RANDOM_50_DIR} -> {EQUIVALENT_50_DIR}")
    apply_caesar_to_dir(RANDOM_50_DIR, EQUIVALENT_50_DIR, shift=CAESAR_SHIFT)

    run_pct_per_eps_experiment(
        dataset1_dir=RANDOM_50_DIR,
        dataset2_dir=EQUIVALENT_50_DIR,
        dataset1_label="Random 50",
        dataset2_label="Equivalent 50 (Caesar)",
        output_dir=OUTPUT_DIR,
        eps_values=EPS_VALUES,
        filter_rounds=FILTER_ROUNDS,
        split_by=SPLIT_BY,
        max_tries=MAX_TRIES,
        min_indices_count=MIN_INDICES_COUNT,
    )
