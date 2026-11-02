"""1.18.1 (Implementierungsplan Fassung 6, chapters 3 and 4): saving editor projects without ever losing a version
silently. Pure Python, no Qt – the editor (1.18.1) and the App wire it in.

* ``Registry`` – one ``Slot`` per project for the whole program, outliving windows: owner token, strictly growing
  ``seq``, the newest state handed in, what is confirmed on disk, the hashes the next write is checked against, the
  status. A slot has its own writer thread (a hanging network drive blocks only that project); one rescue thread
  writes local copies into the per-user data folder.
* ``write_guarded`` – the one write order (3.8): temp file + fsync → the main file under an exclusive handle → its
  full SHA-256 checked against ``base_hash`` → sidecar of the backup (HMAC over name, kind, hash, size) → the main
  file renamed to the backup name under that handle (never replacing) → the new main file created exclusively.
* backups (4.2): rotating kinds are deleted only through ``fsops.delete_verified`` with a valid own sidecar; a backup
  whose content or sidecar does not check out is renamed to a protected kind, never deleted.
* ``classify`` (4.4): drive / folder unreachable is an error (retry, rescue), a missing file with a known
  ``base_hash`` is a conflict the user decides – the file is never created again by itself.
* ``status_of`` (3.9): "saved" only when the newest state of window and slot is confirmed on disk.

Every rename/create/delete goes through fsops (AST guard in tests/test_fsops.py)."""
from __future__ import annotations

import errno
import hashlib
import hmac
import json
import os
import secrets
import threading
import time

from . import fsops, paths, project

BACKUP_DIR = "Sicherungen"
LOCAL_DIR = os.path.join("backup", "editor")
SIDECAR_EXT = ".sha256"
SIDECAR_FORMAT = "fogscout-backup 2"
ROTATE_KEEP = {"sitzung": 10, "laufend": 10, "zwischen": 20, "ansicht": 0}
PROTECTED = ("vor-uebergabe", "vor-zuordnung", "konflikt", "spaet-geaendert", "beschaedigt", "rest", "ohne-pruefsumme")
LAUFEND_EVERY_S = 300.0
BUSY_RETRY_S = (0.05, 0.15, 0.4)
BUSY_AGAIN_S = 2.0
ERROR_RETRY_S = (15.0, 60.0)
MISSING_LOOKS_S = (2.0, 10.0)
HANG_S = 10.0
LEFTOVER_AGE_S = 3600.0
NET_ERRORS = {3, 21, 53, 64, 67, 1222, 1231}          # Windows: path/device/network not there
CLOUD_ERRORS = set(range(362, 400))                     # ERROR_CLOUD_FILE_* and friends


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---- sidecars (4.2)
def sidecar_bytes(file_name: str, sha256: str, size: int, writer: str, kind: str, key: bytes,
                  created: float | None = None) -> bytes:
    lines = [SIDECAR_FORMAT, f"file {file_name}", f"sha256 {sha256}", f"size {int(size)}", f"writer {writer}",
             f"kind {kind}", "created " + time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(created or time.time()))]
    body = "\n".join(lines) + "\n"
    mac = hmac.new(key, body.encode("utf-8"), hashlib.sha256).hexdigest()
    return (body + f"hmac {mac}\n").encode("utf-8")


def read_sidecar(path: str, key: bytes | None, writer: str | None) -> dict | None:
    """The sidecar's fields if it is well formed, signed with our key and written by this installation; else None
    (then the file it describes is never deleted)."""
    if not key or not writer:
        return None
    try:
        with open(path, "rb") as fh:
            raw = fh.read(4096)
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    lines = text.split("\n")
    if len(lines) != 9 or lines[-1] != "" or lines[0] != SIDECAR_FORMAT:
        return None
    fields = {}
    for line in lines[1:8]:
        k, _s, v = line.partition(" ")
        fields[k] = v
    body = "\n".join(lines[:7]) + "\n"
    mac = hmac.new(key, body.encode("utf-8"), hashlib.sha256).hexdigest()
    if fields.get("hmac") != mac or fields.get("writer") != writer or not project.valid_sha(fields.get("sha256")):
        return None
    try:
        fields["size"] = int(fields.get("size", ""))
    except ValueError:
        return None
    fields["raw_sha"], fields["raw_size"] = sha(raw), len(raw)
    return fields


def _sidecar_writer(path: str) -> str | None:
    """The ``writer`` line of a sidecar, unverified – only to leave another installation's backups alone."""
    try:
        with open(path, "rb") as fh:
            for line in fh.read(4096).decode("utf-8", "replace").split("\n"):
                if line.startswith("writer "):
                    return line[7:].strip()
    except OSError:
        pass
    return None


