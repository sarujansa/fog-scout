"""Round recordings with OBS (1.4, user's wish: "die Runden mit OBS aufnehmen … auf die externe Festplatte").

OBS records; this program only tells it when – through obs-websocket (built into OBS 28+), and only on this
PC: the address is fixed to 127.0.0.1, never configurable (rule: no connection off the computer). Nothing here
touches DBD. Per round: start at the map banner (plus, if OBS's replay buffer runs, the seconds before it as a
"pre-roll" file), stop at the detected end, name the file after date/map/killer and note it in an index in the
recording folder (``fogscout-recordings.jsonl``). The folder keeps at most ``limit`` bytes: the oldest
recordings *of this index* go first (never any other file on the drive), kept ones stay.

The external drive (Samsung T7) may get another letter after re-plugging: the folder is remembered by its volume
(``\\\\?\\Volume{…}\\``) plus the path on it; a missing drive means no recording and a note, never C: instead.

Only the standard library (a minimal WebSocket client: RFC 6455 handshake, masked text frames, ping/pong) –
plus, since 1.4.2, the ffmpeg binary that imageio-ffmpeg ships, run as a child process on the two files of a
round only (pre-roll + round → one file, stream copy, nothing re-encoded, no network).
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import queue
import re
import shutil
import stat
import socket
import struct
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field

from . import obsoverlay
from .i18n import _

log = logging.getLogger("fogscout")

HOST = "127.0.0.1"               # fixed: OBS on this PC only (never a setting)
DEFAULT_PORT = 4455
TIMEOUT = 3.0                    # s for connecting and for each answer
INDEX = "fogscout-recordings.jsonl"
OLD_INDEX = "dbdmapscout-recordings.jsonl"     # 1.9: the name until 1.8.91 – taken over when first read
LIMITS_GB = (0, 100, 200, 500, 1000)         # 0 = the whole drive (user: "man kann die ganze Platte verwenden")
DEFAULT_LIMIT_GB = 0
RESERVE = 10 * 1024 ** 3        # free space kept on the drive: older recordings go before it is used up
MIN_FREE = 5 * 1024 ** 3        # below this much free space on the drive: no new recording
RENAME_TRIES = 40               # OBS may still hold the file a moment after StopRecord
RENAME_WAIT = 0.5
REPLAY_WAIT = 4.0               # 1.5.4: s to wait for OBS to finish writing the replay buffer (it saves asynchronously)
REPLAY_POLL = 0.2
MAX_MESSAGE = 16 * 1024 * 1024  # 1.8.38: a WebSocket message larger than this ends the connection (OBS sends KBs)
MAX_ROUND_S = 45 * 60           # a recording longer than this is stopped (an end that was never detected)
MAX_MANUAL_S = 4 * 3600         # 1.15: a recording started by hand (record_start) ends after this at the latest
STATUS_POLL_S = 2.0             # 1.15: the recordings page asks OBS for its state this often, only while it is shown
PROFILE_EVERY_S = 30.0          # … the slow-changing values (encoder, buffer length, output size) only this often
FREE_CHECK_S = 10.0             # 1.15: while recording, the drive's free space is looked at this often (MIN_FREE)
EARLY_WAIT_S = 180              # 1.6: started at the end of the loading screen – no banner within this: filed as it is
CLIP_SECONDS = (15, 30, 45, 60, 90, 120, 180, 300)   # 1.6: F8 instant clip – the last n seconds of the replay buffer
                                                     # (1.15: up to 5 min; the card warns when OBS's buffer is shorter)
DEFAULT_CLIP_S = 30
# 1.6 (user: "only DBD and Discord audio, each switchable"): OBS's own "Application Audio Capture" sources,
# created once in the current scene. OBS picks the window by its executable (priority 2) – the title is only a
# hint. OBS does the capture (Windows process loopback); this program only sends the requests.
AUDIO_KIND = "wasapi_process_output_capture"
AUDIO_APPS = {
    "dbd": ("Fog Scout – DBD", "DeadByDaylight:UnrealWindow:DeadByDaylight-Win64-Shipping.exe"),
    "discord": ("Fog Scout – Discord", "Discord:Chrome_WidgetWin_1:Discord.exe"),
}
AUDIO_PRIORITY_EXE = 2
# 1.8.20 (user plays on Epic: the game track stayed silent – the source looked for the Steam executable): which of
# the windows OBS itself lists for the source is ours. Steam: DeadByDaylight-Win64-Shipping.exe, Epic:
# DeadByDaylight-EGS-Shipping.exe, Microsoft Store/Xbox: DeadByDaylight-WinGDK-Shipping.exe (the user plays mostly
# on Steam, sometimes on the others); Discord also as PTB/Canary. Only OBS's own list is read, never the game.
WINDOW_EXES = {"dbd": re.compile(r"^DeadByDaylight[\w-]*\.exe$", re.I),
               "discord": re.compile(r"^Discord(PTB|Canary)?\.exe$", re.I)}
# 1.8.41 (user: "dass das Programm es selber macht mit der Fenstererkennung und im OBS hinterlegen"): OBS's own
# window capture of the DBD window instead of the whole monitor – created once in the scene on air, on top, fitted
# to the canvas. OBS captures (Windows Graphics Capture, like this program's own wincapture), never game capture,
# which hooks into the game. Priority "title, otherwise a window of the same type": class UnrealWindow is the same
# for Steam, Epic and the Store; _follow_window still points it at the running executable.
WINDOW_KIND = "window_capture"
WINDOW_SOURCE = "Fog Scout – DBD-Fenster"
WINDOW_PRIORITY_CLASS = 0              # OBS: 0 title, else same type · 1 title only · 2 title, else same program
WINDOW_METHOD_WGC = 2                  # OBS window capture: 0 automatic · 1 BitBlt · 2 Windows 10 (1903 and up)
# 1.11.7 (user's decision: "Spielaufnahme ist auch in Ordnung"): OBS's game capture as the other way – OBS hooks into
# the game for it (its anti-cheat-compatible hook), this program still never touches DBD; it only asks OBS to do it.
# OBS cannot change the kind of a source, so it is a second source of ours: the chosen one is shown, the other only
# hidden, never deleted. Its own sound stays off – the game's sound comes from our application audio source.
GAME_KIND = "game_capture"
GAME_SOURCE = "Fog Scout – DBD-Spiel"
CAPTURES = ("window", "game")          # Config.capture: which of our picture sources is shown
# 1.8.89 (user: "nur das DBD-Fenster aufnehmen und das Overlay im Spiel"): the window capture has no overlay (our own
# windows) – an image source of ours shows the picture obsoverlay writes, placed over the window item
OVERLAY_KIND = "image_source"
OVERLAY_SOURCE = "Fog Scout – Overlay"
# 1.9: the program was "DbD Map Scout" until 1.8.91 – a source OBS still holds under that name is ours and is renamed
# once (SetInputName: only these four names, the scene items follow the input; the user's sources are never touched)
OLD_SOURCE_NAME = "DbD Map Scout"
OWN_SOURCES = (AUDIO_APPS["dbd"][0], AUDIO_APPS["discord"][0], WINDOW_SOURCE, OVERLAY_SOURCE, GAME_SOURCE)


def video_source(capture: str) -> tuple:
    """(name, kind, settings when created) of our picture source for ``capture`` "window" / "game"."""
    if capture == "game":
        return GAME_SOURCE, GAME_KIND, {"capture_mode": "window", "window": AUDIO_APPS["dbd"][1],
                                        "priority": WINDOW_PRIORITY_CLASS, "capture_cursor": False,
                                        "capture_audio": False, "anti_cheat_hook": True}
    return WINDOW_SOURCE, WINDOW_KIND, {"window": AUDIO_APPS["dbd"][1], "priority": WINDOW_PRIORITY_CLASS,
                                        "method": WINDOW_METHOD_WGC, "cursor": False}
RECHECK_S = 30.0                       # 1.8.41: while DBD runs, OBS is set up again this often if it was not ready
# 1.8.47 (user: "OBS autostart" – when DBD starts, OBS keeps running after it): OBS started by the program, once per
# DBD start, only when no OBS window is open; then looked for every OBS_START_POLL_S up to OBS_START_WAIT_S
OBS_EXE = "obs64.exe"
OBS_ARGS = ("--minimize-to-tray",)
OBS_START_POLL_S = 3.0
OBS_START_WAIT_S = 60.0
OBS_TITLE = re.compile(r"^OBS \d+\.\d+")         # the main window ("OBS 31.0.2 - Profil: … - Szenen: …")
TAILS_S = (0, 3, 5, 8, 10)      # 1.4.1: seconds recorded after the detected end (the result screen)
DEFAULT_TAIL_S = 5
MIN_FILE_BYTES = 1024 * 1024    # 1.4.1: a recording smaller than this is reported as broken/empty
MAGIC = {b"\x1a\x45\xdf\xa3": "mkv", b"ftyp": "mp4"}   # file signatures (mp4: at offset 4)
SHORT_ROUND_S = 300             # 1.4.2: rounds shorter than this go first when room is needed
FFMPEG_TIMEOUT = 600            # s for joining the two files (stream copy: seconds, not minutes)
SPACE_EVERY = 10.0              # s between two looks at the drive (Recorder.space)
DURATION_RE = re.compile(rb"Duration: (\d+):(\d\d):(\d\d(?:\.\d+)?)")
AUDIO_STREAM_RE = re.compile(rb"Stream #\d+:\d+[^\n]*?: Audio:")   # 1.8.5: one per audio track in ffmpeg -i
# 1.8.6 (1.8.5 had only "with/without Discord"): every sound source on its own OBS audio track, like Medal –
# track 1 = everything (plays anywhere), 2 = the game, 3 = Discord, 4 = the microphone. 1.8.19 (user: "es soll
# wirklich nur DBD aufnehmen und Hintergrundprogramme separat"): 5 = background – every other audio source of the
# user's OBS (OBS puts a new source on all six tracks, so the game track carried Spotify, the browser …). Windows'
# desktop sound holds DBD and Discord too (OBS has no "everything but"), so it goes on track 1 only.
# The clip editor mixes them (audio_graph), F8 takes Config.clip_sources for the clip's first track and keeps the
# buffer's own tracks behind it (clip_sound_args, 1.14.4). OBS writes several tracks only in the
# advanced output mode with the recording tracks ticked ([Output] Mode=Advanced, [AdvOut] RecTracks bit mask) –
# we only read those values, never set them.
SOURCES = ("dbd", "discord", "mic", "other")              # the mixable sources, in the order of tracks 2, 3, 4, 5
SOURCE_TRACKS = {"dbd": (1, 2), "desktop": (1,), "discord": (1, 3), "mic": (1, 4), "other": (1, 5)}
REC_TRACKS_NEEDED = 0b11111
DEFAULT_CLIP_SOURCES = SOURCES                             # F8: 1.11.4 (user: "Discord sound etc. in clips too") every source;
                                                           # 1.8.6–1.11.3 only the game and the own voice
LEGACY = -1                                                # 1.8.5 recordings: track 2 = everything but Discord
NAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
CLIPS_DIR = "Clips"              # 1.5.3: clips (editor, F8 instant clips) beside the recordings
FARMING_DIR = "Farming"         # 1.5.3 (user's wish): recordings of farming rounds go into this subfolder


# 1.15 (recording card): what OBS's profile calls its recording encoder → a short name for the card. Only read
# (GetProfileParameter) – the profile is never written. Simple output mode: SimpleOutput/RecEncoder ("x264",
# "jim_nvenc", "obs_nvenc_h264_tex", "amd", "qsv", "nvenc_hevc" …; "Stream" quality = the stream encoder);
# advanced: AdvOut/RecEncoder ("obs_x264", "ffmpeg_nvenc", "h264_texture_amf", "obs_qsv11_v2", "jim_hevc_nvenc" …;
# "none" = the stream encoder). The replay buffer's length in seconds: SimpleOutput/RecRBTime or AdvOut/RecRBTime.
def profile_keys(mode: str) -> dict:
    """(category, name) of the profile values the recording card reads, for output mode ``mode``."""
    if (mode or "").lower() == "advanced":
        return {"encoder": ("AdvOut", "RecEncoder"), "stream": ("AdvOut", "Encoder"),
                "buffer_s": ("AdvOut", "RecRBTime"), "quality": None}
    return {"encoder": ("SimpleOutput", "RecEncoder"), "stream": ("SimpleOutput", "StreamEncoder"),
            "buffer_s": ("SimpleOutput", "RecRBTime"), "quality": ("SimpleOutput", "RecQuality")}


def encoder_label(raw: str) -> str:
    """"jim_hevc_nvenc" → "NVENC HEVC", "obs_x264" → "x264 (CPU)", "" → "" (unknown)."""
    r = (raw or "").lower()
    if not r or r == "none":
        return ""
    codec = "HEVC" if ("hevc" in r or "h265" in r or "265" in r) else "AV1" if "av1" in r else "H.264"
    if "nvenc" in r:
        return f"NVENC {codec}"
    if "amf" in r or r.startswith("amd") or "_amd" in r:
        return f"AMD AMF {codec}"
    if "qsv" in r:
        return f"Quick Sync {codec}"
    if "x264" in r:
        return "x264 (CPU)" + (" – low CPU" if "lowcpu" in r else "")
    if "x265" in r:
        return "x265 (CPU)"
    if "svt" in r or "aom" in r:
        return "AV1 (CPU)"
    if "apple" in r or "vt_" in r or "videotoolbox" in r:
        return f"VideoToolbox {codec}"
    return raw


def rec_elapsed(a: dict | None, now: float | None = None) -> float:
    """Seconds recorded of the active recording ``a`` (Recorder.active) – the pauses taken out (1.15)."""
    if not a:
        return 0.0
    now = time.time() if now is None else now
    paused = float(a.get("paused_s") or 0.0)
    if a.get("paused_at") is not None:
        paused += max(0.0, now - float(a["paused_at"]))
    return max(0.0, now - float(a.get("since") or now) - paused)


class ObsError(Exception):
    def __init__(self, text="", code=None):
        super().__init__(text)
        self.code = code                         # obs-websocket's request status code (None: not from a request)


BUFFER_OFF_CODE = 604                            # InvalidResourceState: "Replay buffer is not available."


def buffer_missing(e: Exception) -> bool:
    """1.8.32: OBS answers this when its replay buffer is not enabled in the settings (it cannot be started)."""
    return getattr(e, "code", None) == BUFFER_OFF_CODE or "not available" in str(e).lower()


def BUFFER_FAILED() -> str:
    """1.8.42: OBS took the start request, but its replay buffer did not start (OBS shows its own dialog)."""
    return _("OBS konnte den Wiederholungspuffer nicht starten (OBS meldet einen Fehler der Ausgabe, meist des "
             "Kodierers – Details im OBS-Log). Das Programm versucht es erst beim nächsten DBD-Start wieder; bis dahin "
             "keine Sofort-Clips (F8) und kein Vorlauf.")


def BUFFER_HINT() -> str:
    return _("In OBS ist der Wiederholungspuffer nicht aktiviert – OBS: Einstellungen → Ausgabe → "
             "Wiederholungspuffer → „Wiederholungspuffer aktivieren“ und übernehmen. Ohne ihn gibt es keine "
             "Sofort-Clips (F8) und keinen Vorlauf.")


# ------------------------------------------------------------------ obs-websocket (v5) client
def auth_string(password: str, salt: str, challenge: str) -> str:
    """obs-websocket 5 authentication: base64(sha256(base64(sha256(password + salt)) + challenge))."""
    secret = base64.b64encode(hashlib.sha256((password + salt).encode()).digest()).decode()
    return base64.b64encode(hashlib.sha256((secret + challenge).encode()).digest()).decode()


def _frame(payload: bytes, opcode: int = 1) -> bytes:
    """A client frame (always masked, RFC 6455 5.3)."""
    head = bytes([0x80 | opcode])
    n = len(payload)
    if n < 126:
        head += bytes([0x80 | n])
    elif n < 1 << 16:
        head += bytes([0x80 | 126]) + struct.pack("!H", n)
    else:
        head += bytes([0x80 | 127]) + struct.pack("!Q", n)
    mask = os.urandom(4)
    return head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload))


class ObsClient:
    """One connection to obs-websocket on this PC."""

    def __init__(self, port: int = DEFAULT_PORT, password: str = "", timeout: float = TIMEOUT):
        self.port, self.password, self.timeout = int(port), password or "", timeout
        self._sock = None
        self._buf = b""
        self.events = []                       # events that came while waiting for an answer (op 5)
        self.version = ""

    # ---- transport
    def _recv_exact(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self._sock.recv(65536)
            if not chunk:
                raise ObsError(_("OBS hat die Verbindung geschlossen"))
            self._buf += chunk
        data, self._buf = self._buf[:n], self._buf[n:]
        return data

    def _recv_message(self) -> str:
        parts = []
        while True:
            b0, b1 = self._recv_exact(2)
            opcode, fin = b0 & 0x0F, b0 & 0x80
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack("!H", self._recv_exact(2))[0]
            elif n == 127:
                n = struct.unpack("!Q", self._recv_exact(8))[0]
            if n + sum(len(p) for p in parts) > MAX_MESSAGE:     # 1.8.38: no length from the wire allocates GBs
                raise ObsError(_("OBS hat die Verbindung geschlossen"))
            mask = self._recv_exact(4) if b1 & 0x80 else None
            data = self._recv_exact(n)
            if mask:
                data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
            if opcode == 8:
                raise ObsError(_("OBS hat die Verbindung geschlossen"))
            if opcode == 9:                    # ping -> pong
                self._sock.sendall(_frame(data, 10))
                continue
            if opcode == 10:
                continue
            parts.append(data)
            if fin:
                return b"".join(parts).decode("utf-8")

    def _send(self, obj):
        self._sock.sendall(_frame(json.dumps(obj).encode("utf-8")))

    def _read(self):
        return json.loads(self._recv_message())

    # ---- protocol
    def connect(self):
        try:
            self._sock = socket.create_connection((HOST, self.port), timeout=self.timeout)
        except OSError as e:
            raise ObsError(_("OBS nicht erreichbar – läuft OBS, ist der WebSocket-Server an? ({error})", error=e.__class__.__name__)) from None
        self._sock.settimeout(self.timeout)
        try:
            return self._handshake()
        except BaseException:
            self.close()                          # a refused login must not leave the socket open
            raise

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode()
        self._sock.sendall((f"GET / HTTP/1.1\r\nHost: {HOST}:{self.port}\r\nUpgrade: websocket\r\n"
                            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n"
                            f"Sec-WebSocket-Protocol: obswebsocket.json\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise ObsError(_("Keine Antwort von obs-websocket"))
            head += chunk
        head, self._buf = head.split(b"\r\n\r\n", 1)
        lines = head.decode("latin-1").split("\r\n")
        if " 101 " not in lines[0] + " ":
            raise ObsError(_("Kein obs-websocket auf diesem Port"))
        want = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest())
        accept = next((ln.split(":", 1)[1].strip() for ln in lines if ln.lower().startswith("sec-websocket-accept")), "")
        if accept.encode() != want:
            raise ObsError(_("Falsche WebSocket-Antwort"))
        hello = self._read()
        if hello.get("op") != 0:
            raise ObsError(_("Unerwartete Begrüssung von OBS"))
        d = hello.get("d", {})
        self.version = str(d.get("obsWebSocketVersion", ""))
        ident = {"rpcVersion": 1, "eventSubscriptions": 64}        # 64 = Outputs (RecordStateChanged)
        auth = d.get("authentication")
        if auth:
            if not self.password:
                raise ObsError(_("OBS verlangt ein Passwort (OBS: Werkzeuge → WebSocket-Servereinstellungen)"))
            ident["authentication"] = auth_string(self.password, auth["salt"], auth["challenge"])
        self._send({"op": 1, "d": ident})
        try:
            msg = self._read()
        except ObsError:
            raise ObsError(_("OBS hat die Anmeldung abgelehnt – Passwort falsch?")) from None
        if msg.get("op") != 2:
            raise ObsError(_("OBS hat die Anmeldung abgelehnt – Passwort falsch?"))
        return self

    def request(self, kind: str, data: dict | None = None) -> dict:
        rid = uuid.uuid4().hex
        self._send({"op": 6, "d": {"requestType": kind, "requestId": rid, "requestData": data or {}}})
        while True:
            msg = self._read()
            if msg.get("op") == 5:
                self.events.append(msg.get("d", {}))
                continue
            d = msg.get("d", {})
            if msg.get("op") == 7 and d.get("requestId") == rid:
                st = d.get("requestStatus", {})
                if not st.get("result"):
                    raise ObsError(f"{kind}: {st.get('comment') or st.get('code')}", st.get("code"))
                return d.get("responseData") or {}

    def close(self):
        sock, self._sock = self._sock, None
        if sock is not None:
            try:
                sock.sendall(_frame(b"", 8))
            except OSError:
                pass
            sock.close()


# ------------------------------------------------------------------ drive and folder
def _kernel32():
    import ctypes
    from ctypes import wintypes
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.GetVolumePathNameW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
    k.GetVolumeNameForVolumeMountPointW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
    return k


def volume_of(path: str) -> tuple[str, str]:
    """(volume name, path on that volume) of a folder – the volume name stays when the drive letter changes.
    ("", path) outside Windows or when it cannot be read."""
    if sys.platform != "win32":
        return "", path
    import ctypes
    try:
        k = _kernel32()
        mount = ctypes.create_unicode_buffer(512)
        if not k.GetVolumePathNameW(os.path.abspath(path), mount, 512):
            return "", path
        name = ctypes.create_unicode_buffer(512)
        if not k.GetVolumeNameForVolumeMountPointW(mount.value, name, 512):
            return "", path
        return name.value, os.path.relpath(os.path.abspath(path), mount.value)
    except Exception:
        return "", path


def find_folder(volume: str, rel: str, last: str) -> str | None:
    """The folder now: on the volume's current drive letter (the T7 after re-plugging), else the last path if
    no volume is known. None = the drive is not connected."""
    if not volume or sys.platform != "win32":
        return last if last and os.path.isdir(last) else None
    import ctypes
    import string
    k = _kernel32()
    name = ctypes.create_unicode_buffer(512)
    for letter in string.ascii_uppercase:
        root = f"{letter}:\\"
        if k.GetVolumeNameForVolumeMountPointW(root, name, 512) and name.value.lower() == volume.lower():
            path = os.path.normpath(os.path.join(root, rel)) if rel and rel != "." else root
            return path if os.path.isdir(path) else None
    return None


def file_name(t: float, label: str, who: str, ext: str, suffix: str = "") -> str:
    """'2026-10-17 21-40 Coal Tower – Nurse.mkv' – no characters Windows forbids."""
    stamp = time.strftime("%Y-%m-%d %H-%M", time.localtime(t))
    parts = [stamp, NAME_CHARS.sub("", label or "Map").strip() or "Map"]
    name = " ".join(parts) + (f" – {NAME_CHARS.sub('', who).strip()}" if who else "") + suffix
    return name[:150] + ext


# ------------------------------------------------------------------ index
@dataclass
class Recording:
    t: float                     # banner time = the round's key (rounds.jsonl)
    file: str                    # file name in the folder
    pre: str = ""                # pre-roll from the replay buffer ("" = none)
    map_id: str = ""
    label: str = ""
    role: str = ""
    killer: str = ""
    end: float = 0.0
    size: int = 0
    keep: bool = False           # never deleted by the limit
    extra: dict = field(default_factory=dict)
    marks: list = field(default_factory=list)   # 1.4.2: F8 moments, seconds from the start of the file
    farming: bool = False        # 1.4.2: a farming round (cross-play off) – goes first when room is needed
    pre_s: float = 0.0           # 1.4.2: seconds of pre-roll at the start of the file (0 = none or separate)
    yt: str = ""                 # 1.10: the YouTube video id once uploaded (ytupload)


def rel_path(folder: str, name: str) -> str | None:
    """Absolute path of an index entry's file: a plain name or one inside a subfolder (``Farming/…``), never
    outside ``folder`` (no absolute path, no ``..``) – None for anything else. Entries use "/" on every system."""
    if not name or os.path.isabs(name) or name.startswith(("/", "\\")) or ":" in name or "\x00" in name:
        return None                                   # ":" = a drive letter; NUL: os.remove raises ValueError on it
    parts = [p for p in re.split(r"[\\/]", name) if p]
    if not parts or any(p in ("..", ".") for p in parts) or len(parts) > 2:
        return None
    return os.path.join(folder, *parts)


def adopt_old_file(folder: str, old: str, new: str) -> bool:
    """1.9: a file the program wrote under its old name is renamed once (True); nothing when the new one exists."""
    o, n = os.path.join(folder, old), os.path.join(folder, new)
    try:
        if os.path.isfile(o) and not os.path.exists(n):
            os.replace(o, n)
            return True
    except OSError:
        pass
    return False


def load_index(folder: str) -> list[Recording]:
    out = []
    adopt_old_file(folder, OLD_INDEX, INDEX)
    try:
        # 1.12.3: errors="replace" and only objects – a line cut inside a character or one that is no object
        # made the whole index unreadable (pruning, marks and the recordings page failed on every call)
        with open(os.path.join(folder, INDEX), encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if isinstance(d, dict):
                        out.append(Recording(**{k: v for k, v in d.items() if k in Recording.__dataclass_fields__}))
                except (ValueError, TypeError):
                    continue
    except OSError:
        pass
    return out


def save_index(folder: str, recs: list[Recording]):
    path = os.path.join(folder, INDEX)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in sorted(recs, key=lambda r: r.t):
            f.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())           # 1.12.3: on disk before the rename (see history._rewrite)
    os.replace(tmp, path)


FARMING_DAYS = (0, 3, 7, 14, 30)      # 1.8.23 (user's pick): farming recordings go after this many days (0 = never)
DEFAULT_FARMING_DAYS = 7
FARMING_CHECK_S = 3600.0              # how often the recorder thread looks for expired ones


def expired_farming(recs: list[Recording], days: int, now: float) -> list[Recording]:
    """1.8.23 (pure): farming recordings older than ``days`` – never kept ones, never ones with a mark (F8)."""
    if not days or days <= 0:
        return []
    limit = now - days * 86400
    return [r for r in recs if r.farming and not r.keep and not r.marks and r.t < limit]


def prune_farming(folder: str, recs: list[Recording], days: int, now: float | None = None):
    """Delete the expired farming recordings (``expired_farming``) – only files named in the index, only inside
    ``folder``. Returns (entries left, files deleted)."""
    gone = expired_farming(recs, days, time.time() if now is None else now)
    deleted = []
    for r in gone:
        for n in (r.file, r.pre):
            p = rel_path(folder, n) if n else None
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                    deleted.append(n)
                except OSError:
                    pass
    gone_ids = {id(r) for r in gone}
    left = [r for r in recs if id(r) not in gone_ids or os.path.exists(rel_path(folder, r.file) or "")]
    return left, deleted


def prune_rank(r: Recording) -> int:
    """1.4.2: what goes first when room is needed – 0 farming rounds and rounds shorter than SHORT_ROUND_S,
    1 ordinary rounds, 2 rounds with a mark (F8); within a rank the oldest first. Kept ones never."""
    if r.marks:
        return 2
    if r.farming or (r.end and 0 < r.end - r.t < SHORT_ROUND_S):
        return 0
    return 1


def prune(folder: str, recs: list[Recording], limit: int, reserve: int = RESERVE,
          free=None) -> tuple[list[Recording], list[str]]:
    """Keep the folder's recordings under ``limit`` bytes (0 = the whole drive) and ``reserve`` bytes free on
    the drive: delete not-kept ones of the index in ``prune_rank`` order (farming/short first, marked last,
    oldest first) – only files named in it, only inside ``folder``.
    Entries whose files are gone drop out. ``free`` = bytes free now (measured when None).
    Returns (entries left, files deleted)."""
    left, deleted = [], []
    for r in recs:
        main = rel_path(folder, r.file)
        if main and os.path.exists(main):
            paths = [p for p in (rel_path(folder, n) for n in (r.file, r.pre) if n) if p and os.path.exists(p)]
            r.size = sum(os.path.getsize(p) for p in paths)
            left.append(r)
    if free is None:
        try:
            free = shutil.disk_usage(folder).free
        except OSError:
            free = reserve
    total = sum(r.size for r in left)
    for r in sorted([r for r in left if not r.keep], key=lambda r: (prune_rank(r), r.t)):
        if (limit <= 0 or total <= limit) and free >= reserve:
            break
        for n in (r.file, r.pre):
            p = rel_path(folder, n) if n else None                        # only inside the folder
            if p:
                try:
                    os.remove(p)
                    deleted.append(n)
                except OSError:
                    pass
        main = rel_path(folder, r.file)
        if main and os.path.exists(main):   # 1.8.38: not deleted (open in a player): the entry stays and counts –
            continue                        # dropped, the file was an orphan no later pass would ever remove
        total -= r.size
        free += r.size
        left.remove(r)
    return left, deleted


def select_recordings(recs: list[Recording], since: float | None = None, map_label: str | None = None,
                      role: str | None = None, only: str | None = None, hide_farming: bool = False) -> list[Recording]:
    """1.5, tab "Aufnahmen": the index filtered – ``since`` (banner time ≥), map label, role ("killer" /
    "survivor" / "farming" = farming rounds only), ``only`` "marked" / "kept" / "bad", ``hide_farming`` (1.11.5:
    the switch "Farming ausblenden"; 1.8.71–1.11.4 a role left farming rounds out by itself). Newest first."""
    out = []
    for r in recs:
        if since is not None and r.t < since:
            continue
        if map_label and r.label != map_label:
            continue
        if hide_farming and r.farming:
            continue
        if role == "farming":
            if not r.farming:
                continue
        elif role and r.role != role:
            continue
        if only == "marked" and not r.marks:
            continue
        if only == "kept" and not r.keep:
            continue
        if only == "bad" and not (r.extra or {}).get("bad"):
            continue
        out.append(r)
    return sorted(out, key=lambda r: r.t, reverse=True)



# ------------------------------------------------------------------ clips (1.8.13): the list in the tab "Aufnahmen"
CLIPS_INDEX = "fogscout-clips.jsonl"     # in Clips/: what the program made there (only these are deleted)
OLD_CLIPS_INDEX = "dbdmapscout-clips.jsonl"   # 1.9: the name until 1.8.91 – taken over when first read
CLIP_EXTS = (".mp4", ".mkv", ".mov", ".webm", ".flv", ".gif", ".png", ".jpg")   # .gif: the editor's GIFs (1.12)
STILL_EXTS = (".png", ".jpg")
CLIP_KINDS = ("clip", "instant", "still")
_STAMP_RE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d-\d\d) (.+)$")
_COPY_RE = re.compile(r" \(\d+\)$")                     # unique_path / _unique: "name (2)"
PART_EXT = ".tmp"               # 1.12 review: the clip editor's ffmpeg writes "<clip>.mp4.tmp", renamed once whole –
                                # a file still being written is never listed, uploaded or opened
PART_STALE_S = 300.0            # … such a file nobody wrote to for this long was left by a quit or crash mid-save
PARTS_CHECK_S = 60.0            # s between two looks for them (Recorder._settle_parts)
PARTS_WRITING = set()           # part_key of every ".tmp" a save of this process writes now (clipedit) – never touched


@dataclass
class Clip:
    file: str                    # name inside Clips/
    t: float = 0.0               # made at
    kind: str = "clip"           # clip (editor) / instant (F8) / still (picture from the editor)
    source: float = 0.0          # banner time of the round it came from (0 = unknown)
    map_id: str = ""
    label: str = ""
    role: str = ""
    killer: str = ""
    farming: bool = False
    seconds: float = 0.0         # length (0 = unknown / a still)
    size: int = 0                # bytes, filled when listed
    adopted: bool = False        # not in the index: an older version made it (told by its name), never saved
    yt: str = ""                 # 1.10: the YouTube video id once uploaded (ytupload)


def clips_dir(folder: str) -> str:
    return os.path.join(folder, CLIPS_DIR)


def load_clips(cdir: str) -> list[Clip]:
    out = []
    adopt_old_file(cdir, OLD_CLIPS_INDEX, CLIPS_INDEX)
    try:
        with open(os.path.join(cdir, CLIPS_INDEX), encoding="utf-8", errors="replace") as f:   # 1.12.3: as load_index
            for line in f:
                try:
                    d = json.loads(line)
                    if isinstance(d, dict):
                        out.append(Clip(**{k: v for k, v in d.items() if k in Clip.__dataclass_fields__}))
                except (ValueError, TypeError):
                    continue
    except OSError:
        pass
    return out


def save_clips(cdir: str, clips: list[Clip]):
    path = os.path.join(cdir, CLIPS_INDEX)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for c in sorted(clips, key=lambda c: c.t):
            d = asdict(c)
            d.pop("adopted", None)
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _who(who: str) -> tuple[str, str]:
    """The name part after " – " → (role, killer): "Survivor" / "Killer" / a killer's name."""
    who = (who or "").strip()
    if not who:
        return "", ""
    if who.lower() == "survivor":
        return "survivor", ""
    if who.lower() == "killer":
        return "killer", ""
    return "killer", who


