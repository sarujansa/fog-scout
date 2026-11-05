"""Fog Scout's own recording files, without OBS (1.38.34+, project review ARCH-3: split from obsrec.py, whose
Recorder thread talks to OBS): file names, the recordings index (``Recording``, ``load_index``/``save_index``,
``INDEX``), the clips list (``Clip``, ``load_clips``/``save_clips``, ``list_clips``, ``adopt_clip``), pruning
(``prune``/``prune_rank``/``prune_farming`` – deleting only through ``fsops.delete_inside``), filters
(``select_recordings``/``select_clips``), ``settle_parts`` and ``space``. Writes stay with the Recorder thread
(the one writer of both indices). obsrec re-exports every name.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import struct
import time
from dataclasses import asdict, dataclass, field

from . import fsops
from .fsops import rel_path
from .i18n import _

INDEX = "fogscout-recordings.jsonl"
OLD_INDEX = "dbdmapscout-recordings.jsonl"     # 1.9: the name until 1.8.91 – taken over when first read
RESERVE = 10 * 1024 ** 3        # free space kept on the drive: older recordings go before it is used up
SHORT_ROUND_S = 300             # 1.4.2: rounds shorter than this go first when room is needed
NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
CLIPS_DIR = "Clips"              # 1.5.3: clips (editor, F8 instant clips) beside the recordings


def file_name(t: float, label: str, who: str, ext: str, suffix: str = "") -> str:
    """'2026-10-17 21-40 Coal Tower – Nurse.mkv' – no characters Windows forbids."""
    stamp = time.strftime("%Y-%m-%d %H-%M", time.localtime(t))
    parts = [stamp, NAME_CHARS.sub("", label or "Map").strip() or "Map"]
    name = " ".join(parts) + (f" – {NAME_CHARS.sub('', who).strip()}" if who else "") + suffix
    return name[:150] + ext


# ------------------------------------------------------------------ index
@dataclass
class Recording:
    t: float                     # banner time = the round's key (rounds.jsonl)
    file: str                    # file name in the folder
    pre: str = ""                # pre-roll from the replay buffer ("" = none)
    map_id: str = ""
    label: str = ""
    role: str = ""
    killer: str = ""
    end: float = 0.0
    size: int = 0
    keep: bool = False           # never deleted by the limit
    extra: dict = field(default_factory=dict)
    marks: list = field(default_factory=list)   # 1.4.2: F8 moments, seconds from the start of the file
    farming: bool = False        # 1.4.2: a farming round (cross-play off) – goes first when room is needed
    pre_s: float = 0.0           # 1.4.2: seconds of pre-roll at the start of the file (0 = none or separate)
    yt: str = ""                 # 1.10: the YouTube video id once uploaded (ytupload)


def adopt_old_file(folder: str, old: str, new: str) -> bool:
    """1.9: a file the program wrote under its old name is renamed once (True); nothing when the new one exists."""
    o, n = os.path.join(folder, old), os.path.join(folder, new)
    try:
        if os.path.isfile(o) and not os.path.exists(n):
            os.replace(o, n)
            return True
    except OSError:
        pass
    return False


def load_index(folder: str) -> list[Recording]:
    out = []
    adopt_old_file(folder, OLD_INDEX, INDEX)
    try:
        # 1.12.3: errors="replace" and only objects – a line cut inside a character or one that is no object
        # made the whole index unreadable (pruning, marks and the recordings page failed on every call)
        with open(os.path.join(folder, INDEX), encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if isinstance(d, dict):
                        out.append(Recording(**{k: v for k, v in d.items() if k in Recording.__dataclass_fields__}))
                except (ValueError, TypeError):
                    continue
    except OSError:
        pass
    return out


def save_index(folder: str, recs: list[Recording]):
    text = "".join(json.dumps(asdict(r), ensure_ascii=False) + "\n" for r in sorted(recs, key=lambda r: r.t))
    fsops.write_atomic(os.path.join(folder, INDEX), text.encode("utf-8"))     # 1.38.5 (see history._rewrite)


FARMING_DAYS = (0, 3, 7, 14, 30)      # 1.8.23 (user's pick): farming recordings go after this many days (0 = never)
DEFAULT_FARMING_DAYS = 7
FARMING_CHECK_S = 3600.0              # how often the recorder thread looks for expired ones


def expired_farming(recs: list[Recording], days: int, now: float) -> list[Recording]:
    """1.8.23 (pure): farming recordings older than ``days`` – never kept ones, never ones with a mark (F8)."""
    if not days or days <= 0:
        return []
    limit = now - days * 86400
    return [r for r in recs if r.farming and not r.keep and not r.marks and r.t < limit]


def prune_farming(folder: str, recs: list[Recording], days: int, now: float | None = None):
    """Delete the expired farming recordings (``expired_farming``) – only files named in the index, only inside
    ``folder``. Returns (entries left, files deleted)."""
    gone = expired_farming(recs, days, time.time() if now is None else now)
    deleted = []
    for r in gone:
        for n in (r.file, r.pre):
            p = rel_path(folder, n) if n else None
            if p and os.path.exists(p):
                try:
                    fsops.delete_inside(folder, p)      # 1.33.5 (S2): never through a link out of the folder
                    deleted.append(n)
                except OSError:
                    pass
    gone_ids = {id(r) for r in gone}
    left = [r for r in recs if id(r) not in gone_ids or os.path.exists(rel_path(folder, r.file) or "")]
    return left, deleted


def prune_rank(r: Recording) -> int:
    """1.4.2: what goes first when room is needed – 0 farming rounds and rounds shorter than SHORT_ROUND_S,
    1 ordinary rounds, 2 rounds with a mark (F8); within a rank the oldest first. Kept ones never."""
    if r.marks:
        return 2
    if r.farming or (r.end and 0 < r.end - r.t < SHORT_ROUND_S):
        return 0
    return 1


def prune(folder: str, recs: list[Recording], limit: int, reserve: int = RESERVE,
          free=None) -> tuple[list[Recording], list[str]]:
    """Keep the folder's recordings under ``limit`` bytes (0 = the whole drive) and ``reserve`` bytes free on
    the drive: delete not-kept ones of the index in ``prune_rank`` order (farming/short first, marked last,
    oldest first) – only files named in it, only inside ``folder``.
    Entries whose files are gone drop out. ``free`` = bytes free now (measured when None).
    Returns (entries left, files deleted)."""
    left, deleted = [], []
    for r in recs:
        main = rel_path(folder, r.file)
        if main and os.path.exists(main):
            paths = [p for p in (rel_path(folder, n) for n in (r.file, r.pre) if n) if p and os.path.exists(p)]
            r.size = sum(os.path.getsize(p) for p in paths)
            left.append(r)
    if free is None:
        try:
            free = shutil.disk_usage(folder).free
        except OSError:
            free = reserve
    total = sum(r.size for r in left)
    for r in sorted([r for r in left if not r.keep], key=lambda r: (prune_rank(r), r.t)):
        if (limit <= 0 or total <= limit) and free >= reserve:
            break
        for n in (r.file, r.pre):
            p = rel_path(folder, n) if n else None                        # only inside the folder
            if p:
                try:
                    fsops.delete_inside(folder, p)                        # 1.33.5 (S2): and no link out of it
                    deleted.append(n)
                except OSError:
                    pass
        main = rel_path(folder, r.file)
        if main and os.path.exists(main):   # 1.8.38: not deleted (open in a player): the entry stays and counts –
            continue                        # dropped, the file was an orphan no later pass would ever remove
        total -= r.size
        free += r.size
        left.remove(r)
    return left, deleted


def select_recordings(recs: list[Recording], since: float | None = None, map_label: str | None = None,
                      role: str | None = None, only: str | None = None, hide_farming: bool = False) -> list[Recording]:
    """1.5, tab "Aufnahmen": the index filtered – ``since`` (banner time ≥), map label, role ("killer" /
    "survivor" / "farming" = farming rounds only), ``only`` "marked" / "kept" / "bad", ``hide_farming`` (1.11.5:
    the switch "Farming ausblenden"; 1.8.71–1.11.4 a role left farming rounds out by itself). Newest first."""
    out = []
    for r in recs:
        if since is not None and r.t < since:
            continue
        if map_label and r.label != map_label:
            continue
        if hide_farming and r.farming:
            continue
        if role == "farming":
            if not r.farming:
                continue
        elif role and r.role != role:
            continue
        if only == "marked" and not r.marks:
            continue
        if only == "kept" and not r.keep:
            continue
        if only == "bad" and not (r.extra or {}).get("bad"):
            continue
        out.append(r)
    return sorted(out, key=lambda r: r.t, reverse=True)



# ------------------------------------------------------------------ clips (1.8.13): the list in the tab "Aufnahmen"
CLIPS_INDEX = "fogscout-clips.jsonl"     # in Clips/: what the program made there (only these are deleted)
OLD_CLIPS_INDEX = "dbdmapscout-clips.jsonl"   # 1.9: the name until 1.8.91 – taken over when first read
CLIP_EXTS = (".mp4", ".mkv", ".mov", ".webm", ".flv", ".gif", ".png", ".jpg")   # .gif: the editor's GIFs (1.12)
STILL_EXTS = (".png", ".jpg")
CLIP_KINDS = ("clip", "instant", "still")
_STAMP_RE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d-\d\d) (.+)$")
_COPY_RE = re.compile(r" \(\d+\)$")                     # unique_path / _unique: "name (2)"
PART_EXT = ".tmp"               # 1.12 review: the clip editor's ffmpeg writes "<clip>.mp4.tmp", renamed once whole –
                                # a file still being written is never listed, uploaded or opened
PART_STALE_S = 300.0            # … such a file nobody wrote to for this long was left by a quit or crash mid-save
PARTS_CHECK_S = 60.0            # s between two looks for them (Recorder._settle_parts)
PARTS_WRITING = set()           # part_key of every ".tmp" a save of this process writes now (clipedit) – never touched


@dataclass
class Clip:
    file: str                    # name inside Clips/
    t: float = 0.0               # made at
    kind: str = "clip"           # clip (editor) / instant (F8) / still (picture from the editor)
    source: float = 0.0          # banner time of the round it came from (0 = unknown)
    map_id: str = ""
    label: str = ""
    role: str = ""
    killer: str = ""
    farming: bool = False
    seconds: float = 0.0         # length (0 = unknown / a still)
    size: int = 0                # bytes, filled when listed
    adopted: bool = False        # not in the index: an older version made it (told by its name), never saved
    yt: str = ""                 # 1.10: the YouTube video id once uploaded (ytupload)


def clips_dir(folder: str) -> str:
    return os.path.join(folder, CLIPS_DIR)


def load_clips(cdir: str) -> list[Clip]:
    out = []
    adopt_old_file(cdir, OLD_CLIPS_INDEX, CLIPS_INDEX)
    try:
        with open(os.path.join(cdir, CLIPS_INDEX), encoding="utf-8", errors="replace") as f:   # 1.12.3: as load_index
            for line in f:
                try:
                    d = json.loads(line)
                    if isinstance(d, dict):
                        out.append(Clip(**{k: v for k, v in d.items() if k in Clip.__dataclass_fields__}))
                except (ValueError, TypeError):
                    continue
    except OSError:
        pass
    return out


def save_clips(cdir: str, clips: list[Clip]):
    lines = []
    for c in sorted(clips, key=lambda c: c.t):
        d = asdict(c)
        d.pop("adopted", None)
        lines.append(json.dumps(d, ensure_ascii=False) + "\n")
    fsops.write_atomic(os.path.join(cdir, CLIPS_INDEX), "".join(lines).encode("utf-8"))   # 1.38.5


def _who(who: str) -> tuple[str, str]:
    """The name part after " – " → (role, killer): "Survivor" / "Killer" / a killer's name."""
    who = (who or "").strip()
    if not who:
        return "", ""
    if who.lower() == "survivor":
        return "survivor", ""
    if who.lower() == "killer":
        return "killer", ""
    return "killer", who


