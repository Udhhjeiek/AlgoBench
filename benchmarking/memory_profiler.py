"""
benchmarking/memory_profiler.py
-------------------------------
Python memory measurement with tracemalloc.

The reported value is the PEAK of *extra* memory allocated while the algorithm
runs (the input itself is created before tracing starts, so it is not counted).
tracemalloc slows code down, so memory is measured in a SEPARATE run and never
during the timed trials.
"""
import tracemalloc
from typing import Callable, Dict, Tuple


def measure_memory(func: Callable, args: Tuple = ()) -> Dict[str, float]:
    """Run func(*args) once under tracemalloc.  Returns sizes in KiB."""
    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start()
    tracemalloc.reset_peak()
    baseline, _ = tracemalloc.get_traced_memory()
    try:
        func(*args)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        if not was_tracing:
            tracemalloc.stop()
    return {
        "peak_kib": max(0, peak - baseline) / 1024.0,
        "retained_kib": max(0, current - baseline) / 1024.0,
    }
