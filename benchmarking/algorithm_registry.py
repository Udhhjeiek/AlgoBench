"""
AlgoBench algorithm registry and reproducible dataset factory.

The dashboard uses these helpers to register every submitted algorithm with
Member 041's generic BenchmarkEngine and to prepare compatible function inputs.
"""
from __future__ import annotations

import random
from typing import Any, Dict, Iterable, List, Tuple

from algorithms.sorting import quick_sort, merge_sort, heap_sort, insertion_sort
from algorithms.searching import linear_search, binary_search, hash_table_lookup
from algorithms.graph import dijkstra, bellman_ford, bfs
from algorithms.dynamic_programming import (
    lcs_memoization,
    lcs_tabulation,
    knapsack_memoization,
    knapsack_tabulation,
)
from algorithms.matrix import standard_matrix_multiply, strassen_matrix_multiply

from data_generation.graph_generator import generate_graph
from data_generation.matrix_generator import generate_square_matrix_pair
from data_generation.string_generator import generate_string_pair

from .benchmark_engine import BenchmarkEngine


ALGORITHM_OPTIONS: Dict[str, List[str]] = {
    "Sorting": ["Quick Sort", "Merge Sort", "Heap Sort", "Insertion Sort"],
    "Searching": ["Linear Search", "Binary Search", "Hash Table Lookup"],
    "Graph": ["Dijkstra", "Bellman-Ford", "BFS"],
    "Dynamic Programming": [
        "LCS - Memoization",
        "LCS - Tabulation",
        "Knapsack - Memoization",
        "Knapsack - Tabulation",
    ],
    "Matrix": ["Standard Multiplication", "Strassen Multiplication"],
}


def create_default_engine(results_dir: str = "results") -> BenchmarkEngine:
    """Create a fresh engine with all submitted algorithms registered."""
    engine = BenchmarkEngine(results_dir=results_dir)

    # The submitted sorting functions create their own result lists and do not
    # mutate their inputs. Read-only mode avoids an extra, excluded deepcopy.
    engine.register("Sorting", "Quick Sort", quick_sort, mutates_input=False)
    engine.register("Sorting", "Merge Sort", merge_sort, mutates_input=False)
    engine.register("Sorting", "Heap Sort", heap_sort, mutates_input=False)
    engine.register("Sorting", "Insertion Sort", insertion_sort, mutates_input=False,
                    max_size=5000)

    engine.register("Searching", "Linear Search", linear_search, mutates_input=False)
    engine.register("Searching", "Binary Search", binary_search, mutates_input=False)
    engine.register("Searching", "Hash Table Lookup", hash_table_lookup, mutates_input=False)

    engine.register("Graph", "Dijkstra", dijkstra, mutates_input=False)
    engine.register("Graph", "Bellman-Ford", bellman_ford, mutates_input=False)
    engine.register("Graph", "BFS", bfs, mutates_input=False)

    engine.register("Dynamic Programming", "LCS - Memoization",
                    lcs_memoization, mutates_input=False, max_size=150)
    engine.register("Dynamic Programming", "LCS - Tabulation",
                    lcs_tabulation, mutates_input=False, max_size=150)
    engine.register("Dynamic Programming", "Knapsack - Memoization",
                    knapsack_memoization, mutates_input=False, max_size=250)
    engine.register("Dynamic Programming", "Knapsack - Tabulation",
                    knapsack_tabulation, mutates_input=False, max_size=250)

    engine.register("Matrix", "Standard Multiplication",
                    standard_matrix_multiply, mutates_input=False, max_size=128)
    engine.register("Matrix", "Strassen Multiplication",
                    strassen_matrix_multiply, mutates_input=False, max_size=128)

    return engine


