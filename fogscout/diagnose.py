"""Collects window/overlay facts for troubleshooting (text to copy & paste)."""
from __future__ import annotations

import ctypes
import os
import platform
import sys
import time

from . import __version__

# 1.38.16 (user's diagnosis: start step "Log 0,48 s" on Windows): __main__ imports CRASH_FILE/keep_crash from here
# before the splash shows – capture (cv2 + numpy) is imported only where the diagnosis text is made
IS_WIN = sys.platform == "win32"


def spotify_match(app) -> str:
    """1.8.36 (user: queue read, 10 titles, but not shown): whether Spotify's current track is the song Windows
    shows – without any title: Spotify knows one / Windows knows one / they match / the player is Spotify."""
    from . import spotify
    sp, now = getattr(app, "spotify", None), getattr(getattr(app, "media", None), "now", None)
    if sp is None or now is None:
        return "Abgleich –"
    up = sp.upnext
    return (f"Abgleich: Spotify-Titel={'ja' if up.title else 'leer'}, Windows-Titel={'ja' if now.title else 'leer'}, "
            f"gleich={spotify.matches(up, now.title, now.artist)}, Player=Spotify:{spotify.is_spotify(now.app)}")


def _win_info(hwnd):
    if not IS_WIN or not hwnd:
        return "—"
    from ctypes import wintypes
    from .capture import describe_window
    u = ctypes.WinDLL("user32", use_last_error=True)
    u.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    u.IsWindowVisible.argtypes = [wintypes.HWND]
    u.IsIconic.argtypes = [wintypes.HWND]
    get_long = u.GetWindowLongPtrW if ctypes.sizeof(ctypes.c_void_p) == 8 else u.GetWindowLongW
    get_long.argtypes = [wintypes.HWND, ctypes.c_int]
    get_long.restype = ctypes.c_ssize_t
    rc = wintypes.RECT()
    u.GetWindowRect(hwnd, ctypes.byref(rc))
    style = get_long(hwnd, -16) & 0xFFFFFFFF
    ex = get_long(hwnd, -20) & 0xFFFFFFFF
    out = (f"hwnd=0x{int(hwnd):x} {describe_window(hwnd)} rect=({rc.left},{rc.top})-({rc.right},{rc.bottom}) "
           f"style=0x{style:08x} exstyle=0x{ex:08x} visible={bool(u.IsWindowVisible(hwnd))} "
           f"iconic={bool(u.IsIconic(hwnd))} topmost={bool(ex & 0x8)} layered={bool(ex & 0x80000)} "
           f"transparent={bool(ex & 0x20)}")
    try:
        u.GetLayeredWindowAttributes.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD),
                                                 ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(wintypes.DWORD)]
        key, alpha, flags = wintypes.DWORD(), ctypes.c_ubyte(), wintypes.DWORD()
        if u.GetLayeredWindowAttributes(hwnd, ctypes.byref(key), ctypes.byref(alpha), ctypes.byref(flags)):
            out += f" layeredAttr(key=0x{key.value:06x}, alpha={alpha.value}, flags={flags.value})"
        else:
            out += " layeredAttr(nicht gesetzt)"
    except Exception as e:  # pragma: no cover
        out += f" layeredAttr(Fehler {e})"
    try:
        u.GetDpiForWindow.argtypes = [wintypes.HWND]
        out += f" dpi={u.GetDpiForWindow(hwnd)}"
    except Exception:
        pass
    return out


def _own_hwnd(app) -> int:
    try:
        return app._qt_hwnd()
    except Exception:
        return 0


def home_short(path) -> str:
    """1.28 (audit F13): a folder for the diagnosis – the user's home folder as "~" (it holds the account name)."""
    path = str(path or "")
    home = os.path.expanduser("~")
    if home and home not in ("~", os.sep):
        for h in {home, os.path.normcase(home)}:
            if os.path.normcase(path).startswith(os.path.normcase(h)):
                rest = path[len(h):]
                if not rest or rest[0] in "\\/":
                    return "~" + rest
    return path


