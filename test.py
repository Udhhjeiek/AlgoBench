"""
test.py - local test + demo for the Benchmarking / Profiling / GNUplot module (CS25BT041).

    python test.py              # unit tests, then a demo benchmark (CSV + profile + plots)
    python test.py --no-demo    # unit tests only
    python test.py --real       # also benchmark teammates' real algorithms/sorting.py if present

Needs only the Python standard library (3.9+).  GNUplot is optional: if it is not
installed the plotting step is skipped with a message.
"""
import argparse
import os
import random
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from benchmarking import BenchmarkEngine, CSV_FIELDS, load_csv          # noqa: E402
from benchmarking import timer, measure_memory, profile_callable        # noqa: E402
from visualization import gnuplot_runner                                # noqa: E402
from benchmarking import gprof_profiler                                 # noqa: E402


# ----------------------------------------------------------------------------
# Stand-in algorithms + dataset generator (so this works before teammates push)
# ----------------------------------------------------------------------------
def insertion_sort(a):
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right, out, i, j = merge_sort(a[:mid]), merge_sort(a[mid:]), [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def builtin_sort(a):
    return sorted(a)


def make_array(size, input_type="random", seed=42):
    rng = random.Random(seed)
    a = [rng.randint(0, size * 10) for _ in range(size)]
    if input_type == "sorted":
        a.sort()
    elif input_type == "reverse":
        a.sort(reverse=True)
    elif input_type == "nearly_sorted":
        a.sort()
        for _ in range(max(1, size // 20)):
            i, j = rng.randrange(size), rng.randrange(size)
            a[i], a[j] = a[j], a[i]
    return a


def make_engine(results_dir):
    eng = BenchmarkEngine(results_dir=results_dir)
    eng.register("sorting", "Insertion Sort", insertion_sort, max_size=2000)
    eng.register("sorting", "Merge Sort", merge_sort)
    eng.register("sorting", "Built-in Sort", builtin_sort)
    return eng


# ----------------------------------------------------------------------------
# Unit tests
# ----------------------------------------------------------------------------
class TestTimer(unittest.TestCase):
    def test_trial_count_and_positive_times(self):
        t = timer.time_callable(builtin_sort, make_array(500), trials=4, warmup=1)
        self.assertEqual(len(t), 4)
        self.assertTrue(all(x >= 0 for x in t))

    def test_summary_statistics(self):
        s = timer.summarize([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(s["average_time"], 2.5)
        self.assertAlmostEqual(s["median_time"], 2.5)
        self.assertEqual((s["min_time"], s["max_time"]), (1.0, 4.0))
        self.assertAlmostEqual(s["standard_deviation"], 1.2909944, places=5)
        self.assertEqual(timer.summarize([2.0])["standard_deviation"], 0.0)

    def test_shared_dataset_not_mutated(self):
        data = make_array(200)
        original = list(data)
        timer.time_callable(insertion_sort, data, trials=3)   # sorts IN PLACE
        self.assertEqual(data, original)

    def test_tuple_input_is_unpacked(self):
        seen = []
        timer.time_callable(lambda arr, target: seen.append((len(arr), target)),
                            ([1, 2, 3], 2), trials=2, warmup=0)
        self.assertEqual(seen, [(3, 2), (3, 2)])

    def test_setup_is_not_timed(self):
        import time
        def slow_prepare():
            time.sleep(0.05)
            return [3, 1, 2]
        t = timer.time_callable(builtin_sort, prepare=slow_prepare, trials=2, warmup=0)
        self.assertTrue(all(x < 0.04 for x in t))

    def test_bad_trials(self):
        with self.assertRaises(ValueError):
            timer.time_callable(builtin_sort, [1], trials=0)


class TestMemoryAndProfiler(unittest.TestCase):
    def test_memory_peak_grows_with_allocation(self):
        small = measure_memory(lambda: [0] * 1_000)["peak_kib"]
        big = measure_memory(lambda: [0] * 1_000_000)["peak_kib"]
        self.assertGreater(big, small * 100)

    def test_profiler_report(self):
        with tempfile.TemporaryDirectory() as d:
            rep = profile_callable(insertion_sort, (make_array(300),), output_dir=d, label="unit test")
            self.assertIn("insertion_sort", rep["text"])
            self.assertTrue(rep["rows"])
            self.assertIn("Main bottleneck", rep["summary"])
            self.assertTrue(os.path.exists(rep["files"]["prof"]))
            self.assertTrue(os.path.exists(rep["files"]["txt"]))


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.eng = make_engine(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_run_result_fields(self):
        r = self.eng.run("sorting", "Merge Sort", make_array(300), input_type="random", trials=3, seed=1)
        for f in ("category", "algorithm", "input_size", "input_type", "trial_count",
                  "average_time", "median_time", "standard_deviation", "memory_measurement"):
            self.assertIn(f, r)
        self.assertEqual((r["input_size"], r["trial_count"]), (300, 3))
        self.assertGreater(r["memory_measurement"], 0)

    def test_unknown_algorithm(self):
        with self.assertRaises(KeyError):
            self.eng.run("sorting", "Bogo Sort", [1, 2, 3])

    def test_sweep_respects_max_size_and_saves_csv(self):
        rows = self.eng.sweep("sorting", ["Insertion Sort", "Merge Sort"], [500, 1000, 4000],
                              make_array, "random", trials=2, warmup=0, save_as="t.csv")
        names = {(r["algorithm"], r["input_size"]) for r in rows}
        self.assertNotIn(("Insertion Sort", 4000), names)       # max_size=2000
        self.assertIn(("Merge Sort", 4000), names)
        loaded = load_csv(os.path.join(self.tmp, "t.csv"))
        self.assertEqual(len(loaded), len(rows))
        with open(os.path.join(self.tmp, "t.csv")) as fh:
            self.assertEqual(fh.readline().strip().split(","), CSV_FIELDS)

    def test_sweep_progress_and_profile(self):
        calls = []
        rows = self.eng.sweep("sorting", ["Merge Sort"], [200, 400], make_array, "sorted",
                              trials=2, warmup=0, profile_largest=True,
                              progress=lambda d, t, m: calls.append((d, t)))
        self.assertEqual(calls, [(1, 2), (2, 2)])
        self.assertNotIn("profile", rows[0])      # only the largest size is profiled
        self.assertIn("profile", rows[1])

    def test_append_mode_writes_one_header(self):
        r = self.eng.run("sorting", "Built-in Sort", [3, 1, 2], trials=2)
        self.eng.save_csv([r], "a.csv")
        self.eng.save_csv([r], "a.csv", append=True)
        with open(os.path.join(self.tmp, "a.csv")) as fh:
            lines = fh.read().strip().splitlines()
        self.assertEqual(len(lines), 3)

    def test_read_only_algorithm_skips_copy(self):
        data = list(range(10))
        seen = []
        self.eng.register("searching", "Probe", lambda arr: seen.append(arr is data), mutates_input=False)
        self.eng.run("searching", "Probe", data, trials=1, warmup=0, measure_memory=False)
        self.assertTrue(seen and all(seen))


@unittest.skipUnless(gprof_profiler.gprof_available(), "gcc/gprof not installed")
class TestGprof(unittest.TestCase):
    def test_gprof_parser_handles_empty_table(self):
        empty = "Flat profile:\n\nEach sample counts as 0.01 seconds.\n  %   cumulative   self\n time   seconds   seconds\n\n"
        self.assertEqual(gprof_profiler.parse_flat_profile(empty), [])

    def test_gprof_on_c_demo(self):
        tmp = tempfile.mkdtemp()
        try:
            res = gprof_profiler.run_gprof(os.path.join(ROOT, "native", "gprof_demo.c"), tmp)
            if not res["has_samples"]:
                self.skipTest(res["summary"])      # e.g. native Windows gcc: gprof records no samples
            self.assertTrue(any(r["function"] == "dot_row_col" for r in res["rows"]))
            self.assertIn("Main bottleneck (gprof)", res["summary"])
            self.assertTrue(os.path.exists(res["files"]["report"]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestPlotData(unittest.TestCase):
    def test_pivot_and_dat_files(self):
        tmp = tempfile.mkdtemp()
        try:
            eng = make_engine(tmp)
            eng.sweep("sorting", ["Insertion Sort", "Merge Sort"], [500, 1000, 4000], make_array,
                      "random", trials=2, warmup=0, save_as="p.csv")
            jobs = gnuplot_runner.write_dat_files(os.path.join(tmp, "p.csv"), os.path.join(tmp, "plots"))
            self.assertEqual(len(jobs), 1)
            with open(jobs[0]["dat"]) as fh:
                lines = fh.read().splitlines()
            self.assertEqual(lines[0].split("\t")[:4], ["input_size", "Insertion Sort",
                                                         "Insertion Sort std", "Insertion Sort mem"])
            self.assertEqual(len(lines), 4)                       # header + 3 sizes
            self.assertIn("NaN", lines[3])                        # Insertion Sort skipped at n=4000
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ----------------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------------
def print_table(rows):
    print(f"{'algorithm':<16}{'input':<14}{'n':>8}{'avg (s)':>12}{'median (s)':>12}{'stdev (s)':>12}{'mem (KiB)':>12}")
    for r in rows:
        print(f"{r['algorithm']:<16}{r['input_type']:<14}{r['input_size']:>8}"
              f"{r['average_time']:>12.6f}{r['median_time']:>12.6f}"
              f"{r['standard_deviation']:>12.6f}{r['memory_measurement']:>12.1f}")


def demo(engine, category, algorithms, sizes, factory, input_types, label):
    out_csv = f"{label}_demo.csv"
    all_rows = []
    for itype in input_types:
        print(f"\n--- {category} | input type: {itype} ---")
        rows = engine.sweep(category, algorithms, sizes, factory, itype, trials=5, seed=42,
                            profile_largest=(itype == input_types[0]),
                            progress=lambda d, t, m: print(f"  [{d}/{t}] {m}", end="\r"))
        print(" " * 50, end="\r")
        print_table(rows)
        all_rows += rows

    path = engine.save_csv(all_rows, out_csv)
    print(f"\nCSV saved: {path}")

    print("\n--- Profiling (largest size, first input type) ---")
    for r in all_rows:
        if "profile" in r:
            p = r["profile"]
            print(f"\n[{r['algorithm']} n={r['input_size']}] {p['summary']}")
            for row in p["rows"][:3]:
                print(f"   {row['function']:<24}{row['ncalls']:>10} calls  self {row['tottime']:.4f}s  cum {row['cumtime']:.4f}s")
            print(f"   saved: {p['files']['txt']}")

    print("\n--- gprof (native C demo) ---")
    if gprof_profiler.gprof_available():
        try:
            g = gprof_profiler.run_gprof(os.path.join(ROOT, "native", "gprof_demo.c"),
                                         os.path.join(engine.results_dir, "gprof"))
            print(f"backend: {g['backend']}")
            print(g["summary"])
            for row in g["rows"][:3]:
                print(f"   {row['function']:<16}{row['percent_time']:>6.1f}%  self {row['self_seconds']:.2f}s  calls {row['calls']}")
            print("   saved:", g["files"]["report"])
        except Exception as exc:                      # gprof is optional - never abort the demo
            print("gprof step failed (optional):", exc)
    else:
        print("gcc/gprof (or WSL) not found -> skipped (optional; see README, section 3).")

    print("\n--- GNUplot ---")
    plots_dir = os.path.join(engine.results_dir, "plots")
    if shutil.which("gnuplot") is None:
        jobs = gnuplot_runner.write_dat_files(path, plots_dir)
        print("gnuplot not found -> skipped drawing. Data files prepared:",
              ", ".join(j["dat"] for j in jobs))
        print("Install gnuplot (sudo apt install gnuplot / brew install gnuplot) and rerun.")
    else:
        for png in gnuplot_runner.generate_plots(path, plots_dir):
            print("plot created:", png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-demo", action="store_true", help="unit tests only")
    ap.add_argument("--real", action="store_true", help="also benchmark algorithms/sorting.py from Member 1")
    opts = ap.parse_args()

    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    if opts.no_demo:
        return

    results_dir = os.path.join(ROOT, "results")
    engine = make_engine(results_dir)
    demo(engine, "sorting", ["Insertion Sort", "Merge Sort", "Built-in Sort"],
         [250, 500, 1000, 2000, 4000, 8000], make_array, ["random", "sorted"], "sorting")

    if opts.real:
        try:
            from algorithms import sorting as real
        except ImportError as exc:
            print(f"\n--real: cannot import algorithms/sorting.py ({exc}). Merge Member 1's branch first.")
            return
        eng = BenchmarkEngine(results_dir=results_dir)
        names = {"Quick Sort": "quick_sort", "Merge Sort": "merge_sort",
                 "Heap Sort": "heap_sort", "Insertion Sort": "insertion_sort"}
        found = []
        for label, fn in names.items():
            if hasattr(real, fn):
                eng.register("sorting", label, getattr(real, fn),
                             max_size=2000 if label == "Insertion Sort" else None)
                found.append(label)
        print("\nReal algorithms found:", found or "none (check function names in sorting.py)")
        if found:
            demo(eng, "sorting", found, [250, 500, 1000, 2000, 4000], make_array,
                 ["random", "sorted", "reverse", "nearly_sorted"], "sorting_real")


if __name__ == "__main__":
    main()
