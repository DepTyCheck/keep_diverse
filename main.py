import argparse
import logging
import os

from keep_diverse.filter_args import add_filter_args
from keep_diverse.path_args import add_path_arguments
from keep_diverse.knee_plot import Plot, NoOutputKneePlot, DisplayKneeArgs
from keep_diverse.filtered_files_list import FilteredFilesList
from keep_diverse.logger import configure_logger
from keep_diverse.keep_diverse import keep_diverse
from keep_diverse.counter_report import CounterReport, NoCounterReport
from keep_diverse.stop import Stop, DontStop


def main() -> None:
    configure_logger(
        format="%(asctime)s - %(relativeCreated)d ms - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="Texts filter utility")
    add_path_arguments(parser)
    add_filter_args(parser)
    args = parser.parse_args()

    file_paths = [
        os.path.join(args.dir, name)
        for name in os.listdir(args.dir)
        if os.path.isfile(os.path.join(args.dir, name))
    ]

    if args.max_files is not None:
        file_paths = file_paths[: args.max_files]

    knee_plot = (
        NoOutputKneePlot()
        if args.filtration_plot is None
        else Plot(
            output_file=args.filtration_plot,
            display_knee_args=DisplayKneeArgs(
                total_files_count=len(file_paths),
                split_by=args.split_by,
                relative_eps=args.relative_eps,
                max_tries=args.max_tries_to_find_pct,
                min_indices_count=args.min_indices_count,
                filter_rounds=args.filter_rounds,
            ),
        )
    )

    filtered_files_list = FilteredFilesList(
        kept_files_path=args.kept_files,
    )

    counter_report = (
        NoCounterReport()
        if args.counter_report is None
        else CounterReport(
            counter_report_path=args.counter_report,
        )
    )

    stop = (
        Stop(
            files_count=len(file_paths),
            pct=args.stop_pct,
        )
        if args.filter_rounds is None
        else DontStop()
    )

    filter_rounds = args.filter_rounds if args.filter_rounds is not None else 420

    keep_diverse(
        file_paths=file_paths,
        filter_rounds=filter_rounds,
        split_by=args.split_by,
        relative_eps=args.relative_eps,
        max_tries=args.max_tries_to_find_pct,
        min_indices_count=args.min_indices_count,
        knee_plot=knee_plot,
        filtered_files_list=filtered_files_list,
        counter_report=counter_report,
        processes_count=args.processes_count,
        stop=stop,
    )


if __name__ == "__main__":
    main()
