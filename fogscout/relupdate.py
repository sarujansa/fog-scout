"""1.33 (.exe, stage 5): updates of the installed program from GitHub Releases – standard library only.

Every merge to main builds a release (.github/workflows/build.yml, job ``release``): tag ``build-<N>`` with
``FogScout-Setup-<version>.exe`` and ``….exe.sha256``. The packaged program knows its own build number from
``build-info.json`` next to its files (written by CI before PyInstaller).

The program asks GitHub (``API`` – the latest release of this repository, nothing else) only when the user clicks
"Jetzt nach Updates suchen" or, if "Beim Start Updates suchen" is on, once after the start. Downloading the setup
needs the click "Aktualisieren und neu starten"; the file must come from this repository's release download path,
stay under ``MAX_BYTES`` and match the SHA-256 the release states (the ``.sha256`` asset and, when GitHub lists one,
the asset's own digest). Installing needs one more confirmation; then (1.33.2) the program checks the setup once more, starts
it itself and quits – the setup waits for the program to end (installer/fogscout.iss, InitializeSetup). Until 1.33.1 a
helper ran from the program folder and could hold the files the setup replaces. Nothing is sent but the requests, no
account, no token, nothing about the user.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .i18n import _

REPO = "sarujansa/fog-scout"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
DOWNLOAD_PREFIX = f"https://github.com/{REPO}/releases/download/"
TAG = re.compile(r"^build-(\d{1,9})$")
SETUP = re.compile(r"^FogScout-Setup-[0-9][0-9A-Za-z.]*\.exe$")
INFO_FILE = "build-info.json"
UPDATE_DIR = os.path.join("cache", "update")
MAX_BYTES = 400 * 1024 * 1024        # the setup is ~120 MB (1.32)
MAX_JSON = 2 * 1024 * 1024
TIMEOUT_S = 30
CHUNK = 1024 * 1024
USER_AGENT = "FogScout-updater"


@dataclass
class Release:
    build: int
    version: str
    tag: str
    setup_name: str
    setup_url: str
    size: int
    sha_url: str
    digest: str = ""                 # GitHub's own "sha256:…" of the asset, when listed
    sha256: str = ""                 # 1.33.1: the checked SHA-256 after download() – the install helper checks it again


def own_build(root: str) -> dict:
    """{"build": int, "version": str, "commit": str} of this packaged program – {} from a source checkout."""
    try:
        with open(os.path.join(root, INFO_FILE), encoding="utf-8") as fh:
            info = json.load(fh)
        return {"build": int(info.get("build", 0)), "version": str(info.get("version", "")),
                "commit": str(info.get("commit", ""))}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


def parse_release(data: dict) -> Release:
    """The parts of a release that matter, checked; ValueError when anything is not as the workflow makes it."""
    if not isinstance(data, dict) or data.get("draft") or data.get("prerelease"):
        raise ValueError("kein veröffentlichtes Release")
    m = TAG.match(str(data.get("tag_name", "")))
    if not m:
        raise ValueError("unbekanntes Tag")
    tag = m.group(0)
    assets = {a.get("name"): a for a in data.get("assets") or [] if isinstance(a, dict)}
    setups = [n for n in assets if isinstance(n, str) and SETUP.match(n)]
    if len(setups) != 1:
        raise ValueError("kein eindeutiges Setup im Release")
    name = setups[0]
    setup, sha = assets[name], assets.get(name + ".sha256")
    if not sha:
        raise ValueError("Prüfsumme fehlt im Release")
    base = DOWNLOAD_PREFIX + tag + "/"
    for a, n in ((setup, name), (sha, name + ".sha256")):
        if a.get("browser_download_url") != base + n:
            raise ValueError("Download-Adresse gehört nicht zu diesem Programm")
    size = int(setup.get("size") or 0)
    if not 0 < size <= MAX_BYTES:
        raise ValueError("unerwartete Grösse")
    digest = str(setup.get("digest") or "")
    if digest and not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        digest = ""
    version = name[len("FogScout-Setup-"):-len(".exe")]
    return Release(int(m.group(1)), version, tag, name, setup["browser_download_url"], size,
                   sha["browser_download_url"], digest[len("sha256:"):])


def _opener():
    """1.33.1 (audit M-2): redirects (GitHub sends release downloads to its storage host) only to https – since
    1.33.5 the program's one opener (net.py)."""
    from .net import opener
    return opener()


