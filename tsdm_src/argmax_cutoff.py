def argmax_cutoff(ncd1_curve: list[float]) -> int:
    if not ncd1_curve:
        return 0
    best_k = 0
    best_value = ncd1_curve[0]
    for k in range(1, len(ncd1_curve)):
        if ncd1_curve[k] > best_value:
            best_value = ncd1_curve[k]
            best_k = k
    return best_k
