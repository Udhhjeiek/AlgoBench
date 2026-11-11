
import pytest

from data_generation.matrix_generator import (
    generate_matrix,
    generate_square_matrix,
    generate_matrix_pair,
    generate_square_matrix_pair
)


# ============================================================
# RANDOM MATRIX TESTS
# ============================================================

def test_generate_matrix_dimensions():
    matrix = generate_matrix(3, 4, seed=42)

    assert len(matrix) == 3
    assert all(len(row) == 4 for row in matrix)


def test_generate_matrix_value_range():
    matrix = generate_matrix(
        5, 5, min_value=10, max_value=20, seed=42
    )

    assert all(
        10 <= value <= 20
        for row in matrix
        for value in row
    )


def test_generate_matrix_reproducibility():
    assert generate_matrix(4, 4, seed=42) == generate_matrix(
        4, 4, seed=42
    )


def test_generate_matrix_empty():
    assert generate_matrix(0, 5) == []
    assert generate_matrix(5, 0) == [[], [], [], [], []]


def test_generate_matrix_negative_dimensions():
    with pytest.raises(ValueError):
        generate_matrix(-1, 5)


def test_generate_matrix_invalid_dimensions():
    with pytest.raises(TypeError):
        generate_matrix(2.5, 3)


def test_generate_matrix_invalid_value_range():
    with pytest.raises(ValueError):
        generate_matrix(2, 2, min_value=20, max_value=10)


# ============================================================
# SQUARE MATRIX TESTS
# ============================================================

def test_generate_square_matrix_dimensions():
    matrix = generate_square_matrix(5, seed=42)

    assert len(matrix) == 5
    assert all(len(row) == 5 for row in matrix)


def test_generate_square_matrix_reproducibility():
    assert generate_square_matrix(4, seed=10) == (
        generate_square_matrix(4, seed=10)
    )


def test_generate_square_matrix_zero_size():
    assert generate_square_matrix(0) == []


# ============================================================
# MATRIX PAIR TESTS
# ============================================================

def test_generate_matrix_pair_dimensions():
    A, B = generate_matrix_pair(2, 3, 4, seed=42)

    assert len(A) == 2
    assert all(len(row) == 3 for row in A)

    assert len(B) == 3
    assert all(len(row) == 4 for row in B)


def test_generate_matrix_pair_reproducibility():
    first = generate_matrix_pair(3, 4, 2, seed=42)
    second = generate_matrix_pair(3, 4, 2, seed=42)

    assert first == second


def test_generate_matrix_pair_empty_dimensions():
    A, B = generate_matrix_pair(0, 3, 2)

    assert A == []
    assert len(B) == 3
    assert all(len(row) == 2 for row in B)


# ============================================================
# SQUARE MATRIX PAIR TESTS
# ============================================================

def test_generate_square_matrix_pair_dimensions():
    A, B = generate_square_matrix_pair(4, seed=42)

    assert len(A) == 4
    assert len(B) == 4

    assert all(len(row) == 4 for row in A)
    assert all(len(row) == 4 for row in B)


def test_generate_square_matrix_pair_reproducibility():
    first = generate_square_matrix_pair(4, seed=100)
    second = generate_square_matrix_pair(4, seed=100)

    assert first == second


# ============================================================
# VALIDATION TESTS
# ============================================================

@pytest.mark.parametrize(
    "rows, cols",
    [
        (-1, 2),
        (2, -1),
        (-1, -1)
    ]
)
def test_matrix_negative_dimensions(rows, cols):
    with pytest.raises(ValueError):
        generate_matrix(rows, cols)


def test_matrix_pair_negative_dimensions():
    with pytest.raises(ValueError):
        generate_matrix_pair(-1, 2, 3)


def test_matrix_pair_invalid_value_range():
    with pytest.raises(ValueError):
        generate_matrix_pair(
            2, 2, 2,
            min_value=50,
            max_value=10
        )
