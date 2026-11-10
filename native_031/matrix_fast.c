#include <stdint.h>
#include <stddef.h>

/*
 * Export function when compiling on Windows.
 */
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

/*
 * Standard matrix multiplication.
 *
 * A: Input matrix A (row-major)
 * B: Input matrix B (row-major)
 * C: Output matrix (row-major)
 *
 * Dimensions:
 * A = rows_a x cols_a
 * B = cols_a x cols_b
 * C = rows_a x cols_b
 *
 * Returns:
 *  0  -> Success
 * -1  -> Invalid pointers
 */

EXPORT int matrix_multiply(
    const int64_t *A,
    const int64_t *B,
    int64_t *C,
    size_t rows_a,
    size_t cols_a,
    size_t cols_b
) {
    if (rows_a == 0 || cols_a == 0 || cols_b == 0) {
        return 0;
    }

    if (A == NULL || B == NULL || C == NULL) {
        return -1;
    }

    for (size_t i = 0; i < rows_a; i++) {
        for (size_t j = 0; j < cols_b; j++) {

            int64_t sum = 0;

            for (size_t k = 0; k < cols_a; k++) {

                sum += A[i * cols_a + k]
                     * B[k * cols_b + j];

            }

            C[i * cols_b + j] = sum;
        }
    }

    return 0;
}
