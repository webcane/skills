from collections import Counter


def find_anagrams(s: str, p: str) -> list[int]:
    k = len(p)
    if k > len(s):
        return []
    need = Counter(p)
    window = Counter(s[:k])
    res = [0] if window == need else []
    for i in range(k, len(s)):
        window[s[i]] += 1
        out = s[i - k]
        window[out] -= 1
        if window[out] == 0:
            del window[out]
        if window == need:
            res.append(i - k + 1)
    return res
