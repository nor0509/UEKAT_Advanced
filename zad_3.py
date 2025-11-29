def is_even(x: int) -> bool:
    return True if x % 2 ==0 else False

is_even = is_even(4)

print ('Liczba parzysta' if is_even == True else 'Liczba nieparzysta')