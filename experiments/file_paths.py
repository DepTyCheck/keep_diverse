import os
from pathlib import Path


def file_paths(limit: int = 100):
    print(Path(__file__).parent)
    test_dir = Path(__file__).parent.parent / "tests/data_50"

    file_paths = sorted([str(test_dir / name) for name in os.listdir(test_dir)])[:limit]

    return file_paths


def file_paths_with_idxs():
    return [(idx, path) for idx, path in enumerate(file_paths())]
