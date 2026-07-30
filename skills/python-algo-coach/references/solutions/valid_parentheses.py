PAIRS = {")": "(", "]": "[", "}": "{"}


def valid_parentheses(s: str) -> bool:
    stack: list[str] = []
    for c in s:
        if c in PAIRS:
            if not stack or stack.pop() != PAIRS[c]:
                return False
        else:
            stack.append(c)
    return not stack
