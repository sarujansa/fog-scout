"""1.18 Gate 0: the file-system promises the editor's safe saving (1.18.1/1.18.2) will be built on – checked on the
platform itself before any product code relies on them. Only tests, no product code: every primitive is called
through ctypes/os right here. Windows checks run on the windows-latest CI job, the POSIX check on Linux.

Names follow the plan (W = Windows assumption, L = Linux assumption):
W1 GenericDataLocation is %LOCALAPPDATA%       W2 os.rename never replaces an existing file
W3 an open handle without FILE_SHARE_DELETE blocks a rename
W4 a FILE_SHARE_DELETE handle allows the rename and writes into the renamed file
W5/W17 a share-mode-0 handle blocks every other open (also from another process, also with FILE_SHARE_DELETE)
W6 msvcrt.open_osfhandle/os.read/get_osfhandle work on such a handle
W7 st_ino/st_dev stay the same across a rename on the same volume
W16/W23 rename by handle (FileRenameInfo) works, also into a sub-folder
W18 FileRenameInfo with ReplaceIfExists = FALSE refuses an existing target
W19 a writable mapped view whose file handle was closed still blocks the exclusive open
W22 delete by handle (FileDispositionInfo) under a share-mode-0 handle
L1 renameat2(RENAME_NOREPLACE) works on the CI file system and refuses an existing target
"""
import os
import stat
import subprocess
import sys

import pytest

WIN = sys.platform == "win32"
only_windows = pytest.mark.skipif(not WIN, reason="Windows file-system semantics")
only_linux = pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux renameat2")

GENERIC_READ, GENERIC_WRITE, DELETE = 0x80000000, 0x40000000, 0x00010000
SHARE_READ, SHARE_WRITE, SHARE_DELETE = 1, 2, 4
OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL = 3, 0x80
FILE_RENAME_INFO_CLASS, FILE_DISPOSITION_INFO_CLASS = 3, 4
ERROR_SHARING_VIOLATION, ERROR_ALREADY_EXISTS = 32, 183


def _write(path, data=b"original"):
    with open(path, "wb") as fh:
        fh.write(data)


def _read(path):
    with open(path, "rb") as fh:
        return fh.read()


def _k32():
    import ctypes
    from ctypes import wintypes
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                              wintypes.DWORD, wintypes.HANDLE]
    k.CreateFileW.restype = wintypes.HANDLE
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    k.CloseHandle.restype = wintypes.BOOL
    k.SetFileInformationByHandle.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    k.SetFileInformationByHandle.restype = wintypes.BOOL
    k.WriteFile.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD),
                            wintypes.LPVOID]
    k.WriteFile.restype = wintypes.BOOL
    k.CreateFileMappingW.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD,
                                     wintypes.LPCWSTR]
    k.CreateFileMappingW.restype = wintypes.HANDLE
    k.MapViewOfFile.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
    k.MapViewOfFile.restype = wintypes.LPVOID
    k.UnmapViewOfFile.argtypes = [wintypes.LPCVOID]
    k.UnmapViewOfFile.restype = wintypes.BOOL
    return k


def _invalid(h):
    return h is None or h == -1 or h == 2 ** 64 - 1 or h == 2 ** 32 - 1


