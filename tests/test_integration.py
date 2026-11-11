import tempfile

from benchmarking.algorithm_registry import (
    ALGORITHM_OPTIONS,
    build_dataset,
    create_default_engine,
    recommended_input_sizes,
)


def test_all_sixteen_algorithm_implementations_are_registered():
    engine = create_default_engine()
    assert set(engine.categories()) == set(ALGORITHM_OPTIONS)
    assert sum(len(engine.algorithms(category)) for category in engine.categories()) == 16


def test_sorting_datasets_are_reproducible():
    first, _, _ = build_dataset("Sorting", "Quick Sort", 25, "Random", seed=7)
    second, _, _ = build_dataset("Sorting", "Quick Sort", 25, "Random", seed=7)
    assert first == second


def test_search_binary_dataset_is_sorted_when_selected():
    data, actual_type, _ = build_dataset(
        "Searching", "Linear Search", 50, "Random", seed=10,
        binary_search_selected=True
    )
    assert actual_type == "Sorted"
    assert data[0] == sorted(data[0])


def test_hash_lookup_dataset_is_a_mapping_and_query_pair():
    data, _, _ = build_dataset(
        "Searching", "Hash Table Lookup", 30, "Random", seed=11,
        search_mode="Successful Search"
    )
    table, target = data
    assert target in table


def test_graph_dataset_matches_graph_algorithm_signature():
    data, actual_type, _ = build_dataset("Graph", "Dijkstra", 20, "Sparse", seed=42)
    graph, source = data
    assert source == 0
    assert len(graph) == 20
    assert actual_type == "Sparse"


def test_lcs_dataset_is_a_pair_of_strings():
    data, actual_type, _ = build_dataset(
        "Dynamic Programming", "LCS - Tabulation", 12, seed=42
    )
    assert len(data) == 2
    assert len(data[0]) == len(data[1]) == 12
    assert actual_type == "Random Strings"


def test_knapsack_dataset_matches_three_argument_signature():
    data, _, _ = build_dataset(
        "Dynamic Programming", "Knapsack - Memoization", 10, seed=42
    )
    weights, values, capacity = data
    assert len(weights) == len(values) == 10
    assert capacity > 0


def test_matrix_dataset_is_two_compatible_square_matrices():
    data, _, _ = build_dataset("Matrix", "Standard Multiplication", 8, seed=42)
    a, b = data
    assert len(a) == len(b) == 8
    assert all(len(row) == 8 for row in a + b)


def test_default_engine_runs_one_real_sort_and_saves_csv():
    with tempfile.TemporaryDirectory() as temp_dir:
        engine = create_default_engine(results_dir=temp_dir)
        data, input_type, notes = build_dataset("Sorting", "Merge Sort", 20, seed=5)
        row = engine.run(
            "Sorting", "Merge Sort", data, input_size=20,
            input_type=input_type, trials=2, warmup=0,
            measure_memory=True, profile=False, seed=5, notes=notes
        )
        assert row["category"] == "Sorting"
        assert row["algorithm"] == "Merge Sort"
        assert row["trial_count"] == 2
        assert row["average_time"] >= 0
        assert row["memory_measurement"] >= 0
        path = engine.save_csv([row], "integration_test.csv")
        assert path.endswith("integration_test.csv")


def test_input_size_options_protect_slow_insertion_sort():
    sizes = recommended_input_sizes("Sorting", ["Quick Sort", "Insertion Sort"])
    assert max(sizes) <= 5000


import pytest


_ALL_SMALL_ALGORITHMS = [
    ("Sorting", "Quick Sort", 40, "Random"),
    ("Sorting", "Merge Sort", 40, "Random"),
    ("Sorting", "Heap Sort", 40, "Random"),
    ("Sorting", "Insertion Sort", 40, "Random"),
    ("Searching", "Linear Search", 40, "Random"),
    ("Searching", "Binary Search", 40, "Random"),
    ("Searching", "Hash Table Lookup", 40, "Random"),
    ("Graph", "Dijkstra", 12, "Sparse"),
    ("Graph", "Bellman-Ford", 12, "Sparse"),
    ("Graph", "BFS", 12, "Sparse"),
    ("Dynamic Programming", "LCS - Memoization", 8, "Random"),
    ("Dynamic Programming", "LCS - Tabulation", 8, "Random"),
    ("Dynamic Programming", "Knapsack - Memoization", 8, "Random"),
    ("Dynamic Programming", "Knapsack - Tabulation", 8, "Random"),
    ("Matrix", "Standard Multiplication", 4, "Random"),
    ("Matrix", "Strassen Multiplication", 4, "Random"),
]


@pytest.mark.parametrize(
    "category,algorithm,size,input_type",
    _ALL_SMALL_ALGORITHMS,
)
def test_every_registered_algorithm_executes_through_engine(
    tmp_path, category, algorithm, size, input_type
):
    engine = create_default_engine(results_dir=str(tmp_path))
    data, actual_type, notes = build_dataset(
        category,
        algorithm,
        size,
        input_type=input_type,
        seed=123,
        binary_search_selected=(category == "Searching"),
    )

    result = engine.run(
        category,
        algorithm,
        data,
        input_size=size,
        input_type=actual_type,
        trials=1,
        warmup=0,
        measure_memory=True,
        profile=False,
        seed=123,
        notes=notes,
    )

    assert result["category"] == category
    assert result["algorithm"] == algorithm
    assert result["trial_count"] == 1
    assert result["average_time"] >= 0
    assert result["memory_measurement"] is not None



def test_engine_enforces_registered_maximum_input_size():
    engine = create_default_engine()
    data, input_type, notes = build_dataset(
        "Sorting", "Insertion Sort", 20, "Random", seed=1
    )
    # The registry cap is 5,000 for Insertion Sort.
    with pytest.raises(ValueError, match="maximum input size"):
        engine.run(
            "Sorting",
            "Insertion Sort",
            data,
            input_size=5001,
            input_type=input_type,
            trials=1,
            warmup=0,
            measure_memory=False,
            profile=False,
            notes=notes,
        )
