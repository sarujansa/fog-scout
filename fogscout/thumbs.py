"""Small pictures of the maps for the tiles of the maps page (1.8.72), pure – no Qt.

Decoding a 1280-px map picture and shrinking it took 30–45 ms per tile in the window thread (measured: 55 tiles
≈ 2.1 s, in slices of one picture per 10 ms – the page stuttered until all were in, on every first visit and every
style click). Now a thumbnail is made once per picture (``thumbnail``: the file's path, mtime and size are its
key, so a replaced own picture or a new style cache file gets a new one) and kept as a PNG below ``cache/thumbs``;
``Loader`` decodes in a thread of its own and hands the finished RGBA bytes to the window thread, which only
turns them into pixmaps (``_pending`` → the page's timer). The thread never touches Qt (qt_clip 1.8.66).

1.38.45 (user: "das Laden ist immer noch langsam"): the maps page keys its thumbnails by the picture's content
(``content_key``), not by its mtime – every release installs the map files anew with a new mtime, so each update
made all 56 thumbnails (and every style picture, mapstyle.styled_path) again. And the loader decodes in up to
``WORKERS`` threads (measured, 56 map pictures cold: 1 thread 1.82 s, 3 threads 0.70 s; Pillow releases the GIL).
"""
from __future__ import annotations

import hashlib
import os
import queue
import threading
import time

from PIL import Image

from .imageedit import converted

VERSION = 2                       # raise when the thumbnails change: the cache is made anew (2: 16-bit grey)
PRUNE_AFTER_S = 90 * 24 * 3600    # a cache file not used for this long goes (prune, once per session)
WORKERS = 3                       # 1.38.45: threads of a loader that asks for them (the maps page)
CONTENT_MAX = 16 << 20            # 1.38.45: content keys only for files up to this size (map pictures: < 1 MB)

_KEYS: dict = {}                  # (absolute path, mtime_ns, size) -> content key: each file is read once per session
_KEYS_LOCK = threading.Lock()


