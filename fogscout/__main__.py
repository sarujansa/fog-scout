"""Start: python -m fogscout [--simulate BILD|ORDNER] [--test BILD ...]"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import traceback

from . import __version__, i18n
from .i18n import _

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _data() -> str:
    """1.30.1 (.exe, stage 2): where the runtime files go – ROOT from start.bat (as before), the per-user data folder
    for the installed program (paths.data_root)."""
    from .paths import data_root
    return data_root(ROOT)


def _setup_logging(data=None):
    data = data or _data()
    moved = []
    if data == ROOT:                           # only a source checkout ever had the old name's files
        from .rename import migrate
        moved = migrate(ROOT)                  # 1.9: crash files/log/icon of the old name, before the log opens
    logging.basicConfig(
        filename=os.path.join(data, "fogscout.log"), filemode="w", level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8")
    if moved:
        logging.getLogger("fogscout").info("Alte Dateien von DbD Map Scout übernommen: %s", ", ".join(moved))
    _enable_crash_log(data)


_crash_fh = None


def _enable_crash_log(root=ROOT):
    """1.8.66: a hard crash (Qt/C level – the process just goes) leaves no line in the log; faulthandler writes
    every thread's stack to diagnose.CRASH_FILE then. The last run's crash is kept first (diagnose.keep_crash) and
    "Diagnose kopieren" shows it."""
    global _crash_fh
    import faulthandler
    from .diagnose import CRASH_FILE, keep_crash
    keep_crash(root)
    try:
        _crash_fh = open(os.path.join(root, CRASH_FILE), "w", encoding="utf-8")
        faulthandler.enable(_crash_fh, all_threads=True)
    except OSError:
        _crash_fh = None


def _crash_log_clear(root=ROOT):
    """A normal end: nothing crashed. On Windows faulthandler also writes C++ exceptions a library catches itself
    (Qt, pywinrt) – the file only stays when the process did not get here."""
    import faulthandler
    from .diagnose import CRASH_FILE
    global _crash_fh
    if _crash_fh is None:
        return
    faulthandler.disable()
    try:
        _crash_fh.close()
        os.remove(os.path.join(root, CRASH_FILE))
    except OSError:
        pass
    _crash_fh = None


_mutex = None
ERROR_ACCESS_DENIED = 5
ERROR_ALREADY_EXISTS = 183


def _claim_mutex(name: str) -> bool:
    """True if no other copy holds the single-instance mutex. A copy running as administrator (autostart
    task, desktop shortcut) owns a mutex that a normal copy (start.bat double-clicked) may not open:
    CreateMutexW then fails with ERROR_ACCESS_DENIED instead of ERROR_ALREADY_EXISTS – another copy, too."""
    global _mutex
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    k32.CreateMutexW.restype = wintypes.HANDLE
    _mutex = k32.CreateMutexW(None, False, name)
    return ctypes.get_last_error() not in (ERROR_ALREADY_EXISTS, ERROR_ACCESS_DENIED)


def _message(text: str, error: bool = False):
    """A message box without a window of our own (Windows), else stderr."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, text, "Fog Scout", 0x10 if error else 0x40)
            return
        except Exception:
            pass
    print(text, file=sys.stderr)


def _single_instance() -> bool:
    """Only one running copy (a second one could not register the hotkeys)."""
    if sys.platform != "win32":
        return True
    from .restart import MUTEX_NAME, ask_running_copy_to_show, process_name
    if not _claim_mutex(MUTEX_NAME):
        if ask_running_copy_to_show():            # 1.65.1: the running copy brings its window to the front
            return False
        _message(_("Fog Scout läuft bereits, reagiert aber nicht (oder ist gerade beim Beenden).\n\n"
                   "Kurz warten und nochmal starten. Hilft das nicht: im Task-Manager unter „Details“ "
                   "„{exe}“ (Fog Scout) beenden.", exe=process_name()))
        return False
    return True


