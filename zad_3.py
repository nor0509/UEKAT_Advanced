def only_even(numbers):
    print ([n for n in numbers if n % 2 == 0])

numbers = list(range(10,20, 1))
print(numbers)
only_even(numbers)