def _open(path, access, share):
    """CreateFileW → (handle or None, last error)."""
    import ctypes
    k = _k32()
    h = k.CreateFileW(path, access, share, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
    err = ctypes.get_last_error()
    return (None if _invalid(h) else h), err


def _close(h):
    _k32().CloseHandle(h)


def _rename_by_handle(h, target, replace=False):
    """SetFileInformationByHandle(FileRenameInfo) → (ok, last error). FILE_RENAME_INFO: BOOLEAN ReplaceIfExists,
    HANDLE RootDirectory, DWORD FileNameLength (bytes), WCHAR FileName[] – the layout under test (W16)."""
    import ctypes
    from ctypes import wintypes

    class FILE_RENAME_INFO(ctypes.Structure):
        _fields_ = [("ReplaceIfExists", wintypes.BOOLEAN), ("RootDirectory", wintypes.HANDLE),
                    ("FileNameLength", wintypes.DWORD), ("FileName", wintypes.WCHAR * 1)]
    name = os.path.abspath(target)
    size = ctypes.sizeof(FILE_RENAME_INFO) + len(name) * ctypes.sizeof(wintypes.WCHAR)
    buf = ctypes.create_string_buffer(size)
    info = FILE_RENAME_INFO.from_buffer(buf)
    info.ReplaceIfExists = bool(replace)
    info.RootDirectory = None
    info.FileNameLength = len(name) * ctypes.sizeof(wintypes.WCHAR)
    ctypes.memmove(ctypes.addressof(buf) + FILE_RENAME_INFO.FileName.offset, ctypes.create_unicode_buffer(name),
                   (len(name) + 1) * ctypes.sizeof(wintypes.WCHAR))
    ok = _k32().SetFileInformationByHandle(h, FILE_RENAME_INFO_CLASS, buf, size)
    return bool(ok), ctypes.get_last_error()


def _delete_by_handle(h):
    import ctypes
    from ctypes import wintypes

    class FILE_DISPOSITION_INFO(ctypes.Structure):
        _fields_ = [("DeleteFile", wintypes.BOOLEAN)]
    info = FILE_DISPOSITION_INFO(True)
    ok = _k32().SetFileInformationByHandle(h, FILE_DISPOSITION_INFO_CLASS, ctypes.byref(info), ctypes.sizeof(info))
    return bool(ok), ctypes.get_last_error()


# ---- W1
@only_windows
def test_w1_generic_data_location_is_localappdata():
    from PySide6.QtCore import QStandardPaths
    got = QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation)
    assert got and os.path.normcase(os.path.normpath(got)) == os.path.normcase(os.path.normpath(os.environ["LOCALAPPDATA"]))


# ---- W2
@only_windows
def test_w2_os_rename_never_replaces_an_existing_file(tmp_path):
    a, b = str(tmp_path / "a.json"), str(tmp_path / "b.json")
    _write(a, b"new")
    _write(b, b"foreign")
    with pytest.raises(FileExistsError):
        os.rename(a, b)
    assert _read(b) == b"foreign" and _read(a) == b"new"
    os.chmod(b, stat.S_IREAD)                                   # a read-only target as well
    try:
        with pytest.raises(FileExistsError):
            os.rename(a, b)
        assert _read(b) == b"foreign"
    finally:
        os.chmod(b, stat.S_IREAD | stat.S_IWRITE)
    d = tmp_path / "dir.json"                                   # a folder at the target name
    d.mkdir()
    with pytest.raises(OSError):
        os.rename(a, str(d))
    assert d.is_dir() and _read(a) == b"new"


# ---- W3
@only_windows
def test_w3_an_open_handle_without_share_delete_blocks_the_rename(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a)
    with open(a, "rb"):                                         # Python/CRT open: no FILE_SHARE_DELETE
        with pytest.raises(PermissionError) as info:
            os.rename(a, str(tmp_path / "b.json"))
    assert getattr(info.value, "winerror", None) == ERROR_SHARING_VIOLATION
    assert os.path.exists(a)


# ---- W4
@only_windows
def test_w4_a_share_delete_handle_allows_the_rename_and_writes_into_the_renamed_file(tmp_path):
    import ctypes
    from ctypes import wintypes
    a, b = str(tmp_path / "a.json"), str(tmp_path / "b.json")
    _write(a, b"")
    h, err = _open(a, GENERIC_WRITE, SHARE_READ | SHARE_WRITE | SHARE_DELETE)
    assert h is not None, err
    try:
        os.rename(a, b)                                         # allowed while that handle is open
        n = wintypes.DWORD()
        assert _k32().WriteFile(h, b"late write", 10, ctypes.byref(n), None)
    finally:
        _close(h)
    assert not os.path.exists(a) and _read(b) == b"late write"  # the write followed the file, not the name


