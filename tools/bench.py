"""Reproducible offscreen measurements of the control window (not a test – no time limits, nothing asserted).

    python tools/bench.py                    # every scenario, 5 runs each, medians
    python tools/bench.py --runs 3 --only startup,pages
    python tools/bench.py --json out.json    # also write the raw numbers

Every run is a child process on a throw-away root (symlinked maps/models/maps.json, its own settings.json,
rounds.jsonl, recordings folder, DBDMS_DATA_DIR and HOME) – the real program folder and the user's data are never
touched. Qt runs offscreen, so these are Linux/CI numbers: they compare before and after on the same machine, they
are no Windows timings. Windows-only costs (drive letters, EnumWindows, fsync) are counted (calls), not timed.

Scenarios (each prints one JSON line of milliseconds or counts):
  startup     import of fogscout.app, App(), first idle – and RSS after it
  pages       first and second visit of each page (show_page → _poll → _qt_refresh(force) → processEvents)
  overview    _qt_refresh(force=True) on the overview, 30 times
  stats       _stats_render() with 500 and 5000 synthetic rounds
  recordings  _rec_render(force=True) with 300 recordings + 100 clips; calls of recorder.folder()
  idle        CPU seconds of the process over the first 10 s of the event loop on the overview (window shown;
              the pages are built in the background then) and over 10 s after 15 s more (steady)
  latency     a click posted through the window's callback (App._qt_post) every 137 ms – ms until its handler
  folder      calls of obsrec.find_folder (26 drive letters each on Windows) and recordings renders over 10 s of
              the event loop: recordings page shown, then the window hidden with that page selected
"""
from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = ("startup", "pages", "overview", "stats", "recordings", "idle", "latency", "folder")


# ---------------------------------------------------------------- the child: one scenario on a fresh root
def _root(rounds: int = 0, recordings: int = 0) -> str:
    tmp = tempfile.mkdtemp(prefix="fogscout-bench-")
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.join(ROOT, name), os.path.join(tmp, name))
    os.makedirs(os.path.join(tmp, "sim"))
    os.environ["DBDMS_DATA_DIR"] = os.path.join(tmp, "data")
    os.environ["HOME"] = os.path.join(tmp, "home")
    os.makedirs(os.environ["HOME"])
    settings = {"welcome_seen": True}
    if rounds:
        _rounds(os.path.join(tmp, "rounds.jsonl"), rounds)
    if recordings:
        settings.update(rec_on=True, rec_folder=_recordings(os.path.join(tmp, "rec"), recordings))
    with open(os.path.join(tmp, "settings.json"), "w", encoding="utf-8") as fh:
        json.dump(settings, fh)
    return tmp


def _rounds(path: str, n: int):
    rnd = random.Random(7)
    maps = [("coal-tower", "Coal Tower"), ("badham-preschool", "Badham Preschool I"), ("midwich", "Midwich"),
            ("ormond", "Mount Ormond Resort"), ("the-game", "The Game"), ("dead-dawg", "Dead Dawg Saloon")]
    killers = ["The Nurse", "The Wraith", "The Trapper", "The Spirit", "The Blight", ""]
    t0 = time.time() - n * 900
    with open(path, "w", encoding="utf-8") as fh:
        for i in range(n):
            mid, label = rnd.choice(maps)
            role = rnd.choice(["killer", "survivor", ""])
            fh.write(json.dumps({"t": t0 + i * 900, "seconds": rnd.uniform(240, 1200), "map_id": mid, "map": label,
                                 "region": rnd.choice(["eu-central-1", "us-east-1", ""]), "source": "auto",
                                 "wait": rnd.uniform(5, 300), "role": role, "custom": rnd.random() < 0.05,
                                 "farming": rnd.random() < 0.05, "ping": rnd.uniform(15, 120),
                                 "killer": rnd.choice(killers) if role == "killer" else ""}) + "\n")


