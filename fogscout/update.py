"""Update on start: pull the newest state from GitHub and keep the packages in step.

Run by start.bat with the program's Python, before the program starts:

    python fogscout\\update.py            update check; exit code 3 = updated (start.bat restarts itself)
    python fogscout\\update.py --deps     install packages if requirements*.txt changed since last time

Standard library only (it runs before anything else and must not depend on the packages).
Only safe updates: on branch main, no own changes to tracked files, fast-forward only.
Anything else (offline, other branch, local commits, git missing, option off) -> skip
quietly and start the version that is there. Only this launcher step talks to GitHub;
the program itself (detection, overlay) still opens no internet connection.

The result is left in .venv\\update_status.txt for the program to show in its log.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

UPDATED, NOTHING, SKIPPED = 3, 0, 1
FETCH_TIMEOUT = 25          # s; offline or a hanging credential prompt must not block the start
STATUS_FILE = "update_status.txt"
REQUIREMENTS = (("requirements.txt", False), ("requirements-extra.txt", True))   # (file, --no-deps)

# Own small translation table: this script runs before the program and may not import it.
EN = {
    "Update-Prüfung ist ausgeschaltet.": "Update check is switched off.",
    "Update übersprungen: git ist nicht installiert.": "Update skipped: git is not installed.",
    "Update übersprungen: kein Git-Ordner (entpackte Kopie).": "Update skipped: not a git folder (unpacked copy).",
    "Update übersprungen: {reason}": "Update skipped: {reason}",
    "Update übersprungen: Zweig „{current}“ statt „{branch}“.":
        "Update skipped: branch “{current}” instead of “{branch}”.",
    "Update übersprungen: eigene Änderungen an Programmdateien.":
        "Update skipped: own changes to program files.",
    "Update übersprungen: GitHub nicht erreichbar": "Update skipped: GitHub not reachable",
    "Update übersprungen: eigene Commits auf main (kein reines Nachziehen möglich).":
        "Update skipped: own commits on main (a plain fast-forward is not possible).",
    "Update fehlgeschlagen, alter Stand bleibt: {error}": "Update failed, the old version stays: {error}",
    "Update installiert: {old} → {new}": "Update installed: {old} → {new}",
    "Update installiert.": "Update installed.",
    "Installiere Pakete aus {name} ...": "Installing packages from {name} ...",
    "Pakete aus {name} installiert.": "Packages from {name} installed.",
    "Pakete aus {name} konnten nicht installiert werden (Internet?) – nächster Start versucht es wieder.":
        "Packages from {name} could not be installed (internet?) – the next start tries again.",
    "Suche nach Updates ...": "Looking for updates ...",
    "Update-Prüfung fehlgeschlagen: {error}": "Update check failed: {error}",
    "Kein Update – Version {version} ist aktuell.": "No update – version {version} is up to date.",
    "Update verfügbar: {old} → {new}": "Update available: {old} → {new}",
    "Wird nicht installiert: eigene Änderungen an Programmdateien.":
        "Will not be installed: own changes to program files.",
}
_lang = None


def _language(root) -> str:
    """Same choice as the program: settings.json "ui_language", "auto" = Windows language."""
    env = os.environ.get("DBDMS_LANG")
    if env in ("de", "en"):
        return env
    try:
        with open(os.path.join(root, "settings.json"), encoding="utf-8") as fh:
            setting = json.load(fh).get("ui_language", "auto")
    except (OSError, ValueError, AttributeError):
        setting = "auto"
    if setting in ("de", "en"):
        return setting
    try:
        if sys.platform == "win32":
            import ctypes
            return "de" if (ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF) == 0x07 else "en"
        import locale
        return "de" if (locale.getlocale()[0] or os.environ.get("LANG", "")).lower().startswith("de") else "en"
    except Exception:
        return "en"


def _t(root, text, **kw) -> str:
    global _lang
    if _lang is None:
        _lang = _language(root)
    out = EN.get(text, text) if _lang == "en" else text
    return out.format(**kw) if kw else out


UNSAFE_PREFIXES = ("SSL_CERT_", "PYTHON", "GIT_")         # 1.38.21 (audit SEC-2): as fogscout/launch.py – this
UNSAFE_NAMES = ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")   # script runs as administrator from start.bat


def _clean_environment(environ) -> dict:
    """``environ`` without the variables a program of the user may set (HKCU\\Environment) to steer git or the
    certificates it trusts. Proxies stay."""
    return {k: v for k, v in environ.items()
            if not (k.upper().startswith(UNSAFE_PREFIXES) or k.upper() in UNSAFE_NAMES)}


def _git_exe() -> str | None:
    """1.38.57 (security review): git as administrator – on Windows Git for Windows from its machine-wide entry
    (HKLM, only administrators write it), so a git.exe somewhere earlier on the user's PATH is not taken. Else
    the PATH (Linux, or git installed some other way)."""
    if sys.platform == "win32":
        try:
            import winreg
        except ImportError:
            winreg = None
        for view in ((winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY) if winreg else ()):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GitForWindows", 0,
                                    winreg.KEY_READ | view) as key:
                    base = winreg.QueryValueEx(key, "InstallPath")[0]
            except OSError:
                continue
            exe = os.path.join(str(base), "cmd", "git.exe")
            if os.path.isfile(exe):
                return exe
    return shutil.which("git")


# 1.38.57: the only values taken over from the user's global git config (read, never run) – the line endings Git
# for Windows sets and the folders the user marked safe. Everything else in it is ignored.
GLOBAL_KEEP = {"core.autocrlf": ("true", "false", "input"), "core.eol": ("lf", "crlf", "native"),
               "safe.directory": None}
_kept: dict = {}


def _global_settings(exe, env) -> list:
    """``-c key=value`` for GLOBAL_KEEP from the user's global config (``git config --global --get-all``)."""
    if exe in _kept:
        return _kept[exe]
    out = []
    for key, allowed in GLOBAL_KEEP.items():
        try:
            r = subprocess.run([exe, "config", "--global", "--get-all", key], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=10, env=env,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except (OSError, subprocess.TimeoutExpired):
            continue
        if r.returncode != 0:
            continue
        for value in (r.stdout or "").splitlines()[:20]:
            value = value.strip()
            if value and "\0" not in value and (allowed is None or value.lower() in allowed):
                out += ["-c", f"{key}={value}"]
    _kept[exe] = out
    return out


def _git(root, *args, timeout=15):
    # 1.38.21: git runs as administrator in a folder the user writes to – the settings that make git run a program
    # (hooks, the fsmonitor command, a credential helper) are overridden on the command line, which beats every
    # config file. 1.38.57 (security review): the user's global config (%USERPROFILE%\.gitconfig – any program of
    # the user writes it) is switched off entirely (GIT_CONFIG_GLOBAL): there url.…insteadOf, a smudge filter, an
    # askpass program or http.sslVerify=false would steer the administrator's git. The system config stays (Git for
    # Windows keeps core.autocrlf there; switching it off made every file count as changed – the Windows CI showed
    # it), and of the global one only GLOBAL_KEEP is passed on.
    exe = _git_exe() or "git"
    env = dict(_clean_environment(os.environ), GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")   # never wait for a password
    kept = _global_settings(exe, env)
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"         # Git for Windows maps it to nul
    hard = ["-c", "core.fsmonitor=false", "-c", "core.hooksPath=" + os.path.join(root, ".venv", "no-hooks"),
            "-c", "credential.helper=", "-c", "http.sslVerify=true", *kept]
    try:
        r = subprocess.run([exe, *hard, *args], cwd=root, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, env=env,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)
    return r.returncode, (r.stdout or r.stderr).strip()


def _enabled(root) -> bool:
    if os.environ.get("DBDMS_FORCE_UPDATE") == "1":       # "Aktualisieren und neu starten" in the program
        return True
    try:
        with open(os.path.join(root, "settings.json"), encoding="utf-8") as fh:
            return bool(json.load(fh).get("auto_update", True))
    except (OSError, ValueError, AttributeError):
        return True


def _version(root, rev) -> str:
    for package in ("fogscout", "dbdmapscout"):            # 1.9: revisions up to 1.8.91 carry the old package
        code, text = _git(root, "show", f"{rev}:{package}/__init__.py")
        m = re.search(r'__version__\s*=\s*"([^"]+)"', text) if code == 0 else None
        if m:
            return m.group(1)
    return "?"


def _repo_problem(root, branch):
    """Why this folder cannot be updated (message), or None."""
    if _git_exe() is None:
        return _t(root, "Update übersprungen: git ist nicht installiert.")
    if not os.path.isdir(os.path.join(root, ".git")):
        return _t(root, "Update übersprungen: kein Git-Ordner (entpackte Kopie).")
    code, current = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0:
        return _t(root, "Update übersprungen: {reason}", reason=current)
    if current != branch:
        return _t(root, "Update übersprungen: Zweig „{current}“ statt „{branch}“.", current=current, branch=branch)
    return None


# 1.46.6 (user: the old account name should disappear everywhere): clones made before the GitHub account was renamed
# still fetch through GitHub's redirect from the old name – which would end if someone took that name. Exactly
# those origin addresses (also the repository's name before 1.9) are moved to REPO_URL; a fork or any other
# address is left alone.
REPO_URL = "https://github.com/senisinx/fog-scout.git"
OLD_OWNER = "sarujansa"                                # the account's name before 1.46.5 – the only place left
OLD_ORIGIN = re.compile(r"(?i)^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
                        + OLD_OWNER + r"/(?:fog-scout|dbd-map-scout)(?:\.git)?/?$")


def _move_origin(root) -> bool:
    """Point origin from the old account to REPO_URL (only the local .git/config changes). True if moved."""
    code, url = _git(root, "config", "--local", "--get", "remote.origin.url")   # as stored, no insteadOf
    if code != 0 or not OLD_ORIGIN.match(url.strip()):
        return False
    return _git(root, "remote", "set-url", "origin", REPO_URL)[0] == 0


def _fetch(root, branch):
    """git fetch; returns (old, new, None) or (None, None, message)."""
    _move_origin(root)
    _, old = _git(root, "rev-parse", "HEAD")
    code, out = _git(root, "fetch", "--quiet", "origin", branch, timeout=FETCH_TIMEOUT)
    if code != 0:
        return None, None, _t(root, "Update übersprungen: GitHub nicht erreichbar") + (
            f" ({out.splitlines()[-1]})" if out else ".")
    _, new = _git(root, "rev-parse", "FETCH_HEAD")
    return old, new, None


def _changes(root, old, new):
    _, log = _git(root, "log", "--format=%s", f"{old}..{new}")
    changes = [line for line in log.splitlines() if line and not line.startswith("Merge pull request")]
    return "".join(f"\n  • {c}" for c in changes[:12])


def check(root: str, branch: str = "main"):
    """"Nach Updates suchen" in the program: fetch and compare, never change a file.
    Returns (state, message, can_apply) with state "current" | "available" | "error"."""
    problem = _repo_problem(root, branch)
    if problem:
        return "error", problem, False
    old, new, problem = _fetch(root, branch)
    if problem:
        return "error", problem, False
    if new == old:
        return "current", _t(root, "Kein Update – Version {version} ist aktuell.", version=_version(root, old)), False
    if _git(root, "merge-base", "--is-ancestor", "HEAD", "FETCH_HEAD")[0] != 0:
        return "error", _t(root, "Update übersprungen: eigene Commits auf main (kein reines Nachziehen möglich)."), False
    msg = _t(root, "Update verfügbar: {old} → {new}", old=_version(root, old), new=_version(root, new))
    try:
        msg += _changes(root, old, new)
    except Exception:
        pass
    if _git(root, "diff", "--quiet", "HEAD")[0] != 0:
        return "available", msg + "\n" + _t(root, "Wird nicht installiert: eigene Änderungen an Programmdateien."), False
    return "available", msg, True


def update(root: str, branch: str = "main"):
    """Returns (exit code, message for the log)."""
    if not _enabled(root):
        return SKIPPED, _t(root, "Update-Prüfung ist ausgeschaltet.")
    problem = _repo_problem(root, branch)
    if problem:
        return SKIPPED, problem
    if _git(root, "diff", "--quiet", "HEAD")[0] != 0:
        return SKIPPED, _t(root, "Update übersprungen: eigene Änderungen an Programmdateien.")
    old, new, problem = _fetch(root, branch)
    if problem:
        return SKIPPED, problem
    if new == old:
        return NOTHING, ""
    if _git(root, "merge-base", "--is-ancestor", "HEAD", "FETCH_HEAD")[0] != 0:
        return SKIPPED, _t(root, "Update übersprungen: eigene Commits auf main (kein reines Nachziehen möglich).")
    code, out = _git(root, "merge", "--ff-only", "--quiet", "FETCH_HEAD")
    if code != 0:
        return SKIPPED, _t(root, "Update fehlgeschlagen, alter Stand bleibt: {error}", error=out)
    # files (maybe start.bat itself) have changed now: whatever happens below, report UPDATED so
    # start.bat restarts itself instead of reading on in its changed file
    try:
        msg = _t(root, "Update installiert: {old} → {new}", old=_version(root, old), new=_version(root, new))
        msg += _changes(root, old, new)
    except Exception:
        msg = _t(root, "Update installiert.")
    return UPDATED, msg


# ------------------------------------------------------------------ packages
def _digest(path) -> str | None:
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def sync_packages(root: str, venv: str, run=None) -> list:
    """pip install for every requirements file that changed since it was last installed.
    Returns messages. ``run(args) -> exit code`` can be replaced in tests."""
    run = run or (lambda args: subprocess.run(args).returncode)
    msgs = []
    for name, no_deps in REQUIREMENTS:
        digest = _digest(os.path.join(root, name))
        if digest is None:
            continue
        stamp = os.path.join(venv, name + ".sha256")
        try:
            with open(stamp, encoding="utf-8") as fh:
                if fh.read().strip() == digest:
                    continue
        except OSError:
            pass
        print(_t(root, "Installiere Pakete aus {name} ...", name=name))
        # 1.12.3: wheels only – pip never builds a source package here (its setup.py would run as administrator);
        # every pinned package has wheels for Windows and Python 3.12–3.14
        # 1.38.57 (security review): isolated (no pip.ini, no PIP_* of the user – they could name another index),
        # only PyPI, and only files whose SHA-256 is in the requirements file (tools/hash_requirements.py)
        args = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--isolated", "--index-url",
                "https://pypi.org/simple", "--only-binary=:all:", "--require-hashes", "-r", os.path.join(root, name)]
        if no_deps:
            args.insert(-2, "--no-deps")
        if run(args) == 0:
            with open(stamp, "w", encoding="utf-8") as fh:
                fh.write(digest)
            msgs.append(_t(root, "Pakete aus {name} installiert.", name=name))
        else:
            msgs.append(_t(root, "Pakete aus {name} konnten nicht installiert werden (Internet?) – nächster Start "
                                 "versucht es wieder.", name=name))
    return msgs


def _write_status(venv: str, lines) -> None:
    lines = [line for line in lines if line]
    if not lines:
        return
    try:
        with open(os.path.join(venv, STATUS_FILE), "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    except OSError:
        pass


def main(argv) -> int:
    for stream in (sys.stdout, sys.stderr):          # umlauts on an old console code page must not crash
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv = os.path.join(root, ".venv")
    if "--deps" in argv:
        _write_status(venv, sync_packages(root, venv))
        return 0
    print(_t(root, "Suche nach Updates ..."))
    try:
        code, msg = update(root)
    except Exception as e:                          # never block the start
        code, msg = SKIPPED, _t(root, "Update-Prüfung fehlgeschlagen: {error}", error=f"{type(e).__name__}: {e}")
    if msg:
        print(msg)
    _write_status(venv, [msg])
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
