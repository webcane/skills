from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for word in strs:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())