def backup_folder(main: str) -> str:
    folder, name = os.path.split(main)
    return os.path.join(folder, BACKUP_DIR, name[:-len(project.EXT)] if name.endswith(project.EXT) else name)


def backup_name(seq: int, kind: str, content_sha: str, now: float | None = None) -> str:
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now or time.time()))
    return f"{stamp}-{int(seq)}-{kind}-{content_sha[:12]}-{secrets.token_hex(3)}.json"


def parse_backup_name(name: str) -> dict | None:
    if not name.endswith(".json"):
        return None
    parts = name[:-5].split("-")
    if len(parts) < 6:
        return None
    try:
        seq = int(parts[2])
    except ValueError:
        return None
    return {"stamp": parts[0] + parts[1], "seq": seq, "kind": "-".join(parts[3:-2]), "hash12": parts[-2]}


def store_with_sidecar(folder: str, data: bytes, seq: int, kind: str, key, writer, src_tmp: str | None = None) -> str:
    """A new protected/plain backup ``kind`` of ``data`` in ``folder``: sidecar first, then the file – both created
    exclusively. ``src_tmp`` = an existing temp file holding ``data`` (moved instead of written again)."""
    os.makedirs(folder, exist_ok=True)
    digest = sha(data)
    for _attempt in range(5):
        name = backup_name(seq, kind, digest)
        path = os.path.join(folder, name)
        try:
            if key and writer:
                fsops.write_new(path + SIDECAR_EXT, sidecar_bytes(name, digest, len(data), writer, kind, key))
            if src_tmp:
                fsops.create_exclusive(src_tmp, path)
            else:
                fsops.write_new(path, data)
            return path
        except FileExistsError:
            continue
    raise FileExistsError(errno.EEXIST, "no free backup name", folder)


# ---- the write (3.8)
class Outcome:
    __slots__ = ("kind", "tmp", "backup", "backup_sha", "backup_size", "new_hash", "late", "error")

    def __init__(self, kind, **kw):
        self.kind = kind
        for k in self.__slots__[1:]:
            setattr(self, k, kw.get(k))

    def __repr__(self):
        return f"Outcome({self.kind!r})"


def write_guarded(path: str, data: bytes, base_hash: str | None, kind: str, seq: int, key, writer,
                  hook=None, pending_tmp: str | None = None) -> Outcome:
    """Fassung 6, 3.8, steps 0–9. ``base_hash`` None = a new project (no file expected). Outcomes: written /
    conflict (content not ours) / missing (file gone) / appeared (a file was created in the gap) / busy (another
    program has it open) / unsupported. Raises OSError for disk errors; a temp file it leaves is in ``Outcome.tmp``.
    ``pending_tmp``: after a failed step 7 the old main file is a backup already – only step 7 is tried again."""
    step = hook or (lambda n: None)
    if pending_tmp and os.path.exists(pending_tmp):
        with open(pending_tmp, "rb") as fh:            # the state whose step 7 failed comes first …
            earlier = fh.read()
        try:
            fsops.create_exclusive(pending_tmp, path)
        except FileExistsError:
            return Outcome("appeared", tmp=pending_tmp)
        base_hash = sha(earlier)                       # … and this write goes on from it like any other
    step(0)
    tmp = fsops.write_tmp(path, data)
    try:
        if base_hash is None:
            step(7)
            try:
                fsops.create_exclusive(tmp, path)
            except FileExistsError:
                return Outcome("appeared", tmp=tmp)
            return Outcome("written", new_hash=sha(data))
        step(1)
        try:
            h = fsops.ExclusiveHandle(path)
        except FileNotFoundError:
            fsops.discard_tmp(tmp)
            return Outcome("missing")
        except PermissionError:
            fsops.discard_tmp(tmp)
            return Outcome("busy")
        fallback = False
        sidecar = None
        try:
            old = h.read()
            step(2)
            old_sha = sha(old)
            if old_sha != base_hash:
                return Outcome("conflict", tmp=tmp)
            folder = backup_folder(path)
            os.makedirs(folder, exist_ok=True)
            step(3)
            for _attempt in range(5):
                name = backup_name(seq, kind, old_sha)
                bpath = os.path.join(folder, name)
                try:
                    if key and writer:
                        sidecar = bpath + SIDECAR_EXT
                        fsops.write_new(sidecar, sidecar_bytes(name, old_sha, len(old), writer, kind, key))
                    break
                except FileExistsError:
                    sidecar = None
                    continue
            else:
                raise FileExistsError(errno.EEXIST, "no free backup name", folder)
            step(4)
            try:
                h.rename_to(bpath)
            except fsops.UnsupportedFS:
                if not fsops.WIN:
                    raise
                fallback = True                      # Windows file system without rename by handle (plan RR1)
            except BaseException:
                _drop_sidecar(sidecar)
                raise
        finally:
            h.close()
        if fallback:
            try:
                fsops.rename_fallback(path, bpath)
            except BaseException:
                _drop_sidecar(sidecar)
                raise
        step(5)
        try:
            fsops.create_exclusive(tmp, path)
        except FileExistsError:
            return Outcome("appeared", tmp=tmp, backup=bpath, backup_sha=old_sha, backup_size=len(old))
        except OSError as e:
            return Outcome("error_after_move", tmp=tmp, backup=bpath, backup_sha=old_sha, backup_size=len(old),
                           error=e)
        step(7)
        late = False
        try:
            with open(bpath, "rb") as fh:
                late = sha(fh.read()) != old_sha     # step 9: changed after our check (Windows fallback / POSIX)
        except OSError:
            late = True
        if late:
            _protect(bpath, "spaet-geaendert")
        step(8)
        return Outcome("written", new_hash=sha(data), backup=bpath, backup_sha=old_sha, backup_size=len(old),
                       late=late)
    except fsops.UnsupportedFS:
        fsops.discard_tmp(tmp)
        return Outcome("unsupported")
    except BaseException:
        if os.path.exists(tmp):
            fsops.discard_tmp(tmp)
        raise