def adopt_clip(name: str, recs: list[Recording]) -> Clip | None:
    """A file in Clips/ that is not in the index: made by this program before 1.8.13 when its name says so –
    an editor clip/still starts with the name of a recording and goes on with " – Clip …" / " – Bild …",
    an instant clip ends with "(Sofort-Clip)" – then its round comes from that recording or from the name.
    Anything else is someone else's file: None (listed nowhere, never deleted)."""
    stem, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext not in CLIP_EXTS:
        return None
    stem = _COPY_RE.sub("", stem)
    still = ext in STILL_EXTS
    for r in recs:
        base = os.path.splitext(re.split(r"[\\/]", r.file)[-1])[0]
        if base and stem.startswith(base + " – "):
            return Clip(file=name, kind="still" if still else "clip", source=r.t, map_id=r.map_id, label=r.label,
                        role=r.role, killer=r.killer, farming=r.farming, adopted=True)
    tails = [(" " + t, "instant") for t in {"(Sofort-Clip)", _("(Sofort-Clip)")}]
    kind = next((k for tail, k in tails if stem.endswith(tail) and not still), None)
    if kind is not None:
        stem = stem[:-len(next(tail for tail, _k in tails if stem.endswith(tail)))]
    else:
        m = re.search(r" – (?:Clip \d+m\d\ds-\d+m\d\ds|(?:Bild|{}) \d+-\d\d(?:\.\d)?)$".format(re.escape(_("Bild"))),
                      stem)
        if m is None:
            return None
        kind, stem = ("still" if still else "clip"), stem[:m.start()]
    m = _STAMP_RE.match(stem)
    if m is None:
        return None
    rest = m.group(2)
    label, _sep, who = rest.rpartition(" – ") if " – " in rest else (rest, "", "")
    role, killer = _who(who)
    return Clip(file=name, kind=kind, label=label.strip(), role=role, killer=killer, adopted=True)


