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


# 1.38.21 (audit SEC-2): variables any program of the user can set in HKCU\Environment and that steer this process
# or its children when it runs as administrator – which certificates TLS trusts (the update check), what Python
# imports (PYTHONPATH/PYTHONHOME for the helpers started with sys.executable), what git does (hooks, fsmonitor,
# sslCAInfo), where Qt loads plugins from. Proxies stay: a proxy alone cannot break TLS, and some PCs need one.
UNSAFE_PREFIXES = ("SSL_CERT_", "PYTHON", "GIT_")
UNSAFE_NAMES = ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "QT_QPA_PLATFORM_PLUGIN_PATH")


def clean_elevated_environment(environ, bundle: str = "") -> dict:
    """``environ`` without the variables above; the Qt plugin variables stay only when they point into the bundle
    (PyInstaller's runtime hook sets them – from source they are never ours). Pure."""
    out = {}
    for key, value in environ.items():
        upper = key.upper()
        if upper.startswith(UNSAFE_PREFIXES) or upper in UNSAFE_NAMES:
            continue
        if upper in QT_VARS and not (bundle and all(_inside(p, bundle) for p in value.split(os.pathsep) if p)):
            continue
        out[key] = value
    return out


def harden_start_environment() -> list:
    """At the very start of the elevated program: drop those variables from the process (its own TLS context is
    built later and reads SSL_CERT_*; children inherit the rest). Returns the names dropped; [] when not elevated."""
    if not elevated():
        return []
    from . import paths                       # (paths only needs the standard library at import)
    with _LOCK:
        clean = clean_elevated_environment(os.environ, bundle_dir())
        if paths.installed():
            # 1.38.57 (security review): a user-level DBDMS_DATA_DIR would redirect where the elevated, installed
            # program writes. Only installed: CI runs the bare FogScout.exe --selftest elevated with it set.
            clean = {k: v for k, v in clean.items() if k.upper() != paths.ENV}
        gone = sorted(k for k in os.environ if k not in clean)
        for key in gone:
            del os.environ[key]
    return gone


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
                # 1.33.5 (review S8): "" rather than None – None would put the current folder back into the
                # search of every thread while the program starts; "" leaves it out and is all a child inherits
                k32.SetDllDirectoryW("")
            yield
        finally:
            if k32:
                k32.SetDllDirectoryW(old_dir or None)
            for key in [k for k in os.environ if k not in saved]:
                del os.environ[key]
            for key, value in saved.items():
                if os.environ.get(key) != value:
                    os.environ[key] = value


def elevated() -> bool:
    """Windows: this process runs with administrator rights (the scheduled task, UAC); False elsewhere."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _explorer() -> str:
    from .paths import windows_dir                 # 1.33.5 (review S4): by its full path, not searched for
    return os.path.join(windows_dir(), "explorer.exe")


def _through_users_shell(target: str):
    """1.38.21 (audit SEC-1): from the elevated program, a URL or file is handed to ``explorer.exe``, which passes
    it to the user's running shell – the browser or the file's program then starts with the user's own rights.
    ShellExecute from this process (``webbrowser``, ``os.startfile``) would start it elevated and reads the
    handler from ``HKCU\\Software\\Classes`` first, a key every program of the user may write: a known way from
    user to administrator without a prompt (the same threat model as S4/S5 in 1.33.5)."""
    return subprocess.Popen([_explorer(), target], env=child_env())   # noqa: S603


def open_url(url: str, *args, **kwargs) -> bool:
    """``webbrowser.open`` without handing the bundle to the browser; elevated: through the user's shell."""
    with clean_process():
        if elevated():
            if not str(url).lower().startswith(("http://", "https://")):
                return False                              # only web addresses leave this way
            _through_users_shell(url)
            return True
        return webbrowser.open(url, *args, **kwargs)


def open_path(path: str) -> None:
    """A file or folder with its own program (Windows: ``os.startfile``; raises OSError like it); elevated:
    through the user's shell."""
    with clean_process():
        if elevated():
            _through_users_shell(os.path.normpath(path))
            return
        os.startfile(path)                                    # noqa: S606 – the user's own program for the file


def show_in_folder(path: str):
    """Windows Explorer with the file marked (nothing else runs the file)."""
    with clean_process():
        from .paths import windows_dir             # 1.33.5 (review S4): by its full path, not searched for
        return subprocess.Popen([os.path.join(windows_dir(), "explorer.exe"), "/select,",   # noqa: S603
                                 os.path.normpath(path)], env=child_env())


def start_program(args: list, cwd: str | None = None, creationflags: int = 0):
    """Another program, detached (OBS)."""
    with clean_process():
        return subprocess.Popen(args, cwd=cwd, close_fds=True, creationflags=creationflags,   # noqa: S603
                                env=child_env())
