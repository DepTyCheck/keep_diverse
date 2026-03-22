import argparse
import logging
import os
from collections import Counter

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

    filter_args = {
        "split_by": args.split_by,
        "relative_eps": args.relative_eps,
        "max_tries": args.max_tries_to_find_pct,
        "min_indices_count": args.min_indices_count,
        "filter_rounds": filter_rounds,
        "stop_pct": args.stop_pct,
        "processes_count": args.processes_count,
    }

    counter_report_path = args.counter_report
    if counter_report_path is None and args.resume is not None:
        counter_report_path = args.resume

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
                filter_rounds=filter_rounds,
            ),
        )
    )

    filtered_files_list = FilteredFilesList(
        kept_files_path=args.kept_files,
    )

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
        )
        if args.filter_rounds is None
        else DontStop()
    )

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
        start_round=start_round,
        initial_counter=initial_counter,
    )


if __name__ == "__main__":
    main()