def adopt_clip(name: str, recs: list[Recording]) -> Clip | None:
    """A file in Clips/ that is not in the index: made by this program before 1.8.13 when its name says so –
    an editor clip/still starts with the name of a recording and goes on with " – Clip …" / " – Bild …",
    an instant clip ends with "(Sofort-Clip)" – then its round comes from that recording or from the name.
    Anything else is someone else's file: None (listed nowhere, never deleted)."""
    stem, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext not in CLIP_EXTS:
        return None
    stem = _COPY_RE.sub("", stem)
    still = ext in STILL_EXTS
    for r in recs:
        base = os.path.splitext(re.split(r"[\\/]", r.file)[-1])[0]
        if base and stem.startswith(base + " – "):
            return Clip(file=name, kind="still" if still else "clip", source=r.t, map_id=r.map_id, label=r.label,
                        role=r.role, killer=r.killer, farming=r.farming, adopted=True)
    tails = [(" " + t, "instant") for t in {"(Sofort-Clip)", _("(Sofort-Clip)")}]
    kind = next((k for tail, k in tails if stem.endswith(tail) and not still), None)
    if kind is not None:
        stem = stem[:-len(next(tail for tail, _k in tails if stem.endswith(tail)))]
    else:
        m = re.search(r" – (?:Clip \d+m\d\ds-\d+m\d\ds|(?:Bild|{}) \d+-\d\d(?:\.\d)?)$".format(re.escape(_("Bild"))),
                      stem)
        if m is None:
            return None
        kind, stem = ("still" if still else "clip"), stem[:m.start()]
    m = _STAMP_RE.match(stem)
    if m is None:
        return None
    rest = m.group(2)
    label, _sep, who = rest.rpartition(" – ") if " – " in rest else (rest, "", "")
    role, killer = _who(who)
    return Clip(file=name, kind=kind, label=label.strip(), role=role, killer=killer, adopted=True)


