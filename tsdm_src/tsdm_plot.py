import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from keep_diverse.knee import Knee
from keep_diverse.save_plot_safely import save_plot_safely

from .cutoff import cutoff_pct_drop


class TsdmPlot:
    def __init__(self, output_file: str, min_ratio: float = 0.98):
        self.output_file = output_file
        self.min_ratio = min_ratio

    def draw(
        self,
        knee: Knee,
        ncd1_curves: list[list[float]],
        round_idx: int,
        total_rounds: int,
    ) -> None:
        fig, axes = plt.subplots(2, 1, figsize=(10, 8))

        ax_top = axes[0]
        if knee.y_values:
            ax_top.plot(knee.x_values, knee.y_values, marker="o", markersize=2)
            ax_top.axvline(knee.value, color="red", linestyle="--", label=f"knee @ {knee.value}")
            ax_top.legend()
        ax_top.set_title(f"Round {round_idx} / {total_rounds} — removal counter (sorted desc)")
        ax_top.set_xlabel("file rank")
        ax_top.set_ylabel("times removed")

        ax_bot = axes[1]
        for ci, curve in enumerate(ncd1_curves):
            if not curve:
                continue
            ax_bot.plot(range(len(curve)), curve, alpha=0.4, label=f"chunk {ci}" if ci < 5 else None)
            cut = cutoff_pct_drop(curve, min_ratio=self.min_ratio)
            ax_bot.plot([cut], [curve[cut]], marker="o", color="red", markersize=3)
        ax_bot.set_title("NCD1(Y_k) curves per chunk (red dot = cutoff)")
        ax_bot.set_xlabel("removal step k")
        ax_bot.set_ylabel("NCD1")
        if any(ncd1_curves):
            ax_bot.legend(loc="best", fontsize=7)

        fig.tight_layout()
        save_plot_safely(fig, self.output_file)
        plt.close(fig)


class NoOutputTsdmPlot:
    def draw(
        self,
        knee: Knee,
        ncd1_curves: list[list[float]],
        round_idx: int,
        total_rounds: int,
    ) -> None:
        pass
