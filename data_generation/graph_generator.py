
import random


def generate_graph(
    num_vertices,
    graph_type="sparse",
    directed=False,
    weighted=True,
    seed=None,
    min_weight=1,
    max_weight=10,
    ensure_connected=False
):
    """
    Generate a random graph using an adjacency list.

    Parameters:
        num_vertices: Number of vertices.
        graph_type: "sparse" or "dense".
        directed: Generate directed or undirected graph.
        weighted: Generate weighted or unweighted graph.
        seed: Random seed for reproducibility.
        min_weight: Minimum edge weight.
        max_weight: Maximum edge weight.
        ensure_connected: Ensure all vertices are reachable
                          from vertex 0 in the generated graph.

    Returns:
        Dictionary adjacency list:
        {vertex: [(neighbour, weight), ...]}
    """

    if not isinstance(num_vertices, int) or isinstance(num_vertices, bool):
        raise TypeError("num_vertices must be an integer.")

    if num_vertices < 1:
        raise ValueError("num_vertices must be at least 1.")

    if graph_type not in ("sparse", "dense"):
        raise ValueError(
            "graph_type must be 'sparse' or 'dense'."
        )

    if not isinstance(directed, bool) or not isinstance(weighted, bool):
        raise TypeError("directed and weighted must be booleans.")

    if not isinstance(ensure_connected, bool):
        raise TypeError("ensure_connected must be a boolean.")

    if not isinstance(min_weight, int) or isinstance(min_weight, bool):
        raise TypeError("min_weight must be an integer.")

    if not isinstance(max_weight, int) or isinstance(max_weight, bool):
        raise TypeError("max_weight must be an integer.")

    if min_weight > max_weight:
        raise ValueError("min_weight cannot exceed max_weight.")

    rng = random.Random(seed)

    graph = {
        vertex: [] for vertex in range(num_vertices)
    }

    # Maximum possible edges
    if directed:
        max_edges = num_vertices * (num_vertices - 1)
    else:
        max_edges = num_vertices * (num_vertices - 1) // 2

    if graph_type == "sparse":
        target_edges = min(
            max_edges,
            max(num_vertices - 1, (3 * num_vertices) // 2)
        )
    else:
        target_edges = (max_edges + 1) // 2

    edges = set()

    # Add a chain to ensure reachability from vertex 0.
    if ensure_connected:
        for vertex in range(num_vertices - 1):
            edges.add((vertex, vertex + 1))

    if target_edges < len(edges):
        target_edges = len(edges)

    # Generate all possible edges.
    possible_edges = []

    for u in range(num_vertices):

        for v in range(num_vertices):

            if u == v:
                continue

            if not directed and u > v:
                continue

            possible_edges.append((u, v))

    rng.shuffle(possible_edges)

    # Add random edges without duplicates.
    for edge in possible_edges:

        if len(edges) >= target_edges:
            break

        edges.add(edge)

    # Construct adjacency list.
    for u, v in edges:

        if weighted:
            weight = rng.randint(min_weight, max_weight)
        else:
            weight = 1

        graph[u].append((v, weight))

        if not directed:
            graph[v].append((u, weight))

    return graph
