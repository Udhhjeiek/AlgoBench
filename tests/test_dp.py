"""
test_dp.py

Unit tests for AlgoBench Dynamic Programming algorithms.

Tests:
1. LCS Memoization
2. LCS Tabulation
3. Knapsack Memoization
4. Knapsack Tabulation

Testing framework: pytest
"""

import pytest

from algorithms.dynamic_programming import (
    lcs_memoization,
    lcs_tabulation,
    knapsack_memoization,
    knapsack_tabulation
)


# ============================================================
# 1. LCS MEMOIZATION TESTS
# ============================================================

def test_lcs_memoization_basic():
    assert lcs_memoization("ABCDEF", "ACE") == 3


def test_lcs_memoization_identical_strings():
    assert lcs_memoization("HELLO", "HELLO") == 5


def test_lcs_memoization_empty_string():
    assert lcs_memoization("", "ABC") == 0


def test_lcs_memoization_no_common_characters():
    assert lcs_memoization("ABC", "XYZ") == 0


def test_lcs_memoization_classic_example():
    assert lcs_memoization("ABCDGH", "AEDFHR") == 3


# ============================================================
# 2. LCS TABULATION TESTS
# ============================================================

def test_lcs_tabulation_basic():
    assert lcs_tabulation("ABCDEF", "ACE") == 3


def test_lcs_tabulation_identical_strings():
    assert lcs_tabulation("HELLO", "HELLO") == 5


def test_lcs_tabulation_empty_string():
    assert lcs_tabulation("", "ABC") == 0


def test_lcs_tabulation_no_common_characters():
    assert lcs_tabulation("ABC", "XYZ") == 0


def test_lcs_tabulation_classic_example():
    assert lcs_tabulation("ABCDGH", "AEDFHR") == 3


# ============================================================
# 3. KNAPSACK MEMOIZATION TESTS
# ============================================================

def test_knapsack_memoization_basic():
    weights = [1, 3, 4, 5]
    values = [10, 40, 50, 70]
    capacity = 7

    assert knapsack_memoization(weights, values, capacity) == 90


def test_knapsack_memoization_empty_items():
    assert knapsack_memoization([], [], 10) == 0


def test_knapsack_memoization_zero_capacity():
    assert knapsack_memoization([1, 2], [10, 20], 0) == 0


def test_knapsack_memoization_single_item():
    assert knapsack_memoization([2], [50], 2) == 50


def test_knapsack_memoization_item_too_heavy():
    assert knapsack_memoization([5, 6], [50, 60], 3) == 0


# ============================================================
# 4. KNAPSACK TABULATION TESTS
# ============================================================

def test_knapsack_tabulation_basic():
    weights = [1, 3, 4, 5]
    values = [10, 40, 50, 70]
    capacity = 7

    assert knapsack_tabulation(weights, values, capacity) == 90


def test_knapsack_tabulation_empty_items():
    assert knapsack_tabulation([], [], 10) == 0


def test_knapsack_tabulation_zero_capacity():
    assert knapsack_tabulation([1, 2], [10, 20], 0) == 0


def test_knapsack_tabulation_single_item():
    assert knapsack_tabulation([2], [50], 2) == 50


def test_knapsack_tabulation_item_too_heavy():
    assert knapsack_tabulation([5, 6], [50, 60], 3) == 0


# ============================================================
# 5. INPUT VALIDATION TESTS
# ============================================================

@pytest.mark.parametrize(
    "algorithm",
    [knapsack_memoization, knapsack_tabulation]
)
def test_knapsack_mismatched_input_lengths(algorithm):
    with pytest.raises(ValueError):
        algorithm([1, 2], [10], 5)


@pytest.mark.parametrize(
    "algorithm",
    [knapsack_memoization, knapsack_tabulation]
)
def test_knapsack_negative_capacity(algorithm):
    with pytest.raises(ValueError):
        algorithm([1, 2], [10, 20], -1)


@pytest.mark.parametrize(
    "algorithm",
    [knapsack_memoization, knapsack_tabulation]
)
def test_knapsack_negative_weight(algorithm):
    with pytest.raises(ValueError):
        algorithm([-1, 2], [10, 20], 5)


# ============================================================
# 6. CONSISTENCY TESTS
# ============================================================

def test_lcs_implementations_agree():
    text1 = "PROGRAMMING"
    text2 = "ALGORITHM"

    assert (
        lcs_memoization(text1, text2)
        == lcs_tabulation(text1, text2)
    )


def test_knapsack_implementations_agree():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8

    assert (
        knapsack_memoization(weights, values, capacity)
        == knapsack_tabulation(weights, values, capacity)
    )