def _drop_sidecar(sidecar):
    if not sidecar:
        return
    try:
        with open(sidecar, "rb") as fh:
            raw = fh.read()
        fsops.delete_verified(sidecar, sha(raw), len(raw))
    except OSError:
        pass


def _protect(bpath: str, kind: str) -> str | None:
    """Rename a backup to a protected kind (never deleted afterwards); its sidecar stays and is cleaned up as an
    orphan later (it names the old file)."""
    folder, name = os.path.split(bpath)
    info = parse_backup_name(name)
    stem = name[:-5]
    if info:
        bits = stem.split("-")
        new = "-".join(bits[:3] + [kind] + bits[-2:]) + ".json"
    else:
        new = stem + "-" + kind + ".json"
    target = os.path.join(folder, new)
    try:
        with fsops.ExclusiveHandle(bpath) as h:
            h.rename_to(target)
        return target
    except OSError:
        return None


# ---- rotation and orphans (4.2)
def rotate(folder: str, key, writer) -> dict:
    """Delete rotating backups beyond ROTATE_KEEP – only those whose own sidecar checks out and whose full SHA-256
    is still what the sidecar says; the others become protected. Returns counts (for tests and the diagnosis)."""
    out = {"deleted": 0, "protected": 0, "kept": 0}
    try:
        names = os.listdir(folder)
    except OSError:
        return out
    groups = {}
    for name in names:
        info = parse_backup_name(name)
        if info and info["kind"] in ROTATE_KEEP:
            groups.setdefault(info["kind"], []).append((info["seq"], info["stamp"], name, info))
    for kind, items in groups.items():
        items.sort(reverse=True)
        for _seq, _stamp, name, info in items[ROTATE_KEEP[kind]:]:
            path = os.path.join(folder, name)
            if _sidecar_writer(path + SIDECAR_EXT) not in (None, writer):
                out["kept"] += 1                          # another installation's backup (synced folder): its business
                continue
            side = read_sidecar(path + SIDECAR_EXT, key, writer)
            if side is None or side.get("file") != name or side.get("kind") != kind \
                    or not side["sha256"].startswith(info["hash12"]):
                out["protected"] += _protect(path, "ohne-pruefsumme") is not None
                continue
            try:
                ok = fsops.delete_verified(path, side["sha256"], side["size"])
            except OSError:
                out["kept"] += 1
                continue
            if not ok:
                out["protected"] += _protect(path, "spaet-geaendert") is not None
                continue
            out["deleted"] += 1
            try:
                fsops.delete_verified(path + SIDECAR_EXT, side["raw_sha"], side["raw_size"])
            except OSError:
                pass
    return out


def clean_orphan_sidecars(folder: str, key, writer) -> int:
    """Sidecars of ours whose file is gone (a crash between sidecar and rename, or after a deletion): removed – they
    name exactly one file with exactly one content, so they could never authorise deleting anything else."""
    n = 0
    try:
        names = os.listdir(folder)
    except OSError:
        return 0
    for name in names:
        if not name.endswith(SIDECAR_EXT):
            continue
        path = os.path.join(folder, name)
        side = read_sidecar(path, key, writer)
        if side is None or os.path.exists(os.path.join(folder, side.get("file", ""))):
            continue
        try:
            n += bool(fsops.delete_verified(path, side["raw_sha"], side["raw_size"]))
        except OSError:
            pass
    return n


