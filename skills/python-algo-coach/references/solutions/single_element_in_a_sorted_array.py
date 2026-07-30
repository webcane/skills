def single_non_duplicate(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        mid -= mid & 1          # выравниваем на чётный индекс
        if nums[mid] == nums[mid + 1]:
            left = mid + 2
        else:
            right = mid
    return nums[left]
