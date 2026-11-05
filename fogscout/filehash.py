"""1.18.1 (Implementierungsplan Fassung 6, 2.3/2.4): the identity of a recording for editor projects.

* ``qfp`` – quick fingerprint: SHA-256 over the size, the first and the last MiB. Preselection only; never proof.
* ``full_sha256`` – the SHA-256 of the whole file, the only basis of an automatic project assignment. Read in 4 MiB
  blocks into one reused buffer (hashlib and file reads release the GIL – measured: no noticeable load on the GUI
  thread), cancellable, with progress, waiting while paused (a round is being recorded), and checked for a file that
  changed while it was read (stat before and after: OBS still writing, a merge running).
* ``Cache`` – full hashes by (volume, file id, size, mtime) in the per-user data folder: renaming or moving the file
  on the same volume keeps the entry, any change makes a new one.
* ``Hasher`` – one thread for the whole program, one file at a time.

Cloud placeholders (OneDrive "online only") are never hashed by themselves: reading would download the whole file."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import threading

from . import fsops, paths

log = logging.getLogger(__name__)

CHUNK = 4 << 20
QFP_BYTES = 1 << 20
PROGRESS_EVERY = 64 << 20
CACHE_DIR = "cache"
CACHE_FILE = "sha256.json"
CACHE_KEPT = 2000
RETRIES = 3                       # a file that changes while it is read: tries
RETRY_S = 10.0
PAUSE_POLL_S = 0.25
# FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS | FILE_ATTRIBUTE_RECALL_ON_OPEN | FILE_ATTRIBUTE_OFFLINE
PLACEHOLDER_ATTRS = 0x400000 | 0x40000 | 0x1000


class Changed(OSError):
    """The file changed while it was read (size or mtime) – the hash would describe no real state of it."""


class Cancelled(Exception):
    pass


def qfp(path: str) -> str:
    """SHA-256 over size + first MiB + last MiB (preselection only)."""
    size = os.path.getsize(path)
    h = hashlib.sha256(str(size).encode("ascii") + b"\0")
    with open(path, "rb") as fh:
        h.update(fh.read(QFP_BYTES))
        if size > QFP_BYTES:
            fh.seek(max(QFP_BYTES, size - QFP_BYTES))
            h.update(fh.read(QFP_BYTES))
    return h.hexdigest()


def is_placeholder(st) -> bool:
    return bool(getattr(st, "st_file_attributes", 0) & PLACEHOLDER_ATTRS)


def full_sha256(path: str, cancel: threading.Event | None = None, progress=None, paused=None) -> tuple[str, object]:
    """(hex digest, stat) of the whole file. Raises Cancelled, Changed (it changed while being read) or OSError.
    ``progress(done_bytes, total)`` every PROGRESS_EVERY bytes; ``paused()`` true → it waits (``cancel`` still ends it)."""
    st0 = os.stat(path)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_SEQUENTIAL", 0)   # sequential scan on Windows
    fd = os.open(path, flags)
    h = hashlib.sha256()
    done = 0
    next_report = PROGRESS_EVERY
    buf = bytearray(CHUNK)
    view = memoryview(buf)
    try:
        while True:
            if cancel is not None and cancel.is_set():
                raise Cancelled()
            while paused is not None and paused():
                if cancel is not None and cancel.wait(PAUSE_POLL_S):
                    raise Cancelled()
            n = os.readv(fd, [buf]) if hasattr(os, "readv") else _readinto(fd, view)
            if not n:
                break
            h.update(view[:n])
            done += n
            if progress is not None and done >= next_report:
                next_report += PROGRESS_EVERY
                progress(done, st0.st_size)
    finally:
        os.close(fd)
    st1 = os.stat(path)
    if done != st0.st_size or (st1.st_size, st1.st_mtime_ns) != (st0.st_size, st0.st_mtime_ns):
        raise Changed(0, "changed while it was read", path)
    if progress is not None:
        progress(done, st0.st_size)
    return h.hexdigest(), st1


def _readinto(fd, view) -> int:
    data = os.read(fd, len(view))
    view[:len(data)] = data
    return len(data)


def cache_key(st) -> str:
    return f"{st.st_dev}:{st.st_ino}:{st.st_size}:{st.st_mtime_ns}"


class Cache:
    """Full hashes by ``cache_key`` (LRU, CACHE_KEPT entries) in ``<data folder>/cache/sha256.json``. A broken file
    is an empty cache. Without a data folder it lives in memory only."""

    def __init__(self, folder: str | None = None):
        self.folder = folder if folder is not None else paths.ensure(CACHE_DIR)
        self._lock = threading.Lock()
        self._map = {}
        if self.folder:
            try:
                with open(os.path.join(self.folder, CACHE_FILE), encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    self._map = {str(k): v for k, v in data.items()
                                 if isinstance(v, str) and len(v) == 64}
            except (OSError, ValueError):
                self._map = {}

    def get(self, st) -> str | None:
        with self._lock:
            v = self._map.pop(cache_key(st), None)
            if v is not None:
                self._map[cache_key(st)] = v                  # most recent last
            return v

    def put(self, st, sha: str):
        with self._lock:
            self._map.pop(cache_key(st), None)
            self._map[cache_key(st)] = sha
            while len(self._map) > CACHE_KEPT:
                self._map.pop(next(iter(self._map)))
            data = json.dumps(self._map).encode("utf-8")
        self._save_cache(data)

    def forget(self, st):
        with self._lock:
            self._map.pop(cache_key(st), None)
            data = json.dumps(self._map).encode("utf-8")
        self._save_cache(data)

    def _save_cache(self, data: bytes):
        """The one place in project saving that replaces a file: this cache is rebuilt from the recordings at any
        time, so a replace that loses an older version loses nothing (plan 3.7)."""
        if not self.folder:
            return
        path = os.path.join(self.folder, CACHE_FILE)
        try:
            os.makedirs(self.folder, exist_ok=True)
            tmp = fsops.write_tmp(path, data)
        except OSError:
            return
        try:
            os.replace(tmp, path)
        except OSError:
            fsops.discard_tmp(tmp)


class Hasher(threading.Thread):
    """One thread, one file at a time. ``request(path, on_done, on_progress=None, allow_placeholder=False)``;
    ``on_done(result)`` runs on this thread with a dict ``kind`` = done (``sha256``, ``stat``, ``cached``) / placeholder
    / changed / error (``error``) / cancelled. ``cancel(path)``, ``set_paused(on)``, ``stop()``."""

    def __init__(self, cache: Cache | None = None, retry_s: float = RETRY_S):
        super().__init__(daemon=True, name="file-hash")
        self.cache = cache if cache is not None else Cache()
        self.retry_s = retry_s
        self._cv = threading.Condition()
        self._jobs = []
        self._current = None
        self._cancel = threading.Event()
        self._paused = threading.Event()
        self._stopping = False

    def request(self, path, on_done, on_progress=None, allow_placeholder=False):
        """1.22: a file already waiting keeps its place and gains the new answer – a second window asking for the
        same recording (a montage and the round's own editor) never takes the first one's answer away."""
        with self._cv:
            for k, (p, dones, progs, allow) in enumerate(self._jobs):
                if p == path:
                    self._jobs[k] = (p, dones + [on_done], progs + ([on_progress] if on_progress else []),
                                     allow or allow_placeholder)
                    break
            else:
                self._jobs.append((path, [on_done], [on_progress] if on_progress else [], allow_placeholder))
            self._cv.notify()

    def cancel(self, path):
        with self._cv:
            self._jobs = [j for j in self._jobs if j[0] != path]
            if self._current == path:
                self._cancel.set()

    def set_paused(self, on: bool):
        (self._paused.set if on else self._paused.clear)()

    def stop(self):
        with self._cv:
            self._stopping = True
            self._jobs = []
            self._cancel.set()
            self._cv.notify()

    def run(self):
        while True:
            with self._cv:
                while not self._jobs and not self._stopping:
                    self._cv.wait()
                if self._stopping:
                    return
                path, dones, progs, allow = self._jobs.pop(0)
                self._current = path
                self._cancel.clear()

            def progress(*a, _progs=progs):
                for fn in _progs:
                    fn(*a)
            try:
                result = self.hash_now(path, progress if progs else None, allow)
            except Exception as e:                            # never let a bad file end the thread
                result = {"kind": "error", "error": str(e)}
            with self._cv:
                self._current = None
            for on_done in dones:
                try:
                    on_done(result)
                except Exception:                     # 1.34.2 (review W1): the next waiter still gets its answer
                    log.exception("Hash fertig: Fehler beim Weitergeben")
            # 1.38.5: let go of the answers before waiting – the callbacks hold the asking editor's bridge, and as
            # loop locals they kept the last closed editor alive until the next file was hashed
            dones = progs = progress = on_done = result = None

    def hash_now(self, path, on_progress=None, allow_placeholder=False) -> dict:
        """The work of one job, also callable directly (tests)."""
        for attempt in range(RETRIES):
            try:
                st = os.stat(path)
            except OSError as e:
                return {"kind": "error", "error": str(e)}
            if is_placeholder(st) and not allow_placeholder:
                return {"kind": "placeholder", "size": st.st_size}
            hit = self.cache.get(st)
            if hit:
                return {"kind": "done", "sha256": hit, "stat": st, "cached": True}
            try:
                sha, st1 = full_sha256(path, self._cancel, on_progress, self._paused.is_set)
            except Cancelled:
                return {"kind": "cancelled"}
            except Changed:
                if attempt + 1 < RETRIES and not self._cancel.wait(self.retry_s):
                    continue
                return {"kind": "changed"}
            except OSError as e:
                return {"kind": "error", "error": str(e)}
            self.cache.put(st1, sha)
            return {"kind": "done", "sha256": sha, "stat": st1, "cached": False}
        return {"kind": "changed"}


_HASHER = []
_HASHER_LOCK = threading.Lock()


def hasher() -> Hasher:
    """The program's one hasher, started on first use."""
    with _HASHER_LOCK:
        if not _HASHER or not _HASHER[0].is_alive():
            h = Hasher()
            h.start()
            _HASHER[:] = [h]
        return _HASHER[0]