# ---- W5 / W17
@only_windows
def test_w5_exclusive_open_fails_while_any_other_handle_is_open(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a)
    with open(a, "rb"):                                         # even a read-only handle
        h, err = _open(a, GENERIC_READ | DELETE, 0)
        assert h is None and err == ERROR_SHARING_VIOLATION
    h2, err = _open(a, GENERIC_WRITE, SHARE_READ | SHARE_WRITE | SHARE_DELETE)
    assert h2 is not None, err
    try:
        h, err = _open(a, GENERIC_READ | DELETE, 0)             # and a FILE_SHARE_DELETE handle as well
        assert h is None and err == ERROR_SHARING_VIOLATION
    finally:
        _close(h2)
    h, err = _open(a, GENERIC_READ | DELETE, 0)                 # all closed: now it works
    assert h is not None, err
    _close(h)


_CHILD = r"""
import ctypes, sys
from ctypes import wintypes
k = ctypes.WinDLL("kernel32", use_last_error=True)
k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                          wintypes.DWORD, wintypes.HANDLE]
k.CreateFileW.restype = wintypes.HANDLE
out = []
for access in (0x80000000, 0x40000000, 0x00010000, 0):
    for share in range(8):
        h = k.CreateFileW(sys.argv[1], access, share, None, 3, 0x80, None)
        if h is None or h in (-1, 2 ** 64 - 1, 2 ** 32 - 1):
            out.append(str(ctypes.get_last_error()))
        else:
            k.CloseHandle(h)
            out.append("opened")
print(",".join(out))
"""


@only_windows
def test_w17_a_held_exclusive_handle_blocks_every_open_from_another_process(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a)
    h, err = _open(a, GENERIC_READ | DELETE, 0)
    assert h is not None, err
    try:
        res = subprocess.run([sys.executable, "-c", _CHILD, a], capture_output=True, text=True, timeout=60)
        results = res.stdout.strip().split(",")
        assert len(results) == 32, res.stderr
        # every access (read, write, delete, attributes only) with every share mode: a sharing violation – except the
        # attribute-only open (access 0), which Windows lets through without data access
        data_access = results[:24]
        assert all(r == str(ERROR_SHARING_VIOLATION) for r in data_access), results
    finally:
        _close(h)


# ---- W6
@only_windows
def test_w6_the_handle_works_as_a_python_file_descriptor(tmp_path):
    import msvcrt
    a = str(tmp_path / "a.json")
    _write(a, b"0123456789" * 100)
    h, err = _open(a, GENERIC_READ | DELETE, 0)
    assert h is not None, err
    fd = msvcrt.open_osfhandle(h, os.O_RDONLY)
    try:
        assert msvcrt.get_osfhandle(fd) == h
        data = b""
        while True:
            chunk = os.read(fd, 256)
            if not chunk:
                break
            data += chunk
        assert data == b"0123456789" * 100
    finally:
        os.close(fd)                                            # closes the handle as well
    h, err = _open(a, GENERIC_READ | DELETE, 0)                 # really closed
    assert h is not None, err
    _close(h)


# ---- W7
@only_windows
def test_w7_file_id_and_volume_stay_across_a_rename(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a)
    st = os.stat(a)
    assert st.st_ino != 0 and st.st_dev != 0
    sub = tmp_path / "Sicherungen"
    sub.mkdir()
    b = str(sub / "b.json")
    os.rename(a, b)
    st2 = os.stat(b)
    assert (st2.st_ino, st2.st_dev) == (st.st_ino, st.st_dev)


