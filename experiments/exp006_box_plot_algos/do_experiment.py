"""
Experiment 006: box plot of kept-files % — algos5x10 dataset.

Plot 1 (box_pct.png): For each eps, ITERATIONS_NUMBER runs are performed.
    Each box shows the spread of pct_kept across those iterations.

Plot 2 (eps_<val>/kept_counts.png, one per eps): For each eps, shows how many
    times (out of ITERATIONS_NUMBER) each file ended up in the "kept" set.
    Files are grouped by algorithm prefix; each box shows distribution across
    the 10 variants of that algorithm.

Output layout:
    output/
        box_pct.png
        eps_1e-5/
            algos5x10_iter0_eps_1e-5.json
            algos5x10_iter0_eps_1e-5_kept.txt
            ...
            kept_counts.png
        eps_5e-4/
            ...
"""

import logging
import shutil
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from keep_diverse.knee import Knee
from keep_diverse.logger import configure_logger
from experiments.filtration_runner import run_filtration
from experiments.loaded_counter_report import LoadedCounterReport
from experiments.plot_box_pct import plot_box_pct, pct_kept_from_report

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
ALGOS_DIR = DATA_DIR / "algos5x10"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

EPS_VALUES = [1e-5, 5e-4, 1e-4, 5e-3, 1e-3, 5e-2, 1e-2, 5e-1, 1e-1]

FILTER_ROUNDS = 50
ITERATIONS_NUMBER = 10
SPLIT_BY = 50
MAX_TRIES = 10
MIN_INDICES_COUNT = 5

DATASET_LABEL = "Algos5x10"


def kept_files_from_report(path: str) -> set[str]:
    """Return the set of file basenames that are in the 'kept' set (above knee)."""
    report = LoadedCounterReport(path)
    counter = Counter(report.data)
    knee = Knee(counter)
    return {Path(f).name for f in knee.good_files()}


def plot_kept_counts(
    kept_counts: dict[str, int],
    iterations: int,
    eps: float,
    output_path: str,
) -> None:
    """For a single eps, plot how many times each individual file was kept.

    X-axis: each file (sorted by name). Y-axis: integer count (0–iterations).
    """
    sorted_files = sorted(kept_counts.keys())
    counts = [kept_counts[f] for f in sorted_files]
    positions = list(range(1, len(sorted_files) + 1))

    fig, ax = plt.subplots(figsize=(max(8, len(sorted_files) * 0.5), 5))
    fig.suptitle(f"Times kept out of {iterations} iterations  (eps={eps:.0e})", fontsize=12)

    color = plt.cm.tab10.colors[2]
    ax.bar(positions, counts, color=color, alpha=0.7)

    ax.set_xticks(positions)
    ax.set_xticklabels(sorted_files, rotation=45, ha="right", fontsize=7)
    ax.set_xlabel("File")
    ax.set_ylabel(f"Times kept (out of {iterations})")
    ax.set_ylim(0, iterations + 0.5)
    ax.set_yticks(range(0, iterations + 1))
    ax.grid(True, axis="y", alpha=0.3)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}", file=sys.stderr)
    plt.close(fig)


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    all_filenames = sorted(p.name for p in ALGOS_DIR.iterdir() if p.is_file())

    plot1_path = str(OUTPUT_DIR / "box_pct.png")
    dataset_pcts: dict[str, dict[float, list[float]]] = {DATASET_LABEL: {}}

    for eps in sorted(EPS_VALUES):
        eps_label = f"{eps:.0e}".replace("-0", "-")
        eps_dir = OUTPUT_DIR / f"eps_{eps_label}"
        eps_dir.mkdir(parents=True, exist_ok=True)

        pcts: list[float] = []
        kept_counts: dict[str, int] = {f: 0 for f in all_filenames}

        for iteration in range(ITERATIONS_NUMBER):
            logging.info(f"eps={eps:.0e}  iteration {iteration + 1}/{ITERATIONS_NUMBER}")
            report = run_filtration(
                directory=ALGOS_DIR,
                eps=eps,
                output_dir=eps_dir,
                tag=f"algos5x10_iter{iteration}",
                filter_rounds=FILTER_ROUNDS,
                split_by=SPLIT_BY,
                max_tries=MAX_TRIES,
                min_indices_count=MIN_INDICES_COUNT,
            )
            pcts.append(pct_kept_from_report(str(report)))
            for fname in kept_files_from_report(str(report)):
                if fname in kept_counts:
                    kept_counts[fname] += 1

        dataset_pcts[DATASET_LABEL][eps] = pcts

        # Update Plot 1 after each eps so partial results are visible.
        plot_box_pct(datasets=dataset_pcts, output_path=plot1_path)
        logging.info(f"Plot 1 updated -> {plot1_path}")

        # Save Plot 2 for this eps.
        plot2_path = str(eps_dir / "kept_counts.png")
        plot_kept_counts(
            kept_counts=kept_counts,
            iterations=ITERATIONS_NUMBER,
            eps=eps,
            output_path=plot2_path,
        )
        logging.info(f"Plot 2 (eps={eps:.0e}) -> {plot2_path}")
