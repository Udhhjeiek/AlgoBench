
"""
matrix.py

Matrix multiplication algorithms for AlgoBench.

Implemented algorithms:
1. Standard Matrix Multiplication
2. Strassen's Matrix Multiplication

Both functions accept compatible rectangular matrices and
return the resulting matrix.

Strassen's implementation handles non-power-of-two dimensions
by padding matrices before multiplication and cropping the result.
"""

from typing import Sequence


# ============================================================
# 1. MATRIX VALIDATION
# ============================================================

def _validate_matrix(matrix, name):
    """
    Validate that the input is a rectangular matrix.

    Returns:
        tuple: (number of rows, number of columns)
    """

    if not isinstance(matrix, (list, tuple)):
        raise TypeError(f"{name} must be a list or tuple of rows.")

    if len(matrix) == 0:
        return 0, 0

    if not all(isinstance(row, (list, tuple)) for row in matrix):
        raise TypeError(f"Every row in {name} must be a list or tuple.")

    columns = len(matrix[0])

    if any(len(row) != columns for row in matrix):
        raise ValueError(f"{name} must be a rectangular matrix.")

    return len(matrix), columns


def _validate_inputs(A, B):
    """
    Validate two matrices before multiplication.

    The number of columns in A must equal the number of rows in B.
    """

    rows_a, cols_a = _validate_matrix(A, "Matrix A")
    rows_b, cols_b = _validate_matrix(B, "Matrix B")

    if cols_a != rows_b:
        raise ValueError(
            "Matrix dimensions are incompatible for multiplication."
        )

    return rows_a, cols_a, cols_b


# ============================================================
# 2. STANDARD MATRIX MULTIPLICATION
# ============================================================

def standard_matrix_multiply(
    A: Sequence[Sequence[float]],
    B: Sequence[Sequence[float]]
) -> list[list[float]]:
    """
    Multiply two compatible matrices using the standard
    triple-loop matrix multiplication algorithm.

    Parameters:
        A: First matrix of dimensions (m x n).
        B: Second matrix of dimensions (n x p).

    Returns:
        list[list[float]]: Resulting matrix of dimensions (m x p).

    Time Complexity: O(m * n * p)
    Space Complexity: O(m * p) for the output matrix.

    For square matrices:
        Time Complexity: O(n^3)
    """

    rows_a, cols_a, cols_b = _validate_inputs(A, B)

    if rows_a == 0 or cols_b == 0:
        return []

    # Initialize the result matrix with zeros.
    result = [
        [0 for _ in range(cols_b)]
        for _ in range(rows_a)
    ]

    # Standard matrix multiplication.
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += A[i][k] * B[k][j]

    return result


# ============================================================
# 3. STRASSEN HELPER FUNCTIONS
# ============================================================

def _add_matrices(A, B):
    """Add two matrices of equal dimensions."""

    n = len(A)

    return [
        [A[i][j] + B[i][j] for j in range(n)]
        for i in range(n)
    ]


def _subtract_matrices(A, B):
    """Subtract matrix B from matrix A."""

    n = len(A)

    return [
        [A[i][j] - B[i][j] for j in range(n)]
        for i in range(n)
    ]


def _split_matrix(A):
    """
    Divide a square matrix into four equal submatrices.

    Returns:
        A11, A12, A21, A22
    """

    n = len(A)
    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    return A11, A12, A21, A22


def _combine_matrices(C11, C12, C21, C22):
    """Combine four submatrices into one square matrix."""

    top = [
        C11[i] + C12[i]
        for i in range(len(C11))
    ]

    bottom = [
        C21[i] + C22[i]
        for i in range(len(C21))
    ]

    return top + bottom


# ============================================================
# 4. STRASSEN RECURSIVE MULTIPLICATION
# ============================================================

def _strassen_recursive(A, B, threshold=32):
    """
    Internal recursive implementation of Strassen's algorithm.

    The standard algorithm is used for small submatrices to
    reduce recursion overhead.
    """

    n = len(A)

    # Base case: Use standard multiplication for small matrices.
    if n <= threshold:
        return standard_matrix_multiply(A, B)

    # Divide both matrices into four submatrices.
    A11, A12, A21, A22 = _split_matrix(A)
    B11, B12, B21, B22 = _split_matrix(B)

    # Calculate the seven Strassen products.
    M1 = _strassen_recursive(
        _add_matrices(A11, A22),
        _add_matrices(B11, B22),
        threshold
    )

    M2 = _strassen_recursive(
        _add_matrices(A21, A22),
        B11,
        threshold
    )

    M3 = _strassen_recursive(
        A11,
        _subtract_matrices(B12, B22),
        threshold
    )

    M4 = _strassen_recursive(
        A22,
        _subtract_matrices(B21, B11),
        threshold
    )

    M5 = _strassen_recursive(
        _add_matrices(A11, A12),
        B22,
        threshold
    )

    M6 = _strassen_recursive(
        _subtract_matrices(A21, A11),
        _add_matrices(B11, B12),
        threshold
    )

    M7 = _strassen_recursive(
        _subtract_matrices(A12, A22),
        _add_matrices(B21, B22),
        threshold
    )

    # Calculate the four result submatrices.
    C11 = _add_matrices(
        _subtract_matrices(
            _add_matrices(M1, M4), M5
        ),
        M7
    )

    C12 = _add_matrices(M3, M5)

    C21 = _add_matrices(M2, M4)

    C22 = _add_matrices(
        _add_matrices(
            _subtract_matrices(M1, M2), M3
        ),
        M6
    )

    # Combine the four result submatrices.
    return _combine_matrices(C11, C12, C21, C22)


# ============================================================
# 5. STRASSEN MATRIX MULTIPLICATION
# ============================================================

def strassen_matrix_multiply(
    A: Sequence[Sequence[float]],
    B: Sequence[Sequence[float]]
) -> list[list[float]]:
    """
    Multiply two compatible matrices using Strassen's algorithm.

    Supports rectangular matrices and dimensions that are not
    powers of two by padding the matrices before multiplication.

    Parameters:
        A: First matrix of dimensions (m x n).
        B: Second matrix of dimensions (n x p).

    Returns:
        list[list[float]]: Resulting matrix of dimensions (m x p).

    Time Complexity:
        O(n^2.807) for square matrices.

    Space Complexity:
        Additional memory is required for padding and recursion.
    """

    rows_a, cols_a, cols_b = _validate_inputs(A, B)

    if rows_a == 0 or cols_b == 0:
        return []

    # Determine the required square dimension.
    size = max(rows_a, cols_a, cols_b)

    # Find the next power of two.
    padded_size = 1

    while padded_size < size:
        padded_size *= 2

    # Create padded square matrices.
    padded_A = [
        [0] * padded_size
        for _ in range(padded_size)
    ]

    padded_B = [
        [0] * padded_size
        for _ in range(padded_size)
    ]

    # Copy original values into padded matrices.
    for i in range(rows_a):
        for j in range(cols_a):
            padded_A[i][j] = A[i][j]

    for i in range(cols_a):
        for j in range(cols_b):
            padded_B[i][j] = B[i][j]

    # Perform recursive Strassen multiplication.
    padded_result = _strassen_recursive(
        padded_A,
        padded_B
    )

    # Remove the extra padded rows and columns.
    result = [
        padded_result[i][:cols_b]
        for i in range(rows_a)
    ]

    return result