# ---- W16 / W23 / W18
@only_windows
def test_w16_w23_rename_by_handle_moves_the_file_into_a_sub_folder(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a, b"kept content")
    sub = tmp_path / "Sicherungen" / "proj"
    sub.mkdir(parents=True)
    target = str(sub / "backup.json")
    h, err = _open(a, GENERIC_READ | DELETE, 0)
    assert h is not None, err
    try:
        ok, err = _rename_by_handle(h, target)
        assert ok, err
        other, oerr = _open(target, GENERIC_READ, SHARE_READ | SHARE_WRITE | SHARE_DELETE)   # still held: blocked
        assert other is None and oerr == ERROR_SHARING_VIOLATION
    finally:
        _close(h)
    assert not os.path.exists(a) and _read(target) == b"kept content"


@only_windows
def test_w18_rename_by_handle_refuses_an_existing_target(tmp_path):
    a, b = str(tmp_path / "a.json"), str(tmp_path / "b.json")
    _write(a, b"ours")
    _write(b, b"foreign")
    h, err = _open(a, GENERIC_READ | DELETE, 0)
    assert h is not None, err
    try:
        ok, err = _rename_by_handle(h, b, replace=False)
        assert not ok and err == ERROR_ALREADY_EXISTS
    finally:
        _close(h)
    assert _read(a) == b"ours" and _read(b) == b"foreign"


# ---- W19
@only_windows
def test_w19_a_writable_mapped_view_blocks_the_exclusive_open(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a, b"x" * 4096)
    k = _k32()
    fh, err = _open(a, GENERIC_READ | GENERIC_WRITE, SHARE_READ | SHARE_WRITE)
    assert fh is not None, err
    mapping = k.CreateFileMappingW(fh, None, 0x04, 0, 0, None)     # PAGE_READWRITE
    assert mapping
    view = k.MapViewOfFile(mapping, 0x0002, 0, 0, 0)               # FILE_MAP_WRITE
    assert view
    _close(fh)                                                     # the file handle is gone, the view stays
    try:
        h, err = _open(a, GENERIC_READ | DELETE, 0)
        if h is not None:
            _close(h)
        assert h is None and err == ERROR_SHARING_VIOLATION, (
            "W19 false: a mapped view without file handle does not block the exclusive open (plan RR1 addendum)")
    finally:
        k.UnmapViewOfFile(view)
        _close(mapping)


# ---- W22
@only_windows
def test_w22_delete_by_handle_under_an_exclusive_handle(tmp_path):
    a = str(tmp_path / "a.json")
    _write(a)
    h, err = _open(a, GENERIC_READ | DELETE, 0)
    assert h is not None, err
    try:
        ok, err = _delete_by_handle(h)
        assert ok, err
        other, oerr = _open(a, GENERIC_READ, SHARE_READ | SHARE_WRITE | SHARE_DELETE)
        assert other is None                                       # held / delete pending: nobody gets it
    finally:
        _close(h)
    assert not os.path.exists(a)


# ---- L1
def _renameat2():
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    fn = getattr(libc, "renameat2", None)
    if fn is None:
        return None
    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    fn.restype = ctypes.c_int
    return fn


@only_linux
def test_l1_renameat2_noreplace_on_the_ci_file_system(tmp_path):
    import ctypes
    import errno
    fn = _renameat2()
    assert fn is not None, "glibc without renameat2"
    AT_FDCWD, RENAME_NOREPLACE = -100, 1
    a, b = str(tmp_path / "a.json"), str(tmp_path / "b.json")
    _write(a, b"ours")
    _write(b, b"foreign")
    r = fn(AT_FDCWD, a.encode(), AT_FDCWD, b.encode(), RENAME_NOREPLACE)
    assert r == -1 and ctypes.get_errno() == errno.EEXIST
    assert _read(a) == b"ours" and _read(b) == b"foreign"
    os.unlink(b)
    r = fn(AT_FDCWD, a.encode(), AT_FDCWD, b.encode(), RENAME_NOREPLACE)
    assert r == 0 and not os.path.exists(a) and _read(b) == b"ours"
