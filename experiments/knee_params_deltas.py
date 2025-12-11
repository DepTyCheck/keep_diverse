import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
from kneed import KneeLocator
from loaded_counter_report import LoadedCounterReport


def analyze_knees(file_path: str, output_path: str):
    print(f"Loading report from {file_path}...")
    report = LoadedCounterReport(file_path)
    raw_values = report.sorted_values()

    # Calculate deltas (absolute difference between consecutive values)
    # Since values are sorted descending, raw_values[i] >= raw_values[i+1]
    # We want the magnitude of the drop.
    y_values = [raw_values[i] - raw_values[i + 1] for i in range(len(raw_values) - 1)]
    x_values = list(range(len(y_values)))

    x_values_raw = list(range(len(raw_values)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))

    # Plot 1: Raw Values
    ax1.plot(
        x_values_raw,
        raw_values,
        "black",
        linewidth=2,
        label="Values",
    )
    ax1.set_title(f"Knee detection parameters analysis (Raw Values)\nFile: {file_path}")
    ax1.set_xlabel("Files count")
    ax1.set_ylabel("Times to remove")
    # ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3)

    # Plot 2: Deltas
    ax2.plot(
        x_values,
        y_values,
        "black",
        linewidth=2,
        label="Deltas",
    )

    s_params = [0.5, 1.0, 10.0, 50.0]
    poly_degrees = [1, 2, 3, 3.5, 4, 5, 6]

    # Generate distinct colors
    colors = plt.cm.get_cmap(
        "hsv", len(s_params) * len(poly_degrees) + 1
    )  # plt.cm.jet(np.linspace(0, 1, len(s_params) * len(poly_degrees)))
    color_idx = 0

    print("Calculating knees...")
    knees_found = []  # List of tuple(knee_x, knee_y, label, color)

    for s in s_params:
        for degree in poly_degrees:
            kneedle = KneeLocator(
                x_values,
                y_values,
                S=s,
                curve="convex",  # Deltas usually look like a convex curve (L-shape)
                direction="decreasing",
                interp_method="polynomial",
                polynomial_degree=degree,
            )

            knee_x = kneedle.knee
            if knee_x is None:
                print(f"Knee not found for S={s}, Deg={degree}")
                continue
            label = f"S={s}, Deg={degree}, Knee={knee_x}"
            knees_found.append(
                {
                    "x": knee_x,
                    "label": label,
                    "color": colors(color_idx),
                }
            )

            color_idx += 1

    # Group by X to handle overlaps

    knees_by_x = defaultdict(list)
    for k in knees_found:
        knees_by_x[k["x"]].append(k)

    # Determine Y-axis step for stacking
    if not y_values:
        print("No data to plot")
        return

    y_min = min(y_values)
    y_max = max(y_values)
    y_range = y_max - y_min
    y_step = y_range * 0.03 if y_range > 0 else 1.0  # 3% of range step

    # Start stacking from slightly below min or at min
    y_start = y_min

    # for x, knees in knees_by_x.items():
    #     # Draw vertical line for the true X
    #     ax2.axvline(x=x, color="gray", linestyle="--", alpha=0.3)

    #     # Stack knees vertically
    #     current_y = y_start
    #     for knee in knees:
    #         ax2.scatter(
    #             x,
    #             current_y,
    #             color=knee["color"],
    #             s=100,
    #             label=knee["label"],
    #             zorder=5,
    #             edgecolors="white",  # Add edge to make them pop
    #             linewidth=1,
    #         )
    #         current_y += y_step

    ax2.set_title(f"Knee detection parameters analysis (Deltas)")
    ax2.set_xlabel("Files count")
    ax2.set_ylabel("Deltas")
    # ax2.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    file_path = sys.argv[1]
    output_path = sys.argv[2]
    analyze_knees(file_path, output_path)