def _get(url: str, opener, limit: int) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with opener.open(req, timeout=TIMEOUT_S) as r:
        data = r.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Antwort zu gross")
    return data


def latest(opener=None) -> Release:
    data = json.loads(_get(API, opener or _opener(), MAX_JSON).decode("utf-8"))
    return parse_release(data)


def check(root: str, opener=None):
    """(state, message, can_apply, release) – state "current" | "available" | "error"; only reads GitHub."""
    mine = own_build(root)
    try:
        rel = latest(opener)
    except (OSError, ValueError) as e:
        return "error", _("Update-Prüfung fehlgeschlagen: {error}", error=e), False, None
    if rel.build <= mine.get("build", 0):
        return "current", _("Kein Update – Version {version} (Build {build}) ist aktuell.",
                            version=mine.get("version") or "?", build=mine.get("build", 0)), False, None
    return ("available", _("Update verfügbar: {old} → {new} (Build {build}).", old=mine.get("version") or "?",
                           new=rel.version, build=rel.build), True, rel)


def expected_sha(rel: Release, opener=None) -> str:
    """The SHA-256 the release states: its .sha256 file (first word), equal to GitHub's digest when that is listed."""
    text = _get(rel.sha_url, opener or _opener(), 4096).decode("ascii", "replace").strip()
    word = (text.split() or [""])[0].lower()
    if not re.fullmatch(r"[0-9a-f]{64}", word):
        raise ValueError("Prüfsummen-Datei unlesbar")
    if rel.digest and rel.digest != word:
        raise ValueError("Prüfsummen von GitHub und Release passen nicht zusammen")
    return word


def download(rel: Release, data_dir: str, opener=None, progress=None) -> str:
    """Fetch the setup into data_dir/cache/update, check size and SHA-256; returns its path. A failed or wrong
    download leaves nothing behind; older setups there are removed."""
    opener = opener or _opener()
    want = expected_sha(rel, opener)
    folder = os.path.join(data_dir, UPDATE_DIR)
    os.makedirs(folder, exist_ok=True)
    final = os.path.join(folder, rel.setup_name)
    tmp = final + ".part"
    h, got = hashlib.sha256(), 0
    req = urllib.request.Request(rel.setup_url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(req, timeout=TIMEOUT_S) as r, open(tmp, "wb") as fh:
            while True:
                block = r.read(CHUNK)
                if not block:
                    break
                got += len(block)
                if got > MAX_BYTES or got > rel.size:
                    raise ValueError("Download grösser als angekündigt")
                h.update(block)
                fh.write(block)
                if progress:
                    progress(got, rel.size)
        if got != rel.size:
            raise ValueError("Download unvollständig")
        if h.hexdigest() != want:
            raise ValueError("Prüfsumme passt nicht – Datei verworfen")
        if os.path.exists(final):
            os.remove(final)
        os.rename(tmp, final)
        rel.sha256 = want
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    for name in os.listdir(folder):                 # older setups and leftovers: only our own names
        path = os.path.join(folder, name)
        if path != final and (SETUP.match(name) or (name.endswith(".exe.part") and SETUP.match(name[:-5]))):
            try:
                os.remove(path)
            except OSError:
                pass
    return final


def clean_update_folder(folder: str) -> int:
    """1.33.1 (audit M-3): at the start of the installed program – a setup in the update folder was either installed
    (this is the new version) or not wanted; only our own names go (setups and .part leftovers). Returns how many.
    1.34: ``folder`` is the folder itself – the download folder in data_dir and the program folder's "update"."""
    gone = 0
    try:
        names = os.listdir(folder)
    except OSError:
        return 0
    for name in names:
        if SETUP.match(name) or (name.endswith(".exe.part") and SETUP.match(name[:-len(".part")])):
            try:
                os.remove(os.path.join(folder, name))
                gone += 1
            except OSError:
                pass
    return gone


LOG_FILE = "setup.log"


def install_args(log: str | None = None) -> list[str]:
    """Setup parameters for an update: progress only, no questions, Fog Scout starts again afterwards (/update=1 →
    installer/fogscout.iss [Run]/DeinitializeSetup). 1.33.2: ``log`` = Inno Setup's own log (cache/update/setup.log)
    – what went wrong is readable afterwards."""
    args = ["/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/update=1"]
    if log:
        args.append(f'/LOG="{log}"')
    return args
