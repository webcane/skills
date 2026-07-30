def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    nxt: dict[int, int] = {}
    stack: list[int] = []
    for num in nums2:
        while stack and num > stack[-1]:
            nxt[stack.pop()] = num
        stack.append(num)
    return [nxt.get(x, -1) for x in nums1]
