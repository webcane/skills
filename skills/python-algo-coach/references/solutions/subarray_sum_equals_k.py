from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    counts: dict[int, int] = defaultdict(int)
    counts[0] = 1                 # подмассивы, начинающиеся с индекса 0
    running = 0
    res = 0
    for x in nums:
        running += x
        res += counts.get(running - k, 0)
        counts[running] += 1
    return res
