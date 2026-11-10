
"""
dynamic_programming.py

Dynamic Programming algorithms for AlgoBench.

Implemented algorithms:
1. Longest Common Subsequence (LCS) - Memoization
2. Longest Common Subsequence (LCS) - Tabulation
3. 0/1 Knapsack - Memoization
4. 0/1 Knapsack - Tabulation

All functions return their computed results instead of printing them,
making them suitable for benchmarking and integration.
"""

from functools import lru_cache
from typing import Sequence


# ============================================================
# 1. LONGEST COMMON SUBSEQUENCE - MEMOIZATION
# ============================================================

def lcs_memoization(text1: str, text2: str) -> int:
    """
    Calculate the length of the Longest Common Subsequence
    using a top-down recursive memoization approach.

    Parameters:
        text1 (str): First input string.
        text2 (str): Second input string.

    Returns:
        int: Length of the longest common subsequence.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n), including recursion stack.
    """

    m = len(text1)
    n = len(text2)

    @lru_cache(maxsize=None)
    def solve(i: int, j: int) -> int:

        # Base case: One string has been completely traversed.
        if i == m or j == n:
            return 0

        # Characters match: Include this character.
        if text1[i] == text2[j]:
            return 1 + solve(i + 1, j + 1)

        # Characters don't match: Try both possibilities.
        return max(
            solve(i + 1, j),
            solve(i, j + 1)
        )

    return solve(0, 0)


# ============================================================
# 2. LONGEST COMMON SUBSEQUENCE - TABULATION
# ============================================================

def lcs_tabulation(text1: str, text2: str) -> int:
    """
    Calculate the length of the Longest Common Subsequence
    using a bottom-up tabulation approach.

    Parameters:
        text1 (str): First input string.
        text2 (str): Second input string.

    Returns:
        int: Length of the longest common subsequence.

    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """

    m = len(text1)
    n = len(text2)

    # Create a DP table initialized with zeros.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the table from bottom to top.
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):

            if text1[i] == text2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]

            else:
                dp[i][j] = max(
                    dp[i + 1][j],
                    dp[i][j + 1]
                )

    return dp[0][0]


# ============================================================
# 3. 0/1 KNAPSACK - MEMOIZATION
# ============================================================

def knapsack_memoization(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int
) -> int:
    """
    Calculate the maximum value obtainable using the
    0/1 Knapsack problem with top-down memoization.

    Each item can either be selected once or not selected.

    Parameters:
        weights (Sequence[int]): Weights of the items.
        values (Sequence[int]): Values of the items.
        capacity (int): Maximum capacity of the knapsack.

    Returns:
        int: Maximum obtainable value.

    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity), including recursion stack.
    """

    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal lengths.")

    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    if any(weight < 0 for weight in weights):
        raise ValueError("Item weights cannot be negative.")

    n = len(weights)

    @lru_cache(maxsize=None)
    def solve(index: int, remaining_capacity: int) -> int:

        # No items left or no capacity remaining.
        if index == n or remaining_capacity == 0:
            return 0

        # Option 1: Do not select the current item.
        exclude = solve(index + 1, remaining_capacity)

        # Option 2: Select the current item if it fits.
        include = 0

        if weights[index] <= remaining_capacity:
            include = values[index] + solve(
                index + 1,
                remaining_capacity - weights[index]
            )

        return max(include, exclude)

    return solve(0, capacity)


# ============================================================
# 4. 0/1 KNAPSACK - TABULATION
# ============================================================

def knapsack_tabulation(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int
) -> int:
    """
    Calculate the maximum value obtainable using the
    0/1 Knapsack problem with bottom-up tabulation.

    Parameters:
        weights (Sequence[int]): Weights of the items.
        values (Sequence[int]): Values of the items.
        capacity (int): Maximum capacity of the knapsack.

    Returns:
        int: Maximum obtainable value.

    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    """

    if len(weights) != len(values):
        raise ValueError("Weights and values must have equal lengths.")

    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    if any(weight < 0 for weight in weights):
        raise ValueError("Item weights cannot be negative.")

    n = len(weights)

    # dp[i][w] = Maximum value using the first i items
    # with a knapsack capacity of w.
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):

        current_weight = weights[i - 1]
        current_value = values[i - 1]

        for w in range(capacity + 1):

            # Option 1: Exclude the current item.
            dp[i][w] = dp[i - 1][w]

            # Option 2: Include the current item if it fits.
            if current_weight <= w:
                dp[i][w] = max(
                    dp[i][w],
                    current_value + dp[i - 1][w - current_weight]
                )

    return dp[n][capacity]
