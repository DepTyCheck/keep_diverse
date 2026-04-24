from .tsdm1 import tsdm1_sequence
from .argmax_cutoff import argmax_cutoff


def run_chunk_round(
    global_idxs: list[int],
    chunk_bytes: list[bytes],
    singleton_lens: list[int],
) -> tuple[list[int], list[float]]:
    removal_order, ncd1_curve = tsdm1_sequence(
        chunk_bytes=chunk_bytes,
        singleton_lens=singleton_lens,
    )
    if not removal_order:
        return [], ncd1_curve

    cutoff = argmax_cutoff(ncd1_curve)
    local_idxs_to_remove = removal_order[:cutoff]
    removed_global_idxs = [global_idxs[local_i] for local_i in local_idxs_to_remove]
    return removed_global_idxs, ncd1_curve
