"""Tests expect the German texts (the keys); the system language must not matter.

On Windows the tests must never reach the real hosts file: hostsedit.hosts_path() ignores
DBDMS_HOSTS_FILE there on purpose (security of the elevated helper), so any test that would end up
there fails at once instead of writing C:\\Windows\\System32\\drivers\\etc\\hosts.
"""
import os
import sys

import pytest

os.environ.setdefault("DBDMS_LANG", "de")
if sys.platform != "win32":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")      # Qt window tests without a display

WIN = sys.platform == "win32"
only_linux_hosts = pytest.mark.skipif(WIN, reason="would write the real hosts file on Windows")


@pytest.fixture(autouse=True)
def _never_the_real_data_folder(monkeypatch, tmp_path_factory):
    """1.18.1: the per-user data folder (rescue copies, hash cache, installation id, backup key) is a temp folder in
    every test; a test that would still reach the real one fails."""
    folder = tmp_path_factory.mktemp("fogscout-data")
    monkeypatch.setenv("DBDMS_DATA_DIR", str(folder))
    from fogscout import paths
    real = paths._qt_location

    def guarded():
        if not os.environ.get(paths.ENV):
            pytest.fail("test reached the real per-user data folder")
        return real()
    monkeypatch.setattr(paths, "_qt_location", guarded)
    yield
    # the program's one registry and hasher belong to this test's data folder: the next test gets new ones
    ps, fh = sys.modules.get("fogscout.projectsave"), sys.modules.get("fogscout.filehash")
    if ps is not None and ps._REGISTRY:
        ps._REGISTRY[0].wait_idle(10)
        ps._REGISTRY[0].stop()
        ps._REGISTRY.clear()
    if fh is not None and fh._HASHER:
        fh._HASHER[0].stop()
        fh._HASHER.clear()


@pytest.fixture(autouse=True)
def _never_the_real_hosts_file(monkeypatch):
    if WIN:
        from fogscout import hostsedit

        def refuse():
            pytest.fail("test reached the real hosts file")
        monkeypatch.setattr(hostsedit, "hosts_path", refuse)
    yield


_FAKE_MARK = b"FAKEDPAPI1"


def fake_cipher(data: bytes, encrypt: bool) -> bytes:
    """1.28: a reversible stand-in for DPAPI (spotify.CIPHER) – the tests outside Windows store secrets the way the
    program does on Windows; anything not made by it raises ValueError like CryptUnprotectData fails."""
    if encrypt:
        return _FAKE_MARK + bytes(b ^ 0x5A for b in data)
    if not data.startswith(_FAKE_MARK):
        raise ValueError("not ours")
    return bytes(b ^ 0x5A for b in data[len(_FAKE_MARK):])


@pytest.fixture(autouse=True)
def _a_cipher_like_dpapi(monkeypatch):
    """Outside Windows there is no DPAPI (spotify.CIPHER is None and protect() refuses); the tests get the fake one.
    Tests about a missing/failing cipher set spotify.CIPHER themselves. On Windows the real DPAPI is used."""
    from fogscout import spotify
    if spotify.CIPHER is None:
        monkeypatch.setattr(spotify, "CIPHER", fake_cipher)
    yield
