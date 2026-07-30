def sorted_squares(nums: list[int]) -> list[int]:
    n = len(nums)
    out = [0] * n
    left, right = 0, n - 1
    for pos in range(n - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            out[pos] = nums[left] ** 2
            left += 1
        else:
            out[pos] = nums[right] ** 2
            right -= 1
    return out