def list_clips(cdir: str, recs: list[Recording]) -> list[Clip]:
    """The clips on the drive: index entries whose file is there, plus the program's older clips (adopt_clip);
    ``size`` and – for adopted ones – ``t`` (file time) filled. Newest first."""
    try:
        names = os.listdir(cdir)
    except OSError:
        return []
    index = {c.file: c for c in load_clips(cdir)}
    out = []
    for name in names:
        p = os.path.join(cdir, name)
        if name in (CLIPS_INDEX, CLIPS_INDEX + ".tmp", OLD_CLIPS_INDEX) or not os.path.isfile(p):
            continue
        c = index.get(name) or adopt_clip(name, recs)
        if c is None:
            continue
        try:
            st = os.stat(p)
        except OSError:
            continue
        c.size = st.st_size
        if not c.t:
            c.t = st.st_mtime
        out.append(c)
    return sorted(out, key=lambda c: c.t, reverse=True)


def part_key(path: str) -> str:
    """One spelling of a path for PARTS_WRITING."""
    return os.path.normcase(os.path.abspath(path))


def whole(path: str) -> bool | None:
    """1.12 review: did ffmpeg finish ``path``? mp4/mov: the top-level boxes fill the file exactly and the index box
    "moov" is there (while ffmpeg writes, the data box has no size yet: 0); gif: it ends with the trailer. A ".tmp"
    counts as the kind it is named for. None = cannot tell (another kind, the file not readable)."""
    ext = os.path.splitext(path[:-len(PART_EXT)] if path.endswith(PART_EXT) else path)[1].lower()
    if ext not in (".mp4", ".mov", ".gif"):
        return None
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            if ext == ".gif":
                if size < 14 or f.read(6) not in (b"GIF87a", b"GIF89a"):
                    return False
                f.seek(-1, os.SEEK_END)
                return f.read(1) == b";"
            pos, moov = 0, False
            while pos < size:
                f.seek(pos)
                head = f.read(16)
                if len(head) < 8:
                    return False
                n, kind = struct.unpack(">I4s", head[:8])
                if n == 1 and len(head) == 16:               # 64-bit size
                    n = struct.unpack(">Q", head[8:])[0]
                if n < 8:                                    # 0 = "to the end": the size ffmpeg writes last
                    return False
                moov = moov or kind == b"moov"
                pos += n
            return pos == size and moov
    except OSError:
        return None


