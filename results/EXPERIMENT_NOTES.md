# AlgoBench experimental evidence

This folder contains locally generated benchmark evidence collected on the project team's Windows computer in November 2026.

## Scaling experiment sources

The consolidated file `algobench_scaling_results.csv` contains 74 rows drawn from the following five scaling experiments. Each row represents an average of five timed trials.

| Domain | Scaling sizes | Input type | Algorithms |
|---|---|---|---|
| Sorting | 100, 500, 1,000, 2,000, 5,000 | Random integer arrays | Quick, Merge, Heap, Insertion Sort |
| Searching | 1,000, 5,000, 10,000, 50,000 | Sorted arrays; successful query | Linear Search, Binary Search, Hash Table Lookup |
| Graph | 20, 50, 100, 200 vertices | Sparse, connected, undirected weighted graph | Dijkstra, Bellman-Ford, BFS |
| Dynamic Programming | 10, 20, 40, 60, 80, 100 | Random strings for LCS; random items for Knapsack | Memoization and tabulation variants |
| Matrix | 32, 64, 128 | Random square matrices | Standard and Strassen multiplication |

The original timestamped CSV files are retained. The earlier one-size smoke runs are kept separately and are not mixed into the scaling graphs or tables.

## GNUplot outputs

`plots/` contains a `.dat` file and two PNGs (runtime and peak additional traced memory) for each applicable input family:

- `Sorting_Random`
- `Searching_Sorted`
- `Graph_Sparse`
- `Dynamic_Programming_Random_Strings`
- `Dynamic_Programming_Random_Items`
- `Matrix_Random_Matrices`

Dynamic Programming has two separate data families because LCS uses string length while Knapsack uses item count/capacity.

## Profiling artifacts

`profiles/` contains `.txt` cProfile/pstats reports and the corresponding `.prof` files. Some cProfile captures include Streamlit watcher, asyncio, and background-thread activity. Read the algorithm function rows as the useful algorithm-specific evidence; do not attribute all cumulative time in those mixed captures to the algorithm. An isolated worker-process profiler would improve this in a future version.

## Measurement notes

- Runtime is the average of five timed calls after an untimed warm-up.
- Dataset construction and input preparation are outside the timed call.
- Memory is measured separately with `tracemalloc` as peak additional traced Python allocation in KiB; it is not process RSS.
- The Hash Table Lookup experiment times lookup, not dictionary construction.
- BFS reports unweighted edge-count distances and ignores graph edge weights; it is not equivalent to weighted Dijkstra/Bellman-Ford.
- The search experiments are successful lookups on sorted data.
- The Python version visible in profiler paths is CPython 3.14. The CPU model and hardware specifications were not included in the evidence.
- Timings are machine-specific. Microsecond-scale results are especially sensitive to scheduling and timer overhead.

## Testing and application verification

The integration test record reports 158 passing pytest cases and 64 passing subtests, with all 16 registered algorithms smoke-tested through the benchmark engine. The user also confirmed local Streamlit execution for all five categories and GNUplot rendering of the runtime and memory PNGs.
