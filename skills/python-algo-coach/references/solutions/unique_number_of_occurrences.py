from collections import Counter


def unique_occurrences(arr: list[int]) -> bool:
    counts = list(Counter(arr).values())
    return len(set(counts)) == len(counts)
