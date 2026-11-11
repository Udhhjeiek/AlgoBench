# AlgoBench integration status

## Integrated contributions

- CS25BT005: sorting and searching implementations and unit tests.
- CS25BT022: graph algorithms, graph generator, and unit tests.
- CS25BT031: dynamic-programming and matrix algorithms, string/matrix generators, manual checks, and unit tests. Folder/import names were standardized to the common project packages.
- CS25BT041: generic benchmark engine, timer, memory profiler, cProfile, gprof support, GNUplot runner/scripts, and benchmark-engine tests.
- CS25BT051: original Streamlit dashboard, assets, theme/landing interactions, and integration.

## Integration changes

- Added `benchmarking/algorithm_registry.py` to register all 16 functions and build each algorithm's correctly-shaped input.
- Connected Run Benchmark to the real benchmark engine.
- Added single-size and multi-size scaling experiments.
- Added runtime, memory, profiling, CSV, Compare Results, History, and GNUplot data/plot actions.
- Updated chart display to read the engine's `trial_count` and `memory_measurement` result fields.
- Added size caps for slow algorithms and enforced the caps inside the benchmark engine.
- Added Windows-friendly project instructions, Bash scripts, Makefile, README, LaTeX report, and Beamer presentation.

## Validation performed in the integration environment

- 35 Python files syntax-checked successfully.
- `pytest -q tests`: 158 passed and 64 subtests passed.
- All 16 registered algorithms executed through the real benchmark engine in smoke tests.
- Member 041 standalone test suite: 17 tests passed (also included in the unified pytest discovery).
- CSV persistence and GNUplot `.dat` preparation smoke-tested successfully.
- LaTeX report and Beamer presentation compiled successfully.

## Checks to complete on the project computer

The integration environment used to assemble this package did not have Streamlit or the GNUplot executable installed, so it could not launch the browser application or render GNUplot PNGs.

On the Windows project computer:
1. Install dependencies with `pip install -r requirements.txt`.
2. Run `python -m pytest -q tests`.
3. Run `streamlit run app.py` and verify the landing page, both themes, all six navigation pages, benchmark execution, profiles, CSV history, and downloads.
4. Install GNUplot and add it to PATH if PNG generation is required.
5. Capture real experiment CSVs and runtime/memory plots for the report and final demo.

No sample or illustrative benchmark values are shipped as if they were final hardware measurements.
