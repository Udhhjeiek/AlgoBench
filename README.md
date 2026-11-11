# AlgoBench — Algorithm Benchmarking & Profiling Suite

AlgoBench is a Python and Streamlit application for running reproducible algorithm experiments, measuring execution time and memory use, inspecting profiler output, and comparing performance across input sizes.

## Features

- Five algorithm domains: Sorting, Searching, Graph, Dynamic Programming, and Matrix Algorithms.
- Sixteen registered implementations.
- Reproducible data generation using a configurable random seed.
- Repeated timing trials with warm-up runs.
- Runtime statistics: average, median, minimum, maximum, and standard deviation.
- Peak additional Python memory measurement using `tracemalloc`.
- Optional function-level profiling using `cProfile` and `pstats`.
- CSV-backed experiment history.
- Runtime and memory plotting through GNUplot.
- Bright and Dark themes, custom logo/font, animated landing page, and interactive dashboard.

## Algorithms

| Domain | Implementations |
|---|---|
| Sorting | Quick Sort, Merge Sort, Heap Sort, Insertion Sort |
| Searching | Linear Search, Binary Search, Hash Table Lookup |
| Graph | Dijkstra, Bellman-Ford, Breadth-First Search |
| Dynamic Programming | LCS Memoization, LCS Tabulation, 0/1 Knapsack Memoization, 0/1 Knapsack Tabulation |
| Matrix | Standard Matrix Multiplication, Strassen Matrix Multiplication |

## Project structure

```text
AlgoBench/
├── app.py
├── Logo_Final.svg
├── assets/
│   └── NetflixSans-Regular.ttf
├── algorithms/
│   ├── sorting.py
│   ├── searching.py
│   ├── graph.py
│   ├── dynamic_programming.py
│   └── matrix.py
├── data_generation/
│   ├── graph_generator.py
│   ├── matrix_generator.py
│   └── string_generator.py
├── benchmarking/
│   ├── algorithm_registry.py
│   ├── benchmark_engine.py
│   ├── timer.py
│   ├── memory_profiler.py
│   ├── profiler.py
│   └── gprof_profiler.py
├── visualization/
│   ├── dashboard_charts.py
│   ├── gnuplot_runner.py
│   └── gnuplot/
├── tests/
├── scripts/
├── native/
│   └── gprof_demo.c
├── manual_tests/
├── results/
├── requirements.txt
├── Makefile
└── README.md
```

## Installation

Python 3.10 or newer is recommended.

### Windows PowerShell

```powershell
cd AlgoBench

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

If PowerShell blocks virtual-environment activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### Linux / macOS / WSL

```bash
cd AlgoBench

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

The dashboard opens in your browser at the local Streamlit address printed by the command.

## Running a benchmark

1. Open **Run Benchmark**.
2. Choose an algorithm category and one or more algorithms.
3. Select the dataset distribution and size.
4. Set the number of timing trials and random seed.
5. Optionally choose a scaling experiment to run several input sizes.
6. Keep memory measurement enabled to collect `tracemalloc` peak memory.
7. Enable cProfile if you want a separate profiler run. Profiling is deliberately separate from the timed trials.
8. Click **Run Benchmark**.

The dashboard saves the experiment as a CSV file in `results/`, displays the measured rows, and makes them available to Compare Results and History.

### Input conventions

- **Sorting:** generated integer arrays; supported distributions are Random, Sorted, Reverse Sorted, and Nearly Sorted.
- **Searching:** Linear Search and Hash Table Lookup use the selected query mode. Binary Search requires ascending order. If Binary Search is selected, the dashboard sorts the shared collection for the complete search comparison and records the effective input type as `Sorted`.
- **Graph:** the generator creates reproducible undirected, connected weighted graphs. Dijkstra and Bellman-Ford use the positive edge weights. BFS reports unweighted edge-count distances and ignores edge weights.
- **Dynamic Programming:** LCS uses two generated strings. Knapsack uses generated positive item weights and values and a capacity derived from the item count.
- **Matrix:** Standard and Strassen multiplication receive the same pair of generated square matrices for a given size and seed.

The dashboard limits selectable sizes for expensive algorithms (for example, Insertion Sort, dense Bellman-Ford, and quadratic DP) to help avoid impractically long runs.

