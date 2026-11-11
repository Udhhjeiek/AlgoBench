
"""
matrix_generator.py

Generates reproducible matrix datasets for
Standard and Strassen matrix multiplication.
"""

import random


# ============================================================
# 1. INPUT VALIDATION
# ============================================================

def _validate_dimensions(rows, cols):
    """Validate matrix dimensions."""

    if isinstance(rows, bool) or not isinstance(rows, int):
        raise TypeError("Rows must be an integer.")

    if isinstance(cols, bool) or not isinstance(cols, int):
        raise TypeError("Columns must be an integer.")

    if rows < 0 or cols < 0:
        raise ValueError("Matrix dimensions cannot be negative.")


def _validate_value_range(min_value, max_value):
    """Validate the range of generated matrix values."""

    if isinstance(min_value, bool) or not isinstance(min_value, int):
        raise TypeError("Minimum value must be an integer.")

    if isinstance(max_value, bool) or not isinstance(max_value, int):
        raise TypeError("Maximum value must be an integer.")

    if min_value > max_value:
        raise ValueError(
            "Minimum value cannot exceed maximum value."
        )


# ============================================================
# 2. GENERATE A RANDOM MATRIX
# ============================================================

def generate_matrix(
    rows,
    cols,
    min_value=0,
    max_value=100,
    seed=None
):
    """
    Generate a random matrix of specified dimensions.

    Args:
        rows: Number of rows.
        cols: Number of columns.
        min_value: Minimum possible element value.
        max_value: Maximum possible element value.
        seed: Optional random seed.

    Returns:
        A 2D list representing the generated matrix.
    """

    _validate_dimensions(rows, cols)
    _validate_value_range(min_value, max_value)

    rng = random.Random(seed)

    return [
        [
            rng.randint(min_value, max_value)
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]


# ============================================================
# 3. GENERATE A SQUARE MATRIX
# ============================================================

def generate_square_matrix(
    size,
    min_value=0,
    max_value=100,
    seed=None
):
    """
    Generate a square matrix of size x size.

    Useful for benchmarking Strassen multiplication.

    Args:
        size: Number of rows and columns.
        min_value: Minimum possible element value.
        max_value: Maximum possible element value.
        seed: Optional random seed.

    Returns:
        A square matrix as a 2D list.
    """

    _validate_dimensions(size, size)

    return generate_matrix(
        size,
        size,
        min_value,
        max_value,
        seed
    )


# ============================================================
# 4. GENERATE A COMPATIBLE MATRIX PAIR
# ============================================================

def generate_matrix_pair(
    rows,
    inner_dim,
    cols,
    min_value=0,
    max_value=100,
    seed=None
):
    """
    Generate two compatible matrices for multiplication.

    Matrix A has dimensions:
        rows x inner_dim

    Matrix B has dimensions:
        inner_dim x cols

    Resulting matrix has dimensions:
        rows x cols

    Args:
        rows: Number of rows in matrix A.
        inner_dim: Columns in A and rows in B.
        cols: Number of columns in matrix B.
        min_value: Minimum possible element value.
        max_value: Maximum possible element value.
        seed: Optional random seed.

    Returns:
        Tuple containing matrices A and B.
    """

    _validate_dimensions(rows, inner_dim)
    _validate_dimensions(inner_dim, cols)
    _validate_value_range(min_value, max_value)

    rng = random.Random(seed)

    matrix_a = [
        [
            rng.randint(min_value, max_value)
            for _ in range(inner_dim)
        ]
        for _ in range(rows)
    ]

    matrix_b = [
        [
            rng.randint(min_value, max_value)
            for _ in range(cols)
        ]
        for _ in range(inner_dim)
    ]

    return matrix_a, matrix_b


# ============================================================
# 5. GENERATE A SQUARE MATRIX PAIR
# ============================================================

def generate_square_matrix_pair(
    size,
    min_value=0,
    max_value=100,
    seed=None
):
    """
    Generate two compatible square matrices.

    Both matrices have dimensions size x size.

    Useful for comparing Standard and Strassen
    matrix multiplication on identical-sized inputs.
    """

    _validate_dimensions(size, size)

    return generate_matrix_pair(
        size,
        size,
        size,
        min_value,
        max_value,
        seed
    )
