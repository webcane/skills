def reverse_bits(n: int) -> int:
    res = 0
    for _ in range(32):          # ровно 32, иначе теряются ведущие нули
        res = (res << 1) | (n & 1)
        n >>= 1
    return res
