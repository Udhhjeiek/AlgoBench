
import math
import pytest

from algorithms.graph import (
    dijkstra,
    bellman_ford,
    bfs,
    NegativeCycleError
)

from data_generation.graph_generator import generate_graph


# ------------------------------------
# DIJKSTRA TESTS
# ------------------------------------

def test_dijkstra_normal_graph():

    graph = {
        0: [(1, 4), (2, 2)],
        1: [(0, 4), (2, 5), (3, 10)],
        2: [(0, 2), (1, 5), (3, 3)],
        3: [(1, 10), (2, 3)]
    }

    result = dijkstra(graph, 0)

    assert result == {
        0: 0,
        1: 4,
        2: 2,
        3: 5
    }


def test_dijkstra_disconnected_graph():

    graph = {
        0: [(1, 5)],
        1: [(0, 5)],
        2: []
    }

    result = dijkstra(graph, 0)

    assert result[0] == 0
    assert result[1] == 5
    assert result[2] == math.inf


def test_dijkstra_negative_edge():

    graph = {
        0: [(1, -5)],
        1: []
    }

    with pytest.raises(ValueError):
        dijkstra(graph, 0)


def test_dijkstra_invalid_source():

    graph = {
        0: [(1, 2)],
        1: [(0, 2)]
    }

    with pytest.raises(ValueError):
        dijkstra(graph, 5)


# ------------------------------------
# BELLMAN-FORD TESTS
# ------------------------------------

def test_bellman_ford_normal_graph():

    graph = {
        0: [(1, 4), (2, 5)],
        1: [(2, -3)],
        2: []
    }

    result = bellman_ford(graph, 0)

    assert result == {
        0: 0,
        1: 4,
        2: 1
    }


def test_bellman_ford_negative_cycle():

    graph = {
        0: [(1, 1)],
        1: [(2, -3)],
        2: [(0, 1)]
    }

    with pytest.raises(NegativeCycleError):
        bellman_ford(graph, 0)


def test_bellman_ford_disconnected_graph():

    graph = {
        0: [(1, 2)],
        1: [],
        2: [(3, -5)],
        3: []
    }

    result = bellman_ford(graph, 0)

    assert result[0] == 0
    assert result[1] == 2
    assert result[2] == math.inf
    assert result[3] == math.inf


def test_bellman_ford_unreachable_negative_cycle():

    graph = {
        0: [(1, 2)],
        1: [],
        2: [(3, -3)],
        3: [(2, 1)]
    }

    result = bellman_ford(graph, 0)

    assert result[2] == math.inf


# ------------------------------------
# BFS TESTS
# ------------------------------------

def test_bfs_normal_graph():

    graph = {
        0: [(1, 1), (2, 1)],
        1: [(0, 1), (3, 1)],
        2: [(0, 1), (3, 1)],
        3: [(1, 1), (2, 1)]
    }

    order, distances = bfs(graph, 0)

    assert order == [0, 1, 2, 3]

    assert distances == {
        0: 0,
        1: 1,
        2: 1,
        3: 2
    }


def test_bfs_disconnected_graph():

    graph = {
        0: [(1, 1)],
        1: [(0, 1)],
        2: []
    }

    order, distances = bfs(graph, 0)

    assert order == [0, 1]
    assert distances[2] == math.inf


def test_bfs_single_vertex():

    graph = {
        0: []
    }

    order, distances = bfs(graph, 0)

    assert order == [0]
    assert distances == {0: 0}


# ------------------------------------
# GRAPH GENERATOR TESTS
# ------------------------------------

def test_generator_vertex_count():

    graph = generate_graph(
        20,
        seed=42
    )

    assert len(graph) == 20


def test_generator_reproducibility():

    graph1 = generate_graph(
        20,
        seed=42
    )

    graph2 = generate_graph(
        20,
        seed=42
    )

    assert graph1 == graph2


def test_generator_undirected_symmetry():

    graph = generate_graph(
        20,
        directed=False,
        seed=42
    )

    for u in graph:

        for v, weight in graph[u]:

            assert (u, weight) in graph[v]


def test_generator_no_self_loops():

    graph = generate_graph(20, seed=42)

    for u in graph:

        for v, weight in graph[u]:

            assert u != v


def test_generator_sparse_vs_dense():

    sparse = generate_graph(
        20,
        graph_type="sparse",
        seed=42
    )

    dense = generate_graph(
        20,
        graph_type="dense",
        seed=42
    )

    sparse_edges = sum(
        len(neighbours) for neighbours in sparse.values()
    )

    dense_edges = sum(
        len(neighbours) for neighbours in dense.values()
    )

    assert dense_edges > sparse_edges


def test_generator_connected():

    graph = generate_graph(
        20,
        graph_type="sparse",
        ensure_connected=True,
        seed=42
    )

    order, distances = bfs(graph, 0)

    assert len(order) == 20


def test_generator_invalid_vertices():

    with pytest.raises(ValueError):
        generate_graph(0)


def test_generator_invalid_type():

    with pytest.raises(ValueError):
        generate_graph(
            10,
            graph_type="medium"
        )
