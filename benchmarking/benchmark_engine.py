"""
benchmarking/benchmark_engine.py
--------------------------------
Reusable benchmark engine.  It contains NO algorithm-specific logic: it only
receives a callable plus prepared input, times it, measures memory, optionally
profiles it, and records the result in the agreed CSV schema.

Units in the CSV
    *_time / standard_deviation : seconds
    memory_measurement          : KiB (peak extra memory during one call, tracemalloc)

Typical use
    engine = BenchmarkEngine(results_dir="results")
    engine.register("sorting", "Quick Sort", quick_sort)
    rows = engine.sweep("sorting", ["Quick Sort"], [1000, 2000], make_array, "random")
"""
import csv
import datetime as _dt
import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional

from . import timer, memory_profiler, profiler

# Agreed result schema (guide, section 10) + a few extra useful columns.
CSV_FIELDS = [
    "timestamp", "category", "algorithm", "input_size", "input_type",
    "trial_count", "average_time", "median_time", "min_time", "max_time",
    "standard_deviation", "memory_measurement", "seed", "notes",
]

DEFAULT_NOTES = "time = algorithm call only (input copy/setup excluded); memory = tracemalloc peak KiB"


@dataclass
class _Entry:
    func: Callable
    mutates_input: bool = True      # True -> fresh deep copy of the input before every trial
    max_size: Optional[int] = None  # skip sizes above this (e.g. O(n^2) algorithms)


def _infer_size(data: Any) -> Optional[int]:
    first = data[0] if isinstance(data, tuple) and data else data
    try:
        return len(first)
    except TypeError:
        return None


