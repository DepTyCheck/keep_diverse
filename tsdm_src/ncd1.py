import lzma


def c_of_concat(byte_strings: list[bytes]) -> int:
    if not byte_strings:
        return 0
    return len(lzma.compress(b"".join(byte_strings)))


def ncd1(c_full: int, min_c_single: int, max_c_without_i: int) -> float:
    if max_c_without_i <= 0:
        return 0.0
    return (c_full - min_c_single) / max_c_without_i
