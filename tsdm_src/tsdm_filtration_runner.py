"""Reusable runner for TSDm filtration — wraps `tsdm_keep_diverse` and persists
a counter-report JSON plus a kept-files list under a caller-provided output dir.
"""

import os
from pathlib import Path

from keep_diverse.counter_report import CounterReport
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.stop import DontStop

from .tsdm_keep_diverse import tsdm_keep_diverse
from .cutoff import cutoff_kneedle
from .tsdm_plot import NoOutputTsdmPlot


def list_file_paths(directory: Path) -> list[str]:
    return sorted(
        str(directory / name)
        for name in os.listdir(directory)
        if (directory / name).is_file()
    )


def run_tsdm_filtration(
    directory: Path,
    output_dir: Path,
    tag: str,
    filter_rounds: int,
    split_by: int = 50,
    processes_count: int = 1,
    knee_plot=None,
    stop=None,
    cutoff_fn=cutoff_kneedle,
) -> Path:
    """Run TSDm on every file in `directory`. Write `{tag}.json` (counter
    report) and `{tag}_kept.txt` (files above the knee) under `output_dir`.
    Return the counter-report path.
    """
    counter_report_path = output_dir / f"{tag}.json"
    kept_files_path = output_dir / f"{tag}_kept.txt"

    filter_args = {
        "split_by": split_by,
        "filter_rounds": filter_rounds,
        "processes_count": processes_count,
    }

    tsdm_keep_diverse(
        file_paths=list_file_paths(directory),
        filter_rounds=filter_rounds,
        split_by=split_by,
        knee_plot=knee_plot if knee_plot is not None else NoOutputTsdmPlot(),
        filtered_files_list=FilteredFilesList(kept_files_path=str(kept_files_path)),
        counter_report=CounterReport(
            counter_report_path=str(counter_report_path),
            filter_args=filter_args,
        ),
        stop=stop if stop is not None else DontStop(),
        cutoff_fn=cutoff_fn,
        processes_count=processes_count,
        start_round=0,
        initial_counter=None,
    )

    return counter_report_path
