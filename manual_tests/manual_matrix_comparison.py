
from data_generation.matrix_generator import (
    generate_square_matrix_pair,
    generate_matrix_pair,
)

from algorithms.matrix import (
    standard_matrix_multiply,
    strassen_matrix_multiply,
)

sizes = [2, 4, 8, 16, 32, 64]

print("MATRIX MULTIPLICATION COMPARISON")
print("=" * 50)

# Test square matrices
for size in sizes:
    a, b = generate_square_matrix_pair(size, seed=42)

    standard_result = standard_matrix_multiply(a, b)
    strassen_result = strassen_matrix_multiply(a, b)

    assert standard_result == strassen_result, (
        f"Mismatch found for {size}x{size} matrices"
    )

    print(f"Size: {size:>2}x{size:<2} | Results MATCH")

# Test rectangular matrices
rectangular_cases = [
    (3, 5, 2),
    (5, 3, 7),
    (7, 9, 4),
]

print("\nRECTANGULAR MATRIX TESTS")

for rows, inner, cols in rectangular_cases:
    a, b = generate_matrix_pair(rows, inner, cols, seed=42)

    standard_result = standard_matrix_multiply(a, b)
    strassen_result = strassen_matrix_multiply(a, b)

    assert standard_result == strassen_result, (
        f"Mismatch for dimensions {rows}x{inner} and {inner}x{cols}"
    )

    print(f"{rows}x{inner} * {inner}x{cols} | Results MATCH")

print("\n" + "=" * 50)
print("ALL MATRIX MULTIPLICATION CHECKS PASSED!")
