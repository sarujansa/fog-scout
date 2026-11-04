"""1.32 (.exe, stage 4): take over the data of an existing start.bat installation – once, on request, as a copy.

The installer runs ``FogScout.exe --install-tasks`` (elevated) before it points the scheduled task "Fog Scout" at the
.exe. If that task ran start.bat until now, its working directory is the start.bat installation: ``record`` notes the
folder in the data folder. At the first start of the .exe without own settings, ``__main__`` asks once whether to copy
settings, rounds, match data, backups and own map pictures (``copy``); the original folder is only read, never changed
or deleted. Logs, caches and debug pictures stay behind (they are rebuilt). Asked once (``MARKER``), whatever the answer.
"""
from __future__ import annotations

import base64
import os
import shutil
import sys

FILES = ("settings.json", "rounds.jsonl", "official.jsonl")
DIRS = ("backup", "user_maps")
SOURCE_FILE = "takeover-source.txt"         # written by --install-tasks: the start.bat folder
MARKER = "takeover-asked"                   # the question came once


def is_checkout(path) -> bool:
    """A start.bat installation with settings: start.bat, the program package (old or new name) and settings.json."""
    if not path or not os.path.isdir(path):
        return False
    return (os.path.isfile(os.path.join(path, "start.bat")) and os.path.isfile(os.path.join(path, "settings.json"))
            and (os.path.isdir(os.path.join(path, "fogscout")) or os.path.isdir(os.path.join(path, "dbdmapscout"))))


def task_folder_script(name: str) -> str:
    """PowerShell: the working directory of task ``name`` as Base64 of UTF-8 (any path survives the console)."""
    q = "'" + name.replace("'", "''") + "'"
    return (f"$t = Get-ScheduledTask -TaskName {q} -ErrorAction SilentlyContinue\n"
            "if ($t) { [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes([string]$t.Actions[0].WorkingDirectory)) }")


def task_folder(name: str, run=None) -> str | None:
    """The working directory of the scheduled task ``name`` (Windows; reading needs no rights), else None."""
    if sys.platform != "win32" and run is None:
        return None
    from .autostart import powershell
    ok, out = (run or powershell)(task_folder_script(name))
    if not ok or not out.strip():
        return None
    try:
        return base64.b64decode(out.strip().splitlines()[-1]).decode("utf-8") or None
    except (ValueError, UnicodeDecodeError):
        return None


def record(data_dir: str, folder) -> bool:
    """Note a start.bat installation to offer at the first start (only a real one, only if nothing was taken yet)."""
    if not is_checkout(folder) or os.path.exists(os.path.join(data_dir, MARKER)):
        return False
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, SOURCE_FILE), "w", encoding="utf-8") as fh:
        fh.write(os.path.abspath(folder))
    return True


def pending(data_dir: str) -> str | None:
    """The start.bat folder to offer now – None once asked, when the .exe has its own settings, or none was noted."""
    if os.path.exists(os.path.join(data_dir, MARKER)) or os.path.exists(os.path.join(data_dir, "settings.json")):
        return None
    try:
        with open(os.path.join(data_dir, SOURCE_FILE), encoding="utf-8") as fh:
            folder = fh.read().strip()
    except OSError:
        return None
    if os.path.normcase(os.path.abspath(folder)) == os.path.normcase(os.path.abspath(data_dir)):
        return None
    return folder if is_checkout(folder) else None


def copy(src: str, dst: str) -> list[str]:
    """Copy the files and folders worth keeping from ``src`` to ``dst`` – never over an existing file, never deleting
    anything, ``src`` only read. Returns the names that were copied (at least partly)."""
    os.makedirs(dst, exist_ok=True)
    done = []
    for name in FILES:
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isfile(s) and not os.path.exists(d):
            shutil.copy2(s, d)
            done.append(name)
    for name in DIRS:
        top = os.path.join(src, name)
        if not os.path.isdir(top):
            continue
        copied = False
        for base, dirs, files in os.walk(top):
            dirs[:] = [x for x in dirs if not os.path.islink(os.path.join(base, x))]
            rel = os.path.relpath(base, src)
            os.makedirs(os.path.join(dst, rel), exist_ok=True)
            for f in files:
                s = os.path.join(base, f)
                d = os.path.join(dst, rel, f)
                if os.path.isfile(s) and not os.path.islink(s) and not os.path.exists(d):
                    shutil.copy2(s, d)
                    copied = True
        if copied:
            done.append(name + "/")
    return done


def finish(data_dir: str) -> None:
    """The question was answered (either way): never again, the note is gone."""
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, MARKER), "w", encoding="utf-8") as fh:
        fh.write("1")
    try:
        os.remove(os.path.join(data_dir, SOURCE_FILE))
    except OSError:
        pass
