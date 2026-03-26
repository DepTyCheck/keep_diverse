"""
Box plot of kept-files percentage for N datasets.

The figure has one subplot per dataset. Within each subplot the X-axis is
epsilon values and each box shows the distribution of pct_kept values across
multiple iterations at that epsilon.

Input structure expected by plot_box_pct():
    datasets: {label: {eps: [pct_kept_iter0, pct_kept_iter1, ...]}}
"""

import sys
from collections import Counter

import matplotlib.pyplot as plt

from experiments.loaded_counter_report import LoadedCounterReport
from keep_diverse.knee import Knee


def pct_kept_from_report(path: str) -> float:
    """Return the percentage of files kept (via knee) for a counter report."""
    report = LoadedCounterReport(path)
    counter = Counter(report.data)
    knee = Knee(counter)
    total = len(counter)
    kept = total - knee.value
    return kept / total * 100


def plot_box_pct(
    datasets: dict[str, dict[float, list[float]]],
    output_path: str,
) -> None:
    """
    Parameters
    ----------
    datasets : {label: {eps: [pct_kept, ...]}}
        Outer key  — dataset label (one subplot per label).
        Inner key  — epsilon value.
        Value      — list of pct_kept floats (one per iteration).
    output_path : str
        Where to save the PNG.
    """
    labels = list(datasets.keys())
    n = len(labels)

    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), sharey=True)
    if n == 1:
        axes = [axes]
    fig.suptitle("Kept files (%) by ε — distribution over iterations", fontsize=13)

    colors = plt.cm.tab10.colors

    for ax, label, color in zip(axes, labels, colors):
        eps_map = datasets[label]
        sorted_eps = sorted(eps_map.keys())

        if not sorted_eps:
            ax.set_title(f"{label}\n(no data)")
            continue

        data = [eps_map[e] for e in sorted_eps]
        positions = list(range(1, len(sorted_eps) + 1))

        bp = ax.boxplot(
            data,
            positions=positions,
            patch_artist=True,
            notch=False,
            widths=0.5,
        )
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
            patch.set_alpha(0.55)

        # Scatter individual points
        for pos, pcts in zip(positions, data):
            ax.scatter([pos] * len(pcts), pcts, alpha=0.7, zorder=3, s=18, color=color)

        ax.set_xticks(positions)
        ax.set_xticklabels(
            [f"{e:.0e}" for e in sorted_eps], rotation=45, ha="right", fontsize=8
        )
        ax.set_xlabel("relative_eps")
        ax.set_title(label)
        ax.set_ylim(0, 105)
        ax.grid(True, axis="y", alpha=0.3)

    axes[0].set_ylabel("Files kept (%)")

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}", file=sys.stderr)