def home_masked(text) -> str:
    """1.38.57 (security review): the home folder as "~" anywhere in a text (log lines, crash stacks) – not only
    at the start like home_short. Case-insensitive on Windows; only whole folder names (the next character is a
    separator, a quote or the end), so "C:\\Users\\Saru" never eats the start of "C:\\Users\\Saruman"."""
    text = str(text or "")
    home = os.path.expanduser("~").rstrip("\\/")
    if not home or home in ("~",) or len(home) < 3 or home.lower() not in text.lower():
        return text
    import re
    pattern = re.compile(re.escape(home) + r"(?=$|[\\/\s\"':;,)\]])", re.IGNORECASE if IS_WIN else 0)
    return pattern.sub("~", text)


def _qt_version() -> str:
    try:
        import PySide6
        from PySide6.QtCore import qVersion
        return f"{qVersion()} (PySide6 {PySide6.__version__})"
    except Exception as e:  # pragma: no cover
        return f"? ({e})"


def collect(app) -> str:
    from .capture import find_game_window, foreground_root, is_above, window_kind
    lines = [f"Fog Scout {__version__} – Diagnose {time.strftime('%Y-%m-%d %H:%M:%S')}",
             f"Python {sys.version.split()[0]} · Qt {_qt_version()} · {platform.platform()}"]
    try:
        import cv2, mss, numpy, onnxruntime, PIL
        lines.append(f"numpy {numpy.__version__} · opencv {cv2.__version__} · onnxruntime {onnxruntime.__version__} · "
                     f"Pillow {PIL.__version__} · mss {mss.__version__}")
    except Exception as e:
        lines.append(f"Pakete: {e}")
    if IS_WIN:
        try:
            u = ctypes.windll.user32
            lines.append(f"Bildschirm {u.GetSystemMetrics(0)}×{u.GetSystemMetrics(1)}, virtuell "
                         f"{u.GetSystemMetrics(78)}×{u.GetSystemMetrics(79)} ab ({u.GetSystemMetrics(76)},{u.GetSystemMetrics(77)}), "
                         f"Monitore {u.GetSystemMetrics(80)}")
        except Exception:
            pass
    game = find_game_window()
    lines.append(f"Spiel: {game}")
    if game:
        lines.append(f"  {_win_info(game.hwnd)}")
    ov = app.overlay
    oh = ov.hwnd()
    lines.append(f"Overlay: {_win_info(oh)}")
    lines.append(f"  Art: {type(ov).__name__}  letzter Fehler: {getattr(ov, 'last_error', '') or '—'}")
    win = getattr(ov, "win", None)
    if win is not None:                         # the Qt overlay (fallback)
        try:
            g = win.geometry()
            lines.append(f"  qt: sichtbar={win.isVisible()} geometrie=({g.x()},{g.y()} {g.width()}×{g.height()}) "
                         f"dpr={win.devicePixelRatioF()}")
        except Exception as e:
            lines.append(f"  qt: {e}")
    lines.append(f"  shown={ov.shown} pos={ov._pos} hat_map={ov.has_map()} transparent={ov.transparent} "
                 f"über_spiel_gehoben={ov.raised_over_game}×")
    if game and oh:
        lines.append(f"Z-Reihenfolge: Overlay über Spiel = {is_above(oh, game.hwnd)}")
    own = {h for h in (oh, _own_hwnd(app)) if h}
    lines.append(f"Vordergrund: {window_kind(foreground_root(), own)}")     # 1.28: never another program's title
    if IS_WIN:
        from . import appid
        link = appid.start_menu_link()
        lines.append(f"Taskleiste: App-ID={appid.process_app_id() or '—'}  Startmenü-Verknüpfung="
                     f"{(appid.link_app_id(link) or 'ohne App-ID') if os.path.exists(link) else 'fehlt'}")
    lines.append(f"Status: map={app.current} quelle={app.source} sichtbar_gewünscht={app.user_visible} "
                 f"nach_match_aus={app.hidden_after_match} edit={ov.editing} zustand={getattr(app, '_vis_state', None)} "
                 f"letzte_position={getattr(app, '_last_place', None)}")
    lines.append(f"Einstellungen overlay: {app.settings['overlay']}")
    lines.append(f"Einstellungen Erkennung: auto={app.settings.get('auto_detect')} "
                 f"nach_runde_aus={app.settings.get('hide_after_match')} menü_pause={app.settings.get('pause_in_menus')} "
                 f"sprachen={app.settings.get('languages')}")
    moved = sorted(app.settings.get("tab_order") or {})          # 1.8.70: dragged tabs (AutoPage.visible_keys)
    lines.append(f"Reiter umsortiert: {', '.join(moved) if moved else 'nein'}")
    w = getattr(app, "worker", None)
    if w is not None:
        lines.append(f"Rundenende-Erkennung: {w.watch_status}  (Menü pausiert={getattr(app, 'menu_paused', None)}, "
                     f"Überwachung={w.watch_gen}, Overlay-Rechteck={w.overlay_rect})")
        lines.append(f"Banner-Scans: {getattr(w, 'scan_rate', 0):.0f}/s")
        lines.append(f"Aufnahme: {getattr(w, 'capture_info', '?')}  (Fensteraufnahme erlaubt="
                     f"{app.settings.get('window_capture', True)})")
        q = getattr(w, "queue", None)
        lines.append(f"Lobby: letzter Blick {getattr(w, 'lobby_info', '?')} · Zustand "
                     f"{getattr(q, 'state', '?')}, Rolle {getattr(q, 'role', None)}, "
                     f"Crossplay aus={getattr(q, 'crossplay_off', None)} (Blicke mit/ohne Kreuz "
                     f"{getattr(q, 'cross_looks', None)}), letzte Lobby={getattr(q, 'found', None)}, "
                     f"Blicke ohne neues Lesen {getattr(getattr(w, 'lobby_steady', None), 'reused', 0)}")
        lines.append(f"Matchbeginn (Aufnahme ab Ladebildschirm): {w.match_start.describe()}"
                     if getattr(w, "match_start", None) is not None else "Matchbeginn: –")
        bp = getattr(app, "bloodpoints", None)               # 1.13: balance from the lobby, cap check
        lines.append(f"Blutpunkte: {bp.describe() if bp is not None else '–'} · letzter Blick "
                     f"{getattr(w, 'bp_info', '–')}")
        lines.append(f"Runde: {getattr(app, '_hist', None)} · Lobby der App: "
                     f"{ {k: v for k, v in getattr(app, '_queue', {}).items() if k != 'since'} }")
        try:                                                  # 1.38.29: the corpus of decided banners
            from . import corpus
            rep = getattr(app, "_corpus_last", None)
            lines.append(f"Korpus: {corpus.count(app.data_dir)} Banner" + (
                f" · letzte Prüfung {rep.hits}/{rep.total} ({rep.broken} unlesbar, {rep.seconds:.1f} s)" if rep else
                " · noch nicht geprüft"))
        except Exception as e:
            lines.append(f"Korpus: {e}")
        seen = list(getattr(w, "banner_history", []))
        lines.append(f"Letzte Banner ({len(seen)}):" if seen else "Letzte Banner: keine")
        lines.extend("  " + h for h in seen)
        miss = list(getattr(w, "role_misses", []))           # 1.11.1
        lines.append(f"Rolle nicht gelesen (Ergebnisbildschirm, debug/result, {len(miss)}):" if miss
                     else "Rolle nicht gelesen: nie seit Start")
        lines.extend("  " + m for m in miss)
        hist = list(getattr(w, "end_history", []))
        lines.append(f"Letzte Prüfungen ({len(hist)}):" if hist else "Letzte Prüfungen: keine")
        lines.extend("  " + h for h in hist[-40:])
    pres = getattr(app, "presence", None)
    rec = getattr(app, "recorder", None)                 # 1.8.31: the REC dot shows only while this records
    if rec is not None:
        lines.append(f"OBS-Aufnahme: an={bool(app.settings.get('rec_on', False))} nimmt_auf={rec.recording} "
                     f"REC-Punkt={getattr(getattr(app, 'overlay', None), '_rec', None)} "
                     f"Status={getattr(rec, 'status', '') or '–'} "
                     f"Overlay-Bild={bool(app.settings.get('rec_overlay', False))}/"
                     f"{getattr(getattr(app, '_overlay_writer', None), 'writes', 0)}")
    lines.append(f"Discord: {getattr(pres, 'status', '–')} (an={app.settings.get('discord_on')}, "
                 f"ID gesetzt={bool(app.settings.get('discord_client_id'))}, Zustand={getattr(pres, 'state', None)})")
    sp = getattr(app, "spotify", None)
    if sp is not None:
        lines.append(sp.diag_line() + f" (Position={app.settings['overlay'].get('media_next_pos')}, "
                     f"ID gesetzt={bool(app.settings.get('spotify_client_id'))}, "
                     f"{spotify_match(app)})")
    yt = getattr(app, "youtube", None)
    if yt is not None:
        lines.append(yt.diag_line() + f" (ID gesetzt={bool(app.settings.get('youtube_client_id'))}, "
                     f"Sichtbarkeit={app.settings.get('youtube_privacy')})")
    clock = getattr(app, "start_clock", None)             # 1.35: how long the start took, in phases
    if clock is not None:
        lines.append(clock.diag())
    if hasattr(app, "_claude_diag"):                      # 1.26: counts only – never the key or a question
        lines.append(app._claude_diag())
    mon = getattr(app, "sysmon", None)
    if mon is not None:
        lines.append(mon.diag_line() + f" (Anzeige={app.settings.get('sysinfo')}, Rechteck="
                     f"{getattr(getattr(app, 'worker', None), 'hud_rect', None)})")
    own = getattr(app, "selfload", None)                 # 1.11.3: what the program itself costs
    if own is not None:
        lines.append(own.diag_line())
    med = getattr(app, "media", None)
    if med is not None:
        lines.append(med.diag_line() + f" (Anzeige={app.settings['overlay'].get('show_media')})")
    conn = getattr(app, "conn", None)
    if conn is not None:
        lines.extend(conn.diag_lines())
    try:
        lines.extend(app._official_diag())
    except Exception as e:
        lines.append(f"Offizielle Daten: {e}")
    tt = getattr(app, "_ticktimes", None)                 # 1.8.31: where the overlay's tick spends its time
    if tt is not None:
        lines.append(tt.line())
    wk = getattr(app, "worker", None)                    # 1.38.22: the detection's looks and its thread's CPU
    if getattr(wk, "times", None) is not None:
        lines.append(wk.times.line())
        lines.append(wk.cpu.line())
    errs = getattr(app, "_errors_seen", set())
    counts = getattr(app, "_error_counts", {}) or {}                 # 1.38.9: how often each kind came
    lines.append("Fehler seit Start: " + (", ".join(f"{k} {counts.get(k, 1)}×" for k in sorted(errs)) if errs
                                          else "keine"))
    data = getattr(app, "data_dir", None) or getattr(app, "root_dir", None)    # 1.30.1: crash files live there
    if data:
        lines.extend(crash_lines(data))
    root = getattr(app, "root", None)
    lines.extend(lag_lines(getattr(root, "slow", ()), getattr(root, "worst", ())))
    return "\n".join(lines)


