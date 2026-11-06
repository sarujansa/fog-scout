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


# ---------------------------------------------------------------- 1.38.42 (user: "zusammenführen"): back from the ZIP
SETTINGS_NAME = "fogscout-einstellungen.json"   # what archive writes for the settings
MAX_ENTRIES = 5000                              # more than a backup of ours ever holds (corpus 300, maps < 200)
MAX_ENTRY_BYTES = 64 * 1024 * 1024              # one file (rounds.jsonl with 5000 rounds ≈ 3 MB, a map picture ≈ 1 MB)
MAX_TOTAL_BYTES = 1024 * 1024 * 1024            # all of it unpacked
_PART = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._()+-]{0,120}$")   # one path part as our own files name them


class NotOurs(ValueError):
    """The ZIP is no backup of this program (or not readable, or bigger than one of ours can be)."""


def _allowed(name: str) -> bool:
    """A member we take: the settings, rounds/official data, or a file one level inside user_maps/ or corpus/ –
    no folders, no "..", no absolute or Windows paths, plain names only."""
    if name == SETTINGS_NAME or name in FILES:
        return True
    parts = name.split("/")
    return len(parts) == 2 and parts[0] in ARCHIVE_DIRS and bool(_PART.match(parts[1])) and parts[1] not in (".", "..")


def _members(z) -> dict:
    """{name: ZipInfo} of the members we take; NotOurs when nothing of ours is in it or it is too big."""
    infos = z.infolist()
    if len(infos) > MAX_ENTRIES:
        raise NotOurs("too many files")
    out = {i.filename: i for i in infos if not i.is_dir() and _allowed(i.filename)}
    if not out or not (set(out) & ({SETTINGS_NAME} | set(FILES))):
        raise NotOurs("no Fog Scout backup")
    if any(i.file_size > MAX_ENTRY_BYTES for i in out.values()) or sum(i.file_size for i in out.values()) > MAX_TOTAL_BYTES:
        raise NotOurs("too big")
    return out


def _read(z, info) -> bytes:
    with z.open(info) as fh:                      # the size in the header is not trusted: never read past the limit
        data = fh.read(MAX_ENTRY_BYTES + 1)
    if len(data) > MAX_ENTRY_BYTES:
        raise NotOurs("too big")
    return data


def _lines(data: bytes):
    for line in data.decode("utf-8", errors="replace").splitlines():
        if line.strip():
            yield line


def _key(t) -> float:
    return round(float(t), 3)


def _plan(data_dir: str, z, members: dict) -> dict:
    """What a merge would add – nothing is written. Rounds and lost rounds by their start (a round that is in
    both stays as it is now: later corrections win), matches by their start, files of user_maps/corpus by name."""
    import json
    from . import history, official
    plan = {"rounds": [], "lost": [], "matches": [], "gaps": [], "files": [], "known": 0,
            "settings": None}
    hist_path = os.path.join(data_dir, history.FILE)
    have = {_key(r.t) for r in history.load(hist_path)} | {_key(d["t"]) for d in history._lost_lines(hist_path)}
    if "rounds.jsonl" in members:
        for line in _lines(_read(z, members["rounds.jsonl"])):
            try:
                d = json.loads(line)
                if isinstance(d, dict) and d.get("lost"):
                    d["t"] = float(d["t"])
                    r, kind = d, "lost"
                else:
                    r, kind = history._round_line(line), "rounds"
            except (ValueError, KeyError, TypeError, RecursionError):
                continue
            if r is None:
                continue
            t = _key(r["t"] if kind == "lost" else r.t)
            if t in have:
                plan["known"] += 1
                continue
            have.add(t)
            plan[kind].append(r)
    off_path = os.path.join(data_dir, official.FILE)
    stored = {round(m.t) for m in official.load(off_path)}
    if "official.jsonl" in members:
        for line in _lines(_read(z, members["official.jsonl"])):
            try:
                d = json.loads(line)
                if isinstance(d, dict) and d.get("gap"):
                    plan["gaps"].append((float(d["from"]), float(d["to"])))
                    continue
                m = official._match_line(line)
            except (ValueError, KeyError, TypeError, RecursionError):
                continue
            if m is None:
                continue
            if round(m.t) in stored:
                plan["known"] += 1
                continue
            stored.add(round(m.t))
            plan["matches"].append(m)
    for name, info in sorted(members.items()):
        if "/" not in name:
            continue
        if os.path.lexists(os.path.join(data_dir, *name.split("/"))):
            plan["known"] += 1
        else:
            plan["files"].append(name)
    if SETTINGS_NAME in members:
        plan["settings"] = _read(z, members[SETTINGS_NAME])
    return plan


def inspect(data_dir: str, path: str) -> dict:
    """What restoring ``path`` would add: {"rounds", "lost", "matches", "files", "known", "settings"} as counts
    (settings: True when the backup holds them). NotOurs for a ZIP that is no backup of ours."""
    import zipfile
    try:
        with zipfile.ZipFile(path) as z:
            p = _plan(data_dir, z, _members(z))
    except (OSError, zipfile.BadZipFile) as e:
        raise NotOurs(str(e)) from e
    return {"rounds": len(p["rounds"]), "lost": len(p["lost"]), "matches": len(p["matches"]),
            "files": len(p["files"]), "known": p["known"], "settings": p["settings"] is not None}


def restore(data_dir: str, path: str, now: float | None = None) -> dict:
    """Merge the backup ``path`` into ``data_dir``: rounds, lost rounds and matches it has and we do not are added
    (what is in both stays as it is now), files of user_maps/ and corpus/ that do not exist yet are written (never
    over an existing one). The settings are not touched – returned as bytes (``"settings"``, None without) for
    the caller to offer. A copy of rounds/official data goes to backup/ first (tag "restore"). Counts as inspect."""
    import zipfile
    from . import history, official
    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as e:
        raise NotOurs(str(e)) from e
    with z:
        members = _members(z)
        plan = _plan(data_dir, z, members)
        if plan["rounds"] or plan["lost"] or plan["matches"]:
            snapshot(data_dir, now=now, tag="restore")
        if plan["rounds"] or plan["lost"]:
            hist_path = os.path.join(data_dir, history.FILE)
            history._rewrite(hist_path, history.load(hist_path) + plan["rounds"],
                             history._lost_lines(hist_path) + plan["lost"])
        if plan["matches"]:
            off_path = os.path.join(data_dir, official.FILE)
            kept = sorted(official.load(off_path) + plan["matches"], key=lambda m: m.t)[-official.KEEP:]
            gaps = sorted(set(official.load_gaps(off_path)) | set(plan["gaps"]))
            official._write(off_path, kept, [g for g in gaps if kept and g[1] >= kept[0].t])
        written = 0
        root = os.path.realpath(data_dir)
        for name in plan["files"]:
            target = os.path.join(data_dir, *name.split("/"))
            folder = os.path.dirname(target)
            os.makedirs(folder, exist_ok=True)
            if os.path.realpath(folder) != os.path.join(root, name.split("/")[0]):
                continue                          # user_maps/ or corpus/ is a link somewhere else: not followed
            try:
                fsops.write_new(target, _read(z, members[name]))
                written += 1
            except FileExistsError:
                plan["known"] += 1
    return {"rounds": len(plan["rounds"]), "lost": len(plan["lost"]), "matches": len(plan["matches"]),
            "files": written, "known": plan["known"], "settings": plan["settings"]}
