"""
Draw a Knee plot from a counter report produced by keep_diverse.

The plot shows the removal-frequency curve for all files (sorted descending)
and marks the knee point — the boundary between files that are removed and
files that are kept.

Usage:
    python -m experiments.plot_knee \
        --counter-report experiments/exp001_.../output/similar_eps_1e-3.json \
        --output knee.png

    # With an optional title:
    python -m experiments.plot_knee \
        --counter-report path/to/report.json \
        --output knee.svg \
        --title "Similar dataset, eps=1e-3"
"""

import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from experiments.loaded_counter_report import LoadedCounterReport
from keep_diverse.knee import Knee
from keep_diverse.knee_plot import knee_plot
from keep_diverse.save_plot_safely import save_plot_safely


def plot_knee_from_report(
    counter_report_path: str,
    output_path: str,
    title: str | None = None,
) -> None:
    report = LoadedCounterReport(counter_report_path)
    knee = Knee(Counter(report.data))

    fig, ax = plt.subplots(figsize=(10, 5))
    knee_plot(ax, knee)

    kept = len(knee.y_values) - knee.value
    default_title = (
        f"Knee plot — {Path(counter_report_path).name}\n"
        f"rounds: {report.rounds_completed}  |  "
        f"eps: {report.filter_args.get('relative_eps', 'n/a')}  |  "
        f"kept: {kept} / {len(knee.y_values)} ({100 - knee.value / len(knee.y_values) * 100:.1f}%)"
    )
    ax.set_title(title if title is not None else default_title, fontsize=9)

    plt.tight_layout()
    save_plot_safely(fig, output_path)
    print(f"Knee plot saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw a Knee plot from a keep_diverse counter report.")
    parser.add_argument(
        "--counter-report",
        type=str,
        required=True,
        metavar="PATH",
        help="Path to the counter report JSON file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        metavar="PATH",
        help="Output path for the plot (e.g. knee.png or knee.svg).",
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Optional plot title. Defaults to a summary built from the report metadata.",
    )
    args = parser.parse_args()

    plot_knee_from_report(
        counter_report_path=args.counter_report,
        output_path=args.output,
        title=args.title,
    )


if __name__ == "__main__":
    main()