CRASH_FILE = "fogscout-crash.txt"            # 1.8.66: faulthandler of the running program (empty = no crash)
CRASH_LAST = "fogscout-crash-last.txt"       # what the run before this one left there: it crashed hard
CRASH_LINES = 30


def keep_crash(root: str):
    """At start: a non-empty crash file is the last run's hard crash – kept as CRASH_LAST (the previous one goes)."""
    path = os.path.join(root, CRASH_FILE)
    try:
        if os.path.getsize(path) > 0:
            os.replace(path, os.path.join(root, CRASH_LAST))
    except OSError:
        pass


# 1.36: exception codes faulthandler writes on Windows although nothing crashed – a C++ exception a library catches
# itself (MSVC 0xE06D7363), a thread naming (0x406D1388), debug output (0x40010006, 0x4001000A)
HARMLESS_CODES = ("0xe06d7363", "0x406d1388", "0x40010006", "0x4001000a")


def real_crash(text: str) -> bool:
    """1.36: does a crash file show a real crash? "Fatal Python error", "Segmentation fault" (Linux) or a Windows
    exception other than HARMLESS_CODES – a file with only those is a run Windows ended (shutdown), not a crash."""
    for line in str(text or "").splitlines():
        low = line.strip().lower()
        if low.startswith(("fatal python error", "segmentation fault", "bus error", "illegal instruction")):
            return True
        if low.startswith("windows fatal exception:"):
            if not any(code in low for code in HARMLESS_CODES):
                return True
    return False


