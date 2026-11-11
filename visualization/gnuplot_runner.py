"""
visualization/gnuplot_runner.py
-------------------------------
Turns a benchmark CSV into GNUplot graphs.

For every (category, input_type) pair in the CSV it
  1. pivots the rows into one tab-separated .dat file
        input_size | <Algo> | <Algo> std | <Algo> mem | ...
  2. calls  gnuplot  with visualization/gnuplot/runtime_plot.gnuplot
     and memory_plot.gnuplot

Command line:
    python visualization/gnuplot_runner.py results/sorting_demo.csv [out_dir] [--linear] [--no-errbars]
"""
import os
import re
import shutil
import subprocess
import sys
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from benchmarking.benchmark_engine import load_csv  # noqa: E402

SCRIPT_DIR = os.path.join(HERE, "gnuplot")
NAN = "NaN"


def _safe(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")


def pivot_rows(rows: List[dict], category: str, input_type: str):
    """Return (algorithms, header, table_lines) for one category/input_type.
    If an (algorithm,size) pair occurs several times, the LAST row wins."""
    latest: Dict[tuple, dict] = {}
    for r in rows:
        if r["category"] == category and r["input_type"] == input_type and r["input_size"] is not None:
            latest[(r["algorithm"], r["input_size"])] = r
    algos = sorted({a for a, _ in latest})
    sizes = sorted({s for _, s in latest})
    header = ["input_size"]
    for a in algos:
        header += [a, f"{a} std", f"{a} mem"]
    lines = ["\t".join(header)]
    for s in sizes:
        cells = [str(s)]
        for a in algos:
            r = latest.get((a, s))
            if r is None:
                cells += [NAN, NAN, NAN]
            else:
                cells += [repr(r["average_time"]), repr(r["standard_deviation"] or 0.0),
                          NAN if r["memory_measurement"] is None else repr(r["memory_measurement"])]
        lines.append("\t".join(cells))
    return algos, header, lines


def write_dat_files(csv_path: str, out_dir: str) -> List[dict]:
    """Create the pivoted .dat files (no gnuplot needed). Returns a list of job dicts."""
    rows = load_csv(csv_path)
    os.makedirs(out_dir, exist_ok=True)
    jobs = []
    for category, itype in sorted({(r["category"], r["input_type"]) for r in rows}):
        algos, _hdr, lines = pivot_rows(rows, category, itype)
        if not algos:
            continue
        stem = f"{_safe(category)}_{_safe(itype)}"
        dat = os.path.join(out_dir, stem + ".dat")
        with open(dat, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        has_mem = any(r["memory_measurement"] is not None for r in rows
                      if r["category"] == category and r["input_type"] == itype)
        jobs.append({"category": category, "input_type": itype, "dat": dat,
                     "stem": stem, "n": len(algos), "has_memory": has_mem})
    return jobs


def _gnuplot(script: str, variables: Dict[str, object]) -> None:
    assignments = []
    for k, v in variables.items():
        assignments.append(f"{k}={v}" if isinstance(v, (int, float)) else f"{k}='{v}'")
    cmd = ["gnuplot", "-e", "; ".join(assignments), os.path.join(SCRIPT_DIR, script)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"gnuplot failed for {script}:\n{proc.stderr}")


def generate_plots(csv_path: str, out_dir: str = os.path.join("results", "plots"),
                   logscale: bool = True, errbars: bool = True) -> List[str]:
    """Create runtime (and memory) PNGs for every category/input_type in the CSV."""
    if shutil.which("gnuplot") is None:
        raise RuntimeError("gnuplot is not installed. Install it with:  sudo apt install gnuplot  "
                           "(Linux) | brew install gnuplot (macOS)")
    pngs = []
    for job in write_dat_files(csv_path, out_dir):
        label = f"{job['category']} ({job['input_type']} input)"
        common = {"datafile": job["dat"], "n": job["n"], "logscale": int(logscale), "errbars": int(errbars)}
        out = os.path.join(out_dir, job["stem"] + "_runtime.png")
        _gnuplot("runtime_plot.gnuplot", {**common, "out": out, "plot_title": f"Runtime - {label}"})
        pngs.append(out)
        if job["has_memory"]:
            out = os.path.join(out_dir, job["stem"] + "_memory.png")
            _gnuplot("memory_plot.gnuplot", {**common, "out": out, "plot_title": f"Peak memory - {label}"})
            pngs.append(out)
    return pngs


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    made = generate_plots(args[0], args[1] if len(args) > 1 else os.path.join("results", "plots"),
                          logscale="--linear" not in sys.argv, errbars="--no-errbars" not in sys.argv)
    print("\n".join(made))
