MASK = 0xFFFFFFFF
MAX_INT = 0x7FFFFFFF


def get_sum(a: int, b: int) -> int:
    a &= MASK
    b &= MASK
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    return a if a <= MAX_INT else ~(a ^ MASK)
