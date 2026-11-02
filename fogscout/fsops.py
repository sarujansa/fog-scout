"""1.18.1 (Implementierungsplan Fassung 6, 3.7/3.8): the only file operations the editor's project saving uses – none
of them ever replaces an existing file. Checked on the platforms first (tests/test_fsprimitives.py, "Gate 0"):

* ``create_exclusive(src, dst)`` – a finished file takes a name nobody has yet: Windows ``os.rename`` (MoveFileExW
  without MOVEFILE_REPLACE_EXISTING, W2), Linux ``renameat2(RENAME_NOREPLACE)`` (L1). Anything else fails safely
  (``UnsupportedFS``) – there is no fallback that could overwrite.
* ``ExclusiveHandle`` – Windows: the file opened with share mode 0, so no other process can open it while it is held
  (W5/W17); it is read and hashed, renamed (FileRenameInfo, ReplaceIfExists = FALSE – W16/W18/W23) and deleted
  (FileDispositionInfo – W22) through that same handle. POSIX (tests/CI): the same interface without that protection.
* ``delete_verified`` – deletes only when the full SHA-256 and size are what the caller expects.

Pure standard library (os, ctypes, hashlib); nothing here knows about projects."""
from __future__ import annotations

import ctypes
import errno
import hashlib
import os
import secrets
import sys

WIN = sys.platform == "win32"
LINUX = sys.platform.startswith("linux")
TMP_SUFFIX = ".tmp"

# Windows
GENERIC_READ, GENERIC_WRITE, DELETE = 0x80000000, 0x40000000, 0x00010000
OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL = 3, 0x80
FILE_RENAME_INFO_CLASS, FILE_DISPOSITION_INFO_CLASS = 3, 4
ERROR_SHARING_VIOLATION = 32
EXISTS_ERRORS = (80, 183)                     # ERROR_FILE_EXISTS, ERROR_ALREADY_EXISTS
UNSUPPORTED_ERRORS = (1, 50, 87)              # ERROR_INVALID_FUNCTION, ERROR_NOT_SUPPORTED, ERROR_INVALID_PARAMETER
# Linux
AT_FDCWD, RENAME_NOREPLACE = -100, 1
UNSUPPORTED_ERRNOS = {errno.EINVAL, errno.ENOSYS, getattr(errno, "EOPNOTSUPP", 95), getattr(errno, "ENOTSUP", 95)}


class UnsupportedFS(OSError):
    """This platform or file system cannot create/rename without the risk of replacing – the operation was not done."""


def _unsupported(what: str, path: str, code: int = errno.ENOSYS) -> UnsupportedFS:
    return UnsupportedFS(code, f"{what} is not supported here", path)


# ---- Linux: renameat2(RENAME_NOREPLACE)
_RENAMEAT2 = []


def _renameat2():
    if not _RENAMEAT2:
        fn = None
        if LINUX:
            try:
                libc = ctypes.CDLL(None, use_errno=True)
                fn = getattr(libc, "renameat2", None)
                if fn is not None:
                    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
                    fn.restype = ctypes.c_int
            except OSError:
                fn = None
        _RENAMEAT2.append(fn)
    return _RENAMEAT2[0]


def _rename_noreplace_posix(src: str, dst: str):
    fn = _renameat2()
    if fn is None:
        raise _unsupported("renameat2", dst)
    if fn(AT_FDCWD, os.fsencode(src), AT_FDCWD, os.fsencode(dst), RENAME_NOREPLACE) == 0:
        return
    e = ctypes.get_errno()
    if e == errno.EEXIST:
        raise FileExistsError(e, os.strerror(e), dst)
    if e in UNSUPPORTED_ERRNOS:
        raise _unsupported("RENAME_NOREPLACE", dst, e)
    raise OSError(e, os.strerror(e), dst)


# ---- creating
def create_exclusive(src: str, dst: str):
    """Give the finished file ``src`` the name ``dst`` – only if ``dst`` does not exist (else FileExistsError, ``src``
    stays). Never replaces; an unsupported platform or file system raises UnsupportedFS."""
    if WIN:
        os.rename(src, dst)                   # MoveFileExW without MOVEFILE_REPLACE_EXISTING (Gate 0 W2)
    elif LINUX:
        _rename_noreplace_posix(src, dst)     # Gate 0 L1
    else:
        raise _unsupported("exclusive create", dst)


def tmp_name(path: str) -> str:
    """A unique temp name beside ``path`` (same folder = same volume): ``.<name>.<pid>.<random>.tmp``."""
    folder, name = os.path.split(path)
    return os.path.join(folder, f".{name}.{os.getpid()}.{secrets.token_hex(4)}{TMP_SUFFIX}")


def write_tmp(path: str, data: bytes) -> str:
    """``data`` into a new temp file beside ``path`` (created exclusively), flushed and fsync'ed; its name. A failure
    leaves no temp file."""
    tmp = tmp_name(path)
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o644)
    try:
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    except BaseException:
        os.close(fd)
        discard_tmp(tmp)
        raise
    os.close(fd)
    return tmp


def discard_tmp(tmp: str):
    """Remove a temp file this process just made (``write_tmp``) – only names of that pattern."""
    if os.path.basename(tmp).startswith(".") and tmp.endswith(TMP_SUFFIX):
        try:
            os.remove(tmp)
        except OSError:
            pass


