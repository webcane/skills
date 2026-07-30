def rob(nums: list[int]) -> int:
    prev = cur = 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur
