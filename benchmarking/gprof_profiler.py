"""
benchmarking/gprof_profiler.py
------------------------------
gprof support for NATIVE C code (e.g. native/matrix_fast.c or native/gprof_demo.c).

gprof only profiles programs compiled with gcc -pg, so it cannot profile Python
functions - use benchmarking/profiler.py (cProfile) for those.

Steps done here:  gcc -pg  ->  run the program (writes gmon.out)  ->  gprof report.

Requirements
    Linux/macOS : gcc + gprof (binutils)            e.g.  sudo apt install gcc binutils
    Windows     : use WSL (wsl --install; then inside it: sudo apt install gcc binutils).
                  The code detects WSL automatically and runs gcc/gprof inside it.
                  Native MinGW/MSYS2 gcc compiles, but its gprof normally records NO
                  time samples (empty report), so it is not recommended.
    The C program must be a standalone executable (it needs a main()).

Command line:
    python benchmarking/gprof_profiler.py native/gprof_demo.c [out_dir]
"""
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional


def _native_ready() -> bool:
    return shutil.which("gcc") is not None and shutil.which("gprof") is not None


def _wsl_ready() -> bool:
    """True on Windows when WSL is installed and has gcc + gprof inside it."""
    if os.name != "nt" or shutil.which("wsl") is None:
        return False
    try:
        r = subprocess.run(["wsl", "sh", "-c", "command -v gcc && command -v gprof"],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0


def gprof_backend() -> Optional[str]:
    """'wsl' | 'native' | None.  On Windows, WSL is preferred because gprof from
    native MinGW/MSYS2 gcc usually records NO time samples (empty profile)."""
    if _wsl_ready():
        return "wsl"
    return "native" if _native_ready() else None


def gprof_available() -> bool:
    return gprof_backend() is not None


def _run(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")
    return proc


def parse_flat_profile(report: str) -> List[Dict[str, Any]]:
    """Parse the 'Flat profile' table of gprof output into dict rows."""
    rows: List[Dict[str, Any]] = []
    in_table = False
    for line in report.splitlines():
        if line.lstrip().startswith("%") and "cumulative" in line:
            in_table = True
            continue
        if in_table:
            if not line.strip():
                if rows:
                    break
                continue
            m = re.match(r"\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(?:(\d+)\s+([\d.]+)\s+([\d.]+)\s+)?(\S+)\s*$", line)
            if m:
                rows.append({"percent_time": float(m.group(1)), "self_seconds": float(m.group(3)),
                             "calls": int(m.group(4)) if m.group(4) else None, "function": m.group(7)})
    return rows


def run_gprof(c_source: str, output_dir: str = os.path.join("results", "gprof"),
              extra_flags: Optional[List[str]] = None, program_args: Optional[List[str]] = None,
              backend: Optional[str] = None) -> Dict[str, Any]:
    """Compile with -pg, run, and return {'text', 'rows', 'summary', 'has_samples', 'backend', 'files'}.
    backend: 'native', 'wsl' or None (= automatic)."""
    backend = backend or gprof_backend()
    if backend is None:
        raise RuntimeError("gcc and gprof were not found. Linux: sudo apt install gcc binutils. "
                           "Windows: install WSL (wsl --install, then 'sudo apt install gcc binutils' inside it).")
    prefix = ["wsl"] if backend == "wsl" else []

    out_dir = os.path.abspath(output_dir)
    os.makedirs(out_dir, exist_ok=True)
    src_name = os.path.basename(c_source)
    shutil.copyfile(c_source, os.path.join(out_dir, src_name))       # work with RELATIVE names inside out_dir

    native_windows = os.name == "nt" and backend == "native"
    exe_name = "profiled_program" + (".exe" if native_windows else "")
    exe_run = os.path.join(out_dir, exe_name) if backend == "native" else "./" + exe_name

    _run(prefix + ["gcc", "-pg", "-O0", "-o", exe_name, src_name] + (extra_flags or []) + ["-lm"], cwd=out_dir)

    gmon = os.path.join(out_dir, "gmon.out")
    if os.path.exists(gmon):
        os.remove(gmon)
    prog = _run(prefix + [exe_run] + (program_args or []), cwd=out_dir)   # gmon.out is written into cwd
    if not os.path.exists(gmon):
        raise RuntimeError("the program ran but produced no gmon.out (was it compiled with -pg?)")

    report = _run(prefix + ["gprof", exe_run, "gmon.out"], cwd=out_dir).stdout
    report_path = os.path.join(out_dir, os.path.splitext(src_name)[0] + "_gprof.txt")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report)

    rows = parse_flat_profile(report)
    if rows:
        top = max(rows, key=lambda r: r["percent_time"])
        summary = f"Main bottleneck (gprof): {top['function']} - {top['percent_time']:.1f}% of run time"
        summary += f", {top['calls']} call(s)." if top["calls"] else "."
    elif native_windows:
        summary = ("gprof recorded no time samples. This is a known limitation of gprof with native Windows "
                   "(MinGW/MSYS2) gcc. Run it through WSL/Linux instead (see README).")
    else:
        summary = "gprof produced no samples (program ran too briefly - increase the workload)."
    return {"text": report, "rows": rows, "summary": summary, "has_samples": bool(rows), "backend": backend,
            "program_output": prog.stdout, "files": {"report": report_path, "gmon": gmon}}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    res = run_gprof(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join("results", "gprof"))
    print(f"backend: {res['backend']}")
    for r in res["rows"][:8]:
        print(f"  {r['function']:<20}{r['percent_time']:>6.1f}%  self {r['self_seconds']:.2f}s  calls {r['calls']}")
    print(res["summary"])
    print("report saved:", res["files"]["report"])
