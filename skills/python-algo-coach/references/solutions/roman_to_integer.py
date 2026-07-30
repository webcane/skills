VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_integer(s: str) -> int:
    total = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and VALUES[c] < VALUES[s[i + 1]]:
            total -= VALUES[c]
        else:
            total += VALUES[c]
    return total
