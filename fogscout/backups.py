"""Daily snapshots of the round history (1.8.80): rounds.jsonl and official.jsonl copied into backup/.

Pure. ``snapshot`` copies each file once per day – and only when its content differs from the newest copy – to
``backup/<stem>-YYYY-MM-DD.jsonl`` and keeps the newest ``KEEP`` copies per file; "Verlauf löschen" takes one
more copy first (``tag``). Nothing is read back by the program: the copies are for the user (a broken file, a
wrong click)."""
from __future__ import annotations

import hashlib
import os
import re
import time

from . import fsops

DIR = "backup"
KEEP = 14                                   # copies kept per file (the newest)
FILES = ("rounds.jsonl", "official.jsonl")  # history.FILE, official.FILE
_NAME = re.compile(r"^(?P<stem>[a-z]+)-(?P<day>\d{4}-\d{2}-\d{2})(?:-[a-z]+)?\.jsonl$")


def _digest(path: str):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def copies(folder: str, stem: str) -> list:
    """The copies of one file in ``folder``, oldest first (the names sort by day)."""
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    return sorted(n for n in names if (m := _NAME.match(n)) and m.group("stem") == stem)


def snapshot(root: str, now: float | None = None, tag: str = "") -> dict:
    """Copy the files of ``root`` that exist and changed; prune. {"copied": [names], "pruned": [names], "day"}.
    With ``tag`` (letters) the copy is taken even when today's exists – before the history is cleared."""
    folder = os.path.join(root, DIR)
    day = time.strftime("%Y-%m-%d", time.localtime(time.time() if now is None else now))
    out = {"copied": [], "pruned": [], "day": day}
    for name in FILES:
        src = os.path.join(root, name)
        if not os.path.isfile(src):
            continue
        stem = name.split(".")[0]
        target = f"{stem}-{day}{'-' + tag if tag else ''}.jsonl"
        had = copies(folder, stem)
        if target in had:
            continue
        if had and not tag and _digest(os.path.join(folder, had[-1])) == _digest(src):
            continue                                                    # nothing new since the last copy
        try:
            os.makedirs(folder, exist_ok=True)
            with open(src, "rb") as fh:           # 1.38.5: was copy2 + replace without fsync – a power cut right
                data = fh.read()                    # after could leave an empty backup of the very file it guards
            fsops.write_atomic(os.path.join(folder, target), data)
        except OSError:
            continue
        out["copied"].append(target)
        for old in copies(folder, stem)[:-KEEP]:
            try:
                os.remove(os.path.join(folder, old))
                out["pruned"].append(old)
            except OSError:
                pass
    return out


def status(root: str) -> tuple:
    """(number of copies, day of the newest or "") – for the settings' hint."""
    folder = os.path.join(root, DIR)
    all_names = [n for name in FILES for n in copies(folder, name.split(".")[0])]
    days = sorted(_NAME.match(n).group("day") for n in all_names)
    return len(all_names), days[-1] if days else ""


# ---------------------------------------------------------------- 1.38.32 (project review F8): everything in one ZIP
ARCHIVE_FILES = FILES + ("corpus",)            # the own data a user wants to move or keep (corpus: folder)
ARCHIVE_DIRS = ("user_maps", "corpus")


def archive(data_dir: str, dest: str, settings: dict) -> int:
    """The program's own data into the ZIP ``dest`` (the user's file): rounds and match data, the settings as
    "Einstellungen exportieren" writes them (no secrets, no PC-specific values), own map pictures and the banner
    corpus. Logs, caches and recordings stay out. Returns the number of files."""
    import json
    import zipfile
    from .config import EXPORT_SKIP, LOCAL_KEYS, SECRET_KEYS
    clean = {k: v for k, v in settings.items() if k not in SECRET_KEYS and k not in EXPORT_SKIP and k not in LOCAL_KEYS}
    n = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("fogscout-einstellungen.json", json.dumps(clean, indent=2, ensure_ascii=False))
        n += 1
        for name in FILES:
            p = os.path.join(data_dir, name)
            if os.path.isfile(p):
                z.write(p, name)
                n += 1
        for sub in ARCHIVE_DIRS:
            top = os.path.join(data_dir, sub)
            for folder, dirs, files in os.walk(top):
                dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(folder, d))]
                for f in sorted(files):
                    p = os.path.join(folder, f)
                    if os.path.islink(p) or not os.path.isfile(p):
                        continue
                    z.write(p, os.path.relpath(p, data_dir).replace(os.sep, "/"))
                    n += 1
    return n
