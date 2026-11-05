"""Pictures of the control window, offscreen (not a test – for looking at a page before and after a change).

    python tools/screenshots.py                          # every page, dark, 1100×760, zoom 1.0 → a temp folder
    python tools/screenshots.py --out shots --light --zoom 1.5 --size 1100x760 --pages settings,overlay

Like tools/bench.py the program runs on a throw-away root (symlinked maps/models/maps.json, own settings.json,
DBDMS_DATA_DIR, HOME) – the real program folder and the user's data are never touched. Per page one PNG of the window
as the user sees it; a hand-made page (overlay, settings) once per tab with every fold opened, and – when the page
scrolls – one more PNG of the whole content (``…-full.png``). The setup assistant once per step."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
sys.path.insert(0, ROOT)


def _settings(root: str, light: bool, zoom: float):
    path = os.path.join(root, "settings.json")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    data.update(dark_mode=not light, ui_zoom=float(zoom))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


UMLAUTS = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss"})


def _name(*parts) -> str:
    return "-".join(re.sub(r"[^A-Za-z0-9]+", "_", str(p).translate(UMLAUTS)).strip("_")
                    for p in parts if p) + ".png"


def _open_folds(page):
    from PySide6.QtWidgets import QPushButton
    for btn in page.findChildren(QPushButton, "fold"):
        body = btn.__dict__.get("_dbdms_fold")
        if body is not None and not body.isVisibleTo(body.parentWidget()):
            btn.click()


def _top_tabs(widget) -> list:
    """The tab widgets directly below ``widget`` (none of them inside another one below it)."""
    from PySide6.QtWidgets import QTabWidget
    found = widget.findChildren(QTabWidget)
    return [tw for tw in found if not any(o is not tw and o.isAncestorOf(tw) for o in found)]


def shoot(app, out: str, pages=None, settle=None) -> list:
    """Save the pictures of ``app``'s window into ``out``; the list of files written."""
    from PySide6.QtWidgets import QApplication, QScrollArea
    from fogscout import qt_window
    qapp = QApplication.instance()

    def _settle(n=4):
        for _ in range(n):
            qapp.processEvents()
        if settle:
            settle()
    os.makedirs(out, exist_ok=True)
    q = app.qt
    q.show()
    q.build_all()
    _settle()
    written = []

    def grab(widget, *parts):
        path = os.path.join(out, _name(*parts))
        if widget.grab().save(path):
            written.append(path)

    def grab_page(key, page, *parts):
        _open_folds(page)
        app._poll()
        app._qt_refresh(force=True)
        _settle()
        grab(q, key, *parts)
        sa = page.findChild(QScrollArea)
        if sa is not None and sa.widget() is not None and sa.widget().height() > sa.viewport().height():
            grab(sa.widget(), key, *parts, "full")

    def walk(key, page, widget, *parts):
        tabs = _top_tabs(widget)
        if not tabs:
            grab_page(key, page, *parts)
            return
        for tw in tabs:                                   # nested tabs (statistics): one picture per leaf
            for i in range(tw.count()):
                if not tw.isTabVisible(i):
                    continue
                tw.setCurrentIndex(i)
                walk(key, page, tw.widget(i), *parts, tw.tabText(i).replace("&", ""))

    keys = [k for k, _l in qt_window.PAGES if not pages or k in pages]
    for key in keys:
        q.show_page(key)
        app._poll()
        _settle()
        page = q._page(key)
        walk(key, page, page)
    if not pages or "setup" in pages:
        q.show_setup(True)
        for i in range(len(q.setup.pages)):
            q.setup.go(i)
            _settle()
            grab(q, "setup", i + 1)
        q.show_setup(False)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", help="folder for the PNGs (default: a new temp folder)")
    ap.add_argument("--size", default="1100x760", help="window size WxH (default 1100x760)")
    ap.add_argument("--zoom", type=float, default=1.0, help="ui_zoom (0.9 … 1.5)")
    ap.add_argument("--light", action="store_true", help="light theme instead of dark")
    ap.add_argument("--pages", default="", help="comma list of page keys (+ setup); default: all")
    args = ap.parse_args()
    w, h = (int(v) for v in args.size.lower().split("x"))
    out = args.out or tempfile.mkdtemp(prefix="fogscout-shots-")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("DBDMS_LANG", "de")
    import bench                                  # the throw-away root of the measurements
    root = bench._root()
    _settings(root, args.light, args.zoom)
    from fogscout.app import App
    app = App(root, simulate=os.path.join(root, "sim"))
    app.qt.resize(w, h)
    pages = [p for p in args.pages.split(",") if p]
    files = shoot(app, out, pages or None)
    app.quit()
    for f in files:
        print(f)
    print(f"{len(files)} pictures in {out}")
    return 0 if files else 1


if __name__ == "__main__":
    sys.exit(main())
