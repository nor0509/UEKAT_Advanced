# lista skladana
def multiply_by_two(numbers):
    return [number * 2 for number in numbers]


# for
def multiply_by_two_2(numbers):
    for i in range(len(numbers)):
        numbers[i] = numbers[i] * 2
    return numbers


numbers = [5, 12, 4, 2.5, 3.3]
print(multiply_by_two(numbers))
print(multiply_by_two_2(numbers))
