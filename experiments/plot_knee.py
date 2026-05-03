"""
Draw a Knee plot from a counter report produced by keep_diverse.

For TSDm reports that include a `knees_history` field, render a 2-row
figure: the removal-frequency knee plot on top, and a stability panel
(median, Q1, Q3, whiskers, +/- 3% band) on the bottom. For reports
without `knees_history`, render the single-row knee plot only.

`render_knee_figure` is the pure rendering entry point — callers that
already hold the knee + history in memory (e.g. live per-round hooks)
should call it directly instead of round-tripping through JSON.

Usage:
    python -m experiments.plot_knee \
        --counter-report path/to/report.json \
        --output knee.svg
"""

import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from experiments.loaded_counter_report import LoadedCounterReport
from keep_diverse.knee import Knee
from keep_diverse.knee_plot import knee_plot, fill_between_plot
from keep_diverse.save_plot_safely import save_plot_safely


def render_knee_figure(
    knee: Knee,
    knees_history: list[int],
    files_count: int,
    output_path: str,
    title: str | None = None,
) -> None:
    """Render the knee figure to ``output_path``.

    Two stacked panels (top: knee curve, bottom: stability/quartile
    band) when ``knees_history`` is non-empty. Single panel when empty.
    ``title`` is set on the top axis if provided.
    """
    if knees_history:
        fig, (ax_top, ax_bot) = plt.subplots(
            2, 1, figsize=(10, 9), constrained_layout=True
        )
        knee_plot(ax_top, knee)
        history_pairs = list(enumerate(knees_history, start=1))
        fill_between_plot(
            ax_bot,
            history_pairs,
            files_count=files_count,
            include_5pct=False,
        )
    else:
        fig, ax_top = plt.subplots(figsize=(10, 5))
        knee_plot(ax_top, knee)

    if title is not None:
        ax_top.set_title(title, fontsize=9)

    if not knees_history:
        plt.tight_layout()
    save_plot_safely(fig, output_path)


def plot_knee_from_report(
    counter_report_path: str,
    output_path: str,
    title: str | None = None,
) -> None:
    report = LoadedCounterReport(counter_report_path)
    knee = Knee(Counter(report.data))

    if title is None:
        kept = len(knee.y_values) - knee.value
        title = (
            f"Knee plot — {Path(counter_report_path).name}\n"
            f"rounds: {report.rounds_completed}  |  "
            f"eps: {report.filter_args.get('relative_eps', 'n/a')}  |  "
            f"kept: {kept} / {len(knee.y_values)} "
            f"({100 - knee.value / len(knee.y_values) * 100:.1f}%)"
        )

    render_knee_figure(
        knee=knee,
        knees_history=report.knees_history,
        files_count=len(knee.y_values),
        output_path=output_path,
        title=title,
    )
    print(f"Knee plot saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Draw a Knee plot from a keep_diverse counter report."
    )
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
