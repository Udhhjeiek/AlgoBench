"""
benchmarking/timer.py
---------------------
Runtime measurement with time.perf_counter and summary statistics.

Convention for "data"
---------------------
An algorithm is always called as  func(*args).
  * If the prepared input is a tuple, it is unpacked as positional arguments
        e.g. (array, target)  ->  binary_search(array, target)
  * Anything else is passed as a single argument
        e.g. [3, 1, 2]        ->  quick_sort([3, 1, 2])
(So do not represent a graph as a bare tuple unless you want it unpacked.)

What is measured
----------------
ONLY the call  func(*args).  Input copying / preparation is done before the
stopwatch starts, so it is NOT included in the reported time.
"""
import copy
import gc
import statistics
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


def build_args(data: Any = None,
               prepare: Optional[Callable[[], Any]] = None,
               copy_input: bool = True) -> Tuple:
    """Create a fresh argument tuple for ONE trial (never timed)."""
    if prepare is not None:
        item = prepare()
    elif copy_input:
        item = copy.deepcopy(data)       # protects the shared dataset from in-place algorithms
    else:
        item = data
    return item if isinstance(item, tuple) else (item,)


def time_callable(func: Callable,
                  data: Any = None,
                  prepare: Optional[Callable[[], Any]] = None,
                  trials: int = 5,
                  warmup: int = 1,
                  copy_input: bool = True,
                  disable_gc: bool = True) -> List[float]:
    """Run `func` `trials` times (after `warmup` untimed runs); return seconds per trial."""
    if trials < 1:
        raise ValueError("trials must be >= 1")

    for _ in range(max(0, warmup)):
        func(*build_args(data, prepare, copy_input))

    times: List[float] = []
    for _ in range(trials):
        args = build_args(data, prepare, copy_input)   # setup: NOT timed
        gc_was_enabled = gc.isenabled()
        if disable_gc:
            gc.collect()
            gc.disable()
        try:
            start = time.perf_counter()
            func(*args)
            end = time.perf_counter()
        finally:
            if disable_gc and gc_was_enabled:
                gc.enable()
        times.append(end - start)
    return times


def summarize(times: List[float]) -> Dict[str, float]:
    """Average, median, min, max and (sample) standard deviation of the trial times."""
    return {
        "average_time": statistics.fmean(times),
        "median_time": statistics.median(times),
        "min_time": min(times),
        "max_time": max(times),
        "standard_deviation": statistics.stdev(times) if len(times) > 1 else 0.0,
    }
