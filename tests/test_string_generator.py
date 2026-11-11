
import pytest

from data_generation.string_generator import (
    generate_random_string,
    generate_string_pair,
    generate_identical_string_pair,
    generate_no_common_string_pair
)


# ============================================================
# 1. RANDOM STRING TESTS
# ============================================================

def test_random_string_length():
    result = generate_random_string(20, seed=42)

    assert len(result) == 20


def test_random_string_alphabet():
    result = generate_random_string(
        100,
        alphabet="ABC",
        seed=42
    )

    assert all(char in "ABC" for char in result)


def test_random_string_reproducibility():
    a = generate_random_string(20, seed=42)
    b = generate_random_string(20, seed=42)

    assert a == b


def test_random_string_empty():
    assert generate_random_string(0) == ""


def test_random_string_negative_length():
    with pytest.raises(ValueError):
        generate_random_string(-1)


def test_random_string_invalid_length():
    with pytest.raises(TypeError):
        generate_random_string(2.5)


def test_random_string_empty_alphabet():
    with pytest.raises(ValueError):
        generate_random_string(10, alphabet="")


# ============================================================
# 2. RANDOM STRING PAIR TESTS
# ============================================================

def test_string_pair_lengths():
    a, b = generate_string_pair(50, seed=42)

    assert len(a) == 50
    assert len(b) == 50


def test_string_pair_reproducibility():
    a = generate_string_pair(20, seed=42)
    b = generate_string_pair(20, seed=42)

    assert a == b


def test_string_pair_custom_alphabet():
    a, b = generate_string_pair(
        100,
        alphabet="XYZ",
        seed=42
    )

    assert all(c in "XYZ" for c in a + b)


def test_string_pair_zero_length():
    assert generate_string_pair(0) == ("", "")


# ============================================================
# 3. IDENTICAL STRING PAIR TESTS
# ============================================================

def test_identical_strings():
    a, b = generate_identical_string_pair(
        20,
        seed=42
    )

    assert a == b


def test_identical_strings_length():
    a, b = generate_identical_string_pair(
        30,
        seed=42
    )

    assert len(a) == 30
    assert len(b) == 30


def test_identical_strings_reproducibility():
    a = generate_identical_string_pair(20, seed=42)
    b = generate_identical_string_pair(20, seed=42)

    assert a == b


# ============================================================
# 4. NO COMMON CHARACTER TESTS
# ============================================================

def test_no_common_characters():
    a, b = generate_no_common_string_pair(
        20,
        seed=42
    )

    assert set(a).isdisjoint(set(b))


def test_no_common_strings_length():
    a, b = generate_no_common_string_pair(
        15,
        seed=42
    )

    assert len(a) == 15
    assert len(b) == 15


def test_no_common_strings_reproducibility():
    a = generate_no_common_string_pair(20, seed=42)
    b = generate_no_common_string_pair(20, seed=42)

    assert a == b


# ============================================================
# 5. INPUT VALIDATION TESTS
# ============================================================

def test_no_common_negative_length():
    with pytest.raises(ValueError):
        generate_no_common_string_pair(-1)


def test_no_common_invalid_length():
    with pytest.raises(TypeError):
        generate_no_common_string_pair(2.5)


def test_identical_negative_length():
    with pytest.raises(ValueError):
        generate_identical_string_pair(-1)


# ============================================================
# 6. EMPTY INPUT TESTS
# ============================================================

def test_empty_identical_pair():
    assert generate_identical_string_pair(0) == ("", "")


def test_empty_no_common_pair():
    assert generate_no_common_string_pair(0) == ("", "")
