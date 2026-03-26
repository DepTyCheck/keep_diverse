"""
Plot percentage of kept files vs relative_eps for two datasets.

Each data point comes from one counter report. The eps value is read from
filter_args.relative_eps saved inside the report, and the kept-files
percentage is derived from the knee of the removal-count distribution.

Usage:
    python -m experiments.plot_pct_per_eps \
        --dataset1-reports r1.json r2.json r3.json \
        --dataset2-reports s1.json s2.json s3.json \
        --output pct_per_eps.png \
        [--dataset1-label "Dataset A"] \
        [--dataset2-label "Dataset B"]
"""

import argparse
import sys
from collections import Counter

import matplotlib.pyplot as plt

from experiments.loaded_counter_report import LoadedCounterReport
from keep_diverse.knee import Knee


def _pct_kept(report: LoadedCounterReport) -> float:
    counter = Counter(report.data)
    knee = Knee(counter)
    total = len(counter)
    kept = total - knee.value
    return kept / total * 100


def _load_points(report_paths: list[str]) -> list[tuple[float, float]]:
    """Return list of (eps, pct_kept) sorted by eps."""
    points = []
    for path in report_paths:
        report = LoadedCounterReport(path)
        eps = report.filter_args.get("relative_eps")
        if eps is None:
            print(
                f"Warning: {path} has no relative_eps in filter_args, skipping.",
                file=sys.stderr,
            )
            continue
        pct = _pct_kept(report)
        points.append((eps, pct))
    points.sort(key=lambda t: t[0])
    return points


def _plot_dataset(ax, points: list[tuple[float, float]], label: str) -> None:
    if not points:
        ax.set_title(f"{label}\n(no data)")
        return

    eps_values = [p[0] for p in points]
    pct_values = [p[1] for p in points]
    positions = list(range(len(points)))

    ax.plot(positions, pct_values, marker="o", linewidth=1.5, markersize=5)
    ax.set_xticks(positions)
    ax.set_xticklabels([f"{e:.0e}" for e in eps_values], rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("relative_eps")
    ax.set_ylabel("Files kept (%)")
    ax.set_title(label)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    for pos, (eps, pct) in zip(positions, points):
        ax.annotate(
            f"{pct:.1f}%",
            xy=(pos, pct),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
        )


def plot_pct_per_eps(
    dataset1_reports: list[str],
    dataset2_reports: list[str],
    output_path: str,
    dataset1_label: str = "Dataset 1",
    dataset2_label: str = "Dataset 2",
) -> None:
    points1 = _load_points(dataset1_reports)
    points2 = _load_points(dataset2_reports)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Kept files (%) by relative_eps", fontsize=13)

    _plot_dataset(ax1, points1, dataset1_label)
    _plot_dataset(ax2, points2, dataset2_label)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot percentage of kept files vs relative_eps for two datasets.")
    parser.add_argument(
        "--dataset1-reports",
        nargs="+",
        required=True,
        metavar="PATH",
        help="Counter report JSON files for dataset 1.",
    )
    parser.add_argument(
        "--dataset2-reports",
        nargs="+",
        required=True,
        metavar="PATH",
        help="Counter report JSON files for dataset 2.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        metavar="PATH",
        help="Output path for the plot (e.g. pct_per_eps.png).",
    )
    parser.add_argument(
        "--dataset1-label",
        type=str,
        default="Dataset 1",
        help="Display label for dataset 1 (default: 'Dataset 1').",
    )
    parser.add_argument(
        "--dataset2-label",
        type=str,
        default="Dataset 2",
        help="Display label for dataset 2 (default: 'Dataset 2').",
    )

    args = parser.parse_args()

    plot_pct_per_eps(
        dataset1_reports=args.dataset1_reports,
        dataset2_reports=args.dataset2_reports,
        output_path=args.output,
        dataset1_label=args.dataset1_label,
        dataset2_label=args.dataset2_label,
    )


if __name__ == "__main__":
    main()
