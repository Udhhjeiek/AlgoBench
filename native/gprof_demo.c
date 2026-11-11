/* native/gprof_demo.c - small C program used to demonstrate gprof.
 * Naive O(n^3) matrix multiplication split into several functions so that
 * gprof's flat profile and call graph show where the time goes.
 * Build by hand:  gcc -pg -O0 -o gprof_demo gprof_demo.c && ./gprof_demo && gprof gprof_demo gmon.out
 */
#include <stdio.h>
#include <stdlib.h>

#define N 400

static double A[N][N], B[N][N], C[N][N];

static void fill_matrix(double m[N][N], int seed) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            m[i][j] = (double)((i * 31 + j * 17 + seed) % 10);
}

static double dot_row_col(int i, int j) {
    double s = 0.0;
    for (int k = 0; k < N; k++)
        s += A[i][k] * B[k][j];
    return s;
}

static void multiply(void) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            C[i][j] = dot_row_col(i, j);
}

static double checksum(void) {
    double t = 0.0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            t += C[i][j];
    return t;
}

int main(void) {
    fill_matrix(A, 1);
    fill_matrix(B, 2);
    multiply();
    printf("checksum = %.1f\n", checksum());
    return 0;
}
