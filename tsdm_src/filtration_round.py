import random
from concurrent.futures import as_completed

import numpy as np

from keep_diverse.process_pool_utils import safe_process_pool_executor
from keep_diverse.logger import get_logger

from .chunk_round import run_chunk_round


def _split_list_by(elements: list, split_by: int) -> list[list]:
    return [elements[i : i + split_by] for i in range(0, len(elements), split_by)]


def _read_chunk_bytes(paths: list[str]) -> list[bytes]:
    contents = []
    for p in paths:
        with open(p, "rb") as f:
            contents.append(f.read())
    return contents


def _chunk_worker(
    global_idxs: list[int],
    chunk_paths: list[str],
    singleton_lens_for_chunk: list[int],
    min_ratio: float,
) -> tuple[list[int], list[float]]:
    chunk_bytes = _read_chunk_bytes(chunk_paths)
    return run_chunk_round(
        global_idxs=global_idxs,
        chunk_bytes=chunk_bytes,
        singleton_lens=singleton_lens_for_chunk,
        min_ratio=min_ratio,
    )


def filtration_round(
    file_paths: list[str],
    split_by: int,
    singleton_lens_file_path: str,
    processes_count: int,
    min_ratio: float = 0.98,
) -> tuple[list[str], list[list[float]]]:
    logger = get_logger()
    singleton_lens_arr = np.load(singleton_lens_file_path)

    indexed_paths = list(enumerate(file_paths))
    random.shuffle(indexed_paths)

    chunks = _split_list_by(indexed_paths, split_by)
    logger.info(f"Filtration round. {len(chunks)} chunks of up to {split_by} files.")

    removed_global_idxs_all: list[int] = []
    ncd1_curves_all: list[list[float]] = []

    with safe_process_pool_executor(max_workers=processes_count) as executor:
        futures = []
        for chunk in chunks:
            global_idxs = [g for g, _ in chunk]
            chunk_paths = [p for _, p in chunk]
            chunk_singleton_lens = [int(singleton_lens_arr[g]) for g in global_idxs]
            futures.append(
                executor.submit(
                    _chunk_worker,
                    global_idxs,
                    chunk_paths,
                    chunk_singleton_lens,
                    min_ratio,
                )
            )

        for future in as_completed(futures):
            removed_idxs, ncd1_curve = future.result()
            removed_global_idxs_all.extend(removed_idxs)
            ncd1_curves_all.append(ncd1_curve)

    removed_paths = [file_paths[i] for i in removed_global_idxs_all]
    return removed_paths, ncd1_curves_all