def settle_parts(folder: str, now: float | None = None) -> list[str]:
    """1.12 review: a clip the editor was writing when the program ended (quit, update restart, crash) – ffmpeg may
    finish it on its own, but the rename after it never comes, so "<clip>.mp4.tmp" stayed unlisted for good. A ".tmp"
    in Clips/ with one of the program's clip names (adopt_clip), untouched for PART_STALE_S and not written by a save
    of this process: whole → it gets its name and the clips list takes it; cut short → it goes. Someone else's file,
    or one whole() cannot judge, stays. Returns the names given."""
    now = time.time() if now is None else now
    cdir = clips_dir(folder)
    try:
        names = [n for n in os.listdir(cdir) if n.endswith(PART_EXT)
                 and os.path.splitext(n[:-len(PART_EXT)])[1].lower() in (".mp4", ".mov", ".gif")]
    except OSError:
        return []
    recs, given = None, []
    for name in names:
        final, p = name[:-len(PART_EXT)], os.path.join(cdir, name)
        try:
            if part_key(p) in PARTS_WRITING or not os.path.isfile(p) or now - os.path.getmtime(p) < PART_STALE_S:
                continue
        except OSError:
            continue
        recs = load_index(folder) if recs is None else recs
        if adopt_clip(final, recs) is None:
            continue                                         # not a name of ours: someone else's file
        done = whole(p)
        if done is False:
            try:
                fsops.delete_inside(folder, p)                   # 1.33.5 (S2)
            except OSError:
                pass
        if not done:
            continue
        stem, ext = os.path.splitext(final)
        target, n = os.path.join(cdir, final), 2
        while os.path.exists(target) or (n > 2 and os.path.exists(target + PART_EXT)):
            target = os.path.join(cdir, f"{stem} ({n}){ext}")          # as unique_path: never a name being written
            n += 1
        try:
            os.replace(p, target)
        except OSError:
            continue                                         # still open (Windows): next look
        given.append(os.path.basename(target))
    return given


