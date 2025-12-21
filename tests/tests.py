import pytest

from utils import is_palindrome, fibonacci, count_vowels, calculate_discount, flatten_list, word_frequencies


@pytest.mark.parametrize("text, expected", [("Kobyła ma mały bok", True), ("kajak", True), ("python", False), ("", True), ("A", True)])
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (10, 55), (19, 4181)])
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected


@pytest.mark.parametrize("text, expected", [("Ala ma kota", 5), ("bcdfgh", 0), ("AEIOUY", 6), ("Sky", 1)])
def test_count_vowels(text, expected):
    assert count_vowels(text) == expected


@pytest.mark.parametrize("price, discount, expected", [(100, 0.2, 80.0), (100, 0.0, 100.0), (100, 1.0, 0.0), (50, 0.5, 25.0)])
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize("invalid_discount", [-0.1, 1.1, 5.0])
def test_calculate_discount_value_error(invalid_discount):
    with pytest.raises(ValueError):
        calculate_discount(100, invalid_discount)


@pytest.mark.parametrize("nested, expected", [([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]), ([], []), ([1, 2, 3], [1, 2, 3]), ([[1]], [1]), ([[], [1], [[2]]], [1, 2])])
def test_flatten_list(nested, expected):
    assert flatten_list(nested) == expected


def test_word_frequencies():
    text = "Ala ma kota, a kot ma Alę!"
    expected = {"ala": 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "alę": 1}
    assert word_frequencies(text) == expected


def test_word_frequencies_empty():
    assert word_frequencies("") == {}


def test_word_frequencies_punctuation():
    text = "Word... word! WORD?"
    expected = {"word": 3}
    assert word_frequencies(text) == expected
