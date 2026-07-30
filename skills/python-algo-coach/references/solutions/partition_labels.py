def partition_labels(s: str) -> list[int]:
    last = {c: i for i, c in enumerate(s)}
    res: list[int] = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res
