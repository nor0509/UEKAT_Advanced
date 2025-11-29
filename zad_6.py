def list_append_and_more(x: list, y: list) -> list:
    unique = list(set(x + y))
    return [number**3 for number in unique]

x = list(range(10))
y = list(range(20))
print(x+y)
print(list_append_and_more(x, y))