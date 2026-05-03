import argparse
import logging
import os
from collections import Counter

from keep_diverse.path_args import add_path_arguments
from keep_diverse.logger import configure_logger
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.counter_report import CounterReport, NoCounterReport
from keep_diverse.stop import Stop, DontStop

from tsdm_src.filter_args import add_tsdm_filter_args
from tsdm_src.tsdm_plot import TsdmPlot, NoOutputTsdmPlot
from tsdm_src.tsdm_keep_diverse import tsdm_keep_diverse


def main() -> None:
    configure_logger(
        format="%(asctime)s - %(relativeCreated)d ms - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="TSDm-based diverse files filter")
    add_path_arguments(parser)
    add_tsdm_filter_args(parser)
    args = parser.parse_args()

    file_paths = [
        os.path.join(args.dir, name)
        for name in os.listdir(args.dir)
        if os.path.isfile(os.path.join(args.dir, name))
    ]

    if args.max_files is not None:
        file_paths = file_paths[: args.max_files]

    filter_rounds = args.filter_rounds if args.filter_rounds is not None else 420

    start_round = 0
    initial_counter: Counter | None = None

    if args.resume is not None:
        resume_data = CounterReport.load(args.resume)
        start_round = resume_data["rounds_completed"]
        initial_counter = Counter(resume_data["counter"])
        logging.getLogger().info(
            f"Resuming from round {start_round} / {filter_rounds} using {args.resume}"
        )
        if start_round >= filter_rounds:
            logging.getLogger().warning(
                f"Resume report already has {start_round} rounds completed, "
                f"which meets or exceeds --filter-rounds={filter_rounds}. Nothing to do."
            )
            return

    min_ratio = 1.0 - args.cutoff_pct

    filter_args = {
        "split_by": args.split_by,
        "filter_rounds": filter_rounds,
        "stop_pct": args.stop_pct,
        "processes_count": args.processes_count,
        "cutoff_pct": args.cutoff_pct,
    }

    counter_report_path = args.counter_report
    if counter_report_path is None and args.resume is not None:
        counter_report_path = args.resume

    knee_plot = (
        NoOutputTsdmPlot()
        if args.filtration_plot is None
        else TsdmPlot(output_file=args.filtration_plot, min_ratio=min_ratio)
    )

    filtered_files_list = FilteredFilesList(kept_files_path=args.kept_files)

    counter_report = (
        NoCounterReport()
        if counter_report_path is None
        else CounterReport(
            counter_report_path=counter_report_path,
            filter_args=filter_args,
        )
    )

    stop = (
        Stop(
            files_count=len(file_paths),
            pct=args.stop_pct,
            min_rounds=args.stop_min_rounds,
        )
        if args.filter_rounds is None
        else DontStop()
    )

    tsdm_keep_diverse(
        file_paths=file_paths,
        filter_rounds=filter_rounds,
        split_by=args.split_by,
        knee_plot=knee_plot,
        filtered_files_list=filtered_files_list,
        counter_report=counter_report,
        processes_count=args.processes_count,
        stop=stop,
        start_round=start_round,
        initial_counter=initial_counter,
        min_ratio=min_ratio,
    )


if __name__ == "__main__":
    main()