# ---- availability of the project path (4.4)
def classify(path: str) -> str:
    """ok / missing / dir_missing / dir_unreachable / drive – only the project path counts, never the folder of the
    recording."""
    drive, rest = os.path.splitdrive(os.path.abspath(path))
    root = drive + os.sep if drive else os.sep
    try:
        os.stat(root)
    except OSError:
        return "drive"
    folder = os.path.dirname(os.path.abspath(path))
    probe = root
    for part in [p for p in os.path.relpath(folder, root).split(os.sep) if p and p != "."]:
        probe = os.path.join(probe, part)
        try:
            os.stat(probe)
        except FileNotFoundError:
            return "dir_missing"
        except OSError as e:
            if getattr(e, "winerror", None) in NET_ERRORS and probe == os.path.join(root, part):
                return "drive"
            return "dir_unreachable"
    try:
        os.listdir(folder)
    except OSError:
        return "dir_unreachable"
    try:
        os.stat(path)
    except FileNotFoundError:
        return "missing"
    except OSError as e:
        if getattr(e, "winerror", None) in CLOUD_ERRORS or isinstance(e, PermissionError):
            return "dir_unreachable"
        return "dir_unreachable"
    return "ok"


def id_candidates(folder: str, pid: str) -> list:
    """Project files (not backups) carrying ``pid`` – the renamed/copied ones of a missing main file."""
    return [e for e in project.scan(folder) if e.ok and e.id == pid]


# ---- leftovers and local copies (4.3, 4.5)
def leftovers(path: str) -> list:
    """Our temp files of this project file (``.<name>.<pid>.<random>.tmp``), readable ones first by ``rev.seq``."""
    folder, name = os.path.split(path)
    out = []
    try:
        names = os.listdir(folder)
    except OSError:
        return out
    for n in names:
        if n.startswith("." + name + ".") and n.endswith(fsops.TMP_SUFFIX):
            p = os.path.join(folder, n)
            try:
                with open(p, "rb") as fh:
                    data = json.loads(fh.read().decode("utf-8"))
                seq = int((data.get("rev") or {}).get("seq") or 0) if isinstance(data, dict) else -1
            except (OSError, ValueError, UnicodeDecodeError, AttributeError):
                seq = -1
            out.append((seq, p))
    out.sort(reverse=True)
    return out


def adopt_leftovers(path: str, key, writer, now: float | None = None) -> int:
    """After the recovery has looked at them: readable temp files of this project become protected ``rest`` backups
    (sidecar + exclusive move); empty/unreadable ones older than LEFTOVER_AGE_S are removed (our own pattern)."""
    now = now or time.time()
    n = 0
    for seq, p in leftovers(path):
        try:
            with open(p, "rb") as fh:
                data = fh.read()
            age = now - os.stat(p).st_mtime
        except OSError:
            continue
        if seq >= 0:
            try:
                store_with_sidecar(backup_folder(path), data, max(seq, 0), "rest", key, writer, src_tmp=p)
                n += 1
            except OSError:
                pass
        elif age >= LEFTOVER_AGE_S:
            fsops.discard_tmp(p)
    return n


def restore_copy(source_file: str, target: str):
    """„Wiederherstellen“ (only after the user's choice): a copy of ``source_file`` created exclusively at
    ``target`` – FileExistsError when something is there by now (then nothing changed)."""
    with open(source_file, "rb") as fh:
        data = fh.read()
    fsops.write_new(target, data)


def local_key(pid: str | None, source_path: str) -> str:
    return pid or ("src-" + hashlib.sha1(os.path.normcase(os.path.abspath(source_path)).encode("utf-8")).hexdigest()[:16])


def local_name(lkey: str, seq: int, art: str) -> str:
    return f"{lkey}-{int(seq):08d}.{art}.json"


def local_candidates(folder: str | None, lkey: str) -> list:
    """Local copies of a project, newest ``seq`` first: (seq, art, path)."""
    if not folder:
        return []
    out = []
    try:
        names = os.listdir(folder)
    except OSError:
        return out
    for n in names:
        if n.startswith(lkey + "-") and n.endswith(".json"):
            bits = n[len(lkey) + 1:-5].split(".")
            if len(bits) == 2 and bits[0].isdigit():
                out.append((int(bits[0]), bits[1], os.path.join(folder, n)))
    out.sort(reverse=True)
    return out


