KEYPAD = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []
    res: list[str] = []

    def backtrack(index: int, path: list[str]) -> None:
        if index == len(digits):
            res.append("".join(path))
            return
        for letter in KEYPAD[digits[index]]:
            path.append(letter)
            backtrack(index + 1, path)
            path.pop()

    backtrack(0, [])
    return res
