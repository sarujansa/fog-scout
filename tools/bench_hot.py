"""1.34.1: costs of the hot paths of the project review's performance package, offline (no Windows, no game).

    python tools/bench_hot.py [--runs 5]

P1  one minute of the map card at the App's overlay tick (4× a second, timer and REC on, style glass): ms per
    second of play
P2  netwatch: 100 000 synthetic packets (70 % UDP from/to a public peer, 30 % TCP) read from a local datagram socket
    pair the way the helper reads its raw socket: µs per packet (the raw socket itself needs Windows)
P6  obsrec.space() on an index of 500 recordings, called again without a change: ms per call
P7  detector.is_dark on the real loading screen at 3440×1440: ms per call

Each value is the median of --runs runs with the spread (min–max). P3/P4 (screen grabs, window lookups) cost on
Windows only; their counts are in the tests (test_one_grab_per_match_tick…, test_a_known_window_…)."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import socket
import statistics
import struct
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["DBDMS_DATA_DIR"] = tempfile.mkdtemp(prefix="bench-data-")
if importlib.util.find_spec("tkinter") is None:          # overlay_win32 imports Tk only for its fallback
    from unittest import mock
    sys.modules["tkinter"] = mock.MagicMock()


def p1_map_card() -> float:
    from fogscout import overlay_win32 as ow

    class Root:
        def after(self, *a):
            return None

        def after_cancel(self, *a):
            pass

    class Overlay(ow.PictureOverlay):
        def _push(self, *a):
            pass

    ov = Overlay(Root())
    ov._shown = True
    ov.set_map(os.path.join(ROOT, "maps", "Forsaken Boneyard", "Eyrie of Crows.webp"), "")
    ov.set_skin("glass")
    ov.set_server("Frankfurt", 28)
    ov.set_record("Ø 2.8 Kills · 12 Runden")
    ov.set_rec(True)
    real = ow.rec_phase
    ov.set_timer("0:00")
    ov.render(ov.fit_width(470, 518, 406))                 # map loaded and scaled: not part of a second of play
    t0 = time.perf_counter()
    try:
        for s in range(1, 61):
            ov.set_timer(f"{s // 60}:{s % 60:02d}")
            for tick in range(4):
                ow.rec_phase = (lambda now=None, s=s: s % 2 == 0)      # the wall clock's second, not the timer's
                height = ov.fit_width(470, 518, 406)
                ov.render(height)
    finally:
        ow.rec_phase = real
    return (time.perf_counter() - t0) * 1000 / 60


def _packets(n: int) -> list[bytes]:
    local, peer = socket.inet_aton("192.168.1.20"), socket.inet_aton("3.120.5.9")
    out = []
    for i in range(n):
        udp = i % 10 < 7
        src, dst = (local, peer) if i % 2 else (peer, local)
        head = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 48, 0, 0, 64, 17 if udp else 6, 0, src, dst)
        out.append(head + struct.pack("!HHHH", 50000, 7777, 28, 0) + bytes(20))
    return out


def p2_netwatch() -> float:
    """Packets through a real datagram socket pair, read as the helper reads them (on main: recv(65535) + parse +
    add; since 1.34.1: recv_into one buffer + feed) – only the reading side is timed."""
    from fogscout import netwatch
    pkts = _packets(100_000)
    table = netwatch.FlowTable()
    a, b = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)
    feed = getattr(netwatch, "feed", None)
    buf = bytearray(65535)
    local_b = socket.inet_aton("192.168.1.20")
    spent = 0.0
    try:
        for start in range(0, len(pkts), 100):
            chunk = pkts[start:start + 100]
            for pkt in chunk:
                a.send(pkt)
            t0 = time.perf_counter()
            for i in range(len(chunk)):
                t = (start + i) * 0.001
                if feed is not None:
                    n = b.recv_into(buf)
                    feed(table, t, local_b, "192.168.1.20", buf, n)
                else:
                    p = netwatch.parse(b.recv(65535))
                    if p:
                        table.add(t, "192.168.1.20", p)
            spent += time.perf_counter() - t0
    finally:
        a.close()
        b.close()
    return spent * 1e6 / len(pkts)


def p6_space(folder: str) -> float:
    from fogscout import obsrec
    obsrec.space(folder)                                   # the first call reads the index in any case
    t0 = time.perf_counter()
    for _ in range(20):
        obsrec.space(folder)
    return (time.perf_counter() - t0) * 1000 / 20


def _index(folder: str) -> None:
    from fogscout import obsrec
    with open(os.path.join(folder, obsrec.INDEX), "w", encoding="utf-8") as fh:
        for i in range(500):
            fh.write(json.dumps({"file": f"2026-11-{i % 28 + 1:02d} Map {i}.mp4", "t": 1.7e9 + i * 900,
                                 "map": "Eyrie of Crows", "size": 400_000_000 + i, "marks": [12.5] if i % 7 == 0
                                 else [], "role": "killer", "killer": "The Trapper"}) + "\n")


def p7_is_dark(frame) -> float:
    from fogscout import detector
    t0 = time.perf_counter()
    for _ in range(20):
        detector.is_dark(frame)
    return (time.perf_counter() - t0) * 1000 / 20


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=5)
    runs = ap.parse_args().runs
    import cv2
    frame = cv2.resize(cv2.imread(os.path.join(ROOT, "tests", "data", "end", "loading.jpg")), (3440, 1440))
    folder = tempfile.mkdtemp(prefix="bench-rec-")
    _index(folder)
    cases = [("P1 Kartentakt, ms je Spielsekunde", p1_map_card),
             ("P2 netwatch, µs je Paket", p2_netwatch),
             ("P6 space(), ms je Aufruf", lambda: p6_space(folder)),
             ("P7 is_dark, ms je Aufruf", lambda: p7_is_dark(frame))]
    print(f"Python {platform.python_version()}, {platform.machine()}, {os.cpu_count()} CPUs, {runs} Läufe")
    for name, fn in cases:
        fn()                                               # warm: imports, fonts, caches of the first call
        vals = [fn() for _ in range(runs)]
        print(f"{name}: {statistics.median(vals):.3f} ({min(vals):.3f}–{max(vals):.3f})")


if __name__ == "__main__":
    main()