def list_clips(cdir: str, recs: list[Recording]) -> list[Clip]:
    """The clips on the drive: index entries whose file is there, plus the program's older clips (adopt_clip);
    ``size`` and – for adopted ones – ``t`` (file time) filled. Newest first."""
    try:
        names = os.listdir(cdir)
    except OSError:
        return []
    index = {c.file: c for c in load_clips(cdir)}
    out = []
    for name in names:
        p = os.path.join(cdir, name)
        if name in (CLIPS_INDEX, CLIPS_INDEX + ".tmp", OLD_CLIPS_INDEX) or not os.path.isfile(p):
            continue
        c = index.get(name) or adopt_clip(name, recs)
        if c is None:
            continue
        try:
            st = os.stat(p)
        except OSError:
            continue
        c.size = st.st_size
        if not c.t:
            c.t = st.st_mtime
        out.append(c)
    return sorted(out, key=lambda c: c.t, reverse=True)


def part_key(path: str) -> str:
    """One spelling of a path for PARTS_WRITING."""
    return os.path.normcase(os.path.abspath(path))


def whole(path: str) -> bool | None:
    """1.12 review: did ffmpeg finish ``path``? mp4/mov: the top-level boxes fill the file exactly and the index box
    "moov" is there (while ffmpeg writes, the data box has no size yet: 0); gif: it ends with the trailer. A ".tmp"
    counts as the kind it is named for. None = cannot tell (another kind, the file not readable)."""
    ext = os.path.splitext(path[:-len(PART_EXT)] if path.endswith(PART_EXT) else path)[1].lower()
    if ext not in (".mp4", ".mov", ".gif"):
        return None
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            if ext == ".gif":
                if size < 14 or f.read(6) not in (b"GIF87a", b"GIF89a"):
                    return False
                f.seek(-1, os.SEEK_END)
                return f.read(1) == b";"
            pos, moov = 0, False
            while pos < size:
                f.seek(pos)
                head = f.read(16)
                if len(head) < 8:
                    return False
                n, kind = struct.unpack(">I4s", head[:8])
                if n == 1 and len(head) == 16:               # 64-bit size
                    n = struct.unpack(">Q", head[8:])[0]
                if n < 8:                                    # 0 = "to the end": the size ffmpeg writes last
                    return False
                moov = moov or kind == b"moov"
                pos += n
            return pos == size and moov
    except OSError:
        return None


def settle_parts(folder: str, now: float | None = None) -> list[str]:
    """1.12 review: a clip the editor was writing when the program ended (quit, update restart, crash) – ffmpeg may
    finish it on its own, but the rename after it never comes, so "<clip>.mp4.tmp" stayed unlisted for good. A ".tmp"
    in Clips/ with one of the program's clip names (adopt_clip), untouched for PART_STALE_S and not written by a save
    of this process: whole → it gets its name and the clips list takes it; cut short → it goes. Someone else's file,
    or one whole() cannot judge, stays. Returns the names given."""
    now = time.time() if now is None else now
    cdir = clips_dir(folder)
    try:
        names = [n for n in os.listdir(cdir) if n.endswith(PART_EXT)
                 and os.path.splitext(n[:-len(PART_EXT)])[1].lower() in (".mp4", ".mov", ".gif")]
    except OSError:
        return []
    recs, given = None, []
    for name in names:
        final, p = name[:-len(PART_EXT)], os.path.join(cdir, name)
        try:
            if part_key(p) in PARTS_WRITING or not os.path.isfile(p) or now - os.path.getmtime(p) < PART_STALE_S:
                continue
        except OSError:
            continue
        recs = load_index(folder) if recs is None else recs
        if adopt_clip(final, recs) is None:
            continue                                         # not a name of ours: someone else's file
        done = whole(p)
        if done is False:
            try:
                os.remove(p)
            except OSError:
                pass
        if not done:
            continue
        stem, ext = os.path.splitext(final)
        target, n = os.path.join(cdir, final), 2
        while os.path.exists(target) or (n > 2 and os.path.exists(target + PART_EXT)):
            target = os.path.join(cdir, f"{stem} ({n}){ext}")          # as unique_path: never a name being written
            n += 1
        try:
            os.replace(p, target)
        except OSError:
            continue                                         # still open (Windows): next look
        given.append(os.path.basename(target))
    return given


def select_clips(clips: list[Clip], since: float | None = None, role: str | None = None, killer: str | None = None,
                 kind: str | None = None, hide_farming: bool = False) -> list[Clip]:
    """1.8.13 (user: "filtern nach Killer/Survivor"): ``role`` like the recordings ("killer" / "survivor" /
    "farming"), ``killer`` = one killer (rounds as killer), ``kind`` clip / instant / still, ``hide_farming``
    (1.11.5) as for the recordings."""
    out = []
    for c in clips:
        if since is not None and c.t < since:
            continue
        if hide_farming and c.farming:
            continue
        if role == "farming":
            if not c.farming:
                continue
        elif role and c.role != role:
            continue
        if killer and (c.role != "killer" or c.killer != killer):
            continue
        if kind and c.kind != kind:
            continue
        out.append(c)
    return sorted(out, key=lambda c: c.t, reverse=True)

@dataclass
class Space:
    """1.4.2: what the overview's tile "Aufnahmen" shows – measured by the recorder thread, never on the UI thread."""
    free: int = 0                # bytes free on the drive
    total: int = 0               # bytes the drive holds
    used: int = 0                # bytes the recordings of the index take
    count: int = 0
    oldest: float = 0.0          # banner time of the oldest recording (0 = none)
    marked: int = 0              # recordings with an F8 mark
    folder: str = ""             # "" = drive not connected
    t: float = 0.0               # when measured


def space(folder: str | None, recs: list[Recording] | None = None) -> Space:
    if not folder:
        return Space(t=time.time())
    recs = load_index(folder) if recs is None else recs
    try:
        du = shutil.disk_usage(folder)
        free, total = du.free, du.total
    except OSError:
        free = total = 0
    return Space(free=free, total=total, used=sum(r.size for r in recs), count=len(recs),
                 oldest=min((r.t for r in recs), default=0.0), marked=sum(1 for r in recs if r.marks),
                 folder=folder, t=time.time())


VIDEO_EXTS = (".mkv", ".mp4", ".mov", ".flv", ".ts", ".m3u8", ".fragmented.mp4", ".hybrid.mp4", ".hybrid.mov")