# ---- status (3.9)
def status_of(slot, dirty: bool = False, gesture: bool = False, now: float | None = None) -> str:
    """The word the editor shows; "saved" only when the newest state of window and slot is confirmed on disk."""
    now = now if now is not None else time.monotonic()
    s = slot.status
    if s in ("readonly", "ambiguous", "missing", "conflict"):
        return s
    if s == "error":
        return "error_rescued" if slot.rescued_seq >= slot.latest_seq else "error"
    if slot.in_flight is not None and slot.in_flight_since is not None and now - slot.in_flight_since > HANG_S:
        return "hang"
    if dirty or gesture:
        return "changed"
    if slot.in_flight is not None or slot.written_seq < slot.latest_seq:
        return "saving"
    return "saved" if slot.has_file else "new"


# ---- registry and slots (3.4)
class Job:
    __slots__ = ("seq", "content", "content_hash", "view", "view_event", "source", "kind")

    def __init__(self, seq, content, view, view_event, source, kind="write"):
        self.seq, self.content, self.view, self.view_event = seq, content, view, bool(view_event)
        self.source, self.kind = dict(source or {}), kind
        self.content_hash = project.content_hash(content) if content is not None else None


class Slot:
    def __init__(self, registry, path: str, pid: str | None, keys):
        self.registry = registry
        self.path, self.pid = path, pid
        self.keys = set(keys)
        self.owner = None
        self.next_seq = 1
        self.latest = None
        self.latest_seq = 0
        self.pending = None
        self.in_flight = None
        self.in_flight_since = None
        self.written_seq = 0
        self.rescued_seq = 0
        self.base_hash = None                 # full SHA-256 of the bytes last written/read by us (G1)
        self.disk_content_hash = None
        self.disk_view = None
        self.baseline_hash = None              # content when opened (a file is made only for a real change)
        self.status = "saved"
        self.reason = ""
        self.fifo = []
        self.session_backup_done = False
        self.last_laufend = 0.0
        self.pending_tmp = None
        self.retry_at = None
        self.retries = 0
        self.written = []                     # seqs written, in order (tests, diagnosis)
        self.cv = threading.Condition()
        self.thread = None

    @property
    def has_file(self) -> bool:
        return self.base_hash is not None


