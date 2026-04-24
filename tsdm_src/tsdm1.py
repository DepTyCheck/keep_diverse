from concurrent.futures import as_completed

from keep_diverse.process_pool_utils import safe_thread_pool_executor

from .ncd1 import c_of_concat, ncd1


def _c_without(chunk_bytes: list[bytes], skip_idx: int) -> tuple[int, int]:
    parts = [b for i, b in enumerate(chunk_bytes) if i != skip_idx]
    return (skip_idx, c_of_concat(parts))


def _compute_c_without_all(
    chunk_bytes: list[bytes],
    alive_idxs: list[int],
    max_workers: int = 10,
) -> dict[int, int]:
    alive_bytes = [chunk_bytes[i] for i in alive_idxs]
    results: dict[int, int] = {}
    with safe_thread_pool_executor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_c_without, alive_bytes, local_idx)
            for local_idx in range(len(alive_bytes))
        ]
        for future in as_completed(futures):
            local_idx, value = future.result()
            global_idx = alive_idxs[local_idx]
            results[global_idx] = value
    return results


def tsdm1_sequence(
    chunk_bytes: list[bytes],
    singleton_lens: list[int],
) -> tuple[list[int], list[float]]:
    """Run TSDm1 greedy removal on a chunk.

    Returns (removal_order, ncd1_curve). removal_order is a list of
    original chunk indices in the order the greedy loop removed them.
    ncd1_curve[k] is NCD1 of the set Y_k (before the k-th removal).
    Both lists have length max(0, len(chunk_bytes) - 2).
    """
    n = len(chunk_bytes)
    if n < 3:
        return [], []

    alive_idxs = list(range(n))
    removal_order: list[int] = []
    ncd1_curve: list[float] = []

    while len(alive_idxs) > 2:
        alive_bytes = [chunk_bytes[i] for i in alive_idxs]
        c_full = c_of_concat(alive_bytes)
        min_c_single = min(singleton_lens[i] for i in alive_idxs)

        c_without = _compute_c_without_all(chunk_bytes, alive_idxs)
        max_residual_idx = max(alive_idxs, key=lambda i: (c_without[i], -i))
        max_residual_value = c_without[max_residual_idx]

        ncd1_curve.append(ncd1(c_full, min_c_single, max_residual_value))
        removal_order.append(max_residual_idx)
        alive_idxs.remove(max_residual_idx)

    return removal_order, ncd1_curve
