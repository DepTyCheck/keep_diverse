import logging
import shutil
from pathlib import Path

from experiments.filtration_runner import run_filtration
from experiments.plot_pct_per_eps import plot_pct_per_eps


def run_pct_per_eps_experiment(
    dataset1_dir: Path,
    dataset2_dir: Path,
    dataset1_label: str,
    dataset2_label: str,
    output_dir: Path,
    eps_values: list[float],
    filter_rounds: int,
    split_by: int,
    max_tries: int,
    min_indices_count: int,
) -> None:
    logging.getLogger().setLevel(logging.INFO)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    dataset1_reports: list[str] = []
    dataset2_reports: list[str] = []
    plot_path = str(output_dir / "pct_per_eps.png")

    for eps in list(sorted(eps_values)):
        logging.info(f"Filtering {dataset1_label} with eps={eps:.0e}")
        report = run_filtration(dataset1_dir, eps, output_dir, dataset1_dir.name, filter_rounds, split_by, max_tries, min_indices_count)
        dataset1_reports.append(str(report))

        logging.info(f"Filtering {dataset2_label} with eps={eps:.0e}")
        report = run_filtration(dataset2_dir, eps, output_dir, dataset2_dir.name, filter_rounds, split_by, max_tries, min_indices_count)
        dataset2_reports.append(str(report))

        plot_pct_per_eps(
            dataset1_reports=dataset1_reports,
            dataset2_reports=dataset2_reports,
            output_path=plot_path,
            dataset1_label=dataset1_label,
            dataset2_label=dataset2_label,
        )
        logging.info(f"Plot updated -> {plot_path}")
