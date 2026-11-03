"""Measurements of the command palette (audit F6, 1.28) – a script, not a test: nothing asserted, no time limits,
nothing optimised. It answers one question before anyone changes code: what does opening the palette (Ctrl+F)
cost on this PC, and where does the time go?

    python tools/bench_palette.py                 # 5 runs, medians
    python tools/bench_palette.py --runs 3 --json out.json
    python tools/bench_palette.py --visible       # Windows: a real window (default there); Linux: needs a display

Every run is a child process on a throw-away root (maps/models/maps.json linked, or copied where links are not
allowed, its own settings.json and a few hundred synthetic rounds, DBDMS_DATA_DIR and HOME/USERPROFILE in the temp
folder) – the program folder and the user's data are only read, never written. The root is deleted afterwards.
Outside Windows Qt runs offscreen unless --visible: those numbers are a reference for before/after on the same
machine, not Windows timings. The meaningful numbers come from the user's PC (Windows, 3440×1440).

Printed per run (milliseconds) and as medians:
  cold_start      import of fogscout.app + App() + first idle
  first_open      Ctrl+F (MainWindow.focus_search) until the App's entries are in the palette (pages built/filled)
  second_open     the same after Esc – everything built already
  show_states     time spent in MainWindow.show_states during the first opening (sum of calls)
  search_index    time spent in MainWindow.update_search_index during the first opening (sum of calls)
  build_all       MainWindow.build_all on a second, fresh App (every page built at once)
  page_switch     median of five page changes (show_page + idle)
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = ("cold_start", "first_open", "second_open", "show_states", "search_index", "build_all", "page_switch")
PAGES = ("stats", "recordings", "settings", "overlay", "overview")


# ---------------------------------------------------------------- the child: one run on a fresh root
def _link(src: str, dst: str):
    try:
        os.symlink(src, dst, target_is_directory=os.path.isdir(src))
    except (OSError, NotImplementedError):           # Windows without the right to make links: a copy
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def _root(tmp: str, rounds: int) -> str:
    for name in ("maps", "models", "maps.json"):
        _link(os.path.join(ROOT, name), os.path.join(tmp, name))
    os.makedirs(os.path.join(tmp, "sim"))
    home = os.path.join(tmp, "home")
    os.makedirs(home)
    os.environ["DBDMS_DATA_DIR"] = os.path.join(tmp, "data")
    os.environ["HOME"] = home
    os.environ["USERPROFILE"] = home
    rnd = random.Random(7)
    t0 = time.time() - rounds * 900
    with open(os.path.join(tmp, "rounds.jsonl"), "w", encoding="utf-8") as fh:
        for i in range(rounds):
            fh.write(json.dumps({"t": t0 + i * 900, "seconds": rnd.uniform(240, 1200), "map_id": "coal-tower",
                                 "map": "Coal Tower", "source": "auto", "role": rnd.choice(["killer", "survivor"]),
                                 "killer": "The Nurse"}) + "\n")
    with open(os.path.join(tmp, "settings.json"), "w", encoding="utf-8") as fh:
        json.dump({"welcome_seen": True, "autostart": False}, fh)
    return tmp


def _timed(obj, name: str, total: list):
    """Wraps obj.name so every call adds its time to total[0] (instance attribute, the class stays as it is)."""
    real = getattr(obj, name)

    def wrapper(*a, **k):
        s = time.perf_counter()
        try:
            return real(*a, **k)
        finally:
            total[0] += time.perf_counter() - s
    setattr(obj, name, wrapper)


def _idle(app, qapp, rounds: int = 4):
    for _ in range(rounds):
        app._poll()
        qapp.processEvents()


def _open(app, qapp) -> float:
    q = app.qt
    s = time.perf_counter()
    q.focus_search()
    deadline = s + 60
    while time.perf_counter() < deadline:            # until the App's entries (with the settings) are in it
        _idle(app, qapp, 1)
        if any(e.kind == "setting" for e in q.palette._entries):
            break
    return (time.perf_counter() - s) * 1e3


def _child(visible: bool) -> dict:
    if not visible and sys.platform != "win32":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("DBDMS_LANG", "de")
    sys.path.insert(0, ROOT)
    tmp = tempfile.mkdtemp(prefix="fogscout-bench-palette-")
    try:
        root = _root(tmp, 300)
        out = {}
        t0 = time.perf_counter()
        from fogscout.app import App                  # noqa: E402 (timed)
        app = App(root, simulate=os.path.join(root, "sim"))
        from PySide6.QtWidgets import QApplication
        qapp = QApplication.instance()
        app.qt.show()
        _idle(app, qapp, 5)
        out["cold_start"] = (time.perf_counter() - t0) * 1e3
        states, index = [0.0], [0.0]
        _timed(app.qt, "show_states", states)
        _timed(app.qt, "update_search_index", index)
        out["first_open"] = _open(app, qapp)
        out["show_states"], out["search_index"] = states[0] * 1e3, index[0] * 1e3
        app.qt.palette.close_palette()
        _idle(app, qapp)
        out["second_open"] = _open(app, qapp)
        app.qt.palette.close_palette()
        switches = []
        for key in PAGES:
            s = time.perf_counter()
            app.qt.show_page(key)
            _idle(app, qapp)
            switches.append((time.perf_counter() - s) * 1e3)
        out["page_switch"] = statistics.median(switches)
        app.quit()
        tmp2 = tempfile.mkdtemp(prefix="fogscout-bench-palette-")
        try:
            app2 = App(_root(tmp2, 300), simulate=os.path.join(tmp2, "sim"))
            s = time.perf_counter()
            app2.qt.build_all()
            out["build_all"] = (time.perf_counter() - s) * 1e3
            app2.quit()
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)
        out["env"] = _env(qapp)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _env(qapp) -> dict:
    import PySide6
    from PySide6.QtCore import qVersion
    screen = qapp.primaryScreen()
    size = screen.size() if screen is not None else None
    return {"python": platform.python_version(), "pyside6": PySide6.__version__, "qt": qVersion(),
            "os": platform.platform(), "machine": platform.machine(), "cpus": os.cpu_count(),
            "qpa": qapp.platformName(),
            "screen": f"{size.width()}x{size.height()}" if size is not None else "?",
            "scale": screen.devicePixelRatio() if screen is not None else None}


# ---------------------------------------------------------------- the parent: runs, medians
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--json", help="also write the raw numbers to this file")
    ap.add_argument("--visible", action="store_true", help="a real window outside Windows (needs a display)")
    ap.add_argument("--child", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.child:
        print(json.dumps(_child(args.visible)))
        return
    runs = []
    for i in range(max(1, args.runs)):
        cmd = [sys.executable, os.path.abspath(__file__), "--child"] + (["--visible"] if args.visible else [])
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        line = next((ln for ln in reversed(res.stdout.splitlines()) if ln.startswith("{")), None)
        if res.returncode != 0 or line is None:
            print(f"run {i + 1}: failed (exit {res.returncode})\n{res.stderr[-2000:]}", file=sys.stderr)
            continue
        runs.append(json.loads(line))
        print(f"run {i + 1}: " + "  ".join(f"{k} {runs[-1][k]:.0f}" for k in KEYS))
    if not runs:
        sys.exit(1)
    print("environment: " + json.dumps(runs[0]["env"]))
    print(f"medians over {len(runs)} runs (ms):")
    for k in KEYS:
        print(f"  {k:<13} {statistics.median(r[k] for r in runs):8.1f}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(runs, fh, indent=1)


if __name__ == "__main__":
    main()
