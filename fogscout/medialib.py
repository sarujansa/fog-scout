"""The editor's media library (1.16): what can be opened on the timeline – the rounds OBS recorded, the clips of the
Clips folder and video files the user imported for the session –, with search, sort and a line of facts each.
Pure (no Qt): the App lists its recordings and clips as MediaItems, the window shows them."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from .i18n import N_
from .textnorm import fmt_duration, fold

VIDEO_EXTS = (".mp4", ".mkv", ".mov", ".webm", ".flv", ".ts", ".m4v", ".avi")
KINDS = ("round", "clip", "file")
KIND_LABELS = {"round": N_("Runde"), "clip": N_("Clip"), "file": N_("Datei")}
SORTS = (("new", N_("Neueste zuerst")), ("old", N_("Älteste zuerst")), ("name", N_("Name A–Z")),
         ("long", N_("Längste zuerst")), ("short", N_("Kürzeste zuerst")))


@dataclass
class MediaItem:
    path: str                                  # absolute path of the video
    name: str                                  # what the list shows (the round's label, the clip's name)
    kind: str = "round"                        # round / clip / file
    when: float = 0.0                          # made at (time.time()), 0 = unknown
    seconds: float = 0.0                       # length, 0 = unknown (probed when opened)
    size: int = 0                              # bytes
    marks: list = field(default_factory=list)  # F8 marks (rounds)
    sources: list | None = None                # OBS sound sources on their own tracks (rounds), None = unknown
    label: str = ""                            # map
    role: str = ""
    killer: str = ""
    round_t: float = 0.0                       # the round's key (recordings) – the editor's saves join it
    project: bool = False                      # a saved project exists for it

    @property
    def key(self) -> str:
        return os.path.normcase(os.path.abspath(self.path))


def is_video(path: str) -> bool:
    return os.path.splitext(path or "")[1].lower() in VIDEO_EXTS


def from_file(path: str) -> MediaItem:
    """An imported file: name and date from the file system."""
    try:
        st = os.stat(path)
        when, size = st.st_mtime, st.st_size
    except OSError:
        when, size = 0.0, 0
    return MediaItem(path, os.path.splitext(os.path.basename(path))[0], "file", when, 0.0, size)


def filter_items(items, text: str) -> list:
    """The items whose name, map, killer or kind holds every word of ``text`` (folded: case and accents aside)."""
    words = [w for w in fold(text or "").split() if w]
    if not words:
        return list(items)
    out = []
    for it in items:
        hay = fold(" ".join((it.name, it.label, it.killer, it.role, os.path.basename(it.path))))
        if all(w in hay for w in words):
            out.append(it)
    return out


def sort_items(items, key: str) -> list:
    if key == "old":
        return sorted(items, key=lambda it: (it.when, it.name))
    if key == "name":
        return sorted(items, key=lambda it: fold(it.name))
    if key == "long":
        return sorted(items, key=lambda it: (-it.seconds, -it.when))
    if key == "short":
        return sorted(items, key=lambda it: (it.seconds if it.seconds > 0 else 1e12, -it.when))
    return sorted(items, key=lambda it: (-it.when, it.name))


def fmt_when(ts: float, now: float | None = None) -> str:
    """'30.10. 21:14' – with the year when it is not this one; '' for unknown."""
    if not ts:
        return ""
    now = time.time() if now is None else now
    t = time.localtime(ts)
    if t.tm_year != time.localtime(now).tm_year:
        return time.strftime("%d.%m.%Y %H:%M", t)
    return time.strftime("%d.%m. %H:%M", t)


def fmt_len(seconds: float) -> str:
    """'1:23' / '1:02:03'; '–' when unknown."""
    if seconds <= 0:
        return "–"
    text = fmt_duration(seconds)
    return text[1:] if text.startswith("0") and len(text) == 5 else text


def fmt_size(size: int) -> str:
    if size <= 0:
        return ""
    mb = size / 1024 ** 2
    if mb < 1:
        return f"{max(1, round(size / 1024))} kB"
    return f"{mb / 1024:.1f} GB" if mb >= 1024 else f"{mb:.0f} MB"


def facts(item: MediaItem) -> str:
    """The second line of a library row: length · date · size."""
    bits = [fmt_len(item.seconds), fmt_when(item.when), fmt_size(item.size)]
    return " · ".join(b for b in bits if b and b != "–") or "–"
