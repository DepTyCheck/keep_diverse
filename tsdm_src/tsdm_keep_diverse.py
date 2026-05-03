import os
import tempfile
from collections import Counter

import numpy as np

from keep_diverse.compressed_file_lens import compressed_file_lens_list
from keep_diverse.knee import Knee
from keep_diverse.logger import get_logger

from .filtration_round import filtration_round


def tsdm_keep_diverse(
    file_paths: list[str],
    filter_rounds: int,
    split_by: int,
    knee_plot,
    filtered_files_list,
    counter_report,
    stop,
    processes_count: int,
    start_round: int,
    initial_counter,
    min_ratio: float = 0.98,
) -> None:
    logger = get_logger()

    singleton_lens = compressed_file_lens_list(file_paths)
    singleton_lens_arr = np.array(singleton_lens, dtype=np.int64)

    singleton_lens_path = os.path.join(
        tempfile.gettempdir(), "tsdm_singleton_lens_cached.npy"
    )
    np.save(singleton_lens_path, singleton_lens_arr)
    logger.info(f"Saved {len(file_paths)} singleton lens to {singleton_lens_path}")

    if initial_counter is not None:
        removes_counter: Counter = Counter(initial_counter)
        for fp in file_paths:
            if fp not in removes_counter:
                removes_counter[fp] = 0
    else:
        removes_counter = Counter()
        for fp in file_paths:
            removes_counter[fp] = 0

    knees_list: list[int] = []
    finished_rounds = start_round
    rounds_to_run = filter_rounds - start_round
    logger.info(
        f"TSDm filtration. Rounds to run: {rounds_to_run} "
        f"(total: {filter_rounds}, start at: {start_round})"
    )

    for _ in range(rounds_to_run):
        removed_paths, ncd1_curves = filtration_round(
            file_paths=file_paths,
            split_by=split_by,
            singleton_lens_file_path=singleton_lens_path,
            processes_count=processes_count,
            min_ratio=min_ratio,
        )
        removes_counter.update(removed_paths)

        finished_rounds += 1

        knee = Knee(removes_counter)
        knees_list.append(knee.value)

        knee_plot.draw(knee, ncd1_curves, finished_rounds, filter_rounds)
        filtered_files_list.save(knee)
        counter_report.save(removes_counter, finished_rounds, knees_history=knees_list)

        logger.info(
            f"TSDm round {finished_rounds} / {filter_rounds} done. "
            f"Removed this round: {len(removed_paths)}. "
            f"Knee: {knee.value}."
        )

        if stop.should_stop(knees_list):
            logger.info("Early stop triggered.")
            break
