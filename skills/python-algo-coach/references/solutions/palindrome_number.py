def is_palindrome_number(x: int) -> bool:
    if x < 0:
        return False
    if x == 0:
        return True
    if x % 10 == 0:
        return False
    rev = 0
    while x > rev:                       # переворачиваем только половину
        rev = rev * 10 + x % 10
        x //= 10
    return x == rev or x == rev // 10    # вторая ветка — нечётная длина