def select_clips(clips: list[Clip], since: float | None = None, role: str | None = None, killer: str | None = None,
                 kind: str | None = None, hide_farming: bool = False) -> list[Clip]:
    """1.8.13 (user: "filtern nach Killer/Survivor"): ``role`` like the recordings ("killer" / "survivor" /
    "farming"), ``killer`` = one killer (rounds as killer), ``kind`` clip / instant / still, ``hide_farming``
    (1.11.5) as for the recordings."""
    out = []
    for c in clips:
        if since is not None and c.t < since:
            continue
        if hide_farming and c.farming:
            continue
        if role == "farming":
            if not c.farming:
                continue
        elif role and c.role != role:
            continue
        if killer and (c.role != "killer" or c.killer != killer):
            continue
        if kind and c.kind != kind:
            continue
        out.append(c)
    return sorted(out, key=lambda c: c.t, reverse=True)

@dataclass
class Space:
    """1.4.2: what the overview's tile "Aufnahmen" shows – measured by the recorder thread, never on the UI thread."""
    free: int = 0                # bytes free on the drive
    total: int = 0               # bytes the drive holds
    used: int = 0                # bytes the recordings of the index take
    count: int = 0
    oldest: float = 0.0          # banner time of the oldest recording (0 = none)
    marked: int = 0              # recordings with an F8 mark
    folder: str = ""             # "" = drive not connected
    t: float = 0.0               # when measured


_SPACE: dict = {}             # 1.34.1 (review P6): folder -> (index stamp, (used, count, oldest, marked))


def _index_stamp(folder: str):
    try:
        st = os.stat(os.path.join(folder, INDEX))
    except OSError:
        return None
    return st.st_mtime_ns, st.st_size, st.st_ino


def space(folder: str | None, recs: list[Recording] | None = None) -> Space:
    """The tile's numbers. 1.34.1 (review P6): the index is read again only when its file changed (time, size or –
    after save_index's replace – another file); the drive is asked each time."""
    if not folder:
        return Space(t=time.time())
    stamp = None                                         # recs handed in: counted, not kept
    if recs is None:
        stamp = _index_stamp(folder)
        hit = _SPACE.get(folder)
        if stamp is not None and hit is not None and hit[0] == stamp:
            sums = hit[1]
        else:
            recs = load_index(folder)
            stamp = _index_stamp(folder)                 # (load_index may have adopted the old index)
            sums = None
    if recs is not None:
        sums = (sum(r.size for r in recs), len(recs), min((r.t for r in recs), default=0.0),
                sum(1 for r in recs if r.marks))
        if stamp is not None:
            if len(_SPACE) > 8:
                _SPACE.clear()
            _SPACE[folder] = (stamp, sums)
    try:
        du = shutil.disk_usage(folder)
        free, total = du.free, du.total
    except OSError:
        free = total = 0
    used, count, oldest, marked = sums
    return Space(free=free, total=total, used=used, count=count, oldest=oldest, marked=marked, folder=folder,
                 t=time.time())


VIDEO_EXTS = (".mkv", ".mp4", ".mov", ".flv", ".ts", ".m3u8", ".fragmented.mp4", ".hybrid.mp4", ".hybrid.mov")
