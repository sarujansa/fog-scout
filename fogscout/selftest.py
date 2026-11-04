"""1.31 (.exe, stage 3): ``FogScout.exe --selftest <result.json>`` – does the packaged program have everything it needs?

CI builds the program with PyInstaller on Windows and runs this once without a window: a module PyInstaller missed (a
lazy import, a namespace package such as winrt), a data file that did not make it into the folder (maps, models, fonts,
the userscript, HISTORY.md) or ffmpeg from imageio-ffmpeg would otherwise only show on the user's PC. The same check
runs from the source checkout in the test suite (tests/test_selftest.py), so it never drifts from the program.

Nothing is written but the result file, nothing is sent, nothing of the game is touched; the data folder is never
read (settings, rounds). The result: {"ok": bool, "version", "frozen", "root", "passed": [...], "failed": [...]}.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

# files the program reads from its own folder (root_dir) – relative paths
FILES = ("maps.json", "HISTORY.md", "models/ch_PP-OCRv4_rec_infer.onnx", "models/ch_PP-OCRv4_det_infer.onnx",
         "fogscout/matchexport.user.js", "fogscout/fonts/FiraSans-ExtraBold.ttf", "fogscout/fonts/Inter-Regular.otf",
         "fogscout/fonts/Inter-Medium.otf", "fogscout/fonts/Inter-SemiBold.otf", "fogscout/fonts/Inter-Bold.otf")
# third-party modules imported lazily somewhere (only Windows: the ones start.bat installs only there)
LIBRARIES = ("numpy", "cv2", "onnxruntime", "PIL.Image", "mss", "PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets",
             "imageio_ffmpeg")
WIN_LIBRARIES = ("pystray", "winrt.windows.foundation", "winrt.windows.media.control", "winrt.windows.storage.streams",
                 "windows_capture")
MIN_MODULES = 100           # fogscout has 125 modules (1.31); far fewer means PyInstaller left the package out


class Checks:
    def __init__(self):
        self.passed: list[str] = []
        self.failed: list[str] = []

    def run(self, name: str, fn) -> None:
        try:
            note = fn()
        except Exception as e:                       # every failure is one line of the result
            self.failed.append(f"{name}: {type(e).__name__}: {e}")
            return
        self.passed.append(f"{name}: {note}" if note else name)


def _files(root: str) -> str:
    missing = [f for f in FILES if not os.path.isfile(os.path.join(root, *f.split("/")))]
    if missing:
        raise FileNotFoundError(", ".join(missing))
    return f"{len(FILES)} Dateien"


def _map_pictures(root: str) -> str:
    from .catalog import Catalog
    cat = Catalog(root, ("en", "de"))
    paths = {p for m in cat.maps.values() for p in m.variants.values() if p}
    missing = sorted(p for p in paths if not os.path.isfile(os.path.join(cat.maps_dir, p)))
    if missing:
        raise FileNotFoundError(f"{len(missing)} Kartenbilder fehlen, z. B. {missing[0]}")
    if len(cat.maps) < 40:                                  # 45 maps in 1.31
        raise ValueError(f"nur {len(cat.maps)} Maps im Katalog")
    return f"{len(cat.maps)} Maps, {len(paths)} Bilder"


def _modules() -> str:
    import importlib
    import pkgutil
    from . import __path__ as package_path
    names = sorted(m.name for m in pkgutil.iter_modules(package_path) if m.name != "__main__")
    if len(names) < MIN_MODULES or "app" not in names or "hostsedit" not in names or "netwatch" not in names:
        raise ImportError(f"nur {len(names)} Module von fogscout gefunden")
    bad = []
    for name in names:
        try:
            importlib.import_module(f"{__package__}.{name}")
        except Exception as e:
            bad.append(f"{name} ({type(e).__name__}: {e})")
    if bad:
        raise ImportError("; ".join(bad))
    return f"{len(names)} Module"


def _libraries() -> str:
    import importlib
    names = LIBRARIES + (WIN_LIBRARIES if sys.platform == "win32" else ())
    bad = []
    for name in names:
        try:
            importlib.import_module(name)
        except Exception as e:
            bad.append(f"{name} ({type(e).__name__}: {e})")
    if bad:
        raise ImportError("; ".join(bad))
    return f"{len(names)} Bibliotheken"


def _telemetry() -> str:
    if os.environ.get("ORT_DISABLE_TELEMETRY") != "1":       # set by fogscout/__init__.py (CLAUDE.md)
        raise RuntimeError("ORT_DISABLE_TELEMETRY ist nicht 1")
    return ""


def _ocr(root: str) -> str:
    import numpy as np
    from .fullscan import TextDetector
    from .ocr import Recognizer
    rec = Recognizer(os.path.join(root, "models", "ch_PP-OCRv4_rec_infer.onnx"), threads=1)
    probs = rec.probs(np.full((48, 200, 3), 255, np.uint8))
    if probs.ndim != 2 or probs.shape[1] != len(rec.chars):
        raise ValueError(f"unerwartete Ausgabe {probs.shape}")
    TextDetector(os.path.join(root, "models", "ch_PP-OCRv4_det_infer.onnx"), threads=1)
    return f"{len(rec.chars)} Zeichen"


def _ffmpeg() -> str:
    from .obsrec import ffmpeg_exe
    exe = ffmpeg_exe()
    if not exe:
        raise FileNotFoundError("ffmpeg von imageio-ffmpeg fehlt")
    r = subprocess.run([exe, "-hide_banner", "-version"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg -version: Code {r.returncode}")
    return (r.stdout.decode("utf-8", "replace").splitlines() or [""])[0][:60]


def _qt() -> str:
    from .qt_app import application
    app = application()
    from PySide6.QtGui import QFontDatabase
    families = QFontDatabase.families()
    if not any("Fira" in f for f in families):              # qt_app loads FiraSans from fogscout/fonts
        raise FileNotFoundError("Schrift Fira Sans nicht geladen")
    return app.platformName()


def run(root: str) -> dict:
    from . import __version__
    from .paths import frozen
    c = Checks()
    c.run("Dateien", lambda: _files(root))
    c.run("Kartenbilder", lambda: _map_pictures(root))
    c.run("Bibliotheken", _libraries)
    c.run("Module", _modules)
    c.run("Telemetrie aus", _telemetry)
    c.run("OCR", lambda: _ocr(root))
    c.run("ffmpeg", _ffmpeg)
    c.run("Qt", _qt)
    return {"ok": not c.failed, "version": __version__, "frozen": frozen(), "root": root,
            "passed": c.passed, "failed": c.failed}


def main(root: str, out: str) -> int:
    """Write the result to ``out`` (a windowed .exe has no console); 0 = everything there."""
    try:
        res = run(root)
    except Exception as e:                                  # the check itself broke: still a result file
        res = {"ok": False, "failed": [f"Selbsttest: {type(e).__name__}: {e}"], "passed": []}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    return 0 if res["ok"] else 1
