"""Experiment 003 (TSDm) — full filtration over every dataset in data/, run
with both cutoff strategies (kneedle and max-NCD1) for side-by-side comparison.

For each dataset directory under data/ and for each cutoff in CUTOFFS, runs one
TSDm filtration job (split_by 50, stability stop at pct=0.03, capped at
FILTER_ROUNDS), re-rendering the standard TsdmPlot after every round into
output/<dataset>/<cutoff>/knee.svg. After each run, (re)writes a cross-dataset
summary: output/summary.txt and a grouped bar chart
output/knee_points_summary.svg comparing the final knee cut points per
(dataset, cutoff).

WARNING: the full run is long — greedy per-chunk NCD1 over ~150 files, many
rounds, five datasets, two cutoffs. Likely many hours.

Run with:  python -m tsdm_experiments.exp003_very_big.do_experiment
"""

import logging
import shutil
import time
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from experiments.loaded_counter_report import LoadedCounterReport
from keep_diverse.knee import Knee
from keep_diverse.logger import configure_logger
from keep_diverse.stop import Stop
from tsdm_src.cutoff import cutoff_argmax, cutoff_kneedle
from tsdm_src.tsdm_filtration_runner import run_tsdm_filtration
from tsdm_src.tsdm_plot import TsdmPlot

EXPERIMENT_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_DIR / "data"
OUTPUT_DIR = EXPERIMENT_DIR / "output"

SPLIT_BY = 50
FILTER_ROUNDS = 200          # safety cap; Stop ends earlier when stable
STOP_PCT = 0.03
PROCESSES_COUNT = 1

CUTOFFS: list[tuple[str, Callable[[list[float]], int]]] = [
    ("kneedle", cutoff_kneedle),
    ("argmax", cutoff_argmax),
]


def discover_datasets(data_dir: Path) -> list[Path]:
    return sorted(p for p in data_dir.iterdir() if p.is_dir())


def write_summary(
    results: list[tuple[str, str, int, int, int]],
    output_dir: Path,
) -> None:
    with open(output_dir / "summary.txt", "w") as f:
        for ds_name, cutoff_name, knee_value, kept, total in results:
            f.write(
                f"{ds_name}\t{cutoff_name}\tknee={knee_value}\tkept={kept}/{total}\n"
            )
        f.write(f"# rows={len(results)}\n")

    by_ds: OrderedDict[str, dict[str, tuple[int, int, int]]] = OrderedDict()
    cutoff_order: list[str] = []
    for ds_name, cutoff_name, knee_value, kept, total in results:
        by_ds.setdefault(ds_name, {})[cutoff_name] = (knee_value, kept, total)
        if cutoff_name not in cutoff_order:
            cutoff_order.append(cutoff_name)

    dataset_names = list(by_ds.keys())
    n_cutoffs = len(cutoff_order)
    width = 0.8 / max(n_cutoffs, 1)

    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    for i, cutoff_name in enumerate(cutoff_order):
        heights: list[int] = []
        labels: list[str] = []
        for ds_name in dataset_names:
            entry = by_ds[ds_name].get(cutoff_name)
            if entry is None:
                heights.append(0)
                labels.append("")
            else:
                knee_value, kept, total = entry
                heights.append(knee_value)
                labels.append(f"kept {kept}/{total}")
        offsets = [
            x_idx + (i - (n_cutoffs - 1) / 2) * width
            for x_idx in range(len(dataset_names))
        ]
        bars = ax.bar(offsets, heights, width, label=cutoff_name)
        for bar, lbl in zip(bars, labels):
            if not lbl:
                continue
            ax.annotate(
                lbl,
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    ax.set_xticks(list(range(len(dataset_names))))
    ax.set_xticklabels(dataset_names)
    ax.tick_params(axis="x", labelrotation=30)
    ax.set_title("TSDm — final knee per dataset × cutoff")
    ax.set_ylabel("knee cut index (files removed)")
    ax.legend(title="cutoff")
    fig.savefig(output_dir / "knee_points_summary.svg")
    plt.close(fig)


if __name__ == "__main__":
    configure_logger(level=logging.INFO)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    datasets = discover_datasets(DATA_DIR)
    logging.info(f"Found {len(datasets)} datasets: {[d.name for d in datasets]}")
    logging.info(f"Cutoffs: {[name for name, _ in CUTOFFS]}")

    results: list[tuple[str, str, int, int, int]] = []
    start = time.perf_counter()

    for dataset_dir in datasets:
        name = dataset_dir.name
        files_count = sum(1 for p in dataset_dir.iterdir() if p.is_file())

        for cutoff_name, cutoff_fn in CUTOFFS:
            ds_out = OUTPUT_DIR / name / cutoff_name
            ds_out.mkdir(parents=True)

            stop = Stop(files_count=files_count, pct=STOP_PCT)
            knee_plot = TsdmPlot(
                output_file=str(ds_out / "knee.svg"), total_rounds=None
            )
            tag = f"{name}__{cutoff_name}"

            logging.info(
                f"=== {name} / cutoff={cutoff_name}: {files_count} files ==="
            )
            report_path = run_tsdm_filtration(
                directory=dataset_dir,
                output_dir=ds_out,
                tag=tag,
                filter_rounds=FILTER_ROUNDS,
                split_by=SPLIT_BY,
                processes_count=PROCESSES_COUNT,
                stop=stop,
                knee_plot=knee_plot,
                cutoff_fn=cutoff_fn,
            )

            report = LoadedCounterReport(str(report_path))
            knee = Knee(Counter(report.data))
            kept = files_count - knee.value
            results.append((name, cutoff_name, knee.value, kept, files_count))
            logging.info(
                f"=== {name} / cutoff={cutoff_name}: knee={knee.value}, "
                f"kept={kept}/{files_count} ==="
            )

            write_summary(results, OUTPUT_DIR)

    elapsed = time.perf_counter() - start
    logging.info(f"elapsed_seconds={elapsed:.3f}")
    print(f"elapsed_seconds={elapsed:.3f}")
