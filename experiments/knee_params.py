import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
from kneed import KneeLocator
from kneefinder import KneeFinder
from loaded_counter_report import LoadedCounterReport


def analyze_knees(file_path: str, output_path: str):
    print(f"Loading report from {file_path}...")
    report = LoadedCounterReport(file_path)
    y_values = report.sorted_values()
    x_values = list(range(len(y_values)))

    plt.figure(figsize=(12, 8))
    plt.plot(
        x_values,
        y_values,
        "black",
        linewidth=2,
        label="Times to remove",
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

    # for s in s_params:
    #     for degree in poly_degrees:
    #         kneedle = KneeLocator(
    #             x_values,
    #             y_values,
    #             S=s,
    #             curve="concave",
    #             direction="decreasing",
    #             interp_method="polynomial",
    #             polynomial_degree=degree,
    #         )

    #         knee_x = kneedle.knee
    #         if knee_x is None:
    #             print(f"Knee not found for S={s}, Deg={degree}")
    #             continue
    #         label = f"S={s}, Deg={degree}, Knee={knee_x} ({knee_x / len(y_values) * 100:.2f}%)"
    #         knees_found.append(
    #             {
    #                 "x": knee_x,
    #                 "label": label,
    #                 "color": colors(color_idx),
    #             }
    #         )

    #         color_idx += 1

    # Group by X to handle overlaps

    knees_by_x = defaultdict(list)
    for k in knees_found:
        knees_by_x[k["x"]].append(k)

    # Determine Y-axis step for stacking
    y_min = min(y_values)
    y_max = max(y_values)
    y_range = y_max - y_min
    y_step = y_range * 0.03  # 3% of range step

    # Start stacking from slightly below min or at min
    y_start = y_min

    kf = KneeFinder(x_values, y_values)

    knee_x, knee_y = kf.find_knee()
    # plt.scatter(knee_x, knee_y, color="red", s=100, label="Knee")
    plt.axvline(
        x=knee_x,
        color="blue",
        linestyle="--",
        label=f"Simple Knee = {knee_x} ({knee_x / len(y_values) * 100:.2f}%)",
    )
    # plt.scatter(
    #     knee_x,
    #     knee_y,
    #     color="red",
    #     s=100,
    #     label=f"Simple Knee = {knee_x} ({knee_x / len(y_values) * 100:.2f}%)",
    #     zorder=5,
    #     edgecolors="white",  # Add edge to make them pop
    #     linewidth=1,
    # )

    kneedle = KneeLocator(
        x_values,
        y_values,
        S=1,
        curve="concave",
        direction="decreasing",
        interp_method="polynomial",
        polynomial_degree=3,
    )
    adv_x_knee = kneedle.knee
    plt.axvline(
        x=adv_x_knee,
        color="red",
        linestyle="--",
        # alpha=0.3,
        label=f"Advanced Knee = {adv_x_knee} ({adv_x_knee / len(y_values) * 100:.2f}%)",
    )

    # for x, knees in knees_by_x.items():
    #     # Draw vertical line for the true X
    #     plt.axvline(x=x, color="gray", linestyle="--", alpha=0.3)

    #     # Stack knees vertically
    #     current_y = y_start
    #     for knee in knees:
    #         plt.scatter(
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

    plt.title(f"Knee Detection Parameters Analysis\nFile: {file_path}")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    file_path = sys.argv[1]
    output_path = sys.argv[2]
    analyze_knees(file_path, output_path)
