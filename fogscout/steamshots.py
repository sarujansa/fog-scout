"""Steam's screenshots of Dead by Daylight (1.12, user: "Screenshots die ich mit F12 mache" → "lass es ruhig auf
F12"): F12 stays Steam's key, Steam writes the pictures into its own folder – this module only finds that folder and
lists the picture files in it. Read only: nothing there is ever written, renamed or deleted (an edited picture goes
into Fog Scout's own folder, imageedit.out_name). No game files – Steam's screenshot folder holds Steam's own JPGs.

Where: the Steam folder from the registry (HKCU\\Software\\Valve\\Steam, value SteamPath – read, like the OBS folder
in obsrec), then ``userdata/<account>/760/remote/381210/screenshots`` for every account on the PC (381210 = DBD).
A folder of the user's own (Steam can save uncompressed copies elsewhere) can be set instead (``shots_folder``).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

APP_ID = "381210"                    # Dead by Daylight on Steam
EXTENSIONS = (".jpg", ".jpeg", ".png")
LIST_LIMIT = 2000                    # newest pictures listed at most (a folder of years of screenshots)


@dataclass
class Shot:
    path: str
    t: float                         # file time (Steam names them by time too)
    size: int
    source: str = "steam"            # steam | own (a folder set by the user) | edited (Fog Scout's copies)


def steam_path() -> str | None:
    """Steam's folder from the registry (Windows), None elsewhere or when Steam is not installed."""
    if sys.platform != "win32":
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as k:
            path, _kind = winreg.QueryValueEx(k, "SteamPath")
    except OSError:
        return None
    path = os.path.normpath(str(path)) if path else ""
    return path if path and os.path.isdir(path) else None


def shot_dirs(steam: str | None) -> list[str]:
    """DBD's screenshot folders below ``steam`` – one per Steam account that took any."""
    if not steam:
        return []
    root = os.path.join(steam, "userdata")
    try:
        accounts = sorted(os.listdir(root))
    except OSError:
        return []
    out = []
    for acc in accounts:
        if not acc.isdigit():
            continue
        d = os.path.join(root, acc, "760", "remote", APP_ID, "screenshots")
        if os.path.isdir(d):
            out.append(d)
    return out


def list_shots(folders, source: str = "steam", limit: int = LIST_LIMIT) -> list[Shot]:
    """Pictures directly in ``folders`` (not in Steam's "thumbnails" below), newest first, at most ``limit``."""
    shots = []
    for folder in folders:
        try:
            entries = list(os.scandir(folder))
        except OSError:
            continue
        for e in entries:
            if not e.name.lower().endswith(EXTENSIONS):
                continue
            try:
                if not e.is_file(follow_symlinks=False):
                    continue
                st = e.stat(follow_symlinks=False)
            except OSError:
                continue
            shots.append(Shot(e.path, st.st_mtime, st.st_size, source))
    shots.sort(key=lambda s: s.t, reverse=True)
    return shots[:limit]


def folders(settings_folder: str | None, steam: str | None) -> list[tuple[str, str]]:
    """[(folder, source)] to list: the user's own folder when set, else Steam's DBD folders."""
    if settings_folder:
        return [(settings_folder, "own")] if os.path.isdir(settings_folder) else []
    return [(d, "steam") for d in shot_dirs(steam)]


def _steam_areas(steam: str | None) -> list[str]:
    """Steam's DBD screenshot area of every account (``…/760/remote/381210``, its "screenshots" folder or not)."""
    if not steam:
        return []
    root = os.path.join(steam, "userdata")
    try:
        accounts = os.listdir(root)
    except OSError:
        return []
    return [os.path.join(root, acc, "760", "remote", APP_ID) for acc in accounts if acc.isdigit()]


def _inside(path: str, folder: str) -> bool:
    """Is ``path`` ``folder`` or in it (Windows: any case, links followed)?"""
    p, f = (os.path.normcase(os.path.realpath(v)) for v in (path, folder))
    return p == f or p.startswith(f.rstrip(os.sep) + os.sep)


_FROM_REGISTRY = object()


def edit_folder(rec_folder: str | None, steam=_FROM_REGISTRY) -> str:
    """Where edited pictures go: "Screenshots" in the recordings folder, else "Pictures/Fog Scout" of the user –
    never Steam's folder: a recordings folder in Steam's DBD screenshots (``steam``: Steam's folder, from the
    registry when not given) gets "Pictures/Fog Scout" too."""
    own = os.path.join(os.path.expanduser("~"), "Pictures", "Fog Scout")
    if not rec_folder:
        return own
    out = os.path.join(rec_folder, "Screenshots")
    steam = steam_path() if steam is _FROM_REGISTRY else steam
    return own if any(_inside(out, area) for area in _steam_areas(steam)) else out
