def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last_seen:
            left = max(left, last_seen[c] + 1)   # max обязателен: "dvdf"
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best
