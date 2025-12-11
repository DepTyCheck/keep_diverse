import argparse


def add_filter_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--split-by",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--relative-eps",
        type=float,
        default=0.00001,
    )
    parser.add_argument(
        "--max-tries-to-find-pct",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--min-indices-count",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--filter-rounds",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--stop-pct",
        type=float,
        required=False,
        default=0.03,
    )
    parser.add_argument(
        "--processes-count",
        type=int,
        default=10,
    )
