
"""
test_matrix.py

Unit tests for AlgoBench Matrix Algorithms.
"""

import pytest

from algorithms_031.matrix import (
    standard_matrix_multiply,
    strassen_matrix_multiply
)


# ============================================================
# 1. STANDARD MATRIX MULTIPLICATION
# ============================================================

def test_standard_basic():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    assert standard_matrix_multiply(A, B) == [
        [19, 22],
        [43, 50]
    ]


def test_standard_rectangular():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]

    assert standard_matrix_multiply(A, B) == [
        [58, 64],
        [139, 154]
    ]


def test_standard_identity():
    A = [[1, 2], [3, 4]]
    identity = [[1, 0], [0, 1]]

    assert standard_matrix_multiply(A, identity) == A


def test_standard_zero_matrix():
    A = [[1, 2], [3, 4]]
    B = [[0, 0], [0, 0]]

    assert standard_matrix_multiply(A, B) == [
        [0, 0],
        [0, 0]
    ]


def test_standard_single_element():
    assert standard_matrix_multiply([[5]], [[4]]) == [[20]]


# ============================================================
# 2. STRASSEN MATRIX MULTIPLICATION
# ============================================================

def test_strassen_basic():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    assert strassen_matrix_multiply(A, B) == [
        [19, 22],
        [43, 50]
    ]


def test_strassen_rectangular():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]

    assert strassen_matrix_multiply(A, B) == [
        [58, 64],
        [139, 154]
    ]


def test_strassen_non_power_of_two():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

    assert strassen_matrix_multiply(A, B) == [
        [30, 24, 18],
        [84, 69, 54],
        [138, 114, 90]
    ]


def test_strassen_single_element():
    assert strassen_matrix_multiply([[5]], [[4]]) == [[20]]


def test_strassen_identity():
    A = [[1, 2], [3, 4]]
    identity = [[1, 0], [0, 1]]

    assert strassen_matrix_multiply(A, identity) == A


# ============================================================
# 3. INPUT VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "algorithm",
    [standard_matrix_multiply, strassen_matrix_multiply]
)
def test_incompatible_dimensions(algorithm):
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[1, 2], [3, 4]]

    with pytest.raises(ValueError):
        algorithm(A, B)


@pytest.mark.parametrize(
    "algorithm",
    [standard_matrix_multiply, strassen_matrix_multiply]
)
def test_ragged_matrix(algorithm):
    A = [[1, 2], [3]]
    B = [[1], [2]]

    with pytest.raises(ValueError):
        algorithm(A, B)


@pytest.mark.parametrize(
    "algorithm",
    [standard_matrix_multiply, strassen_matrix_multiply]
)
def test_invalid_matrix_type(algorithm):
    with pytest.raises(TypeError):
        algorithm("invalid", [[1]])


# ============================================================
# 4. ALGORITHM CONSISTENCY
# ============================================================

def test_algorithms_produce_same_result():
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    B = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    assert (
        standard_matrix_multiply(A, B)
        == strassen_matrix_multiply(A, B)
    )


def test_recursive_strassen_64x64():
    A = [
        [i + j for j in range(64)]
        for i in range(64)
    ]

    B = [
        [i * j + 1 for j in range(64)]
        for i in range(64)
    ]

    assert (
        standard_matrix_multiply(A, B)
        == strassen_matrix_multiply(A, B)
    )


# ============================================================
# 5. EMPTY MATRICES
# ============================================================

@pytest.mark.parametrize(
    "algorithm",
    [standard_matrix_multiply, strassen_matrix_multiply]
)
def test_empty_matrices(algorithm):
    assert algorithm([], []) == []