def _recordings(folder: str, n: int) -> str:
    from fogscout import obsrec
    os.makedirs(os.path.join(folder, obsrec.CLIPS_DIR))
    t0 = time.time() - n * 1800
    recs, clips = [], []
    for i in range(n):
        t = t0 + i * 1800
        name = obsrec.file_name(t, "Coal Tower", "Nurse", ".mkv")
        name = f"{os.path.splitext(name)[0]} {i}.mkv"
        with open(os.path.join(folder, name), "wb") as fh:
            fh.write(b"\0" * 64)
        recs.append(obsrec.Recording(t=t, file=name, label="Coal Tower", role="killer", killer="nurse", end=t + 600,
                                     size=64, marks=[30.0] if i % 3 == 0 else []))
    obsrec.save_index(folder, recs)
    for i in range(min(100, n)):
        t = t0 + i * 1800 + 60
        name = f"{time.strftime('%Y-%m-%d %H-%M', time.localtime(t))} Coal Tower {i} (Sofort-Clip).mp4"
        with open(os.path.join(folder, obsrec.CLIPS_DIR, name), "wb") as fh:
            fh.write(b"\0" * 64)
        clips.append(obsrec.Clip(file=name, t=t, kind="clip", label="Coal Tower", size=64))
    obsrec.save_clips(os.path.join(folder, obsrec.CLIPS_DIR), clips)
    return folder


def _settle(app_qapp, rounds=3):
    for _ in range(rounds):
        app_qapp.processEvents()


def _rss_mb() -> float:
    try:
        with open("/proc/self/statm") as fh:
            return int(fh.read().split()[1]) * os.sysconf("SC_PAGE_SIZE") / 1e6
    except (OSError, ValueError, IndexError):
        return 0.0


def _child(scenario: str) -> dict:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("DBDMS_LANG", "de")
    sys.path.insert(0, ROOT)
    out = {}
    rounds = 5000 if scenario == "stats" else 0
    recs = 300 if scenario in ("recordings", "folder") else 0
    root = _root(rounds=rounds, recordings=recs)
    t0 = time.perf_counter()
    from fogscout.app import App                          # noqa: E402 (timed)
    t1 = time.perf_counter()
    app = App(root, simulate=os.path.join(root, "sim"))
    t2 = time.perf_counter()
    from PySide6.QtWidgets import QApplication
    qapp = QApplication.instance()
    _settle(qapp, 5)
    t3 = time.perf_counter()
    q = app.qt
    try:
        if scenario == "startup":
            out = {"import_ms": (t1 - t0) * 1e3, "app_ms": (t2 - t1) * 1e3, "idle_ms": (t3 - t2) * 1e3,
                   "total_ms": (t3 - t0) * 1e3, "rss_mb": _rss_mb()}
        elif scenario == "pages":
            from fogscout import qt_window
            for visit in ("first", "second"):
                for key, _label in qt_window.PAGES:
                    s = time.perf_counter()
                    q.show_page(key)
                    app._poll()
                    app._qt_refresh(force=True)
                    _settle(qapp)
                    out[f"{visit}:{key}"] = (time.perf_counter() - s) * 1e3
        elif scenario == "overview":
            q.show_page("overview")
            app._poll()
            _settle(qapp)
            times = []
            for _ in range(30):
                s = time.perf_counter()
                app._qt_refresh(force=True)
                times.append((time.perf_counter() - s) * 1e3)
            out = {"refresh_median_ms": statistics.median(times), "refresh_max_ms": max(times)}
        elif scenario == "stats":
            q.show_page("stats")
            app._poll()
            _settle(qapp)
            app._stats_render()                          # first: the join of 5000 rounds
            times = []
            for _ in range(10):
                s = time.perf_counter()
                app._stats_render()
                _settle(qapp, 1)
                times.append((time.perf_counter() - s) * 1e3)
            out = {"render_5000_median_ms": statistics.median(times)}
        elif scenario == "recordings":
            calls = {"n": 0}
            real = app.recorder.folder

            def counted():
                calls["n"] += 1
                return real()
            app.recorder.folder = counted
            q.show_page("recordings")
            app._poll()
            _settle(qapp)
            times, per = [], []
            for _ in range(10):
                calls["n"] = 0
                s = time.perf_counter()
                app._rec_render(force=True)
                times.append((time.perf_counter() - s) * 1e3)
                per.append(calls["n"])
            calls["n"] = 0
            q.show_page("overview")
            app._poll()
            app._qt_refresh(force=True)
            out = {"render_300_median_ms": statistics.median(times), "folder_calls_per_render": max(per),
                   "folder_calls_overview_refresh": calls["n"]}
        elif scenario == "idle":
            from PySide6.QtCore import QTimer
            q.show_page("overview")
            app._poll()
            _settle(qapp)
            QTimer.singleShot(10_000, lambda: qapp.exit(0))
            c0, w0 = time.process_time(), time.perf_counter()
            qapp.exec()
            out = {"cpu_percent_of_core": (time.process_time() - c0) / (time.perf_counter() - w0) * 100,
                   "rss_after_mb": _rss_mb()}
            QTimer.singleShot(15_000, lambda: qapp.exit(0))
            qapp.exec()
            QTimer.singleShot(10_000, lambda: qapp.exit(0))
            c0, w0 = time.process_time(), time.perf_counter()
            qapp.exec()
            out.update(cpu_steady_percent=(time.process_time() - c0) / (time.perf_counter() - w0) * 100,
                       rss_steady_mb=_rss_mb())
        elif scenario == "latency":
            from PySide6.QtCore import QTimer
            q.show_page("overview")
            app._poll()
            _settle(qapp)
            sent, got, real = {}, [], app._dispatch

            def spy(ev):
                if isinstance(ev, tuple) and ev[:2] == ("ui", "bench-click"):
                    got.append((time.perf_counter() - sent[ev[2]]) * 1e3)
                    return
                real(ev)
            app._dispatch = spy

            def click():
                n = len(sent) + 1
                sent[n] = time.perf_counter()
                app._qt_post("bench-click", n)
            beat = QTimer()
            beat.timeout.connect(click)
            beat.start(137)
            QTimer.singleShot(137 * 41, lambda: qapp.exit(0))
            qapp.exec()
            beat.stop()
            out = {"click_to_handler_median_ms": statistics.median(got), "click_to_handler_max_ms": max(got),
                   "clicks": len(got)}
        elif scenario == "folder":
            from PySide6.QtCore import QTimer
            from fogscout import obsrec
            calls, renders = {"n": 0}, {"n": 0}
            real_find, real_render = obsrec.find_folder, app._rec_render

            def find(*a):
                calls["n"] += 1
                return real_find(*a)

            def render(*a, **k):
                renders["n"] += 1
                return real_render(*a, **k)
            obsrec.find_folder, app._rec_render = find, render
            q.show_page("recordings")
            app._poll()
            _settle(qapp)
            for phase in ("shown", "hidden"):
                if phase == "hidden":
                    q.hide()
                calls["n"] = renders["n"] = 0
                QTimer.singleShot(10_000, lambda: qapp.exit(0))
                qapp.exec()
                out[f"find_folder_{phase}"] = calls["n"]
                out[f"renders_{phase}"] = renders["n"]
    finally:
        try:
            app.quit()
        except Exception:
            pass
    return out