def last_crash(root: str):
    """1.36: (time, True) of the kept last crash when it was a real one, else None – for the start's hint."""
    path = os.path.join(root, CRASH_LAST)
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read(200_000)
        return (os.path.getmtime(path), True) if real_crash(text) else None
    except OSError:
        return None


def crash_lines(root: str) -> list:
    """1.8.66 (user: "das Programm crasht ab und zu, wenn ich Videos öffne" – a hard crash left nothing in the log):
    the start of the last hard crash's thread stacks, written by faulthandler."""
    path = os.path.join(root, CRASH_LAST)
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read().strip().splitlines()
        when = time.strftime("%d.%m.%y %H:%M", time.localtime(os.path.getmtime(path)))
    except OSError:
        return ["Letzter harter Absturz: keiner aufgezeichnet"]
    if not text:
        return ["Letzter harter Absturz: keiner aufgezeichnet"]
    more = [f"  … {len(text) - CRASH_LINES} Zeilen mehr in {CRASH_LAST}"] if len(text) > CRASH_LINES else []
    return ([f"Letzter harter Absturz ({when}, {CRASH_LAST}):"]
            + ["  " + home_masked(t) for t in text[:CRASH_LINES]] + more)   # 1.38.57: the stack's paths hold the account name


def _lag_line(t, what, took, late) -> str:
    return (f"  {time.strftime('%H:%M:%S', time.localtime(t))}  {what}  {took:.0f} ms"
            + (f" / {late:.0f} ms" if late >= 1 else ""))


def lag_lines(slow, worst=()) -> list:
    """Fenster-Hänger: Timer/Ereignisse ≥ 30 ms oder ≥ 60 ms zu spät (mainloop.MainLoop.note), neueste zuerst;
    seit 1.8.69 dazu die längsten seit dem Start (im Match verdrängen die Takte mit 30–48 ms sonst alles Ältere)."""
    slow = list(slow)
    if not slow:
        return ["Fenster-Hänger (≥ 30 ms): keine"]
    out = [f"Fenster-Hänger (≥ 30 ms, letzte {len(slow)}; dauerte / zu spät):"]
    out += [_lag_line(*e) for e in reversed(slow)]
    worst = list(worst)
    if worst:
        out.append(f"Längste Fenster-Hänger seit dem Start ({len(worst)}; dauerte / zu spät):")
        out += [_lag_line(*e) for e in worst]
    return out
