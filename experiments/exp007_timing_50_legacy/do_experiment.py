"""Experiment 007 — wall-clock time for one legacy `keep_diverse` filtration
over two 50-file datasets (sv and otk), counterpart to tsdm `exp000_timing_50`.

Datasets:
- `data/`     -> `tests/data_50`                          (sv, ~2 KB/file)
- `data_otk/` -> `experiments/exp005_.../data/otk`        (otk, ~45 KB/file)

Runs one legacy `keep_diverse` filtration round per dataset and prints
`<tag> elapsed_seconds=<float>` for each, plus a final summary line so the
two timings can be compared directly.
"""

import logging
import shutil
import time
from pathlib import Path

from keep_diverse.logger import configure_logger
from experiments.filtration_runner import run_filtration

EXPERIMENT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = EXPERIMENT_DIR / "output"

DATASETS = [
    ("sv (tests/data_50)", EXPERIMENT_DIR / "data",     "sv"),
    ("otk (exp005)",       EXPERIMENT_DIR / "data_otk", "otk"),
]

FILTER_ROUNDS = 1
SPLIT_BY = 50
RELATIVE_EPS = 1e-5
MAX_TRIES = 10
MIN_INDICES_COUNT = 10


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    timings: dict[str, float] = {}

    for label, data_dir, tag in DATASETS:
        logging.info(f"Running dataset: {label}")
        start = time.perf_counter()
        run_filtration(
            directory=data_dir,
            eps=RELATIVE_EPS,
            output_dir=OUTPUT_DIR,
            tag=tag,
            filter_rounds=FILTER_ROUNDS,
            split_by=SPLIT_BY,
            max_tries=MAX_TRIES,
            min_indices_count=MIN_INDICES_COUNT,
        )
        elapsed = time.perf_counter() - start
        timings[label] = elapsed
        logging.info(f"{label} elapsed_seconds={elapsed:.3f}")
        print(f"{tag} elapsed_seconds={elapsed:.3f}")

    print()
    print("=== summary ===")
    for label, elapsed in timings.items():
        print(f"{label:<25} {elapsed:>8.3f}s")