def obs_file(path) -> str:
    """1.8.38 (QA audit): a path OBS named (StopRecord, the replay buffer) before it is moved or deleted – the
    program runs as admin, and anything listening on the port could answer in OBS's place. Only a regular video
    file, no link and no junction/reparse point; else "" (logged)."""
    p = str(path or "")
    if not p:
        return ""
    try:
        st = os.lstat(p)
        ok = (p.lower().endswith(VIDEO_EXTS) and stat.S_ISREG(st.st_mode)
              and not getattr(st, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    except OSError:
        return p if p.lower().endswith(VIDEO_EXTS) else ""     # not written yet: looked at again before the move
    if not ok:
        log.warning("OBS nannte eine Datei, die keine Aufnahme ist – nicht angefasst: %s", os.path.basename(p))
    return p if ok else ""


# ------------------------------------------------------------------ ffmpeg (1.4.2): pre-roll + round → one file
def ffmpeg_exe() -> str | None:
    """The ffmpeg binary imageio-ffmpeg ships (BSD-2; no PATH lookup – only the one pip installed into .venv),
    None when the package or the file is missing. 1.8.38 (QA audit): not ``get_ffmpeg_exe()`` – that takes
    IMAGEIO_FFMPEG_EXE unchecked and, without a valid binary of its own, ffmpeg from sys.prefix or PATH; the
    program runs as admin. The bin folder and file name are those of imageio-ffmpeg 0.6.0 (pinned)."""
    try:
        from imageio_ffmpeg._definitions import FNAME_PER_PLATFORM, get_platform
        from imageio_ffmpeg._utils import _get_bin_dir
        exe = os.path.join(_get_bin_dir(), FNAME_PER_PLATFORM.get(get_platform(), ""))
    except Exception:
        return None
    return exe if os.path.isfile(exe) else None


def _run(args: list[str], timeout: float = FFMPEG_TIMEOUT) -> tuple[int, bytes]:
    """ffmpeg as a child process without a console window; (exit code, stderr)."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        p = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                           timeout=timeout, creationflags=flags)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e).encode()
    return p.returncode, p.stderr or b""


def media_duration(path: str, ffmpeg: str | None = None, run=None) -> float | None:
    """Length of a video in seconds from ffmpeg's own file summary (``ffmpeg -i``; imageio-ffmpeg has no ffprobe)."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg:
        return None
    _rc, err = (run or _run)([ffmpeg, "-hide_banner", "-i", path], timeout=30)
    m = DURATION_RE.search(err)
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def track_flags(tracks) -> dict:
    """The ``inputAudioTracks`` value for SetInputAudioTracks: tracks 1–5 on or off (6 is left alone)."""
    return {str(n): n in tracks for n in range(1, 6)}


def track_sources(n_tracks: int) -> dict:
    """Which sources a recording with ``n_tracks`` audio tracks carries on their own track, as 0-based stream
    indexes: 3 or more tracks = the 1.8.6 layout (dbd 1, discord 2, mic 3, 1.8.19 background 4 when there),
    exactly 2 = the 1.8.5 layout (track 2 = everything but Discord, marked LEGACY), otherwise nothing to pick."""
    if n_tracks >= 3:
        d = {"dbd": 1, "discord": 2}
        if n_tracks >= 4:
            d["mic"] = 3
        if n_tracks >= 5:
            d["other"] = 4
        return d
    if n_tracks == 2:
        return {"dbd": 1, "discord": LEGACY}
    return {}


def audio_graph(n_tracks: int, mix, inp: int = 0, tag: str = "") -> tuple[str, str | None]:
    """(filter_complex part, ``-map`` value) for the wanted ``mix`` {source: volume, 1.0 = as recorded} of a file
    with ``n_tracks`` audio tracks: ("", "0:a?") = ffmpeg's default, nothing to mix; ("", None) = no sound at
    all; ("", "0:a:N") = one track as it is (stream copy possible); else a volume/amix graph ending in [aout]
    with map "[aout]" – the sound is then re-encoded. ``inp`` = the ffmpeg input the tracks come from and ``tag``
    = a suffix for the graph's labels (the clip editor mixes each part of a clip from an input of its own, one
    graph each). Pure."""
    if mix is None or n_tracks < 2:
        return "", f"{inp}:a?"
    srcs = track_sources(n_tracks)
    vol = {k: max(0.0, float(mix.get(k, 0) or 0)) for k in SOURCES}
    if srcs.get("discord") == LEGACY:                      # 1.8.5 file: all or all-but-Discord, one volume
        if vol["discord"] > 0:
            parts = [(0, max(vol["dbd"], vol["discord"]))]
        else:
            parts = [(1, vol["dbd"])] if vol["dbd"] > 0 else []
    else:
        parts = [(idx, vol[name]) for name, idx in srcs.items() if vol[name] > 0]
    if not parts:
        return "", None
    if len(parts) == 1 and abs(parts[0][1] - 1.0) < 1e-3:
        return "", f"{inp}:a:{parts[0][0]}"
    out = f"[aout{tag}]"
    chain = ";".join(f"[{inp}:a:{i}]volume={v:.3f}[a{k}{tag}]" for k, (i, v) in enumerate(parts))
    if len(parts) == 1:
        return chain.replace(f"[a0{tag}]", out), out
    chain += ";" + "".join(f"[a{k}{tag}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0{out}"
    return chain, out


def clip_sound_args(n_tracks: int, clip_sources) -> tuple[list, list]:
    """(map arguments, codec arguments) of ffmpeg for the instant clip cut from a buffer file with ``n_tracks``
    audio tracks (1.8.6, pure): the wanted ``clip_sources`` mixed from the file's own tracks (audio_graph) as the
    clip's first audio track – what every player and Discord play –, a file without tracks as it is, no source =
    no sound. 1.14.4 (user: "die normalen Videos haben mehrere Tonspuren, nur die Clips nicht"): the file's own
    tracks 2… follow as stream copies in their order (track_sources: the layout of a round's recording), so the
    clip editor mixes a clip like a round; only the first track is the default one (``-disposition``). The
    picture is never re-encoded, the copies neither – only the mix, when it is one."""
    if n_tracks < 2:
        return ["-map", "0"], ["-c", "copy"]
    flt, amap = audio_graph(n_tracks, {s: 1.0 for s in clip_sources})
    if amap is None:
        return ["-map", "0:v", "-an"], ["-c", "copy"]
    maps = (["-filter_complex", flt] if flt else []) + ["-map", "0:v", "-map", amap]
    codec = ["-c", "copy"] + (["-c:a:0", "aac", "-b:a:0", "160k"] if flt else [])
    for i in range(1, n_tracks):
        maps += ["-map", f"0:a:{i}"]
        codec += [f"-disposition:a:{i}", "0"]
    return maps, codec + ["-disposition:a:0", "default"]


def audio_tracks(path: str, ffmpeg: str | None = None, run=None) -> int:
    """1.8.5: how many audio streams a video has (``ffmpeg -i``); 0 without ffmpeg or on failure."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg:
        return 0
    _rc, err = (run or _run)([ffmpeg, "-hide_banner", "-i", path], timeout=30)
    return len(AUDIO_STREAM_RE.findall(err))


def merge_files(parts: list[str], out: str, ffmpeg: str | None = None, run=None) -> bool:
    """Join video files of the same format into ``out`` without re-encoding (concat demuxer, stream copy):
    seconds of work, the picture stays as OBS wrote it. False when ffmpeg is missing or fails – the parts stay."""
    ffmpeg = ffmpeg or ffmpeg_exe()
    if not ffmpeg or len(parts) < 2:
        return False
    lst = out + ".txt"
    try:
        with open(lst, "w", encoding="utf-8") as f:
            for p in parts:
                f.write("file '" + os.path.abspath(p).replace("'", "'\\''") + "'\n")
        rc, err = (run or _run)([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                                "-i", lst, "-map", "0", "-c", "copy", out])
    finally:
        try:
            os.remove(lst)
        except OSError:
            pass
    ok = rc == 0 and os.path.exists(out) and os.path.getsize(out) > 0
    if not ok:
        log.info("ffmpeg: Zusammenfügen fehlgeschlagen (%s): %s", rc, err[-400:].decode("utf-8", "replace").strip())
        try:
            os.remove(out)
        except OSError:
            pass
    return ok


# ------------------------------------------------------------------ the recorder thread
@dataclass
class Config:
    on: bool = False
    port: int = DEFAULT_PORT
    password: str = ""
    volume: str = ""
    rel: str = ""
    folder: str = ""             # last known absolute path
    limit_gb: int = DEFAULT_LIMIT_GB
    pre: bool = True
    tail_s: float = DEFAULT_TAIL_S   # 1.4.1: keep recording this long after the end (result screen)
    buffer_auto: bool = True         # 1.4.1: start OBS's replay buffer with DBD, stop it when DBD is gone
    merge: bool = True               # 1.4.2: pre-roll + round → one file (ffmpeg, stream copy)
    farming_sub: bool = True         # 1.5.3: farming rounds into the subfolder FARMING_DIR
    early: bool = True               # 1.6: start at the end of the loading screen (spawn), the banner names it
    instant: bool = True             # 1.6: F8 saves the last clip_s seconds of the replay buffer as a clip
    clip_s: int = DEFAULT_CLIP_S
    audio: bool = True               # 1.6: set OBS's audio sources (below) when DBD starts
    audio_dbd: bool = True
    audio_discord: bool = True
    audio_desktop: bool = False      # the rest of the desktop sound (OBS "Desktop Audio")
    audio_mic: bool = False          # OBS "Mic/Aux"
    tracks: bool = True              # 1.8.6: every source on its own OBS track (SOURCE_TRACKS), 1 = everything
    clip_sources: tuple = DEFAULT_CLIP_SOURCES   # 1.8.6: what the F8 clip keeps when the buffer file has the tracks
    farming_days: int = DEFAULT_FARMING_DAYS     # 1.8.23: farming recordings go after this many days (0 = never)
    window: bool = False             # 1.8.41: our window capture of DBD in OBS (WINDOW_SOURCE) instead of the monitor
    capture: str = "window"          # 1.11.7: … through OBS's window capture or its game capture (GAME_SOURCE)
    obs_start: bool = False          # 1.8.47: start OBS when DBD starts and OBS cannot be reached
    overlay: bool = False            # 1.8.89: our overlay as an image source over the window capture
    overlay_file: str = ""           # … the PNG obsoverlay writes (absolute)

    @property
    def wants_buffer(self) -> bool:
        return self.pre or self.instant


def obs_window_open(windows) -> bool:
    """1.8.47 (pure): an OBS main window among ``windows`` [(title, class)] – also hidden in the tray (EnumWindows
    lists hidden windows too). A second start would only open OBS's "already running" question."""
    return any(OBS_TITLE.match(t or "") and (c or "").startswith("Qt") for t, c in windows)


def obs_exe(registry=None, env=None) -> str | None:
    """1.8.47: obs64.exe – the folder the OBS installer stores in HKLM\\SOFTWARE\\OBS Studio, else the usual one in
    Program Files. Absolute paths only (the program runs as administrator), never PATH or the current folder.
    ``registry``/``env`` for tests."""
    env = os.environ if env is None else env
    folders = list(registry if registry is not None else _obs_registry())
    for var in ("ProgramW6432", "ProgramFiles"):
        if env.get(var):
            folders.append(os.path.join(env[var], "obs-studio"))
    for folder in folders:
        if folder and os.path.isabs(folder):
            exe = os.path.join(folder, "bin", "64bit", OBS_EXE)
            if os.path.isfile(exe):
                return exe
    return None


def _obs_registry() -> list:
    if sys.platform != "win32":
        return []
    import winreg
    out = []
    for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\OBS Studio", 0, winreg.KEY_READ | view) as k:
                value, kind = winreg.QueryValueEx(k, "")
                if kind in (winreg.REG_SZ, winreg.REG_EXPAND_SZ) and value:
                    out.append(os.path.expandvars(value))
        except OSError:
            pass
    return out


def _top_windows() -> list:
    from .capture import top_windows                # Win32 only; capture never opens a process
    return top_windows()


def profile_hint(mode: str, rec_tracks: str) -> str:
    """1.8.5 (pure): what the user has to tick in OBS for a second audio track, "" when the profile is fine.
    ``mode`` = [Output] Mode ("Simple"/"Advanced"), ``rec_tracks`` = [AdvOut] RecTracks (bit mask, track 1 = 1)."""
    try:
        mask = int(str(rec_tracks).strip() or "1")
    except ValueError:
        mask = 1
    if str(mode).strip().lower() == "advanced" and mask & REC_TRACKS_NEEDED == REC_TRACKS_NEEDED:
        return ""
    return _("Für die Tonmischung im Clip-Editor in OBS: Einstellungen → Ausgabe → Ausgabemodus „Erweitert“ → Reiter "
             "Aufnahme → Audiospur 1 bis 5 anhaken (1 alles, 2 Spiel, 3 Discord, 4 Mikrofon, 5 Hintergrund)")


def check_file(path: str) -> str | None:
    """1.4.1: None if the recording looks fine, else why not ("leer"/"zu klein"/"kein Video") – OBS may have
    failed silently (drive gone, encoder error)."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            head = f.read(12)
    except OSError:
        return "fehlt"
    if size == 0:
        return "leer"
    if size < MIN_FILE_BYTES:
        return "zu klein"
    if not (head[:4] in MAGIC or head[4:8] in MAGIC):
        return "kein Video"
    return None


class Recorder(threading.Thread):
    """Talks to OBS off the UI thread. ``post(kind, **data)`` reports back: status (text, ok), started, saved,
    deleted, error."""

    def __init__(self, post):
        super().__init__(name="obs-recorder", daemon=True)
        self._post = post
        self.cmds = queue.Queue()
        self.cfg = Config()
        self.active = None           # the round being recorded: dict(t, map_id, label, role, killer, pre, since)
        self.status = ""
        self._pending = None         # (meta, deadline): the end came, the tail is still being recorded (1.4.1)
        self._game = None            # last known: DBD running? (set_game)
        self._buffer_ours = False    # we started OBS's replay buffer: we stop it with DBD
        self.space = Space()         # 1.4.2: the drive and the index, for the overview's tile
        self._space_t = 0.0
        self._farming_t = 0.0        # 1.8.23: last look for expired farming recordings
        self._parts_t = 0.0          # 1.12 review: last look for clips left as ".tmp" (settle_parts)
        self._routed = None          # 1.8.23: sources OBS had on their own track (None = unknown / not routed)
        self._ready = False          # 1.8.41: OBS was set up for this DBD session (else retried every RECHECK_S)
        self._buffer_tried = False   # 1.8.42: we asked OBS to start its replay buffer (once per DBD/OBS session)
        self._buffer_check = False   # … and look on the next round whether it really runs
        self._next_check = 0.0
        self._obs_started = False    # 1.8.47: we started OBS for this DBD session (never a second time)
        self._obs_wait = 0.0         # … and look for it often until then
        self._obs_late = False       # … "started, but not reachable" said
        self._obs_open = False       # … an OBS window was open when we looked (its WebSocket server is off)
        self._overlay_item = None    # 1.8.89: (scene, scene item id) of our image source while it is wanted
        self._overlay_box = None     # … where the overlay picture lies, relative to the DBD window (set_overlay)
        self._overlay_placed = None  # … the transform sent last (nothing is sent twice)
        self._poll_waiting = False   # 1.15: a "poll" command sits in the queue
        self._slow = {}              # 1.15: slow-changing OBS values for the card (encoder, buffer length, output size)
        self._slow_t = 0.0
        self._free_t = 0.0           # 1.15: last look at the drive's free space while recording
        self.paused = False          # 1.15: the recording on air is paused (ours)
        self.start_obs = self._start_obs_process       # tests replace it

    @property
    def recording(self) -> bool:
        return self.active is not None

    def active_round_named(self) -> bool:
        """1.15: the recording on air already carries a map (a round's recording, or a manual one a banner named)."""
        a = self.active
        return bool(a and a.get("map_id"))

    # ---- called from the UI thread
    def configure(self, cfg: Config):
        self.cmds.put(("config", cfg))

    def start_round(self, **meta):
        self.cmds.put(("start", meta))

    def relabel(self, **meta):
        """1.8.39: the round on record is another map/layout (later banner frames, the user's correction): the
        running recording takes its name and map from ``meta`` (map_id, label) – nothing restarts."""
        self.cmds.put(("relabel", meta))

    def start_early(self, **meta):
        """1.6: the loading screen ended – record from the spawn on; the banner (start_round) names the round."""
        self.cmds.put(("early", meta))

    def instant_clip(self, **meta):
        """1.6: F8 – the last clip_s seconds of OBS's replay buffer as a clip in Clips/."""
        self.cmds.put(("clip", meta))

    def apply_audio(self):
        """1.6: set OBS's audio sources now (settings changed)."""
        self.cmds.put(("audio", None))

    def stop_round(self, **meta):
        self.cmds.put(("stop", meta))

    def test(self):
        self.cmds.put(("test", None))

    def mark(self):
        """1.4.2: F8 – note this moment in the running recording (the clip editor jumps to it later)."""
        self.cmds.put(("mark", None))

    def set_keep(self, t: float, on: bool):
        """1.5: "behalten" – never deleted for room. Index writes stay on this thread."""
        self.cmds.put(("keep", (float(t), bool(on))))

    def delete(self, t: float):
        """1.5: remove one recording (its files from the index only) and its index entry."""
        self.cmds.put(("delete", float(t)))

    def add_clip(self, **meta):
        """1.8.13: the editor saved a clip / still – into the clips index (written on this thread only)."""
        self.cmds.put(("clip_add", meta))

    def delete_clip(self, name: str):
        """1.8.13: remove one clip – only a file of the clips index (or one the program made before it)."""
        self.cmds.put(("clip_delete", str(name)))

    def set_farming(self, t: float, on: bool):
        """1.5.4: the statistics marked the round as farming (or not): the recording follows – flag in the index,
        file into / out of the subfolder FARMING_DIR. Unknown rounds are ignored."""
        self.cmds.put(("farming", (float(t), bool(on))))

    def set_link(self, kind: str, rel: str, video_id: str):
        """1.10: a file was uploaded to YouTube – the video id into the index entry of the recording (``kind``
        "round", ``rel`` as in Recording.file) or the clip ("clip", "Clips/<name>"). Index writes stay here."""
        self.cmds.put(("link", (str(kind), str(rel), str(video_id))))

    def set_overlay(self, box):
        """1.8.89: the overlay picture (obsoverlay.Writer) covers ``box`` = (x, y, w, h) relative to the DBD window,
        None = nothing shown; our image item in OBS is moved there (own source only). Called from the writer."""
        self.cmds.put(("overlay", tuple(int(v) for v in box) if box else None))

    def set_game(self, on: bool):
        """DBD running or not (1.4.1): starts/stops OBS's replay buffer, checks OBS and the drive once."""
        if bool(on) != self._game:
            self.cmds.put(("game", bool(on)))

    def record_start(self, **meta):
        """1.15: start a recording by hand (button/hotkey) – outside a round too; it runs until record_stop,
        DBD closes or MAX_MANUAL_S. ``meta`` as start_round (t, map_id, label, role, killer, farming, source)."""
        self.cmds.put(("rec_start", meta))

    def record_stop(self):
        """1.15: stop the recording on air now – a manual one or the round's (its tail is skipped)."""
        self.cmds.put(("rec_stop", None))

    def record_pause(self, on: bool):
        """1.15: pause / resume the recording on air (OBS PauseRecord/ResumeRecord); marks keep their place."""
        self.cmds.put(("rec_pause", bool(on)))

    def poll(self):
        """1.15: ask OBS for its state once (recording, buffer, output size, fps, encoder, space) → event
        ``obs_status``; the recordings page calls it every STATUS_POLL_S while shown. A poll still waiting in the
        queue is not doubled."""
        if not self._poll_waiting:
            self._poll_waiting = True
            self.cmds.put(("poll", None))

    def quit(self):
        self.cmds.put(("quit", None))

    # ---- thread
    IDLE_WAIT_S = 5.0                 # how long the thread waits for a command before its idle work

    def run(self):
        while True:
            wait = self.IDLE_WAIT_S if self._pending is None else max(0.05, min(self.IDLE_WAIT_S, self._pending[1] - time.time()))
            try:
                cmd, arg = self.cmds.get(timeout=wait)
            except queue.Empty:
                # 1.16.1 (audit, reproduced): only ObsError was caught here – an OSError while the index was written
                # (drive unplugged between folder() and the write, disk full, a virus scanner holding the .tmp) ended
                # the thread for good: no recording ever again, a running OBS recording never filed, nothing in the
                # log. Every idle step is tried on its own; the thread never dies of one of them.
                for step in (self._due, self._watchdog, self._recheck, self._look_at_space, self._expire_farming,
                             self._settle_parts):
                    try:
                        step()
                    except ObsError as e:
                        self._say(str(e), False)
                    except Exception:
                        log.exception("OBS-Aufnahme: %s", step.__name__)
                        self._say(_("Aufnahme: Fehler in {step} – siehe Log.", step=step.__name__.strip("_")), False)
                continue
            try:
                if cmd == "quit":
                    # 1.8.38: quitting mid-round (or in the tail) stops the recording and our replay buffer –
                    # else OBS records on, the file is never filed and every later round finds "OBS nimmt schon
                    # auf" and starts nothing
                    try:
                        self._game_changed(False)
                    except Exception:
                        log.exception("OBS-Aufnahme beim Beenden")
                    return
                if cmd == "config":
                    changed = arg != self.cfg
                    self.cfg = arg
                    self._look_at_space(force=True)    # the tile follows a new folder/switch at once
                    if changed and self._game:         # 1.8.42 (user: "Fenster wurde nicht hinterlegt"): a setting
                        self._ready = False            # changed while DBD runs – OBS is set up again within seconds,
                        self._next_check = 0.0         # not only at the next DBD start
                elif cmd == "test":
                    self._test()
                elif cmd == "start":
                    self._begin(arg)
                elif cmd == "early":
                    self._begin_early(arg)
                elif cmd == "relabel":
                    if self.active is not None:
                        self.active.update({k: v for k, v in arg.items() if k in ("map_id", "label") and v})
                elif cmd == "clip":
                    self._instant_clip(arg)
                elif cmd == "audio":
                    self._audio_now()
                elif cmd == "stop":
                    self._stop_later(arg)
                elif cmd == "game":
                    if arg != self._game:               # 1.12.3: the ticks of a busy thread queued it again and
                        self._game_changed(arg)         # again – each reset the once-per-DBD-start guards
                elif cmd == "overlay":
                    self._overlay_moved(arg)
                elif cmd == "mark":
                    self._mark()
                elif cmd == "rec_start":
                    self._manual_start(arg)
                elif cmd == "rec_stop":
                    self._manual_stop()
                elif cmd == "rec_pause":
                    self._pause(arg)
                elif cmd == "poll":
                    self._poll_waiting = False
                    self._poll()
                elif cmd == "keep":
                    self._set_keep(*arg)
                elif cmd == "delete":
                    self._delete_one(arg)
                elif cmd == "farming":
                    self._set_farming(*arg)
                elif cmd == "link":
                    self._set_link(*arg)
                elif cmd == "clip_add":
                    self._add_clip(arg)
                elif cmd == "clip_delete":
                    self._delete_clip(arg)
            except ObsError as e:
                self._say(str(e), False)
            except Exception as e:                     # never let the thread die
                log.exception("OBS-Aufnahme")
                self._say(_("Fehler: {error}", error=e), False)

    def _say(self, text, ok):
        self.status = text
        self._post("status", text=text, ok=ok)

    def _buffer_state(self, c):
        """True/False = OBS's replay buffer runs or not; None = not enabled in OBS's settings (1.8.32)."""
        try:
            return bool(c.request("GetReplayBufferStatus").get("outputActive"))
        except ObsError as e:
            if buffer_missing(e):
                return None
            raise

    def _client(self) -> ObsClient:
        return ObsClient(self.cfg.port, self.cfg.password).connect()

    def _mark(self):
        if self.active is None:
            self._post("marked", pos=None)
            return
        pos = round(rec_elapsed(self.active), 1)          # 1.15: pauses do not move the marks
        self.active.setdefault("marks", []).append(pos)
        self._post("marked", pos=pos, n=len(self.active["marks"]))

    def _set_keep(self, t, on):
        folder = self.folder()
        if folder is None:
            self._warn(_("Aufnahme-Laufwerk nicht angeschlossen."))
            return
        recs = load_index(folder)
        hit = next((r for r in recs if r.t == t), None)
        if hit is None:
            return
        hit.keep = on
        save_index(folder, recs)
        self._post("changed", what="keep", t=t, on=on, file=hit.file)
        self._look_at_space(force=True)

    def _set_farming(self, t, on):
        folder = self.folder()
        if folder is None:
            return
        recs = load_index(folder)
        hit = next((r for r in recs if abs(r.t - t) < 1e-6), None)
        if hit is None:
            return
        hit.farming = on
        if self.cfg.farming_sub:                            # the file follows the flag (both parts)
            dest = os.path.join(folder, FARMING_DIR) if on else folder
            prefix = FARMING_DIR + "/" if on else ""
            try:
                os.makedirs(dest, exist_ok=True)
            except OSError:
                dest = None
            for attr in ("file", "pre"):
                name = getattr(hit, attr)
                src = rel_path(folder, name) if name else None
                if dest is None or not src or not os.path.exists(src):
                    continue
                base = os.path.basename(src)
                if os.path.dirname(src) == os.path.normpath(dest):
                    continue                                # already where it belongs
                target = os.path.join(dest, self._unique(dest, base))
                moved = self._move(src, target)
                if moved == target:
                    setattr(hit, attr, prefix + os.path.basename(target))
        save_index(folder, recs)
        self._post("changed", what="farming", t=t, on=on, file=hit.file)
        self._look_at_space(force=True)

    def _set_link(self, kind, rel, video_id):
        folder = self.folder()
        if folder is None:
            return
        if kind == "clip":
            cdir = clips_dir(folder)
            clips = load_clips(cdir)
            hit = next((c for c in clips if c.file == os.path.basename(rel)), None)
            if hit is None:
                return
            hit.yt = video_id
            save_clips(cdir, clips)
        else:
            recs = load_index(folder)
            hit = next((r for r in recs if r.file == rel), None)
            if hit is None:
                return
            hit.yt = video_id
            save_index(folder, recs)
        self._post("changed", what="link", file=rel, kind=kind, id=video_id)

    def _delete_one(self, t):
        folder = self.folder()
        if folder is None:
            self._warn(_("Aufnahme-Laufwerk nicht angeschlossen."))
            return
        recs = load_index(folder)
        hit = next((r for r in recs if r.t == t), None)
        if hit is None:
            return
        gone = []
        for n in (hit.file, hit.pre):
            p = rel_path(folder, n) if n else None                        # only inside the folder
            if p:
                try:
                    os.remove(p)
                    gone.append(n)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    self._warn(_("Aufnahme nicht gelöscht ({error}): {file}", error=e.__class__.__name__, file=n))
                    return
        recs.remove(hit)
        save_index(folder, recs)
        self._post("changed", what="delete", t=t, file=hit.file)
        if gone:
            self._post("deleted", files=gone, manual=True)
        self._look_at_space(force=True)

    def _add_clip(self, meta, folder=None):
        folder = folder or self.folder()
        name = os.path.basename(str(meta.get("file") or ""))
        if folder is None or not name:
            return
        cdir = clips_dir(folder)
        clips = [c for c in load_clips(cdir) if c.file != name]
        try:
            size = os.path.getsize(os.path.join(cdir, name))
        except OSError:
            return                                          # not in Clips/: not ours to list
        fields = {k: v for k, v in meta.items() if k in Clip.__dataclass_fields__ and k not in ("file", "size")}
        clips.append(Clip(file=name, size=size, **{"t": time.time(), **fields}))
        try:
            save_clips(cdir, clips)
        except OSError as e:
            log.info("Clip-Index nicht geschrieben: %s", e)
            return
        self._post("changed", what="clip", file=name)

    def _delete_clip(self, name):
        folder = self.folder()
        if folder is None:
            self._warn(_("Aufnahme-Laufwerk nicht angeschlossen."))
            return
        cdir = clips_dir(folder)
        if os.path.basename(name) != name or name in (CLIPS_INDEX, OLD_CLIPS_INDEX, ""):
            return                                          # only a plain name inside Clips/
        hit = next((c for c in list_clips(cdir, load_index(folder)) if c.file == name), None)
        if hit is None:
            return                                          # someone else's file: never
        try:
            os.remove(os.path.join(cdir, name))
        except FileNotFoundError:
            pass
        except OSError as e:
            self._warn(_("Clip nicht gelöscht ({error}): {file}", error=e.__class__.__name__, file=name))
            return
        clips = load_clips(cdir)
        if any(c.file == name for c in clips):
            save_clips(cdir, [c for c in clips if c.file != name])
        self._post("changed", what="clip_delete", file=name)
        self._look_at_space(force=True)

    def _look_at_space(self, force=False):
        """Drive and index for the overview – every SPACE_EVERY s while recording is on."""
        if not force and time.time() - self._space_t < SPACE_EVERY:
            return
        self._space_t = time.time()
        self.space = space(self.folder()) if self.cfg.on else Space(t=self._space_t)

    def _expire_farming(self, force=False):
        """1.8.23: once an hour (and after each saved round) the farming recordings older than ``farming_days``
        go – index entries and their files, nothing else."""
        if not self.cfg.on or not self.cfg.farming_days or (not force and time.time() - self._farming_t < FARMING_CHECK_S):
            return
        self._farming_t = time.time()
        folder = self.folder()
        if folder is None:
            return
        recs = load_index(folder)
        left, deleted = prune_farming(folder, recs, int(self.cfg.farming_days))
        if len(left) != len(recs):
            save_index(folder, left)
        if deleted:
            self._post("deleted", files=deleted, farming=True, days=int(self.cfg.farming_days))
            self._look_at_space(force=True)

    def _settle_parts(self):
        """Every PARTS_CHECK_S: a clip the editor was writing when the program ended gets its name (settle_parts)."""
        if time.time() - self._parts_t < PARTS_CHECK_S:
            return
        self._parts_t = time.time()
        folder = self.folder()
        try:
            given = settle_parts(folder) if folder else []
        except Exception:                              # never let the thread die (the idle look catches ObsError only)
            log.exception("Clips nach dem Programmende")
            return
        for name in given:
            log.info("Clip nach dem Programmende fertig geworden: %s", name)
            self._post("changed", what="clip", file=name)

    def folder(self) -> str | None:
        return find_folder(self.cfg.volume, self.cfg.rel, self.cfg.folder)

    def _test(self):
        c = self._client()
        try:
            ver = c.request("GetVersion")
            rec = c.request("GetRecordStatus")
            try:
                buf = self._buffer_state(c)
            except ObsError:
                buf = False
        finally:
            c.close()
        folder = self.folder()
        bits = [_("OBS {version} verbunden", version=ver.get("obsVersion", "?"))]
        bits.append(_("nimmt gerade auf") if rec.get("outputActive") else _("bereit"))
        if buf is None and (self.cfg.pre or self.cfg.instant):
            bits.append(_("Wiederholungspuffer in OBS nicht aktiviert (Einstellungen → Ausgabe → Wiederholungspuffer)"))
        elif self.cfg.pre:
            bits.append(_("Wiederholungspuffer läuft") if buf else _("Wiederholungspuffer aus (kein Vorlauf)"))
        bits.append(_("Ordner: {folder}", folder=folder) if folder else _("Ordner/Laufwerk nicht gefunden"))
        self._say(" · ".join(bits), bool(folder))

    # (named _begin/_finish: threading.Thread has its own _stop(), which join() calls on Python 3.12 – a method
    # of ours with that name broke join with "missing argument meta")
    def _stop_later(self, meta):
        """The round ended: keep recording for the tail (result screen), then stop. 1.15: a recording started by
        hand runs on (it is the user's to stop); the round's marks and name stay in it."""
        if self.active is None or self.active.get("manual"):
            return
        if self.cfg.tail_s <= 0:
            self._finish(meta)
        else:
            self._pending = (meta, time.time() + float(self.cfg.tail_s))

    def _due(self):
        if self._pending is not None and time.time() >= self._pending[1]:
            meta, self._pending = self._pending[0], None
            self._finish(meta)

    def _flush(self):
        """A recording still running (or in its tail) ends now."""
        if self._pending is not None:
            meta, self._pending = self._pending[0], None
            self._finish(meta)
        elif self.active is not None:
            self._finish({})

    def _game_changed(self, on: bool):
        self._game = on
        self._ready = False
        self._overlay_item = self._overlay_placed = None
        self._buffer_tried = self._buffer_check = False
        self._obs_started = self._obs_late = False
        if not on:
            self._flush()                               # DBD closed: the round is over
            if self._buffer_ours:
                self._buffer_ours = False
                try:
                    c = self._client()
                    try:
                        c.request("StopReplayBuffer")
                    finally:
                        c.close()
                except ObsError as e:
                    log.info("OBS: Wiederholungspuffer nicht gestoppt (%s)", e)
            return
        self._next_check = time.time() + RECHECK_S
        self._setup(quiet=False)

    def _recheck(self):
        """1.8.41: while DBD runs, every RECHECK_S – OBS opened after DBD (before: "OBS läuft nicht" once, then no
        replay buffer and no sources until DBD restarted), recordings switched on mid-game, OBS restarted (its
        replay buffer stopped). A silent retry: the warning came once already."""
        if not self._game or not self.cfg.on or time.time() < self._next_check:
            return
        now = time.time()
        self._next_check = now + (OBS_START_POLL_S if now < self._obs_wait and not self._ready else RECHECK_S)
        if not self._ready:
            self._setup(quiet=True)
            return
        buffer = self.cfg.wants_buffer and self.cfg.buffer_auto
        overlay = self._overlay_wanted() and self._overlay_item is not None and self._overlay_box is not None
        if not (buffer or overlay):
            return
        try:
            c = self._client()
        except ObsError:
            self._ready = False                         # OBS closed: set up again once it is back (a new OBS
            self._buffer_tried = self._buffer_check = False   # gets one start of its own)
            return
        try:
            if overlay:                                 # 1.8.89: the user may have moved or resized the window
                try:                                    # item in OBS – our picture follows it
                    self._place_overlay(c)
                except ObsError as e:
                    log.info("OBS: Overlay nicht nachgeführt (%s)", e)
            if not buffer:
                return
            state = self._buffer_state(c)
            if state:
                self._buffer_check = False
            elif state is False and self._buffer_check:
                # 1.8.42 (user's screenshot: OBS "Starten des Replaypuffers fehlgeschlagen"): our start did not take –
                # OBS shows a dialog for every failed start, so no second one; the user hears it once, here
                self._buffer_check = self._buffer_ours = False
                self._warn(BUFFER_FAILED())
            elif state is False:
                self._start_buffer(c)
        except ObsError as e:
            log.info("OBS: Wiederholungspuffer nicht geprüft (%s)", e)
        finally:
            c.close()

    def _launch_obs(self) -> bool:
        """1.8.47: OBS not reachable when DBD starts – start it (once per DBD start, never next to an open OBS) and
        look for it every OBS_START_POLL_S. True = started now (no warning yet)."""
        self._obs_open = False
        if not self.cfg.obs_start or self._obs_started:
            return False
        try:
            if obs_window_open(_top_windows()):
                self._obs_open = True                   # OBS runs, only its WebSocket server is off/elsewhere
                return False
        except Exception:
            log.debug("OBS-Fenster nicht geprüft", exc_info=True)
            return False
        exe = obs_exe()
        self._obs_started = True
        if exe is None:
            self._warn(_("OBS nicht gefunden – bitte OBS selbst starten (gesucht unter Programme\\obs-studio)."))
            return False
        try:
            self.start_obs(exe)
        except OSError as e:
            self._warn(_("OBS konnte nicht gestartet werden: {error}", error=e))
            return False
        self._obs_wait = time.time() + OBS_START_WAIT_S
        self._next_check = time.time() + OBS_START_POLL_S
        self._say(_("OBS wird gestartet …"), True)
        log.info("OBS gestartet: %s", exe)
        return True

    @staticmethod
    def _start_obs_process(exe: str):
        """OBS in its own folder (it finds its data there), minimised to the tray, detached from this program."""
        flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        subprocess.Popen([exe, *OBS_ARGS], cwd=os.path.dirname(exe), close_fds=True, creationflags=flags)

    def _start_buffer(self, c: ObsClient):
        """StartReplayBuffer at most once per DBD start and OBS session (1.8.42): when OBS cannot start the output
        (encoder, driver), every request opens an error dialog in OBS – 1.8.41 asked again every RECHECK_S."""
        if self._buffer_tried:
            return
        self._buffer_tried = self._buffer_check = True
        c.request("StartReplayBuffer")
        self._buffer_ours = True

    def _setup(self, quiet: bool):
        """DBD runs: check drive and OBS, set the audio sources, our window capture (1.8.41) and the replay buffer.
        ``quiet``: a retry – no second warning."""
        if not self.cfg.on:
            return
        folder = self.folder()
        if folder is None:
            if not quiet:
                self._warn(_("Aufnahme-Laufwerk nicht angeschlossen – die Runden werden nicht aufgenommen."))
            return
        try:
            c = self._client()
        except ObsError as e:
            if self._launch_obs():
                return
            if self._obs_open and not quiet:
                self._warn(_("OBS ist offen, aber nicht erreichbar – in OBS unter Werkzeuge → "
                             "WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})",
                             error=e))
            elif self._obs_started and not self._obs_late and time.time() >= self._obs_wait:
                self._obs_late = True
                self._warn(_("OBS wurde gestartet, ist aber nicht erreichbar – in OBS unter Werkzeuge → "
                             "WebSocket-Servereinstellungen den Server aktivieren und Port/Passwort prüfen. ({error})",
                             error=e))
            elif not quiet and not self._obs_started:
                self._warn(_("OBS läuft nicht – die Runden werden nicht aufgenommen. ({error})", error=e))
            return
        self._ready = True
        try:
            sound = self._audio(c) if self.cfg.audio else ""     # 1.8.7: a sound problem must stay in the status
            picture = self._video(c)                              # 1.8.41
            picture = " ".join(t for t in (picture, self._overlay_video(c)) if t)   # 1.8.89
            sound = " ".join(t for t in (sound, picture) if t)
            if self.cfg.wants_buffer and self.cfg.buffer_auto:
                try:
                    state = self._buffer_state(c)
                    if state is None:                   # 1.8.32: not enabled in OBS – say how, once per start
                        sound = " ".join(t for t in (sound, BUFFER_HINT()) if t)
                    elif not state:
                        self._start_buffer(c)
                except ObsError as e:
                    log.info("OBS: Wiederholungspuffer nicht gestartet (%s)", e)
            if sound:
                self._say(_("OBS bereit – Runden werden aufgenommen. {problem}", problem=sound), False)
            else:
                self._say(_("OBS bereit – Runden werden aufgenommen"), True)
        finally:
            c.close()

    def _warn(self, text):
        self._say(text, False)
        self._post("warn", text=text)

    def _begin_early(self, meta):
        """1.6: recording from the end of the loading screen on, before any banner: provisional until _begin."""
        if self.active is not None or not self.cfg.on or not self.cfg.early:
            return
        self._begin(dict(meta, early=True), pre_roll=False)

    def _begin(self, meta, pre_roll=True):
        a = self.active
        if a is not None and a.get("manual"):
            # 1.15: a recording started by hand is on air – the round goes into it (nothing restarts); the first
            # banner names it, later rounds only add their marks
            if not meta.get("early") and not a.get("map_id"):
                a.update({k: v for k, v in meta.items() if k in ("t", "map_id", "label", "role", "killer", "source")
                          and v})
                a["farming"] = bool(a.get("farming") or meta.get("farming"))
                self._say(_("Nimmt die Runde in der laufenden Aufnahme auf"), True)
            self._post("started", t=meta.get("t"), manual=True)
            return
        if (a is not None and a.get("early") and not meta.get("early") and self._pending is None
                and time.time() - a.get("since", 0) <= EARLY_WAIT_S):
            # 1.6: the banner of the round recorded since the loading screen: it names it, nothing restarts
            marks = a.get("marks", [])
            merged = dict(a)
            merged.update({k: v for k, v in meta.items() if v is not None})
            merged.update(early=False, marks=marks, farming=bool(a.get("farming") or meta.get("farming")))
            self.active = merged
            self._say(_("Nimmt die Runde auf (seit dem Ladebildschirm)"), True)
            self._post("started", t=meta.get("t"))
            return
        self._flush()                                   # a new banner while recording: close the old one first
        if not self.cfg.on:
            return
        folder = self.folder()
        if folder is None:
            self._say(_("Aufnahme-Laufwerk nicht angeschlossen – Runde wird nicht aufgenommen"), False)
            return
        if shutil.disk_usage(folder).free < MIN_FREE:
            self._say(_("Aufnahme-Laufwerk fast voll – Runde wird nicht aufgenommen"), False)
            return
        c = self._client()
        try:
            if c.request("GetRecordStatus").get("outputActive"):
                self._say(_("OBS nimmt schon auf (von Hand?) – nichts gestartet"), False)
                return
            try:
                c.request("SetRecordDirectory", {"recordDirectory": folder})     # obs-websocket 5.3+ (OBS 30)
            except ObsError:
                log.info("OBS: Aufnahmeordner nicht setzbar – OBS nimmt in seinen eigenen Ordner auf")
            pre = ""
            if self.cfg.pre and pre_roll:
                try:
                    if self._buffer_state(c):
                        pre = self._save_replay(c)
                except ObsError as e:
                    log.info("OBS: kein Vorlauf (%s)", e)
            c.request("StartRecord")
        finally:
            c.close()
        self.active = dict(meta, pre=pre, since=time.time(), marks=[],
                           sources=sorted(self._routed) if self._routed is not None else None)    # 1.8.23
        if meta.get("early"):
            self._say(_("Nimmt auf – seit dem Ende des Ladebildschirms, wartet auf das Map-Banner"), True)
            self._post("started", t=meta.get("t"), early=True)
            return
        self._say(_("Nimmt die Runde auf"), True)
        self._post("started", t=meta.get("t"))

    @staticmethod
    def _save_replay(c: ObsClient) -> str:
        """SaveReplayBuffer and the path of *this* replay. OBS writes the buffer asynchronously: a fixed 0.3-s wait
        (1.4–1.5.3) often still got the previous replay's path or none – the new file then stayed behind under
        OBS's own name "Replay_…" (user's report). Now: the path before, save, then poll until the path changes
        and the file exists (or the ReplayBufferSaved event names it), at most REPLAY_WAIT s."""
        try:
            before = c.request("GetLastReplayBufferReplay").get("savedReplayPath", "") or ""
        except ObsError:
            before = ""
        c.request("SaveReplayBuffer")
        deadline = time.time() + REPLAY_WAIT
        path = ""
        while time.time() < deadline:
            time.sleep(REPLAY_POLL)
            saved = [e for e in c.events if e.get("eventType") == "ReplayBufferSaved"]
            if saved:
                path = (saved[-1].get("eventData") or {}).get("savedReplayPath", "") or path
            cur = c.request("GetLastReplayBufferReplay").get("savedReplayPath", "") or ""
            if cur and cur != before:
                path = cur
            if path and os.path.exists(path):
                return obs_file(path)
        path = obs_file(path)
        if path:
            log.info("OBS: Vorlauf %s noch nicht geschrieben – wird am Rundenende gesucht", path)
        else:
            log.info("OBS: Vorlauf nicht gefunden (Pfad unverändert: %s)", before or "–")
        return path

    def _finish(self, meta):
        rec, self.active = self.active, None
        self.paused = False
        if rec is None:
            return
        rec.update({k: v for k, v in meta.items() if v})
        c = self._client()
        try:
            path = c.request("StopRecord").get("outputPath", "")
        finally:
            c.close()
        if not obs_file(path):
            self._say(_("OBS hat keinen Dateinamen genannt – Aufnahme nicht zugeordnet"), False)
            return
        self._file_away(rec, path)

    def _file_away(self, rec, path):
        folder = self.folder() or os.path.dirname(path)
        sub = FARMING_DIR if rec.get("farming") and self.cfg.farming_sub else ""     # 1.5.3: farming rounds apart
        dest = os.path.join(folder, sub) if sub else folder
        try:
            os.makedirs(dest, exist_ok=True)
        except OSError:
            sub, dest = "", folder
        ext = os.path.splitext(path)[1] or ".mkv"
        who = rec.get("killer") or {"killer": "Killer", "survivor": "Survivor"}.get(rec.get("role") or "", "")
        name = self._unique(dest, file_name(rec.get("t") or time.time(), rec.get("label", ""), who, ext))
        target = os.path.join(dest, name)
        final = self._move(path, target)
        pre = obs_file(rec.get("pre"))
        pre_name = ""
        if pre and os.path.exists(pre):
            pname = self._unique(dest, file_name(rec.get("t") or time.time(), rec.get("label", ""), who,
                                                 os.path.splitext(pre)[1] or ext, " (Vorlauf)"))
            moved = self._move(pre, os.path.join(dest, pname))
            pre_name = os.path.basename(moved) if os.path.dirname(moved) == dest else ""
        if os.path.dirname(final) != dest:            # another drive than the folder: leave it, still noted
            self._say(_("Aufnahme liegt in OBS' eigenem Ordner: {path}", path=final), False)
            return
        bad = check_file(final)                        # 1.4.1: OBS may have failed silently
        marks = list(rec.get("marks") or [])
        pre_s, extra = 0.0, {}
        if pre_name and not bad and self.cfg.merge:    # 1.4.2: pre-roll + round → one file
            final, pre_name, pre_s, joined = self._join(dest, os.path.join(dest, pre_name), final)
            if joined:
                marks = [round(m + pre_s, 1) for m in marks]
            else:
                extra["merge_failed"] = True
        if bad:
            extra["bad"] = bad
        if rec.get("manual"):                          # 1.15: started by hand (button/hotkey)
            extra["manual"] = True
        if rec.get("sources") is not None:             # 1.8.23: the sources OBS had (the clip editor tells "none")
            extra["sources"] = list(rec["sources"])
        prefix = sub + "/" if sub else ""              # index names: "Farming/…" with "/" on every system
        if pre_name:
            pre_name = prefix + pre_name
        recs = load_index(folder)
        recs.append(Recording(t=float(rec.get("t") or time.time()), file=prefix + os.path.basename(final), pre=pre_name,
                              map_id=rec.get("map_id", ""), label=rec.get("label", ""), role=rec.get("role", ""),
                              killer=rec.get("killer", ""), end=time.time(), extra=extra, marks=marks,
                              farming=bool(rec.get("farming")), pre_s=pre_s))
        limit = int(self.cfg.limit_gb) * 1024 ** 3
        recs, deleted = prune(folder, recs, limit)
        save_index(folder, recs)
        if bad:
            self._warn(_("Aufnahme sieht beschädigt aus ({why}): {file} – OBS-Einstellungen prüfen (Encoder, Platte).",
                         why=bad, file=os.path.basename(final)))
        elif extra.get("merge_failed"):
            self._say(_("Gespeichert: {file} – Vorlauf nicht angefügt, liegt als eigene Datei daneben",
                        file=os.path.basename(final)), True)
        else:
            self._say(_("Gespeichert: {file}", file=os.path.basename(final)), True)
        self._post("saved", file=os.path.basename(final), t=rec.get("t"), marks=len(marks))
        if deleted:
            self._post("deleted", files=deleted)
        self._look_at_space(force=True)
        self._expire_farming(force=True)

    @staticmethod
    def _join(folder, pre_path, round_path):
        """Pre-roll and round into one file named like the round (ffmpeg, stream copy). Returns
        (file, pre name left, seconds of pre-roll, joined?) – on failure both files stay as they were."""
        ffmpeg = ffmpeg_exe()
        if not ffmpeg or os.path.splitext(pre_path)[1].lower() != os.path.splitext(round_path)[1].lower():
            return round_path, os.path.basename(pre_path), 0.0, False
        pre_s = media_duration(pre_path, ffmpeg)
        tmp = os.path.splitext(round_path)[0] + " (zusammen)" + os.path.splitext(round_path)[1]
        if not merge_files([pre_path, round_path], tmp, ffmpeg):
            return round_path, os.path.basename(pre_path), 0.0, False
        try:
            os.remove(pre_path)
            os.replace(tmp, round_path)
        except OSError as e:
            log.info("ffmpeg: zusammengefügte Datei nicht abgelegt (%s)", e)
            try:
                os.remove(tmp)
            except OSError:
                pass
            return round_path, os.path.basename(pre_path) if os.path.exists(pre_path) else "", 0.0, False
        return round_path, "", float(pre_s or 0.0), True

    @staticmethod
    def _unique(folder, name):
        base, ext = os.path.splitext(name)
        n, out = 2, name
        while os.path.exists(os.path.join(folder, out)):
            out = f"{base} ({n}){ext}"
            n += 1
        return out

    @staticmethod
    def _move(src, dst) -> str:
        """Rename (same drive: instant); OBS may still hold the file a moment. Another drive: left where it is."""
        if os.path.splitdrive(os.path.abspath(src))[0].lower() != os.path.splitdrive(os.path.abspath(dst))[0].lower():
            return src
        for _i in range(RENAME_TRIES):
            try:
                os.replace(src, dst)
                return dst
            except PermissionError:
                time.sleep(RENAME_WAIT)
            except OSError:
                break
        return src

    def _watchdog(self):
        """An end that never came (DBD crashed, detection missed it): stop after MAX_ROUND_S. 1.6: a recording
        started at the loading screen whose banner never came within EARLY_WAIT_S is stopped and filed as it is
        (an unknown map is still a round – nothing is deleted)."""
        a = self.active
        if a is None or self._pending is not None:
            return
        now = time.time()
        age = now - a.get("since", now)
        if now - self._free_t >= FREE_CHECK_S:          # 1.15: the drive filling up ends the recording cleanly
            self._free_t = now
            folder = self.folder()
            try:
                low = folder is not None and shutil.disk_usage(folder).free < MIN_FREE
            except OSError:
                low = False
            if low:
                self._finish({})
                self._warn(_("Aufnahme-Laufwerk fast voll – Aufnahme beendet"))
                return
        if a.get("manual"):
            if age > MAX_MANUAL_S:
                log.info("OBS: Aufnahme von Hand läuft seit %d s – beendet", MAX_MANUAL_S)
                self._finish({})
            return
        if a.get("early") and age > EARLY_WAIT_S:
            log.info("OBS: kein Map-Banner %d s nach dem Ladebildschirm – Aufnahme beendet", EARLY_WAIT_S)
            self._finish({"label": a.get("label") or _("Unbekannte Map")})
        elif age > MAX_ROUND_S:
            self._finish({})

    # ---- 1.15: recording by hand, pause, the card's state
    def _manual_start(self, meta):
        """Start a recording now (button/hotkey): like _begin, but it runs until record_stop, DBD closes or
        MAX_MANUAL_S – the automatic round recording must not be on for it, only a folder."""
        if self.active is not None:
            self._say(_("Es läuft schon eine Aufnahme"), True)
            return
        folder = self.folder()
        if folder is None:
            self._say(_("Aufnahme-Laufwerk nicht angeschlossen – nichts gestartet"), False)
            return
        if shutil.disk_usage(folder).free < MIN_FREE:
            self._say(_("Aufnahme-Laufwerk fast voll – nichts gestartet"), False)
            return
        c = self._client()
        try:
            if c.request("GetRecordStatus").get("outputActive"):
                self._say(_("OBS nimmt schon auf (von Hand?) – nichts gestartet"), False)
                return
            try:
                c.request("SetRecordDirectory", {"recordDirectory": folder})
            except ObsError:
                log.info("OBS: Aufnahmeordner nicht setzbar – OBS nimmt in seinen eigenen Ordner auf")
            c.request("StartRecord")
        finally:
            c.close()
        meta = {k: v for k, v in (meta or {}).items() if v}
        meta.setdefault("t", time.time())
        meta.setdefault("label", _("Aufnahme"))
        self.active = dict(meta, manual=True, pre="", since=time.time(), marks=[], paused_s=0.0, paused_at=None,
                           sources=sorted(self._routed) if self._routed is not None else None)
        self.paused = False
        self._free_t = time.time()
        self._say(_("Nimmt auf (von Hand gestartet)"), True)
        self._post("started", t=meta.get("t"), manual=True)

    def _manual_stop(self):
        if self.active is None:
            self._say(_("Keine Aufnahme läuft"), True)
            return
        self._flush()                                   # the tail, if one runs, ends now too

    def _pause(self, on: bool):
        """OBS PauseRecord / ResumeRecord on the recording on air; the paused time is taken out of the marks."""
        a = self.active
        if a is None:
            self._say(_("Keine Aufnahme läuft"), True)
            return
        if bool(on) == bool(a.get("paused_at") is not None):
            return
        c = self._client()
        try:
            try:
                c.request("PauseRecord" if on else "ResumeRecord")
            except ObsError as e:
                # OBS refuses a pause of a paused output (and the other way round): take its word for the state
                if bool(c.request("GetRecordStatus").get("outputPaused")) != bool(on):
                    raise e
        finally:
            c.close()
        now = time.time()
        if on:
            a["paused_at"] = now
        else:
            a["paused_s"] = float(a.get("paused_s") or 0.0) + max(0.0, now - float(a.get("paused_at") or now))
            a["paused_at"] = None
        self.paused = bool(on)
        self._say(_("Aufnahme pausiert") if on else _("Aufnahme läuft weiter"), True)
        self._post("paused", on=bool(on))

    def _poll(self):
        """The recording card's state in one connection: GetRecordStatus, GetReplayBufferStatus, GetStats every
        time; GetVideoSettings and the profile's encoder / buffer length every PROFILE_EVERY_S. Only reads."""
        d = {"connected": False, "error": "", "recording": False, "paused": False, "seconds": 0.0, "bytes": 0,
             "ours": self.active is not None, "manual": bool(self.active and self.active.get("manual")),
             "marks": len((self.active or {}).get("marks") or []), "label": (self.active or {}).get("label", ""),
             "buffer": False, "folder": self.folder() or ""}
        try:
            c = self._client()
        except ObsError as e:
            d["error"] = str(e)
            self._post("obs_status", **d)
            return
        try:
            rec = c.request("GetRecordStatus")
            d.update(connected=True, recording=bool(rec.get("outputActive")), paused=bool(rec.get("outputPaused")),
                     seconds=float(rec.get("outputDuration") or 0) / 1000.0, bytes=int(rec.get("outputBytes") or 0))
            if d["ours"] and self.active.get("paused_at") is not None:
                d["paused"] = True
            try:
                d["buffer"] = self._buffer_state(c)
            except ObsError:
                d["buffer"] = False
            try:
                st = c.request("GetStats")
                d.update(active_fps=float(st.get("activeFps") or 0.0), cpu=float(st.get("cpuUsage") or 0.0),
                         disk_free=float(st.get("availableDiskSpace") or 0.0) * 1024 ** 2,
                         render_skipped=int(st.get("renderSkippedFrames") or 0),
                         render_total=int(st.get("renderTotalFrames") or 0),
                         output_skipped=int(st.get("outputSkippedFrames") or 0),
                         output_total=int(st.get("outputTotalFrames") or 0))
            except ObsError:
                pass
            now = time.time()
            if now - self._slow_t >= PROFILE_EVERY_S or not self._slow:
                self._slow_t = now
                self._slow = self._read_profile(c)
            d.update(self._slow)
        except ObsError as e:
            d["error"] = str(e)
        finally:
            c.close()
        self._post("obs_status", **d)

    def _read_profile(self, c: ObsClient) -> dict:
        """Output size and rate (GetVideoSettings), encoder and replay buffer length (profile, read only)."""
        out = {}
        try:
            v = c.request("GetVideoSettings")
            num, den = float(v.get("fpsNumerator") or 0), float(v.get("fpsDenominator") or 1)
            out.update(width=int(v.get("outputWidth") or 0), height=int(v.get("outputHeight") or 0),
                       fps=round(num / den, 3) if num and den else 0.0)
        except ObsError:
            pass
        try:
            mode = self._profile(c, "Output", "Mode")
            keys = profile_keys(mode)
            raw = self._profile(c, *keys["encoder"])
            if keys["quality"] and self._profile(c, *keys["quality"]).lower() == "stream" or raw.lower() == "none":
                raw = self._profile(c, *keys["stream"])
            out["encoder"] = encoder_label(raw)
            out["mode"] = mode
            rb = self._profile(c, *keys["buffer_s"])
            out["buffer_s"] = int(float(rb)) if rb.strip() else None
        except (ObsError, ValueError):
            pass
        return out

    # ---- 1.6: audio sources in OBS
    def _audio_now(self):
        if not (self.cfg.on and self.cfg.audio and self._game):
            return
        try:
            c = self._client()
        except ObsError as e:
            log.info("OBS: Ton nicht eingestellt (%s)", e)
            return
        try:
            self._audio(c)
        finally:
            c.close()

    @staticmethod
    def _input_names(c: ObsClient) -> set:
        """The names of OBS's inputs; 1.9: one of ours still named after the old program name is renamed first."""
        names = {i.get("inputName") for i in c.request("GetInputList").get("inputs", [])}
        for new in OWN_SOURCES:
            old = new.replace("Fog Scout", OLD_SOURCE_NAME, 1)
            if old in names and new not in names:
                c.request("SetInputName", {"inputName": old, "newInputName": new})
                names.discard(old)
                names.add(new)
                log.info("OBS-Quelle umbenannt: %s -> %s", old, new)
        return names

    def _audio(self, c: ObsClient) -> str:
        """DBD and Discord as OBS application audio sources (created in the current scene the first time),
        each muted or not as set; OBS's desktop audio and microphone muted or not as set. Errors only in the log
        and the status: older OBS (< 28) has no application audio capture."""
        notes = []
        try:
            names = self._input_names(c)
            scene = None
            for key, on in (("dbd", self.cfg.audio_dbd), ("discord", self.cfg.audio_discord)):
                name, window = AUDIO_APPS[key]
                if name not in names:
                    if not on:
                        continue                          # never created, not wanted: nothing to do
                    if scene is None:
                        cur = c.request("GetCurrentProgramScene")
                        scene = cur.get("currentProgramSceneName") or cur.get("sceneName") or ""
                    c.request("CreateInput", {"sceneName": scene, "inputName": name, "inputKind": AUDIO_KIND,
                                              "inputSettings": {"window": window, "priority": AUDIO_PRIORITY_EXE},
                                              "sceneItemEnabled": True})
                    notes.append(_("Tonquelle angelegt: {name}", name=name))
                elif on:
                    if scene is None:
                        cur = c.request("GetCurrentProgramScene")
                        scene = cur.get("currentProgramSceneName") or cur.get("sceneName") or ""
                    notes += self._in_scene(c, scene, name)
                if on:
                    exe = self._follow_window(c, key, name)
                    if exe:
                        notes.append(_("Tonquelle {name} hört jetzt auf {exe}", name=name, exe=exe))
                c.request("SetInputMute", {"inputName": name, "inputMuted": not on})
            special = c.request("GetSpecialInputs")
            others = []
            for key, on in (("desktop1", self.cfg.audio_desktop), ("desktop2", self.cfg.audio_desktop),
                            ("mic1", self.cfg.audio_mic), ("mic2", self.cfg.audio_mic),
                            ("mic3", self.cfg.audio_mic), ("mic4", self.cfg.audio_mic)):
                name = special.get(key)
                if name:
                    c.request("SetInputMute", {"inputName": name, "inputMuted": not on})
                    others.append(("mic" if key.startswith("mic") else "desktop", name))
            hint = self._tracks(c, names, others) if self.cfg.tracks else ""
            if not self.cfg.tracks:
                self._routed = None
        except ObsError as e:
            log.info("OBS: Ton nicht eingestellt (%s)", e)
            text = _("Ton in OBS nicht eingestellt: {error}", error=e)
            self._say(text, False)
            return text
        for n in notes:
            log.info("OBS: %s", n)
        return hint

    @staticmethod
    def _follow_window(c: ObsClient, key: str, name: str, priority: int = AUDIO_PRIORITY_EXE) -> str:
        """1.8.20: point our source at the window OBS offers for the program (WINDOW_EXES) – Steam or Epic DBD,
        Discord stable/PTB/Canary; the executable it now follows, "" when nothing changed: the program is not
        running (OBS does not list it then) or the source already points at a listed match. A failure only goes
        to the log. ``priority`` (1.8.41): how OBS matches the window – the window capture uses another one."""
        try:
            items = c.request("GetInputPropertiesListPropertyItems",
                              {"inputName": name, "propertyName": "window"}).get("propertyItems") or []
            found = [i.get("itemValue") for i in items if i.get("itemEnabled", True)
                     and WINDOW_EXES[key].match(str(i.get("itemValue") or "").rsplit(":", 1)[-1])]
            if not found:
                return ""
            found.sort(key=lambda v: ("Shipping" not in v, ":UnrealWindow:" not in v))   # the game, not a launcher
            current = (c.request("GetInputSettings", {"inputName": name}).get("inputSettings") or {}).get("window")
            if current in found:
                return ""
            c.request("SetInputSettings", {"inputName": name, "inputSettings": {"window": found[0],
                                                                                "priority": priority}})
        except ObsError as e:
            log.info("OBS: Fenster der Quelle %s nicht geprüft (%s)", name, e)
            return ""
        return found[0].rsplit(":", 1)[-1]

    def _capture(self) -> str:
        """1.11.7: which of our picture sources is wanted – "window" (OBS window capture) or "game"."""
        return self.cfg.capture if self.cfg.capture in CAPTURES else "window"

    def _video(self, c: ObsClient) -> str:
        """1.8.41: our window capture of DBD (WINDOW_SOURCE) in the scene on air – created on top of it and fitted
        to the canvas the first time, added to another scene the same way, shown again when hidden, pointed at the
        running DBD (Steam/Epic/Store). Switched off: only hidden in this scene, never deleted – the user's own
        sources (the monitor capture) are never touched. 1.11.7: the same for our game capture (GAME_SOURCE) – the
        one of the two that Config.capture names is shown, the other hidden. Returns a problem for the status line,
        else ""."""
        notes = []
        want = self._capture() if self.cfg.window else None
        try:
            names = self._input_names(c)
            ours = [k for k in CAPTURES if video_source(k)[0] in names or k == want]
            if not ours:
                return ""                                 # never created, not wanted: nothing to do
            cur = c.request("GetCurrentProgramScene")
            scene = cur.get("currentProgramSceneName") or cur.get("sceneName") or ""
            for key in sorted(ours, key=lambda k: k == want):  # hide the other one first, then show the wanted one
                self._video_source(c, scene, names, key, key == want, notes)
        except ObsError as e:
            log.info("OBS: Bildquelle nicht eingerichtet (%s)", e)
            return _("DBD-Fenster in OBS nicht eingerichtet: {error}", error=e)
        for n in notes:
            log.info("OBS: %s", n)
        return ""

    def _video_source(self, c: ObsClient, scene: str, names: set, capture: str, wanted: bool, notes: list):
        """One of our picture sources: created / added to the scene / shown again and pointed at DBD when
        ``wanted``, else only hidden in this scene."""
        name, kind, settings = video_source(capture)
        if name not in names:
            if not wanted:
                return
            made = c.request("CreateInput", {"sceneName": scene, "inputName": name, "inputKind": kind,
                                             "sceneItemEnabled": True, "inputSettings": settings})
            self._fit(c, scene, made.get("sceneItemId"))
            notes.append(_("Bildquelle angelegt: {name} (Szene „{scene}“)", name=name, scene=scene))
        elif scene:
            items = [i for i in c.request("GetSceneItemList", {"sceneName": scene}).get("sceneItems", [])
                     if i.get("sourceName") == name]
            if not wanted:
                for i in items:
                    if i.get("sceneItemEnabled", True):
                        c.request("SetSceneItemEnabled", {"sceneName": scene, "sceneItemId": i.get("sceneItemId"),
                                                          "sceneItemEnabled": False})
                        notes.append(_("Bildquelle in der Szene „{scene}“ ausgeblendet: {name}", scene=scene,
                                       name=name))
                return
            if not items:
                made = c.request("CreateSceneItem", {"sceneName": scene, "sourceName": name,
                                                     "sceneItemEnabled": True})
                self._fit(c, scene, made.get("sceneItemId"))
                notes.append(_("Bildquelle zur Szene „{scene}“ hinzugefügt: {name}", scene=scene, name=name))
            elif not any(i.get("sceneItemEnabled", True) for i in items):
                c.request("SetSceneItemEnabled", {"sceneName": scene, "sceneItemId": items[0].get("sceneItemId"),
                                                  "sceneItemEnabled": True})
                notes.append(_("Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}", scene=scene,
                               name=name))
        elif not wanted:
            return
        exe = self._follow_window(c, "dbd", name, WINDOW_PRIORITY_CLASS)
        if exe:
            notes.append(_("Bildquelle {name} zeigt jetzt {exe}", name=name, exe=exe))

    @staticmethod
    def _fit(c: ObsClient, scene: str, item_id):
        """Our new scene item at the top left, scaled into the canvas (the DBD window may differ from it, e.g. a
        2560×1440 canvas for 3440×1440 with its black bars). Placed once – a later change by the user stays."""
        if item_id is None or not scene:
            return
        video = c.request("GetVideoSettings")
        w, h = int(video.get("baseWidth") or 0), int(video.get("baseHeight") or 0)
        if w <= 0 or h <= 0:
            return
        c.request("SetSceneItemTransform", {"sceneName": scene, "sceneItemId": item_id, "sceneItemTransform": {
            "positionX": 0, "positionY": 0, "alignment": 5, "boundsType": "OBS_BOUNDS_SCALE_INNER",
            "boundsAlignment": 0, "boundsWidth": w, "boundsHeight": h}})

    def _overlay_wanted(self) -> bool:
        """1.8.89: only together with our window capture – a display capture shows the real overlay already."""
        return bool(self.cfg.window and self.cfg.overlay and self.cfg.overlay_file)

    def _overlay_video(self, c: ObsClient) -> str:
        """1.8.89 (user: "nur das DBD-Fenster aufnehmen und das Overlay im Spiel"): our image source with the overlay
        picture (OVERLAY_SOURCE, the file obsoverlay writes) in the scene on air – created on top of the window
        capture, shown while wanted, else only hidden (never deleted; the user's sources are never touched),
        pointed at our file. Returns a problem for the status line, else ""."""
        want = self._overlay_wanted()
        self._overlay_item = None
        notes = []
        try:
            names = self._input_names(c)
            if OVERLAY_SOURCE not in names and not want:
                return ""
            cur = c.request("GetCurrentProgramScene")
            scene = cur.get("currentProgramSceneName") or cur.get("sceneName") or ""
            if not scene:
                return ""
            if OVERLAY_SOURCE not in names:
                made = c.request("CreateInput", {"sceneName": scene, "inputName": OVERLAY_SOURCE,
                                                 "inputKind": OVERLAY_KIND, "sceneItemEnabled": True,
                                                 "inputSettings": {"file": self.cfg.overlay_file, "unload": False}})
                self._overlay_item = (scene, made.get("sceneItemId"))
                notes.append(_("Bildquelle angelegt: {name} (Szene „{scene}“)", name=OVERLAY_SOURCE, scene=scene))
            else:
                items = [i for i in c.request("GetSceneItemList", {"sceneName": scene}).get("sceneItems", [])
                         if i.get("sourceName") == OVERLAY_SOURCE]
                if not want:
                    for i in items:
                        if i.get("sceneItemEnabled", True):
                            c.request("SetSceneItemEnabled", {"sceneName": scene, "sceneItemId": i.get("sceneItemId"),
                                                              "sceneItemEnabled": False})
                            notes.append(_("Bildquelle in der Szene „{scene}“ ausgeblendet: {name}", scene=scene,
                                           name=OVERLAY_SOURCE))
                    for n in notes:
                        log.info("OBS: %s", n)
                    return ""
                if not items:
                    made = c.request("CreateSceneItem", {"sceneName": scene, "sourceName": OVERLAY_SOURCE,
                                                         "sceneItemEnabled": True})
                    self._overlay_item = (scene, made.get("sceneItemId"))
                    notes.append(_("Bildquelle zur Szene „{scene}“ hinzugefügt: {name}", scene=scene,
                                   name=OVERLAY_SOURCE))
                else:
                    self._overlay_item = (scene, items[0].get("sceneItemId"))
                    if not any(i.get("sceneItemEnabled", True) for i in items):
                        c.request("SetSceneItemEnabled", {"sceneName": scene, "sceneItemId": items[0].get("sceneItemId"),
                                                          "sceneItemEnabled": True})
                        notes.append(_("Bildquelle in der Szene „{scene}“ wieder eingeblendet: {name}", scene=scene,
                                       name=OVERLAY_SOURCE))
                have = c.request("GetInputSettings", {"inputName": OVERLAY_SOURCE}).get("inputSettings") or {}
                if have.get("file") != self.cfg.overlay_file:              # another program folder than before
                    c.request("SetInputSettings", {"inputName": OVERLAY_SOURCE,
                                                   "inputSettings": {"file": self.cfg.overlay_file, "unload": False}})
            self._overlay_placed = None
            self._overlay_on_top(c, notes)
            self._place_overlay(c)
        except ObsError as e:
            log.info("OBS: Overlay-Bildquelle nicht eingerichtet (%s)", e)
            return _("Overlay in OBS nicht eingerichtet: {error}", error=e)
        for n in notes:
            log.info("OBS: %s", n)
        return ""

    def _overlay_moved(self, box):
        """The writer wrote a picture for ``box`` (relative to the DBD window, None = nothing shown)."""
        self._overlay_box = box
        if box is None or not self._game or not self._ready or self._overlay_item is None or not self._overlay_wanted():
            return
        try:
            c = self._client()
        except ObsError as e:
            log.info("OBS: Overlay nicht platziert (%s)", e)
            return
        try:
            self._place_overlay(c)
        except ObsError as e:
            log.info("OBS: Overlay nicht platziert (%s)", e)
        finally:
            c.close()

    def _overlay_on_top(self, c: ObsClient, notes: list):
        """1.11.7: our overlay item above our picture source – a game capture chosen later is created on top of the
        scene, over the overlay. Only our own overlay item is moved (SetSceneItemIndex), never another source."""
        if self._overlay_item is None:
            return
        scene, item_id = self._overlay_item
        items = c.request("GetSceneItemList", {"sceneName": scene}).get("sceneItems", [])
        index = {i.get("sceneItemId"): i.get("sceneItemIndex", n) for n, i in enumerate(items)}
        pic = next((i for i in items if i.get("sourceName") == video_source(self._capture())[0]), None)
        if pic is None or item_id not in index:
            return
        top = index[pic.get("sceneItemId")]
        if index[item_id] < top:
            c.request("SetSceneItemIndex", {"sceneName": scene, "sceneItemId": item_id, "sceneItemIndex": top})
            notes.append(_("Bildquelle {name} über {over} gelegt", name=OVERLAY_SOURCE, over=pic.get("sourceName")))

    def _place_overlay(self, c: ObsClient):
        """Move our image item over the overlay's place: the window item's transform (GetSceneItemList, read
        only) says where OBS draws the DBD window on the canvas, obsoverlay.overlay_transform does the maths;
        nothing is sent while the transform is the one sent last or OBS has no picture of the window yet.
        1.11.7: the item of the picture source in use – window or game capture."""
        if self._overlay_item is None or self._overlay_box is None:
            return
        scene, item_id = self._overlay_item
        items = c.request("GetSceneItemList", {"sceneName": scene}).get("sceneItems", [])
        name = video_source(self._capture())[0]
        win = next((i for i in items if i.get("sourceName") == name), None)
        if win is None:
            return
        tf = obsoverlay.overlay_transform(win.get("sceneItemTransform") or {}, self._overlay_box)
        if tf is None or tf == self._overlay_placed:
            return
        c.request("SetSceneItemTransform", {"sceneName": scene, "sceneItemId": item_id, "sceneItemTransform": tf})
        self._overlay_placed = tf

    @staticmethod
    def _in_scene(c: ObsClient, scene: str, name: str) -> list:
        """1.8.18 (user: Discord never heard in the clips): an application audio source plays – and is recorded –
        only while it is in the scene on air. Ours was created in the scene of that moment; recording in another
        scene left its track silent. A wanted source missing from the program scene is added to it, a hidden one
        is shown again (``sceneItemEnabled`` off mutes it too). Groups and nested scenes are not looked into – a
        second scene item of the same source does not double its sound."""
        if not scene:
            return []
        items = c.request("GetSceneItemList", {"sceneName": scene}).get("sceneItems", [])
        mine = [i for i in items if i.get("sourceName") == name]
        if not mine:
            c.request("CreateSceneItem", {"sceneName": scene, "sourceName": name, "sceneItemEnabled": True})
            return [_("Tonquelle zur Szene „{scene}“ hinzugefügt: {name}", scene=scene, name=name)]
        if not any(i.get("sceneItemEnabled", True) for i in mine):
            c.request("SetSceneItemEnabled", {"sceneName": scene, "sceneItemId": mine[0].get("sceneItemId"),
                                              "sceneItemEnabled": True})
            return [_("Tonquelle in der Szene „{scene}“ wieder eingeblendet: {name}", scene=scene, name=name)]
        return []

    def _tracks(self, c: ObsClient, names: set, others: list):
        """1.8.6: every source on track 1 (everything) and its own track (SOURCE_TRACKS: game 2, Discord 3,
        microphone 4) – the clip editor mixes them like Medal. Only sources that exist are touched (nothing is
        created here). 1.8.19: every other audio source of the user's OBS goes from tracks 2–4 to track 5
        (background; tracks 1 and 6 stay as they are, logged by name), the desktop sound to track 1 only – else
        "game" held all of it. Then a look at the
        profile: OBS writes several tracks only in the advanced output mode with the recording tracks ticked; we
        never change the profile, the status line says what to tick."""
        wanted = list(others)
        for key in ("dbd", "discord"):
            name = AUDIO_APPS[key][0]
            if name in names or getattr(self.cfg, "audio_" + key):
                wanted.append((key, name))
        for key, name in wanted:
            c.request("SetInputAudioTracks", {"inputName": name, "inputAudioTracks": track_flags(SOURCE_TRACKS[key])})
        moved, background = [], False
        for name in sorted(n for n in names - {n for _k, n in wanted} if n):
            try:                                        # a source without sound (picture, scene) answers an error
                tracks = c.request("GetInputAudioTracks", {"inputName": name}).get("inputAudioTracks") or {}
                background = True
                want = {"2": False, "3": False, "4": False, "5": True}
                if any(bool(tracks.get(t)) != on for t, on in want.items()):
                    c.request("SetInputAudioTracks", {"inputName": name, "inputAudioTracks": want})
                    moved.append(name)
            except ObsError:
                continue
        if moved:
            log.info("OBS: %s", _("Auf Spur 5 (Hintergrund) statt bei Spiel/Discord/Mikrofon: {names}",
                                  names=", ".join(moved)))
        # 1.8.23: what a recording from now on has on its own track and switched on – the clip editor tells
        # "no source" apart from "recorded but silent"
        routed = {key for key in ("dbd", "discord") if getattr(self.cfg, "audio_" + key)}
        if self.cfg.audio_mic and any(k == "mic" for k, _n in others):
            routed.add("mic")
        if background:
            routed.add("other")
        self._routed = routed
        hint = profile_hint(self._profile(c, "Output", "Mode"), self._profile(c, "AdvOut", "RecTracks"))
        if hint:
            log.info("OBS: %s", hint)
            self._say(hint, False)
        return hint

    @staticmethod
    def _profile(c: ObsClient, category: str, name: str) -> str:
        d = c.request("GetProfileParameter", {"parameterCategory": category, "parameterName": name})
        value = d.get("parameterValue")
        if value is None:
            value = d.get("defaultParameterValue")
        return "" if value is None else str(value)

    def _clip_sound(self, src: str, ffmpeg: str) -> tuple[list, list]:
        """1.8.6: ffmpeg's map and codec arguments for the instant clip (clip_sound_args) – the sources of
        Config.clip_sources mixed from the buffer file's own tracks as the first track, the tracks themselves
        behind it (1.14.4); a file without them (one track) is taken as it is."""
        return clip_sound_args(audio_tracks(src, ffmpeg), self.cfg.clip_sources)

    # ---- 1.6: F8 instant clip
    def _instant_clip(self, meta):
        """Save OBS's replay buffer, keep its last clip_s seconds as Clips/<name>.mp4 (ffmpeg, stream copy). The
        saved replay is our own file (made by our request, path from OBS): it is removed once the clip exists;
        without ffmpeg it is moved into Clips as it is."""
        if not (self.cfg.on and self.cfg.instant):
            return
        folder = self.folder()
        if folder is None:
            self._post("clip", ok=False, why=_("Aufnahme-Laufwerk nicht angeschlossen"))
            return
        try:
            c = self._client()
        except ObsError as e:                             # 1.8.32: F8 always gets an answer
            self._post("clip", ok=False, why=str(e))
            raise
        try:
            state = self._buffer_state(c)
            if state is None:                             # 1.8.32 (user's log: "Replay buffer is not available")
                self._post("clip", ok=False, why=BUFFER_HINT())
                self._say(BUFFER_HINT(), False)
                return
            if not state:
                self._post("clip", ok=False, why=_("Wiederholungspuffer in OBS läuft nicht"))
                return
            src = self._save_replay(c)
        except ObsError as e:
            self._post("clip", ok=False, why=str(e))
            raise
        finally:
            c.close()
        if not src or not os.path.exists(src) or not obs_file(src):
            self._post("clip", ok=False, why=_("OBS hat den Puffer nicht gespeichert"))
            return
        clips = os.path.join(folder, CLIPS_DIR)
        os.makedirs(clips, exist_ok=True)
        who = meta.get("killer") or {"killer": "Killer", "survivor": "Survivor"}.get(meta.get("role") or "", "")
        name = file_name(time.time(), meta.get("label") or _("Clip"), who, "", " " + _("(Sofort-Clip)"))
        ffmpeg = ffmpeg_exe()
        out = None
        if ffmpeg:
            out = os.path.join(clips, self._unique(clips, name + ".mp4"))
            maps, codec = self._clip_sound(src, ffmpeg)
            rc, err = _run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-sseof", f"-{int(self.cfg.clip_s)}",
                            "-i", src, *maps, *codec, "-avoid_negative_ts", "make_zero",
                            "-movflags", "+faststart", out])
            if rc != 0 or not os.path.exists(out) or os.path.getsize(out) == 0:
                log.info("ffmpeg: Sofort-Clip nicht geschnitten (%s): %s", rc,
                         err[-300:].decode("utf-8", "replace").strip())
                try:
                    os.remove(out)
                except OSError:
                    pass
                out = None
        if out is not None:
            try:
                os.remove(src)
            except OSError:
                pass
        else:                                            # no ffmpeg / cut failed: the whole buffer is the clip
            target = os.path.join(clips, self._unique(clips, name + (os.path.splitext(src)[1] or ".mkv")))
            out = self._move(src, target)
        if os.path.dirname(out) == clips:                 # 1.8.13: into the clips list with its round
            self._add_clip({"file": os.path.basename(out), "kind": "instant", "seconds": float(self.cfg.clip_s),
                            **{k: meta[k] for k in ("source", "map_id", "label", "role", "killer", "farming")
                               if k in meta}}, folder)
        self._post("clip", ok=True, file=os.path.basename(out), seconds=int(self.cfg.clip_s),
                   label=meta.get("label") or "", role=meta.get("role") or "", killer=meta.get("killer") or "",
                   source=float(meta.get("source") or 0.0))          # 1.10: the YouTube title
        self._look_at_space(force=True)