# ---------------------------------------------------------------- the parent: runs, medians, table
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--only", default=",".join(SCENARIOS))
    ap.add_argument("--json")
    ap.add_argument("--child")
    args = ap.parse_args()
    if args.child:
        print("BENCH " + json.dumps(_child(args.child)), flush=True)
        os._exit(0)                                       # as the program does: no slow interpreter teardown
    results = {}
    for scenario in [s for s in args.only.split(",") if s in SCENARIOS]:
        runs = []
        for _ in range(args.runs):
            p = subprocess.run([sys.executable, os.path.abspath(__file__), "--child", scenario],
                               capture_output=True, text=True, timeout=600)
            line = next((ln for ln in p.stdout.splitlines() if ln.startswith("BENCH ")), None)
            if line is None:
                print(f"{scenario}: failed\n{p.stderr[-2000:]}", file=sys.stderr)
                break
            runs.append(json.loads(line[6:]))
        if not runs:
            continue
        med = {k: statistics.median(r[k] for r in runs) for k in runs[0]}
        results[scenario] = {"median": med, "runs": runs}
        print(f"\n{scenario} (median of {len(runs)})")
        for k, v in med.items():
            print(f"  {k:32s} {v:9.1f}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"python": sys.version.split()[0], "platform": sys.platform, "cpus": os.cpu_count(),
                       "results": results}, fh, indent=1)


if __name__ == "__main__":
    main()