class BenchmarkEngine:
    def __init__(self, results_dir: str = "results", profile_dir: Optional[str] = None):
        self.results_dir = results_dir
        self.profile_dir = profile_dir or os.path.join(results_dir, "profiles")
        self._registry: Dict[tuple, _Entry] = {}

    # ------------------------------------------------------------------ registry
    def register(self, category: str, name: str, func: Callable,
                 mutates_input: bool = True, max_size: Optional[int] = None) -> None:
        """Add an algorithm. Set mutates_input=False for read-only algorithms
        (e.g. binary search on a big array) to skip the per-trial copy."""
        self._registry[(category, name)] = _Entry(func, mutates_input, max_size)

    def categories(self) -> List[str]:
        return sorted({c for c, _ in self._registry})

    def algorithms(self, category: Optional[str] = None) -> List[str]:
        return sorted(n for c, n in self._registry if category in (None, c))

    def _entry(self, category: str, name: str) -> _Entry:
        try:
            return self._registry[(category, name)]
        except KeyError:
            raise KeyError(f"'{name}' is not registered under category '{category}'. "
                           f"Registered: {self.algorithms(category)}") from None

    # ------------------------------------------------------------------ one benchmark
    def run(self, category: str, algorithm: str, data: Any = None, *,
            prepare: Optional[Callable[[], Any]] = None,
            input_size: Optional[int] = None, input_type: str = "unspecified",
            trials: int = 5, warmup: int = 1,
            measure_memory: bool = True, profile: bool = False,
            seed: Optional[int] = None, notes: str = DEFAULT_NOTES,
            profile_top_n: int = 15) -> Dict[str, Any]:
        """Benchmark ONE algorithm on ONE input. Returns a result dict (CSV fields +
        'raw_times' and, if profile=True, 'profile')."""
        entry = self._entry(category, algorithm)
        if input_size is None:
            input_size = _infer_size(data)

        if entry.max_size is not None and input_size is not None and input_size > entry.max_size:
            raise ValueError(
                f"{algorithm} is configured for a maximum input size of "
                f"{entry.max_size}; received {input_size}."
            )

        times = timer.time_callable(entry.func, data, prepare=prepare, trials=trials,
                                    warmup=warmup, copy_input=entry.mutates_input)
        row: Dict[str, Any] = {
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "category": category, "algorithm": algorithm,
            "input_size": input_size, "input_type": input_type,
            "trial_count": trials, **timer.summarize(times),
            "memory_measurement": None, "seed": seed, "notes": notes,
            "raw_times": times,
        }

        if measure_memory:      # separate run: tracemalloc would distort timings
            args = timer.build_args(data, prepare, entry.mutates_input)
            row["memory_measurement"] = memory_profiler.measure_memory(entry.func, args)["peak_kib"]

        if profile:             # separate run as well
            args = timer.build_args(data, prepare, entry.mutates_input)
            row["profile"] = profiler.profile_callable(
                entry.func, args, top_n=profile_top_n, output_dir=self.profile_dir,
                label=f"{category}_{algorithm}_{input_type}_{input_size}")
        return row

    # ------------------------------------------------------------------ experiment
    def sweep(self, category: str, algorithms: Iterable[str], sizes: Iterable[int],
              dataset_factory: Callable[[int, str, int], Any], input_type: str = "random",
              *, trials: int = 5, warmup: int = 1, seed: int = 42,
              measure_memory: bool = True, profile_largest: bool = False,
              progress: Optional[Callable[[int, int, str], None]] = None,
              save_as: Optional[str] = None) -> List[Dict[str, Any]]:
        """Run several algorithms over several sizes.

        dataset_factory(size, input_type, seed) -> input (or tuple of args).
        It is called ONCE per size and every algorithm receives an identical copy,
        so comparisons are fair and reproducible.
        progress(done, total, message) is called after each benchmark (for a progress bar).
        If save_as is given the rows are written to results_dir/save_as.
        """
        algorithms, sizes = list(algorithms), sorted(sizes)
        jobs = [(s, a) for s in sizes for a in algorithms
                if self._entry(category, a).max_size is None or s <= self._entry(category, a).max_size]
        largest = {a: max((s for s, x in jobs if x == a), default=None) for a in algorithms}

        rows: List[Dict[str, Any]] = []
        data_cache: Dict[int, Any] = {}
        for done, (size, algo) in enumerate(jobs, start=1):
            if size not in data_cache:
                data_cache = {size: dataset_factory(size, input_type, seed)}   # keep only current size
            rows.append(self.run(
                category, algo, data_cache[size], input_size=size, input_type=input_type,
                trials=trials, warmup=warmup, measure_memory=measure_memory, seed=seed,
                profile=profile_largest and size == largest[algo]))
            if progress:
                progress(done, len(jobs), f"{algo} @ n={size}")
        if save_as:
            self.save_csv(rows, save_as)
        return rows

    # ------------------------------------------------------------------ storage
    def save_csv(self, rows: List[Dict[str, Any]], filename: Optional[str] = None,
                 append: bool = False) -> str:
        """Write rows (CSV_FIELDS only) to results_dir/filename. Returns the path."""
        os.makedirs(self.results_dir, exist_ok=True)
        if filename is None:
            cat = rows[0]["category"] if rows else "results"
            filename = f"{cat}_{_dt.datetime.now():%Y%m%d_%H%M%S}.csv"
        path = os.path.join(self.results_dir, filename)
        new_file = not (append and os.path.exists(path))
        with open(path, "a" if append else "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
            if new_file:
                writer.writeheader()
            for r in rows:
                writer.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in CSV_FIELDS})
        return path

    def save_json(self, rows: List[Dict[str, Any]], filename: str) -> str:
        os.makedirs(self.results_dir, exist_ok=True)
        path = os.path.join(self.results_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump([{k: r.get(k) for k in CSV_FIELDS} for r in rows], fh, indent=2)
        return path

    def list_result_files(self) -> List[str]:
        """CSV files in results_dir, newest first (for the Experiment History page)."""
        if not os.path.isdir(self.results_dir):
            return []
        files = [os.path.join(self.results_dir, f) for f in os.listdir(self.results_dir) if f.endswith(".csv")]
        return sorted(files, key=os.path.getmtime, reverse=True)


def load_csv(path: str) -> List[Dict[str, Any]]:
    """Read a results CSV back, converting numeric columns."""
    numeric_int = {"input_size", "trial_count", "seed"}
    numeric_float = {"average_time", "median_time", "min_time", "max_time",
                     "standard_deviation", "memory_measurement"}
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            for k in numeric_int:
                r[k] = int(r[k]) if r.get(k) not in (None, "") else None
            for k in numeric_float:
                r[k] = float(r[k]) if r.get(k) not in (None, "") else None
            out.append(r)
    return out