def run_test(paths, languages):
    """Offline check: run the detector on screenshots and print what it reads."""
    import cv2
    import numpy as np
    from .catalog import Catalog
    from .detector import ROI, BannerReader
    from .ocr import Recognizer
    cat = Catalog(ROOT, languages)
    reader = BannerReader(Recognizer(os.path.join(ROOT, "models", "ch_PP-OCRv4_rec_infer.onnx")), cat)
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(os.path.join(p, f) for f in os.listdir(p)
                            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")))
        else:
            files.append(p)
    for f in files:
        img = cv2.imdecode(np.fromfile(f, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            print(f"{f}: kann nicht gelesen werden")
            continue
        h, w = img.shape[:2]
        roi = img[int(ROI[1] * h):int(ROI[3] * h), int(ROI[0] * w):int(ROI[2] * w)]
        sep, res = reader.read(roi, w, h)
        if sep is None:
            print(f"{os.path.basename(f)}: kein Map-Banner gefunden")
        elif res is None:
            print(f"{os.path.basename(f)}: Banner gefunden, aber kein Text lesbar")
        else:
            m = cat.maps[res.best[0]]
            ok = "OK " if res.name_fit >= -9 else "?? "
            print(f"{os.path.basename(f)}: {ok}{m.label(res.best[1])}  (gelesen: '{res.name_text}' / "
                  f"'{res.realm_text}', Passung {res.name_fit:.1f}, {res.ms:.0f} ms)")


def _log_thread_deaths():
    """1.16.1 (audit): an exception that ends a thread goes to sys.stderr by default – under pythonw.exe that is
    None and the traceback is thrown away (faulthandler only covers crashes of the C level). Into the log instead,
    with the thread's name, so a dead recorder, uploader or player thread is at least visible there."""
    import threading
    logger = logging.getLogger("fogscout")

    def hook(args):
        logger.error("Thread %s beendet durch Ausnahme", getattr(args.thread, "name", "?"),
                     exc_info=(args.exc_type, args.exc_value, args.exc_traceback))
    threading.excepthook = hook


HELPER_MODULES = ("hostsedit", "netwatch")      # = regions.HELPERS (test_frozen)


def run_helper(argv) -> int:
    """1.31 (.exe, stage 3): ``FogScout.exe --helper <name> <file> <file>`` – the packaged program has no loose .py
    files, so the elevated helpers (regions.helper_command) are the program itself with this first argument. Only the
    two helpers, only their own two file arguments; nothing else of the program starts (no window, no mutex, no log)."""
    if not argv or argv[0] not in HELPER_MODULES:
        return 2
    if argv[0] == "hostsedit":
        from . import hostsedit as helper
    else:
        from . import netwatch as helper
    return helper.main([argv[0] + ".py", *argv[1:]])


def _autostart_wanted(data: str) -> bool:
    """The user's choice in settings.json (default on) – a reinstall keeps an autostart that was switched off."""
    import json
    try:
        with open(os.path.join(data, "settings.json"), encoding="utf-8") as fh:
            return json.load(fh).get("autostart", True) is not False
    except (OSError, ValueError, AttributeError):
        return True


def install_tasks() -> int:
    """1.32 (.exe, stage 4): ``FogScout.exe --install-tasks`` – run by the installer with administrator rights. Notes a
    start.bat installation the task "Fog Scout" ran until now (takeover, offered at the first start), then points the
    tasks and the Start menu/desktop shortcuts at the .exe; the logon task unless autostart was switched off."""
    from . import autostart, takeover
    if not autostart.for_session_user():
        # 1.33.1 (audit H-4): elevated with another administrator's credentials – nothing in that account; one Start
        # menu shortcut for everybody instead (no task: Windows asks when an administrator function is used)
        exe = autostart.frozen_exe()
        ok = bool(exe) and autostart.powershell(autostart.common_shortcut_script(exe))[0]
        return 0 if ok else 1
    data = _data()
    takeover.record(data, takeover.task_folder(autostart.TASK))
    ok, _msg = autostart.install(ROOT)
    if ok and _autostart_wanted(data):
        ok, _msg = autostart.set_autostart(ROOT, True)
    return 0 if ok else 1


def remove_tasks() -> int:
    """1.32: ``FogScout.exe --remove-tasks`` – the uninstaller: tasks and shortcuts go, the data folder stays."""
    from . import autostart
    return 0 if autostart.uninstall()[0] else 1


def offer_takeover(data: str, ask=None) -> list:
    """1.32: the first start of the .exe without own settings – copy a start.bat installation's data on request
    (takeover.py; asked once, the original only read). ``ask(text) -> bool`` for tests. Returns what was copied."""
    from . import takeover
    folder = takeover.pending(data)
    if not folder:
        return []
    text = _("Fog Scout wurde bisher über start.bat genutzt:\n{folder}\n\nEinstellungen, Runden, Match-Daten, "
             "Sicherungen und eigene Kartenbilder in die installierte Version übernehmen? Der alte Ordner bleibt "
             "unverändert.", folder=folder)
    if not (ask or _ask_yes_no)(text):
        takeover.finish(data)                    # "No": never asked again
        return []
    copied = takeover.copy(folder, data)         # 1.33.1 (audit H-1): an OSError leaves the note – asked again
    takeover.finish(data)
    return copied


def _ask_yes_no(text: str) -> bool:
    if sys.platform != "win32":
        return False
    import ctypes
    return ctypes.windll.user32.MessageBoxW(None, text, "Fog Scout", 0x4 | 0x20) == 6     # MB_YESNO|QUESTION, IDYES


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--helper":      # before anything else: runs with administrator rights
        sys.exit(run_helper(sys.argv[2:]))
    if len(sys.argv) == 2 and sys.argv[1] in ("--install-tasks", "--remove-tasks"):   # 1.32: the installer
        sys.exit(install_tasks() if sys.argv[1] == "--install-tasks" else remove_tasks())
    from .starttime import StartClock
    clock = StartClock()                          # 1.35: the start's phases (log line, diagnosis, self-check)
    ap = argparse.ArgumentParser(prog="fogscout")
    ap.add_argument("--simulate", help="Screenshots statt Bildschirm verwenden (Datei oder Ordner)")
    ap.add_argument("--test", nargs="+", help="Nur testen: Screenshots auswerten und Ergebnis ausgeben")
    ap.add_argument("--lang", default="en,de", help="Sprachen für --test, z.B. en,de")
    ap.add_argument("--tray", action="store_true", help="im Infobereich starten (Autostart mit Windows)")
    ap.add_argument("--restart", action="store_true", help=argparse.SUPPRESS)   # helper of the update button
    ap.add_argument("--no-update", action="store_true", help=argparse.SUPPRESS)  # with --restart: plain restart
    ap.add_argument("--selftest", metavar="RESULT", help=argparse.SUPPRESS)      # 1.31: CI checks the packaged .exe
    args = ap.parse_args()

    if args.selftest:
        from .selftest import main as selftest
        sys.exit(selftest(ROOT, args.selftest, clock))

    if args.restart:
        from .restart import wait_and_start
        wait_and_start(ROOT, update=not args.no_update)
        return

    if args.test:
        run_test(args.test, [l.strip() for l in args.lang.split(",") if l.strip()])
        return

    from .appid import set_process_app_id
    set_process_app_id()                          # before the first window: own taskbar button and icon
    data = _data()
    i18n.init_from_settings(os.path.join(data, "settings.json"))
    if not _single_instance():
        return
    taken = []
    if data != ROOT:                              # 1.32: the installed program – a start.bat installation to take over
        try:
            taken = offer_takeover(data)
        except OSError as e:
            _message(_("Übernahme fehlgeschlagen: {error}", error=e), error=True)
        if taken:
            i18n.init_from_settings(os.path.join(data, "settings.json"))     # the taken-over language
    _setup_logging(data)
    if taken:
        logging.getLogger("fogscout").info("Aus der start.bat-Installation übernommen: %s", ", ".join(taken))
    _log_thread_deaths()
    from .capture import enable_dpi_awareness
    enable_dpi_awareness()
    splash = None
    if not args.tray:                             # 1.14.2: the splash screen – not for the silent start in the tray
        from .splash import start as splash_start
        splash = splash_start(data, __version__)
    clock.mark("splash")
    try:
        from .app import App
        clock.mark("loaded")
        app = App(ROOT, simulate=args.simulate, start_in_tray=args.tray,
                  progress=splash.progress if splash is not None else None, data_dir=data, start_clock=clock)
        clock.mark("built")
        if splash is not None:
            splash.finish()                       # fades while the window comes up (App.run pumps the events)
        app.exit_watchdog = True                  # a quit that hangs ends the process anyway
        app.run()
    except Exception:
        if splash is not None:
            splash.close()                        # never over the error message
        text = traceback.format_exc()
        logging.getLogger("fogscout").error(text)
        _message(_("Start fehlgeschlagen:") + "\n\n" + text[-1500:], error=True)
        sys.exit(1)
    # 1.65.1 (user: after an update the program did not come back, a click said "läuft bereits"): end the
    # process now. Settings are saved in App.quit; a thread that does not stop (tray icon, window capture)
    # or a hang while Python shuts down would keep the process – and its single-instance mutex – alive.
    logging.getLogger("fogscout").info("Beendet.")
    _crash_log_clear(data)
    logging.shutdown()
    os._exit(0)


if __name__ == "__main__":
    main()
