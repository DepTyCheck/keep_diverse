"""
Shared helpers for experiment scripts that run keep_diverse filtration
over a directory and save a counter report.
"""

import os
from pathlib import Path

from keep_diverse.counter_report import CounterReport
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.keep_diverse import keep_diverse
from keep_diverse.knee_plot import NoOutputKneePlot
from keep_diverse.stop import DontStop


def list_file_paths(directory: Path) -> list[str]:
    return sorted(
        str(directory / name)
        for name in os.listdir(directory)
        if (directory / name).is_file()
    )


def run_filtration(
    directory: Path,
    eps: float,
    output_dir: Path,
    tag: str,
    filter_rounds: int,
    split_by: int,
    max_tries: int,
    min_indices_count: int,
) -> Path:
    """Filter all files in `directory` with the given `eps`, save a counter
    report to `output_dir`, and return its path."""
    eps_label = f"{eps:.0e}".replace("-0", "-")
    counter_report_path = output_dir / f"{tag}_eps_{eps_label}.json"
    kept_files_path = output_dir / f"{tag}_eps_{eps_label}_kept.txt"

    filter_args = {
        "split_by": split_by,
        "relative_eps": eps,
        "max_tries": max_tries,
        "min_indices_count": min_indices_count,
        "filter_rounds": filter_rounds,
    }

    keep_diverse(
        file_paths=list_file_paths(directory),
        filter_rounds=filter_rounds,
        split_by=split_by,
        relative_eps=eps,
        max_tries=max_tries,
        min_indices_count=min_indices_count,
        knee_plot=NoOutputKneePlot(),
        filtered_files_list=FilteredFilesList(kept_files_path=str(kept_files_path)),
        counter_report=CounterReport(
            counter_report_path=str(counter_report_path),
            filter_args=filter_args,
        ),
        stop=DontStop(),
    )

    return counter_report_path