def write_new(path: str, data: bytes):
    """A new file ``path`` with ``data`` – complete or not at all, never over an existing one (FileExistsError)."""
    tmp = write_tmp(path, data)
    try:
        create_exclusive(tmp, path)
    except BaseException:
        discard_tmp(tmp)
        raise


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---- Windows: one handle, share mode 0
_K32 = []


def _k32():
    if not _K32:
        from ctypes import wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                                  wintypes.DWORD, wintypes.HANDLE]
        k.CreateFileW.restype = wintypes.HANDLE
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        k.SetFileInformationByHandle.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
        k.SetFileInformationByHandle.restype = wintypes.BOOL
        _K32.append(k)
    return _K32[0]


def _invalid(h) -> bool:
    return h is None or h in (-1, 2 ** 64 - 1, 2 ** 32 - 1)


def _rename_info(target: str):
    from ctypes import wintypes

    class FILE_RENAME_INFO(ctypes.Structure):
        _fields_ = [("ReplaceIfExists", wintypes.BOOLEAN), ("RootDirectory", wintypes.HANDLE),
                    ("FileNameLength", wintypes.DWORD), ("FileName", wintypes.WCHAR * 1)]
    name = os.path.abspath(target)
    wchar = ctypes.sizeof(wintypes.WCHAR)
    size = ctypes.sizeof(FILE_RENAME_INFO) + len(name) * wchar
    buf = ctypes.create_string_buffer(size)
    info = FILE_RENAME_INFO.from_buffer(buf)
    info.ReplaceIfExists = False                         # never replace (Gate 0 W18)
    info.RootDirectory = None
    info.FileNameLength = len(name) * wchar
    ctypes.memmove(ctypes.addressof(buf) + FILE_RENAME_INFO.FileName.offset, ctypes.create_unicode_buffer(name),
                   (len(name) + 1) * wchar)
    return buf, size


class ExclusiveHandle:
    """``path`` opened for reading and deleting. Windows: share mode 0 – while this object holds it, no other process
    can open the file at all (Gate 0 W5/W17), so what ``read`` returned is what ``rename_to``/``delete`` act on.
    Opening fails with PermissionError (winerror 32) while anybody else has the file open, FileNotFoundError when it
    is gone. POSIX: an ordinary descriptor – no such protection (plan RR17)."""

    def __init__(self, path: str):
        self.path = path
        self._fd = None
        if WIN:
            import msvcrt
            k = _k32()
            h = k.CreateFileW(path, GENERIC_READ | DELETE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
            if _invalid(h):
                raise ctypes.WinError(ctypes.get_last_error())
            self._fd = msvcrt.open_osfhandle(h, os.O_RDONLY)
        else:
            self._fd = os.open(path, os.O_RDONLY)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False

    def close(self):
        if self._fd is not None:
            fd, self._fd = self._fd, None
            os.close(fd)

    def read(self) -> bytes:
        os.lseek(self._fd, 0, os.SEEK_SET)
        out = bytearray()
        while True:
            chunk = os.read(self._fd, 1 << 20)
            if not chunk:
                return bytes(out)
            out += chunk

    def rename_to(self, dst: str):
        """The file takes the name ``dst`` – never over an existing file (FileExistsError). Windows: through this
        handle (FileRenameInfo), the file stays held; a file system that refuses that raises UnsupportedFS and nothing
        happened (the caller may then use ``rename_fallback`` after ``close``)."""
        if WIN:
            import msvcrt
            buf, size = _rename_info(dst)
            if not _k32().SetFileInformationByHandle(msvcrt.get_osfhandle(self._fd), FILE_RENAME_INFO_CLASS, buf, size):
                err = ctypes.get_last_error()
                if err in EXISTS_ERRORS:
                    raise FileExistsError(errno.EEXIST, "target exists", dst)
                if err in UNSUPPORTED_ERRORS:
                    raise _unsupported("rename by handle", dst, err)
                raise ctypes.WinError(err)
        else:
            _rename_noreplace_posix(self.path, dst)
        self.path = dst

    def delete(self):
        """Windows: the file goes when this handle closes (FileDispositionInfo) – nobody could open it in between.
        POSIX: unlinked by name (the gap between the last read and this, plan RR17)."""
        if WIN:
            import msvcrt
            from ctypes import wintypes

            class FILE_DISPOSITION_INFO(ctypes.Structure):
                _fields_ = [("DeleteFile", wintypes.BOOLEAN)]
            info = FILE_DISPOSITION_INFO(True)
            if not _k32().SetFileInformationByHandle(msvcrt.get_osfhandle(self._fd), FILE_DISPOSITION_INFO_CLASS,
                                                     ctypes.byref(info), ctypes.sizeof(info)):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            os.unlink(self.path)


def rename_fallback(src: str, dst: str):
    """Windows only, after a file system refused rename by handle: an ordinary rename that still never replaces
    (MoveFileExW without REPLACE_EXISTING) – the small gap between closing the handle and this is plan RR1."""
    if not WIN:
        raise _unsupported("rename fallback", dst)
    os.rename(src, dst)


def delete_verified(path: str, sha256: str, size: int) -> bool:
    """Delete ``path`` only if its full SHA-256 and size are ``sha256``/``size`` – checked and deleted under one
    exclusive handle on Windows. False (nothing deleted) when the content differs; PermissionError while another
    program has it open; FileNotFoundError when it is gone."""
    with ExclusiveHandle(path) as h:
        data = h.read()
        if len(data) != int(size) or sha256_bytes(data) != str(sha256):
            return False
        h.delete()
    return True
