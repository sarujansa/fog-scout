"""1.33.3: start programs that are not Fog Scout's own – OBS, Explorer, the browser, a file's own program.

The packaged program (PyInstaller, ``paths.frozen()``) changes its own process so that its libraries are found in
``_internal``: the bootloader points the DLL search at that folder (``SetDllDirectoryW``) and the PySide6 runtime hook
puts it in front of ``PATH`` and sets ``QT_PLUGIN_PATH``/``QML2_IMPORT_PATH``. A program started from here inherits all
of it. Saru's update to 1.33.2 stopped at ``_internal\\msvcp140.dll``: OBS, started by Fog Scout ("OBS automatisch
starten"), had loaded the C++ runtime from Fog Scout's folder instead of Windows' – it held the file and ran with a
runtime it was never built against (and, being a Qt program too, saw our Qt plugin folder).

Everything that starts another program goes through here (``open_url``, ``open_path``, ``show_in_folder``,
``start_program``; ``tests/test_launch.py`` keeps it that way): while it starts, the DLL search is Windows' own and
the environment is the one Fog Scout was started with. From a source checkout (start.bat) nothing changes.
Standard library only (spotify.py and ytupload.py use it).
"""
from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import threading
import webbrowser

QT_VARS = ("QT_PLUGIN_PATH", "QML2_IMPORT_PATH")     # PyInstaller's pyi_rth_pyside6 sets them to the bundle
_LOCK = threading.RLock()                             # the process-wide state is changed by one start at a time


def bundle_dir() -> str:
    """The packaged program's ``_internal`` folder – "" when running from source."""
    return str(getattr(sys, "_MEIPASS", "") or "") if getattr(sys, "frozen", False) else ""


def _inside(path: str, folder: str) -> bool:
    if not path or not folder:
        return False
    p = os.path.normcase(os.path.abspath(path)).rstrip("\\/")
    f = os.path.normcase(os.path.abspath(folder)).rstrip("\\/")
    return p == f or p.startswith(f + os.sep)


def child_env(environ=None, bundle: str | None = None) -> dict:
    """The environment for another program: without the bundle's folders in ``PATH``, without the Qt variables that
    point into the bundle and without PyInstaller's own ``_PYI_*`` variables. Unchanged from source."""
    env = dict(os.environ if environ is None else environ)
    bundle = bundle_dir() if bundle is None else bundle
    if not bundle:
        return env
    for key in list(env):
        upper = key.upper()
        if upper == "PATH":
            parts = [p for p in env[key].split(os.pathsep) if p and not _inside(p, bundle)]
            env[key] = os.pathsep.join(parts)
        elif upper in QT_VARS:
            if all(_inside(p, bundle) for p in env[key].split(os.pathsep) if p):
                del env[key]
        elif upper.startswith("_PYI_") or upper == "_MEIPASS2":
            del env[key]
    return env


def _kernel32():
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.GetDllDirectoryW.argtypes = [wintypes.DWORD, wintypes.LPWSTR]
    k32.GetDllDirectoryW.restype = wintypes.DWORD
    k32.SetDllDirectoryW.argtypes = [wintypes.LPCWSTR]
    k32.SetDllDirectoryW.restype = wintypes.BOOL
    return k32


def dll_directory() -> str:
    """What SetDllDirectoryW set for this process ("" = Windows' own search; always "" outside Windows)."""
    if sys.platform != "win32":
        return ""
    import ctypes
    buf = ctypes.create_unicode_buffer(32768)
    n = _kernel32().GetDllDirectoryW(len(buf), buf)
    return buf.value if n else ""


@contextlib.contextmanager
def clean_process():
    """While a program is started: Windows' own DLL search and the clean environment (``child_env``) – also for
    starts that take no environment (``os.startfile``, ``webbrowser``, ShellExecute). Restored right after."""
    bundle = bundle_dir()
    if not bundle:
        yield
        return
    with _LOCK:
        saved = dict(os.environ)
        clean = child_env(saved, bundle)
        k32 = _kernel32() if sys.platform == "win32" else None
        old_dir = dll_directory() if k32 else ""
        try:
            for key in [k for k in saved if k not in clean]:
                del os.environ[key]
            for key, value in clean.items():
                if saved.get(key) != value:
                    os.environ[key] = value
            if k32:
                k32.SetDllDirectoryW(None)
            yield
        finally:
            if k32:
                k32.SetDllDirectoryW(old_dir or None)
            for key in [k for k in os.environ if k not in saved]:
                del os.environ[key]
            for key, value in saved.items():
                if os.environ.get(key) != value:
                    os.environ[key] = value


def open_url(url: str, *args, **kwargs) -> bool:
    """``webbrowser.open`` without handing the bundle to the browser."""
    with clean_process():
        return webbrowser.open(url, *args, **kwargs)


def open_path(path: str) -> None:
    """A file or folder with its own program (Windows: ``os.startfile``; raises OSError like it)."""
    with clean_process():
        os.startfile(path)                                    # noqa: S606 – the user's own program for the file


def show_in_folder(path: str):
    """Windows Explorer with the file marked (nothing else runs the file)."""
    with clean_process():
        return subprocess.Popen(["explorer", "/select,", os.path.normpath(path)],     # noqa: S603, S607
                                env=child_env())


def start_program(args: list, cwd: str | None = None, creationflags: int = 0):
    """Another program, detached (OBS)."""
    with clean_process():
        return subprocess.Popen(args, cwd=cwd, close_fds=True, creationflags=creationflags,   # noqa: S603
                                env=child_env())
