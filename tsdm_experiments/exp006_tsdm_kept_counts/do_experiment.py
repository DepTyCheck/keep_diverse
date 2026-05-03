"""Experiment 006 (TSDm) — per-file kept-counts across 10 TSDm iterations on
the algos5x10 dataset.

No eps sweep (TSDm has no eps). No plots. Prints a ranked table of
`{filename}\t{count}/{ITERATIONS_NUMBER}` lines to stdout and mirrors them to
`output/kept_counts.txt`. Per-iteration artifacts (counter report JSON +
kept-files list) are saved under `output/` by the runner.
"""

import logging
import shutil
from collections import Counter
from pathlib import Path

from keep_diverse.knee import Knee
from keep_diverse.logger import configure_logger
from experiments.loaded_counter_report import LoadedCounterReport
from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
ALGOS_DIR = DATA_DIR / "algos5x10"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

FILTER_ROUNDS = 50
ITERATIONS_NUMBER = 10
SPLIT_BY = 50
PROCESSES_COUNT = 1


def kept_files_from_report(path: str) -> set[str]:
    """Return the set of file basenames above the knee in a counter report."""
    report = LoadedCounterReport(path)
    counter = Counter(report.data)
    knee = Knee(counter)
    return {Path(f).name for f in knee.good_files()}


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    all_filenames = sorted(p.name for p in ALGOS_DIR.iterdir() if p.is_file())
    kept_counts: dict[str, int] = {f: 0 for f in all_filenames}

    for iteration in range(ITERATIONS_NUMBER):
        logging.info(f"iteration {iteration + 1}/{ITERATIONS_NUMBER}")
        report_path = run_tsdm_filtration(
            directory=ALGOS_DIR,
            output_dir=OUTPUT_DIR,
            tag=f"algos5x10_iter{iteration}",
            filter_rounds=FILTER_ROUNDS,
            split_by=SPLIT_BY,
            processes_count=PROCESSES_COUNT,
        )
        for fname in kept_files_from_report(str(report_path)):
            if fname in kept_counts:
                kept_counts[fname] += 1

    ranked = sorted(kept_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    lines = [f"{fname}\t{count}/{ITERATIONS_NUMBER}" for fname, count in ranked]

    for line in lines:
        print(line)
    print(f"# total_files={len(all_filenames)} iterations={ITERATIONS_NUMBER}")

    with open(OUTPUT_DIR / "kept_counts.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")
        f.write(f"# total_files={len(all_filenames)} iterations={ITERATIONS_NUMBER}\n")
