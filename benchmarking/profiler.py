"""
benchmarking/profiler.py
------------------------
Function-level profiling with cProfile / pstats.

profile_callable() returns a dict:
    text      - the pstats table as a string (show it in the dashboard / report)
    rows      - top functions as a list of dicts (for tables)
    summary   - one-sentence bottleneck interpretation
    files     - paths of the saved .prof and .txt files (if output_dir was given)
"""
import cProfile
import io
import os
import pstats
import re
from typing import Any, Callable, Dict, List, Optional, Tuple


def _safe(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", label).strip("_") or "profile"


def profile_callable(func: Callable,
                     args: Tuple = (),
                     top_n: int = 15,
                     sort_by: str = "cumulative",
                     output_dir: Optional[str] = None,
                     label: str = "profile") -> Dict[str, Any]:
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        func(*args)
    finally:
        profiler.disable()

    stats = pstats.Stats(profiler)
    stream = io.StringIO()
    pstats.Stats(profiler, stream=stream).sort_stats(sort_by).print_stats(top_n)
    text = stream.getvalue()

    total_self = sum(v[2] for v in stats.stats.values()) or 1e-12   # sum of tottime
    rows: List[Dict[str, Any]] = []
    for (filename, line, name), (cc, nc, tt, ct, _callers) in stats.stats.items():
        if "_lsprof.Profiler" in name:          # profiler's own bookkeeping, not the algorithm
            continue
        rows.append({
            "function": name,
            "location": f"{os.path.basename(filename)}:{line}",
            "ncalls": str(nc) if nc == cc else f"{nc}/{cc}",
            "tottime": tt,
            "cumtime": ct,
            "percent_self": 100.0 * tt / total_self,
        })
    key = "tottime" if sort_by in ("tottime", "time") else "cumtime"
    rows.sort(key=lambda r: r[key], reverse=True)
    rows = rows[:top_n]

    summary = bottleneck_summary(stats.stats, total_self)

    files: Dict[str, str] = {}
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.join(output_dir, _safe(label))
        profiler.dump_stats(base + ".prof")        # inspect later: python -m pstats <file>.prof
        with open(base + ".txt", "w", encoding="utf-8") as fh:
            fh.write(text)
        files = {"prof": base + ".prof", "txt": base + ".txt"}

    return {"text": text, "rows": rows, "summary": summary, "files": files}


def bottleneck_summary(stat_items: Dict, total_self: float) -> str:
    """Name the function with the largest self time (where time is really spent)."""
    (fname, line, name), (cc, nc, tt, ct, _c) = max(stat_items.items(), key=lambda kv: kv[1][2])
    return (f"Main bottleneck: {name} ({os.path.basename(fname)}:{line}) - "
            f"{100.0 * tt / total_self:.1f}% of self time, {nc} call(s).")
