from kneefinder import KneeFinder


def cutoff_pct_drop(ncd1_curve: list[float], min_ratio: float = 0.98) -> int:
    """Largest k such that ncd1_curve[k] >= min_ratio * ncd1_curve[0].

    Greedy semantics: ncd1_curve[k] is NCD1 of the chunk after k removals
    (curve[0] = full chunk, no removals). Returned value is the number of
    files to remove from the chunk. ``min_ratio`` corresponds to a tolerated
    NCD1 drop of (1 - min_ratio); the default 0.98 tolerates a 2% drop.
    """
    if not ncd1_curve:
        return 0
    threshold = min_ratio * ncd1_curve[0]
    for k in range(len(ncd1_curve)):
        if ncd1_curve[k] < threshold:
            return max(0, k - 1)
    return len(ncd1_curve) - 1


def cutoff_argmax(ncd1_curve: list[float]) -> int:
    """Smallest k that attains max(ncd1_curve). Empty curve -> 0."""
    if not ncd1_curve:
        return 0
    best_k, best_v = 0, ncd1_curve[0]
    for k in range(1, len(ncd1_curve)):
        if ncd1_curve[k] > best_v:
            best_v = ncd1_curve[k]
            best_k = k
    return best_k


def cutoff_kneedle(ncd1_curve: list[float]) -> int:
    """Knee of the curve via kneefinder.KneeFinder.

    Curves shorter than 3 points (or pathological inputs that raise inside
    KneeFinder) -> 0. Mirrors the legacy keep_diverse/knee.py guard.
    """
    if len(ncd1_curve) < 3:
        return 0
    xs = list(range(len(ncd1_curve)))
    try:
        kf = KneeFinder(xs, list(ncd1_curve))
        knee_x, _ = kf.find_knee()
        return int(knee_x)
    except (IndexError, ValueError):
        return 0
