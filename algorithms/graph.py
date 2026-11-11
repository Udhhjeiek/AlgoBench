
import heapq
import math


def _validate_graph(graph, source):
    """
    Validate graph structure and source vertex.
    Graph format: {vertex: [(neighbour, weight), ...]}
    """
    if not isinstance(graph, dict):
        raise TypeError("Graph must be a dictionary.")

    if not graph:
        raise ValueError("Graph cannot be empty.")

    if source not in graph:
        raise ValueError("Source vertex does not exist.")

    for vertex, neighbours in graph.items():
        for neighbour, weight in neighbours:
            if neighbour not in graph:
                raise ValueError(
                    f"Vertex {neighbour} is missing from graph."
                )

            if not isinstance(weight, (int, float)):
                raise TypeError("Edge weights must be numeric.")

            if not math.isfinite(weight):
                raise ValueError("Edge weights must be finite.")


def dijkstra(graph, source):
    """
    Dijkstra's shortest path algorithm.

    Parameters:
        graph: Weighted adjacency list.
        source: Starting vertex.

    Returns:
        Dictionary containing shortest distances.
        Unreachable vertices have distance infinity.

    Time Complexity:
        O((V + E) log V) with a binary heap.
    """

    _validate_graph(graph, source)

    for neighbours in graph.values():
        for neighbour, weight in neighbours:
            if weight < 0:
                raise ValueError(
                    "Dijkstra cannot handle negative edge weights."
                )

    distances = {
        vertex: math.inf for vertex in graph
    }

    distances[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:

        current_distance, current_vertex = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current_vertex]:
            continue

        for neighbour, weight in graph[current_vertex]:

            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    return distances


class NegativeCycleError(ValueError):
    """Raised when a reachable negative-weight cycle exists."""


def bellman_ford(graph, source):
    """
    Bellman-Ford shortest path algorithm.

    Supports negative edge weights.
    Detects reachable negative-weight cycles.

    Returns:
        Dictionary of shortest distances.

    Raises:
        NegativeCycleError if a reachable negative cycle exists.

    Time Complexity:
        O(VE)
    """

    _validate_graph(graph, source)

    distances = {
        vertex: math.inf for vertex in graph
    }

    distances[source] = 0

    edges = []

    for vertex in graph:
        for neighbour, weight in graph[vertex]:
            edges.append((vertex, neighbour, weight))

    V = len(graph)

    # Relax all edges V-1 times
    for _ in range(V - 1):

        updated = False

        for u, v, weight in edges:

            if distances[u] != math.inf:

                new_distance = distances[u] + weight

                if new_distance < distances[v]:

                    distances[v] = new_distance
                    updated = True

        # Stop early if no distance changes
        if not updated:
            break

    # Detect reachable negative-weight cycles
    for u, v, weight in edges:

        if distances[u] != math.inf:

            if distances[u] + weight < distances[v]:

                raise NegativeCycleError(
                    "Reachable negative-weight cycle detected."
                )

    return distances


from collections import deque


def bfs(graph, source):
    """
    Breadth-First Search.

    Parameters:
        graph: Adjacency list.
        source: Starting vertex.

    Returns:
        (traversal_order, distances)

        traversal_order:
            List of vertices in BFS order.

        distances:
            Shortest unweighted distances from source.
            Unreachable vertices have infinity.

    Time Complexity:
        O(V + E)
    """

    _validate_graph(graph, source)

    visited = set()

    distances = {
        vertex: math.inf for vertex in graph
    }

    traversal_order = []

    queue = deque([source])

    visited.add(source)
    distances[source] = 0

    while queue:

        current = queue.popleft()

        traversal_order.append(current)

        for neighbour, weight in graph[current]:

            if neighbour not in visited:

                visited.add(neighbour)

                distances[neighbour] = (
                    distances[current] + 1
                )

                queue.append(neighbour)

    return traversal_order, distances