def content_key(path: str) -> str | None:
    """1.38.45: a short hash of the file's bytes – the same picture keeps its key when an update writes it again
    with a new mtime. Read once per session and file state (path, mtime, size); None when the file cannot be read
    or is larger than ``CONTENT_MAX`` (the caller falls back to mtime and size)."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    if st.st_size > CONTENT_MAX:
        return None
    stamp = (os.path.abspath(path), st.st_mtime_ns, st.st_size)
    with _KEYS_LOCK:
        key = _KEYS.get(stamp)
    if key is None:
        try:
            with open(path, "rb") as fh:
                key = hashlib.sha1(fh.read()).hexdigest()[:16]
        except OSError:
            return None
        with _KEYS_LOCK:
            _KEYS[stamp] = key
    return key


def cache_name(path: str, box: tuple, by_content: bool = False) -> str:
    """File name of the thumbnail of ``path`` in a cache folder: path, mtime, size and box, so that a changed
    picture never shows its old thumbnail. ``by_content`` (1.38.45, the maps page): the picture's bytes instead of
    path and mtime – a reinstalled, unchanged map keeps its thumbnail (screenshots stay by mtime: reading thousands
    of large files would cost more than it saves)."""
    content = content_key(path) if by_content else None
    if content is not None:
        key = f"content|{content}|{box[0]}x{box[1]}|v{VERSION}"
        return hashlib.sha1(key.encode("utf-8")).hexdigest()[:24] + ".png"
    try:
        st = os.stat(path)
        stamp = f"{st.st_mtime_ns}|{st.st_size}"
    except OSError:
        stamp = "missing"
    key = f"{os.path.abspath(path)}|{stamp}|{box[0]}x{box[1]}|v{VERSION}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:24] + ".png"


def thumbnail(path: str, box: tuple, cache_dir: str | None = None, by_content: bool = False) -> Image.Image:
    """The picture at ``path`` shrunk to fit ``box`` (RGBA, first frame). From ``cache_dir`` when it is there
    (the file's mtime is refreshed – ``prune`` keeps what is used), else decoded and, with a cache folder, saved
    for the next time. The errors of a broken picture are the caller's. ``by_content``: see cache_name."""
    target = os.path.join(cache_dir, cache_name(path, box, by_content)) if cache_dir else None
    if target and os.path.isfile(target):
        try:
            with Image.open(target) as im:
                pic = im.convert("RGBA")
            try:
                os.utime(target)
            except OSError:
                pass
            return pic
        except (OSError, ValueError):
            pass                                      # unreadable cache file: made anew below
    with Image.open(path) as im:
        im.seek(0)
        if im.format == "JPEG":                       # 1.12.2: screenshots – decoded at a reduced scale (draft)
            im.draft("RGB", (max(1, box[0]) * 2, max(1, box[1]) * 2))
        pic = converted(im, "RGBA")
    pic.thumbnail((max(1, box[0]), max(1, box[1])), Image.LANCZOS)      # as the tiles were drawn before
    if target:
        try:
            os.makedirs(cache_dir, exist_ok=True)
            tmp = target + f".{os.getpid()}.tmp"
            pic.save(tmp, "PNG", optimize=False)
            os.replace(tmp, target)                   # never a half-written file under the final name
        except OSError:
            pass
    return pic


def prune(cache_dir: str, now: float | None = None, max_age_s: float = PRUNE_AFTER_S) -> int:
    """Delete thumbnails nobody used for ``max_age_s`` (their mtime is refreshed on every use); the number
    removed. Only our own PNG files in the folder."""
    if not cache_dir or not os.path.isdir(cache_dir):
        return 0
    now = time.time() if now is None else now
    gone = 0
    for name in os.listdir(cache_dir):
        if not name.endswith((".png", ".jpg")):          # 1.16.1: qt_library keeps JPEGs of the recordings here
            continue
        full = os.path.join(cache_dir, name)
        try:
            if now - os.stat(full).st_mtime > max_age_s:
                os.remove(full)
                gone += 1
        except OSError:
            pass
    return gone


class Loader:
    """Thumbnails in a thread: ``request(paths)`` replaces the list to do (the newest request wins, a picture
    already in hand is finished first); ``take()`` in the window thread gives the finished ones as
    (path, width, height, RGBA bytes) – a broken picture comes as (path, 0, 0, b"").

    1.38.45: up to ``workers`` threads take from the same list (the order of the results may differ from the
    request's) – one at first, the others only once a picture has to be made (a cold cache): reading cached
    thumbnails in three threads made the page slower (measured, warm: 1 thread ~270 ms, 3 threads ~450 ms until all
    56 tiles – they compete with the window thread for the GIL). ``by_content`` keys the disk cache by the pictures'
    bytes (cache_name)."""

    def __init__(self, box: tuple, cache_dir: str | None = None, name: str = "map-thumbs", workers: int = 1,
                 by_content: bool = False):
        self.box = tuple(box)
        self.name = name
        self.cache_dir = cache_dir
        self.workers = max(1, int(workers))
        self.by_content = bool(by_content)
        self._done: queue.Queue = queue.Queue()
        self._lock = threading.Condition()
        self._todo: list = []
        self._gen = 0
        self._threads: list = []
        self._prune_lock = threading.Lock()
        self._pruned = False

    def request(self, paths):
        """Make these (in this order); what an earlier request still had to do is dropped."""
        with self._lock:
            self._todo = list(paths)
            self._gen += 1
            self._threads = [t for t in self._threads if t.is_alive()]
            if not self._threads and self._todo:
                self._start_thread()
            self._lock.notify_all()

    def _start_thread(self):
        """One more worker (under ``_lock``)."""
        t = threading.Thread(target=self._run, daemon=True, name=f"{self.name}-{len(self._threads) + 1}")
        self._threads.append(t)
        t.start()

    def _grow(self):
        """1.38.45: a picture had to be made – the others of the list likely too: all workers on it."""
        with self._lock:
            self._threads = [t for t in self._threads if t.is_alive()]
            while len(self._threads) < min(self.workers, len(self._threads) + len(self._todo)):
                self._start_thread()

    def _cold(self, path: str) -> bool:
        """No thumbnail of ``path`` in the disk cache yet (it has to be decoded and shrunk)."""
        if not self.cache_dir:
            return True
        try:
            return not os.path.isfile(os.path.join(self.cache_dir, cache_name(path, self.box, self.by_content)))
        except OSError:
            return True

    def take(self, limit: int = 8) -> list:
        """Up to ``limit`` finished thumbnails (window thread)."""
        out = []
        while len(out) < limit:
            try:
                out.append(self._done.get_nowait())
            except queue.Empty:
                break
        return out

    @property
    def busy(self) -> bool:
        with self._lock:
            return bool(self._todo) or not self._done.empty()

    def _next(self, wait_s: float):
        with self._lock:
            if not self._todo:
                self._lock.wait(wait_s)
            if self._todo:
                return self._todo.pop(0)
            return None

    def _run(self):
        idle_since = time.time()
        me = threading.current_thread()
        while True:
            path = self._next(1.0)
            if path is None:
                if time.time() - idle_since > 30:            # nothing to do for a while: the thread ends
                    with self._lock:
                        if not self._todo:
                            self._threads = [t for t in self._threads if t is not me]
                            return
                continue
            idle_since = time.time()
            if self.workers > 1 and self._cold(path):
                self._grow()
            try:
                item = self.make(path)
            except Exception:                                # one bad picture never ends the thread
                item = (path, 0, 0, b"")
            self._done.put(item)
            with self._prune_lock:
                due, self._pruned = not self._pruned and bool(self.cache_dir), True
            if due:
                try:
                    prune(self.cache_dir)
                except OSError:
                    pass

    def make(self, path: str) -> tuple:
        """One thumbnail as (path, width, height, RGBA bytes) – also usable without the thread (tests). Any error
        of the picture makes it a broken one: Pillow raises more than OSError/ValueError (DecompressionBombError
        for a picture over 2 × MAX_IMAGE_PIXELS, SyntaxError for some broken files)."""
        try:
            pic = thumbnail(path, self.box, self.cache_dir, self.by_content)
            return (path, pic.width, pic.height, pic.tobytes("raw", "RGBA"))
        except Exception:
            return (path, 0, 0, b"")
