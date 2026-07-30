from collections import deque


def level_order(root) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):       # фиксируем размер уровня
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
