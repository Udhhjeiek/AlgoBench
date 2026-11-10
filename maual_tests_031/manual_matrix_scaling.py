
from data_generation_031.matrix_generator import (
    generate_matrix,
    generate_square_matrix,
    generate_matrix_pair,
    generate_square_matrix_pair,
)

sizes = [10, 50, 100, 250]

print("MATRIX GENERATOR SCALING TEST")
print("=" * 45)

for size in sizes:
    # 1. Generate a rectangular matrix
    matrix = generate_matrix(size, size + 5, seed=42)
    assert len(matrix) == size
    assert all(len(row) == size + 5 for row in matrix)

    # 2. Check reproducibility
    matrix_again = generate_matrix(size, size + 5, seed=42)
    assert matrix == matrix_again

    # 3. Generate a square matrix
    square = generate_square_matrix(size, seed=42)
    assert len(square) == size
    assert all(len(row) == size for row in square)

    # 4. Generate compatible matrices for multiplication
    a, b = generate_matrix_pair(size, size, size, seed=42)
    assert len(a) == size
    assert len(b) == size
    assert len(a[0]) == len(b)

    # 5. Generate a square matrix pair
    x, y = generate_square_matrix_pair(size, seed=42)
    assert len(x) == size
    assert len(y) == size

    print(f"Size: {size:>3} | All checks PASSED")

print("=" * 45)
print("ALL MATRIX SCALING CHECKS PASSED!")
