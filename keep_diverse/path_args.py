import argparse


def add_path_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--filtration-plot", type=str, required=False, default=None)
    parser.add_argument("--kept-files", type=str, required=True)
    parser.add_argument("--counter-report", type=str, required=False, default=None)
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--max-files", type=int, required=False, default=None)
