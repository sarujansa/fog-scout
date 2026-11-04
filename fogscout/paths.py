"""1.18.1 (Implementierungsplan Fassung 6, 4.3): the per-user application data folder – rescue copies of editor
projects, the SHA-256 cache of recordings, the installation id and the key that signs backup sidecars. Never the
program folder (it may be read-only, and it is shared by every user): Qt's GenericDataLocation + ``FogScout`` –
%LOCALAPPDATA%\\FogScout on Windows (Gate 0 W1), ~/.local/share/FogScout elsewhere. ``DBDMS_DATA_DIR`` replaces it
(the tests point it at a temp folder; tests/conftest.py fails any test that reaches the real one)."""
from __future__ import annotations

import os
import secrets
import sys

from . import fsops

APP_DIR = "FogScout"
ENV = "DBDMS_DATA_DIR"
WRITER_FILE = "writer-id"
KEY_FILE = "backup-key"
KEY_BYTES = 32


def _qt_location() -> str:
    try:
        from PySide6.QtCore import QStandardPaths
        return QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation) or ""
    except Exception:                                   # no Qt (helper processes, broken install): the fallback
        return ""


def user_data_dir() -> str | None:
    """The folder (not created); None when no per-user location is known – then there is no rescue copy, never a
    fallback to the program folder."""
    forced = os.environ.get(ENV)
    if forced:
        return forced
    base = _qt_location() or os.environ.get("LOCALAPPDATA") or ""
    return os.path.join(base, APP_DIR) if base else None


def frozen() -> bool:
    """1.30.1 (.exe, stage 2): running as the packaged program (PyInstaller sets ``sys.frozen``), not from a source
    checkout via start.bat."""
    return bool(getattr(sys, "frozen", False))


def data_root(program_root: str) -> str:
    """1.30.1 (.exe, stage 2): where the program's own runtime files live – settings.json, rounds.jsonl,
    official.jsonl, the log, crash files, cache/, backup/, user_maps/, debug/. From a source checkout (start.bat) the
    program folder, exactly as before; the packaged program sits in Program Files (read-only, shared by every user),
    so there it is the per-user data folder. Created when missing."""
    if not frozen():
        return program_root
    path = user_data_dir()
    if not path:
        raise OSError("no per-user data folder (LOCALAPPDATA) for the settings")
    os.makedirs(path, exist_ok=True)
    return path


def ensure(sub: str = "") -> str | None:
    """``user_data_dir()/sub`` created and proven writable (a probe file written, fsync'ed and removed); None if not."""
    root = user_data_dir()
    if not root:
        return None
    path = os.path.join(root, sub) if sub else root
    try:
        os.makedirs(path, exist_ok=True)
        probe = fsops.write_tmp(os.path.join(path, "probe"), b"ok")
        fsops.discard_tmp(probe)
        return path
    except OSError:
        return None


def _read_or_create(name: str, make, valid) -> bytes | None:
    """The content of ``name`` in the data folder, created once (exclusively) by ``make()``. A file that is there but
    not ``valid`` is never overwritten – None then (the caller treats its backups as unverifiable)."""
    root = ensure()
    if root is None:
        return None
    path = os.path.join(root, name)
    for _attempt in range(2):
        try:
            with open(path, "rb") as fh:
                data = fh.read()
            return data if valid(data) else None
        except FileNotFoundError:
            try:
                fsops.write_new(path, make())
            except FileExistsError:                       # another start made it a moment ago: read that one
                continue
            except OSError:
                return None
        except OSError:
            return None
    return None


def writer_id() -> str | None:
    """This installation's id (32 hex), written into every project revision and backup sidecar."""
    data = _read_or_create(WRITER_FILE, lambda: secrets.token_hex(16).encode("ascii"),
                           lambda d: len(d.strip()) == 32 and all(c in b"0123456789abcdef" for c in d.strip()))
    return data.strip().decode("ascii") if data else None


def backup_key() -> bytes | None:
    """The key of the HMAC in backup sidecars (Fassung 6, 4.2) – 32 random bytes, made once, never rewritten."""
    return _read_or_create(KEY_FILE, lambda: secrets.token_bytes(KEY_BYTES), lambda d: len(d) == KEY_BYTES)
