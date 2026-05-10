import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from keep_diverse.knee import Knee
from keep_diverse.knee_plot import knee_plot, fill_between_plot
from keep_diverse.save_plot_safely import save_plot_safely


class TsdmPlot:
    def __init__(self, output_file: str, total_rounds: int | None):
        self.output_file = output_file
        self.total_rounds = total_rounds

    def draw(
        self,
        knee: Knee,
        knees_history: list[int],
        round_idx: int,
        ncd1_curves: list[list[float]] | None = None,
    ) -> None:
        files_count = len(knee.y_values)
        kept = files_count - knee.value
        if self.total_rounds is None:
            title = f"Round {round_idx} — kept {kept} / {files_count}"
        else:
            title = f"Round {round_idx} / {self.total_rounds} — kept {kept} / {files_count}"

        fig, (ax_top, ax_bot) = plt.subplots(
            2, 1, figsize=(10, 9), constrained_layout=True
        )
        knee_plot(ax_top, knee)
        ax_top.set_title(title, fontsize=9)

        history_pairs = list(enumerate(knees_history, start=1))
        fill_between_plot(
            ax_bot,
            history_pairs,
            files_count=files_count,
            include_5pct=False,
        )

        save_plot_safely(fig, self.output_file)
        plt.close(fig)


class NoOutputTsdmPlot:
    def draw(
        self,
        knee: Knee,
        knees_history: list[int],
        round_idx: int,
        ncd1_curves: list[list[float]] | None = None,
    ) -> None:
        pass