## Measurement methodology

AlgoBench uses Member 041's generic `BenchmarkEngine`.

- Runtime is measured with `time.perf_counter()`.
- The engine performs warm-up calls and then repeated timed trials.
- Dataset creation and input copying/preparation are outside the timed interval. The reported runtime is the algorithm call itself.
- Memory is measured in a separate execution using `tracemalloc`. `memory_measurement` is peak additional traced memory in KiB; it is not total process RAM.
- cProfile/pstats profiling is also a separate execution. Its overhead is not included in timing results.
- Each CSV row records the algorithm, category, input size/type, trial count, runtime statistics, memory measurement, seed, and measurement notes.

This separation keeps timing, memory tracing, and profiler overhead from contaminating one another.

## Results and history

- `results/*.csv` contains saved experiment records.
- `results/profiles/` contains `.prof` and `.txt` profiler artifacts when cProfile is enabled.
- `results/plots/` contains GNUplot `.dat` files and generated plot images.
- The History page loads saved CSV experiments.
- Compare Results can display current results and generate GNUplot data/plots from a saved CSV.

Do not treat old example results as measurements for your own machine. Each run should be generated from your own selected dataset and hardware.


## Included experimental evidence and final documents

This release includes the team's local scaling experiments for all five algorithm domains under `results/`:

- Eight original timestamped benchmark CSVs plus `algobench_scaling_results.csv` (74 scaling datapoints).
- GNUplot `.dat` files and runtime/memory PNGs for Sorting, Searching, Graph, Dynamic Programming (LCS and Knapsack), and Matrix.
- cProfile/pstats text reports and their binary `.prof` artifacts.
- The final 22-page LaTeX report (`reports/report.pdf`) and 13-slide Beamer presentation (`reports/presentation.pdf`), with their `.tex` sources.
- `results/EXPERIMENT_NOTES.md` describes the tested sizes, workload conventions, and measurement caveats.

The numeric values are machine-specific measurements from the team's Windows / CPython 3.14 environment. Hash-table construction is excluded from the lookup timing; BFS reports unweighted distances; and some Streamlit-hosted cProfile reports include background event-loop activity. These caveats are discussed in the report.

## GNUplot

The Python package prepares `.dat` files without GNUplot. Rendering the PNG plots requires the GNUplot executable to be installed and available on `PATH`.

The app's Compare Results page provides separate actions to:
- Prepare GNUplot data files.
- Render runtime and memory PNGs.

The command-line equivalent is:

```bash
python visualization/gnuplot_runner.py results/your_experiment.csv
```

If GNUplot is not found, install it for your operating system and reopen the terminal so the updated `PATH` is available.

## Profiling native C code with gprof

`benchmarking/gprof_profiler.py` supports gprof for standalone C programs compiled with `gcc -pg`. It is separate from Python's cProfile profiler.

Example:

```bash
python benchmarking/gprof_profiler.py native/gprof_demo.c
```

Requirements:
- Linux/macOS: `gcc` and `gprof` (usually supplied by GCC/binutils packages).
- Windows: use WSL with GCC and gprof installed inside WSL; native MinGW gprof may not collect time samples.

## Tests

Run the algorithm, generator, and integration tests:

```bash
python -m pytest -q tests
```

Run Member 041's benchmark-engine test suite without its demo benchmark:

```bash
python test.py --no-demo
```

Or run both through the helper script:

```bash
bash scripts/run_tests.sh
```

## Make targets

When GNU Make is installed:

```bash
make install       # install requirements into the active Python environment
make run           # run Streamlit
make test          # run the complete pytest suite (including Member 041 tests)
make test-engine    # run Member 041's original standalone test script
make plots CSV=results/your_experiment.csv
make clean         # remove Python caches and pytest cache
```

## Git collaboration

The team uses one feature branch per member and `main` as the integrated branch.

1. Commit work on the assigned member branch.
2. Push the branch to GitHub.
3. Open a pull request into `main`.
4. Review the changed files and run tests before merging.
5. Do not commit virtual environments, Python caches, or generated `.prof` binaries.

Keep commits focused and descriptive so the repository history clearly documents each stage of development.
