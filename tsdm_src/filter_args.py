import argparse


def add_tsdm_filter_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--split-by",
        type=int,
        default=50,
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
        "--stop-min-rounds",
        type=int,
        required=False,
        default=20,
        help=(
            "Minimum rounds before the stability stop can fire. Default: 20."
        ),
    )
    parser.add_argument(
        "--processes-count",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--cutoff-pct",
        type=float,
        default=0.02,
        help=(
            "Tolerated NCD1 drop at the chunk cutoff, as a fraction of the "
            "starting NCD1 (e.g. 0.02 = 2%%). Default: 0.02."
        ),
    )