def recommended_input_sizes(
    category: str,
    algorithms: Iterable[str],
    input_type: str = "Random",
) -> List[int]:
    """Return practical sizes so deliberately slow algorithms remain usable."""
    algorithms = set(algorithms)

    if category == "Sorting":
        if "Insertion Sort" in algorithms:
            return [100, 250, 500, 1000, 2000, 5000]
        return [100, 500, 1000, 5000, 10000, 50000]

    if category == "Searching":
        return [100, 500, 1000, 5000, 10000, 50000]

    if category == "Graph":
        if input_type == "Dense" and "Bellman-Ford" in algorithms:
            return [10, 20, 30, 50, 75, 100]
        if input_type == "Dense":
            return [10, 20, 50, 100, 150, 200]
        return [10, 20, 50, 100, 200, 400]

    if category == "Dynamic Programming":
        has_lcs = any(name.startswith("LCS") for name in algorithms)
        has_knapsack = any(name.startswith("Knapsack") for name in algorithms)
        if has_lcs and has_knapsack:
            return [10, 20, 40, 60, 80, 100]
        if has_lcs:
            return [10, 20, 40, 60, 80, 100, 120, 150]
        return [10, 20, 40, 60, 80, 100, 150, 200, 250]

    if category == "Matrix":
        return [8, 16, 32, 48, 64, 96, 128]

    raise ValueError(f"Unsupported algorithm category: {category}")


def build_dataset(
    category: str,
    algorithm: str,
    size: int,
    input_type: str = "Random",
    seed: int = 42,
    search_mode: str = "Successful Search",
    binary_search_selected: bool = False,
) -> Tuple[Any, str, str]:
    """
    Build the exact call input expected by the selected algorithm.

    Returns:
        (data, recorded_input_type, notes)

    A tuple is intentional for multi-argument functions because BenchmarkEngine
    unpacks tuple inputs as positional arguments.
    """
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError("Dataset size must be a positive integer.")

    rng = random.Random(seed)

    if category == "Sorting":
        values = [rng.randint(0, max(10, size * 3)) for _ in range(size)]
        if input_type == "Sorted":
            values.sort()
        elif input_type == "Reverse Sorted":
            values.sort(reverse=True)
        elif input_type == "Nearly Sorted":
            values.sort()
            for _ in range(max(1, size // 100)):
                i = rng.randrange(size)
                j = rng.randrange(size)
                values[i], values[j] = values[j], values[i]
        return values, input_type, "Integer array; sorting implementations return a new sorted list."

    if category == "Searching":
        # All selected algorithms receive the same ordering when Binary Search
        # is part of the experiment; this keeps the comparison meaningful.
        actual_type = "Sorted" if binary_search_selected else input_type
        values = [rng.randint(0, max(10, size * 3)) for _ in range(size)]
        if actual_type == "Sorted":
            values.sort()
        elif actual_type == "Reverse Sorted":
            values.sort(reverse=True)

        if search_mode == "Successful Search":
            target = values[size // 2]
        else:
            target = max(values) + max(1, size)

        if algorithm == "Hash Table Lookup":
            table = {value: index for index, value in enumerate(values)}
            return (table, target), actual_type, (
                "Dictionary lookup; successful/unsuccessful query matches the selected search mode."
            )

        if algorithm == "Binary Search":
            # Binary search requires ascending order; ensure it even if called
            # outside the Streamlit form.
            if actual_type != "Sorted":
                values.sort()
                actual_type = "Sorted"
            return (values, target), actual_type, (
                "Binary Search input is ascending-sorted as required by the implementation."
            )

        return (values, target), actual_type, (
            "Linear Search scans the same array values used by the selected query."
        )

    if category == "Graph":
        graph_type = "dense" if input_type == "Dense" else "sparse"
        graph = generate_graph(
            num_vertices=size,
            graph_type=graph_type,
            directed=False,
            weighted=True,
            seed=seed,
            min_weight=1,
            max_weight=10,
            ensure_connected=True,
        )
        notes = "Undirected connected weighted graph; source vertex is 0."
        if algorithm == "BFS":
            notes += " BFS reports unweighted edge-count distances; edge weights are ignored."
        return (graph, 0), input_type, notes

    if category == "Dynamic Programming":
        if algorithm.startswith("LCS"):
            pair = generate_string_pair(size, seed=seed)
            return pair, "Random Strings", "Two reproducible uppercase strings of equal length."
        weights = [rng.randint(1, max(2, size)) for _ in range(size)]
        values = [rng.randint(1, 100) for _ in range(size)]
        capacity = max(1, size * 5)
        return (weights, values, capacity), "Random Items", (
            f"{size} items; knapsack capacity={capacity}; generated weights and values are positive."
        )

    if category == "Matrix":
        pair = generate_square_matrix_pair(size, seed=seed)
        return pair, "Random Matrices", (
            f"Two reproducible {size} x {size} integer matrices; same pair for both methods."
        )

    raise ValueError(f"Unsupported category/algorithm: {category} / {algorithm}")
