def is_in(numbers: list, x: int) -> bool:
    return True if x in numbers else False

numbers = list(range(40))

print(is_in(numbers, 41))