class Registry:
    """The program's slots. ``claim``/``release`` by window token, ``submit`` the newest state, ``secured`` for the
    quit phases. ``hook(slot, step)`` and ``sleep`` are for tests (no real waiting there)."""

    def __init__(self, data_dir: str | None = None, key: bytes | None = None, writer: str | None = None,
                 clock=time.monotonic, sleep=None, hook=None):
        self.data_dir = data_dir
        self.key = key if key is not None else paths.backup_key()
        self.writer = writer if writer is not None else paths.writer_id()
        self.clock = clock
        self.sleep = sleep
        self.hook = hook
        self.lock = threading.Lock()
        self.slots = []
        self.rejected = 0
        self._rescue_cv = threading.Condition()
        self._rescue_jobs = []
        self._rescue_thread = None
        self._stopping = False

    # -- claiming
    def find(self, keys) -> Slot | None:
        keys = {k for k in keys if k}
        with self.lock:
            for s in self.slots:
                if s.keys & keys:
                    return s
        return None

    def claim(self, keys, token, path: str, pid: str | None = None, base: dict | None = None):
        """(slot, from_memory): the slot of these keys, now owned by ``token`` – or (slot, None) when another window
        owns it (``slot.owner`` tells which). ``from_memory`` = the newest state of the slot when it is newer than the
        disk (an earlier window's last save still running) – the new window starts with it (I5). ``base`` = what was
        loaded from disk: ``base_hash``, ``content_hash``, ``view``, ``has_file``."""
        keys = [k for k in keys if k]
        with self.lock:
            slot = next((s for s in self.slots if s.keys & set(keys)), None)
            if slot is None:
                slot = Slot(self, path, pid, keys)
                if base:
                    slot.base_hash = base.get("base_hash")
                    slot.disk_content_hash = base.get("content_hash")
                    slot.disk_view = base.get("view")
                    slot.baseline_hash = base.get("baseline_hash") or base.get("content_hash")
                self.slots.append(slot)
            slot.keys |= set(keys)
        with slot.cv:
            if slot.owner is not None and slot.owner != token:
                return slot, False
            slot.owner = token
            newer = slot.latest is not None and (slot.latest_seq > slot.written_seq or slot.in_flight is not None)
            return slot, (slot.latest if newer else None)

    def release(self, slot: Slot, token):
        with slot.cv:
            if slot.owner == token:
                slot.owner = None
            slot.cv.notify_all()
        self._prune()

    def _prune(self):
        with self.lock:
            self.slots = [s for s in self.slots if s.owner is not None or s.pending is not None
                          or s.in_flight is not None or s.fifo or s.latest_seq > max(s.written_seq, s.rescued_seq)]

    def set_identity(self, slot: Slot, pid: str, path: str):
        """A new project got its id (GUI thread, first save): the slot is found by it from now on."""
        with self.lock:
            slot.pid, slot.path = pid, path
            slot.keys.add(pid)

    # -- submitting
    def submit(self, slot: Slot, token, content: dict, view=None, view_event=False, source=None) -> int | None:
        """The newest state from window ``token``: a job with the next ``seq`` replaces a waiting one (``view_event``
        kept, 3.3). None when ``token`` does not own the slot (a late timer of a closed window, I2)."""
        with slot.cv:
            if slot.owner != token:
                self.rejected += 1
                return None
            seq = slot.next_seq
            slot.next_seq += 1
            job = Job(seq, content, view, view_event, source)
            if slot.pending is not None and slot.pending.view_event:
                job.view_event = True
            slot.pending = job
            slot.latest, slot.latest_seq = job, seq
            slot.cv.notify_all()
        self._ensure_thread(slot)
        return seq

    def submit_fifo(self, slot: Slot, kind: str, data: bytes):
        """A backup job (``vor-uebergabe``/``vor-zuordnung``) of the current file – runs before the next write."""
        with slot.cv:
            slot.fifo.append(("backup", kind, data))
            slot.cv.notify_all()
        self._ensure_thread(slot)

    def _ensure_thread(self, slot: Slot):
        with slot.cv:
            if slot.thread is None or not slot.thread.is_alive():
                slot.thread = threading.Thread(target=self._run, args=(slot,), daemon=True, name="project-save")
                slot.thread.start()

    # -- the slot's thread
    def _wait(self, slot, seconds):
        if self.sleep is not None:
            self.sleep(seconds)
            return
        with slot.cv:
            slot.cv.wait(seconds)

    def _run(self, slot: Slot):
        while True:
            with slot.cv:
                while not slot.fifo and slot.pending is None and not self._stopping:
                    if slot.retry_at is not None:
                        delay = slot.retry_at - self.clock()
                        if delay <= 0:
                            slot.retry_at = None
                            if slot.latest is not None and slot.written_seq < slot.latest_seq:
                                slot.pending = slot.latest
                            continue
                        slot.cv.wait(min(delay, 1.0))
                        continue
                    if slot.owner is None:
                        return                          # idle and nobody owns it: the thread ends (I4)
                    slot.cv.wait(1.0)
                if self._stopping:
                    return
                if slot.fifo:
                    task = slot.fifo.pop(0)
                    job = None
                else:
                    task = None
                    job, slot.pending = slot.pending, None
                    slot.in_flight, slot.in_flight_since = job.seq, self.clock()
            try:
                if task is not None:
                    self._backup_task(slot, task)
                elif job.seq > slot.written_seq:
                    self._write(slot, job)
            except Exception as e:                      # never let a failure end the thread silently
                self._failed(slot, job, e)
            finally:
                with slot.cv:
                    if task is None:
                        slot.in_flight = slot.in_flight_since = None
                    slot.cv.notify_all()
            self._prune()

    def _hook(self, slot, n):
        if self.hook is not None:
            self.hook(slot, n)

    def _backup_task(self, slot, task):
        _kind, kind, data = task
        store_with_sidecar(backup_folder(slot.path), data, slot.written_seq, kind, self.key, self.writer)

    def _data(self, slot, job) -> bytes:
        rev = {"seq": job.seq, "writer": self.writer or "", "saved": time.time()}
        d = project.to_dict2(job.content, slot.pid or "", job.source, rev, job.view)
        return json.dumps(d, indent=1, ensure_ascii=False).encode("utf-8")

    def _write(self, slot: Slot, job: Job):
        if slot.status in ("missing", "conflict", "ambiguous", "readonly"):
            self.rescue(slot, job, "fehlt" if slot.status == "missing" else "rettung")
            return
        view_due = job.view_event and project.view_differs(job.view, slot.disk_view)
        same = job.content_hash == (slot.disk_content_hash if slot.has_file else slot.baseline_hash)
        if same and not view_due:
            with slot.cv:                               # the disk already holds what this job asks for
                slot.written_seq = max(slot.written_seq, job.seq)
                slot.status = "saved"
            return
        if same and not slot.has_file:                  # a view alone never makes a project
            with slot.cv:
                slot.written_seq = max(slot.written_seq, job.seq)
            return
        if same:
            kind = "ansicht"
        elif not slot.session_backup_done:
            kind = "sitzung"
        elif self.clock() - slot.last_laufend >= LAUFEND_EVERY_S:
            kind = "laufend"
        else:
            kind = "zwischen"
        data = self._data(slot, job)
        out = None
        for wait in BUSY_RETRY_S + (None,):
            out = write_guarded(slot.path, data, slot.base_hash, kind, job.seq, self.key, self.writer,
                                hook=lambda n: self._hook(slot, n), pending_tmp=slot.pending_tmp)
            if out.kind != "busy" or wait is None:
                break
            self._wait(slot, wait)
        self._settle(slot, job, out, kind, data)

    def _settle(self, slot, job, out, kind, data):
        if out.kind == "written":
            with slot.cv:
                slot.pending_tmp = None
                slot.base_hash = out.new_hash
                slot.disk_content_hash = job.content_hash
                slot.disk_view = job.view
                slot.written_seq = max(slot.written_seq, job.seq)
                slot.written.append(job.seq)
                slot.status, slot.reason, slot.retries = "saved", "", 0
                if out.backup and kind == "sitzung":         # a new project has no state before it to keep
                    slot.session_backup_done = True
                if out.backup and kind in ("sitzung", "laufend"):
                    slot.last_laufend = self.clock()
            if out.backup and kind == "ansicht" and not out.late:
                try:
                    if fsops.delete_verified(out.backup, out.backup_sha, out.backup_size):
                        _drop_sidecar(out.backup + SIDECAR_EXT)
                except OSError:
                    pass
            if out.backup:
                folder = os.path.dirname(out.backup)
                rotate(folder, self.key, self.writer)
                clean_orphan_sidecars(folder, self.key, self.writer)
            self._clean_local(slot)
            return
        if out.kind in ("conflict", "appeared"):
            if out.tmp and os.path.exists(out.tmp):
                try:
                    store_with_sidecar(backup_folder(slot.path), data, job.seq, "konflikt", self.key, self.writer,
                                       src_tmp=out.tmp)
                except OSError:
                    fsops.discard_tmp(out.tmp)
            self._mark(slot, "conflict", out.kind)
            self.rescue(slot, job, "rettung")
            return
        if out.kind == "missing":
            self._missing(slot, job)
            return
        if out.kind == "busy":
            self._mark(slot, "error", "busy")
            self.rescue(slot, job, "rettung")
            with slot.cv:
                slot.retry_at = self.clock() + BUSY_AGAIN_S
            return
        if out.kind == "error_after_move":
            with slot.cv:
                slot.pending_tmp = out.tmp
            self._failed(slot, job, out.error)
            return
        if out.kind == "unsupported":
            self._mark(slot, "error", "unsupported")
            self.rescue(slot, job, "rettung")
            return

    def _missing(self, slot, job):
        where = classify(slot.path)
        if where in ("drive", "dir_unreachable"):
            self._mark(slot, "error", where)
            self.rescue(slot, job, "rettung")
            self._retry_later(slot)
            return
        if where == "missing":
            for wait in MISSING_LOOKS_S:                  # a sync client replacing the file: gone for a moment
                self._wait(slot, wait)
                if os.path.exists(slot.path):
                    with slot.cv:
                        if slot.pending is None:
                            slot.pending = job
                    return
        folder = os.path.dirname(slot.path)
        twins = id_candidates(folder, slot.pid) if slot.pid else []
        self._mark(slot, "ambiguous" if len(twins) > 1 else "missing", where if not twins else "renamed")
        self.rescue(slot, job, "fehlt")

    def _failed(self, slot, job, error):
        reason = "full" if getattr(error, "errno", None) == errno.ENOSPC or getattr(error, "winerror", None) == 112 \
            else type(error).__name__
        self._mark(slot, "error", reason)
        if job is not None:
            self.rescue(slot, job, "rettung")
        self._retry_later(slot)

    def _retry_later(self, slot):
        with slot.cv:
            delay = ERROR_RETRY_S[min(slot.retries, len(ERROR_RETRY_S) - 1)]
            slot.retries += 1
            slot.retry_at = self.clock() + delay

    def _mark(self, slot, status, reason=""):
        with slot.cv:
            slot.status, slot.reason = status, reason
            slot.cv.notify_all()

    # -- local rescue (4.3)
    def rescue(self, slot: Slot, job: Job, art: str):
        """A local copy of ``job`` in the per-user data folder (rescue thread); ``rescued_seq`` when it is on disk."""
        with self._rescue_cv:
            self._rescue_jobs.append((slot, job, art))
            if self._rescue_thread is None or not self._rescue_thread.is_alive():
                self._rescue_thread = threading.Thread(target=self._rescue_run, daemon=True, name="project-rescue")
                self._rescue_thread.start()
            self._rescue_cv.notify_all()

    def local_folder(self) -> str | None:
        if self.data_dir:
            try:
                os.makedirs(self.data_dir, exist_ok=True)
                return self.data_dir
            except OSError:
                return None
        return paths.ensure(LOCAL_DIR)

    def _rescue_run(self):
        while True:
            with self._rescue_cv:
                if not self._rescue_jobs:
                    return
                slot, job, art = self._rescue_jobs.pop(0)
            try:
                self.rescue_now(slot, job, art)
            except Exception:
                with slot.cv:
                    slot.reason = (slot.reason + "+rescue").lstrip("+")

    def rescue_now(self, slot: Slot, job: Job, art: str) -> str | None:
        folder = self.local_folder()
        if folder is None:
            with slot.cv:
                slot.reason = (slot.reason + "+norescue").lstrip("+")
            return None
        rev = {"seq": job.seq, "writer": self.writer or "", "saved": time.time()}
        d = project.to_dict2(job.content, slot.pid or "", job.source, rev, job.view)
        d["local"] = {"path": slot.path, "art": art}
        data = json.dumps(d, indent=1, ensure_ascii=False).encode("utf-8")
        lkey = local_key(slot.pid, job.source.get("path") or slot.path)
        path = os.path.join(folder, local_name(lkey, job.seq, art))
        try:
            if self.key and self.writer:
                fsops.write_new(path + SIDECAR_EXT,
                                sidecar_bytes(os.path.basename(path), sha(data), len(data), self.writer, art, self.key))
            fsops.write_new(path, data)
        except FileExistsError:
            pass                                       # this seq is there already
        with slot.cv:
            slot.rescued_seq = max(slot.rescued_seq, job.seq)
            slot.cv.notify_all()
        return path

    def _clean_local(self, slot: Slot):
        """Rescue copies (``rettung``) up to the seq now confirmed in the project file are no longer needed – removed
        only through delete_verified with their own sidecar. ``fehlt``/``wiederherstellung`` stay for the user."""
        folder = self.local_folder()
        if folder is None:
            return
        lkey = local_key(slot.pid, (slot.latest.source.get("path") if slot.latest else None) or slot.path)
        for seq, art, path in local_candidates(folder, lkey):
            if art != "rettung" or seq > slot.written_seq:
                continue
            side = read_sidecar(path + SIDECAR_EXT, self.key, self.writer)
            if side is None or side.get("file") != os.path.basename(path):
                continue
            try:
                if fsops.delete_verified(path, side["sha256"], side["size"]):
                    fsops.delete_verified(path + SIDECAR_EXT, side["raw_sha"], side["raw_size"])
            except OSError:
                pass

    # -- quitting (4.7)
    def unsecured(self) -> list:
        """Slots whose newest state is neither confirmed in the project file nor in a local copy."""
        with self.lock:
            return [s for s in self.slots if s.latest_seq > max(s.written_seq, s.rescued_seq)]

    def secure_all(self):
        """Quit phase 1: every slot with an unconfirmed state gets a local copy as well (the project write keeps
        running); poll ``unsecured()`` until it is empty – never end the process before."""
        for s in self.unsecured():
            if s.latest is not None:
                self.rescue(s, s.latest, "rettung")

    def wait_idle(self, timeout: float = 30.0) -> bool:
        """Tests: until no slot has anything waiting or running."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            with self.lock:
                busy = [s for s in self.slots if s.pending is not None or s.in_flight is not None or s.fifo]
            with self._rescue_cv:
                rescuing = bool(self._rescue_jobs) or (self._rescue_thread is not None and self._rescue_thread.is_alive())
            if not busy and not rescuing:
                return True
            time.sleep(0.005)
        return False

    def stop(self):
        self._stopping = True
        with self.lock:
            slots = list(self.slots)
        for s in slots:
            with s.cv:
                s.cv.notify_all()


_REGISTRY = []
_REGISTRY_LOCK = threading.Lock()


def registry() -> Registry:
    """The program's one registry."""
    with _REGISTRY_LOCK:
        if not _REGISTRY:
            _REGISTRY.append(Registry())
        return _REGISTRY[0]
