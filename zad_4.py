def only_second(numbers):
    for i in range(0, len(numbers), 2):
        print(numbers[i])

numbers = list(range(31,41))
print(numbers)
only_second(numbers)