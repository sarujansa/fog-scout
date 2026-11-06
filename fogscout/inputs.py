"""Input display (1.39, user: "In vielen Twitch-Streams sehe ich Controller-Eingaben sichtbar", approved 06.11.2026):
which keys of a fixed list, which mouse buttons and which gamepad controls are held down right now – for the overlay
card "Eingaben" (drawn in overlay_render.input_card, placed by app_inputs).

Hard rule (CLAUDE.md "Eingaben lesen"): read only, never send. Passive polling of Windows' input state in this
process – ``GetAsyncKeyState`` for the keys in KEYS and nothing else, ``XInputGetState`` (xinput1_4.dll /
xinput9_1_0.dll from System32 only) for the gamepad. No hook, no Raw Input, no window message, nothing of the game
process. A look only happens while the App allows it (setting on, a round runs, DBD's window known) and DBD's window
is the foreground window – checked before every look, so typing in another program is never seen. Nothing is
written anywhere: the state lives in memory, never in the log, the diagnosis or a request to Claude.
"""
from __future__ import annotations

import logging
import math
import sys
import threading
import time
from dataclasses import dataclass

log = logging.getLogger("fogscout")

IS_WIN = sys.platform == "win32"

# (id, virtual-key code, keycap) – DBD's default keys: move, interact/action, ability, item, sprint, crouch, the
# mouse buttons. The only keys ever asked for; letters outside this list are never looked at.
KEYS = (("q", 0x51, "Q"), ("w", 0x57, "W"), ("e", 0x45, "E"), ("r", 0x52, "R"),
        ("shift", 0x10, "SHIFT"), ("a", 0x41, "A"), ("s", 0x53, "S"), ("d", 0x44, "D"),
        ("ctrl", 0x11, "CTRL"), ("space", 0x20, "SPACE"),
        ("lmb", 0x01, ""), ("rmb", 0x02, ""), ("mmb", 0x04, ""))
KEY_IDS = tuple(k for k, _vk, _cap in KEYS)
MOUSE_IDS = ("lmb", "rmb", "mmb")

# XINPUT_GAMEPAD.wButtons
PAD_BUTTONS = (("up", 0x0001), ("down", 0x0002), ("left", 0x0004), ("right", 0x0008), ("start", 0x0010),
               ("back", 0x0020), ("ls", 0x0040), ("rs", 0x0080), ("lb", 0x0100), ("rb", 0x0200),
               ("a", 0x1000), ("b", 0x2000), ("x", 0x4000), ("y", 0x8000))
PAD_IDS = tuple(k for k, _bit in PAD_BUTTONS)

STICK_DEAD = 0.24              # share of the stick's travel that counts as resting (XInput's own: 7849 / 32767)
TRIGGER_DEAD = 30 / 255        # XINPUT_GAMEPAD_TRIGGER_THRESHOLD
ERROR_DEVICE_NOT_CONNECTED = 1167
PAD_RESCAN_S = 2.0             # a slot without a controller is asked again only this often (XInput is slow there)

LAYOUTS = ("auto", "keyboard", "gamepad")
POLL_S = 1 / 60                # a look this often while allowed …
IDLE_S = 0.25                  # … otherwise the thread waits this long (or until allowed again)


@dataclass(frozen=True)
class InputState:
    """What is held down at one look. ``keys`` ⊂ KEY_IDS, ``pad`` ⊂ PAD_IDS; triggers 0…1, sticks −1…1 (up = +);
    ``pad_on`` = a controller answered."""
    keys: frozenset = frozenset()
    pad: frozenset = frozenset()
    lt: float = 0.0
    rt: float = 0.0
    lx: float = 0.0
    ly: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    pad_on: bool = False


EMPTY = InputState()


def _stick(v: float) -> float:
    """Raw axis −1…1 → 0 inside the dead zone, else rescaled to reach ±1 at the edge."""
    a = abs(v)
    if a <= STICK_DEAD:
        return 0.0
    return (1.0 if v > 0 else -1.0) * min(1.0, (a - STICK_DEAD) / (1 - STICK_DEAD))


def _trigger(v: float) -> float:
    return 0.0 if v <= TRIGGER_DEAD else min(1.0, (v - TRIGGER_DEAD) / (1 - TRIGGER_DEAD))


def pad_state(buttons: int, lt: int, rt: int, lx: int, ly: int, rx: int, ry: int) -> InputState:
    """An XINPUT_GAMEPAD's raw values → InputState (pure)."""
    return InputState(pad=frozenset(k for k, bit in PAD_BUTTONS if int(buttons) & bit),
                      lt=round(_trigger(lt / 255), 3), rt=round(_trigger(rt / 255), 3),
                      lx=round(_stick(lx / 32767), 3), ly=round(_stick(ly / 32767), 3),
                      rx=round(_stick(rx / 32767), 3), ry=round(_stick(ry / 32767), 3), pad_on=True)


def pad_active(st: InputState) -> bool:
    """Something on the gamepad is moved or held."""
    return bool(st.pad) or any((st.lt, st.rt, st.lx, st.ly, st.rx, st.ry))


STICK_DIRS = 8                 # a stick is shown in eight directions …
STICK_FAR = 0.75               # … half way out below this share of its travel, all the way above


def stick_steps(x: float, y: float) -> tuple:
    """A stick's position as the card shows it: (0, 0), or one of STICK_DIRS directions at half or full travel –
    a resting thumb that wobbles a little does not redraw the card, and every shown position is drawn only once."""
    m = math.hypot(x, y)
    if m <= 0:
        return (0.0, 0.0)
    a = round(math.atan2(y, x) / (2 * math.pi / STICK_DIRS)) * (2 * math.pi / STICK_DIRS)
    r = 1.0 if m >= STICK_FAR else 0.5
    return (round(math.cos(a) * r, 3) + 0.0, round(math.sin(a) * r, 3) + 0.0)


def draw_key(st: InputState, layout: str) -> tuple:
    """What the card shows of ``st`` in ``layout`` – the card is drawn anew only when this changes (triggers in
    eighths, sticks in stick_steps)."""
    if layout == "gamepad":
        return ("gamepad", tuple(sorted(st.pad)), round(st.lt * 8), round(st.rt * 8),
                stick_steps(st.lx, st.ly), stick_steps(st.rx, st.ry))
    return ("keyboard", tuple(sorted(st.keys)))


class DeviceChoice:
    """Setting "automatisch": the card shows the device used last – a key press switches to the keyboard, a
    gamepad control to the gamepad; nothing held keeps the last one (no flicker between two layouts)."""

    def __init__(self, device: str = "keyboard"):
        self.device = device

    def update(self, st: InputState) -> str:
        if st.keys:
            self.device = "keyboard"
        elif pad_active(st):
            self.device = "gamepad"
        return self.device

    def layout(self, setting: str, st: InputState) -> str:
        """The layout to draw for the setting (auto / keyboard / gamepad)."""
        device = self.update(st)
        return setting if setting in ("keyboard", "gamepad") else device


SAMPLE = InputState(keys=frozenset({"w", "shift", "lmb"}), pad=frozenset({"a", "rb"}), rt=0.7, lx=0.0, ly=0.8,
                    rx=-0.5, ry=0.2, pad_on=True)      # the preview / edit mode / "Overlay testen"


class Win32Poll:
    """One look at the input state (Windows only): None while ``hwnd`` is not the foreground window, else an
    InputState of the KEYS and the first connected controller."""

    def __init__(self):
        import ctypes
        from ctypes import wintypes
        self._ctypes = ctypes
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)
        self._user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
        self._user32.GetAsyncKeyState.restype = ctypes.c_short
        self._user32.GetForegroundWindow.restype = wintypes.HWND
        self._user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
        self._user32.GetAncestor.restype = wintypes.HWND
        self._xinput, self._state_t = self._load_xinput()
        self._slot = None                     # the slot of the controller found last
        self._scan_at = 0.0

    def _load_xinput(self):
        """xinput1_4.dll (Windows 8+), else xinput9_1_0.dll – by their full path in System32, never by name (the
        program runs as administrator: a DLL of the same name elsewhere must never be loaded)."""
        ctypes = self._ctypes
        from ctypes import wintypes

        from .paths import system_exe

        class Gamepad(ctypes.Structure):
            _fields_ = [("wButtons", wintypes.WORD), ("bLeftTrigger", ctypes.c_ubyte),
                        ("bRightTrigger", ctypes.c_ubyte), ("sThumbLX", ctypes.c_short), ("sThumbLY", ctypes.c_short),
                        ("sThumbRX", ctypes.c_short), ("sThumbRY", ctypes.c_short)]

        class State(ctypes.Structure):
            _fields_ = [("dwPacketNumber", wintypes.DWORD), ("Gamepad", Gamepad)]

        for name in ("xinput1_4.dll", "xinput9_1_0.dll"):
            try:
                dll = ctypes.WinDLL(system_exe(name))
            except OSError:
                continue
            dll.XInputGetState.argtypes = [wintypes.DWORD, ctypes.POINTER(State)]
            dll.XInputGetState.restype = wintypes.DWORD
            return dll, State
        return None, None

    def _foreground(self, hwnd: int) -> bool:
        h = self._user32.GetForegroundWindow()
        if not h:
            return False
        root = self._user32.GetAncestor(h, 2) or h          # GA_ROOT
        return int(root) == int(hwnd)

    def _keys(self) -> frozenset:
        down = self._user32.GetAsyncKeyState
        return frozenset(k for k, vk, _cap in KEYS if down(vk) & 0x8000)

    def _pad(self, now: float):
        if self._xinput is None:
            return None
        slots = (self._slot,) if self._slot is not None else ()
        if self._slot is None and now >= self._scan_at:
            slots, self._scan_at = (0, 1, 2, 3), now + PAD_RESCAN_S
        for i in slots:
            st = self._state_t()
            if self._xinput.XInputGetState(i, self._ctypes.byref(st)) == 0:
                self._slot = i
                g = st.Gamepad
                return pad_state(g.wButtons, g.bLeftTrigger, g.bRightTrigger, g.sThumbLX, g.sThumbLY, g.sThumbRX,
                                 g.sThumbRY)
            if i == self._slot:
                self._slot, self._scan_at = None, now + PAD_RESCAN_S     # unplugged: look again later
        return None

    def __call__(self, hwnd: int):
        if not hwnd or not self._foreground(hwnd):
            return None
        keys = self._keys()
        pad = self._pad(time.monotonic())
        if pad is None:
            return InputState(keys=keys)
        return InputState(keys=keys, pad=pad.pad, lt=pad.lt, rt=pad.rt, lx=pad.lx, ly=pad.ly, rx=pad.rx, ry=pad.ry,
                          pad_on=True)


class Reader:
    """The input state, looked at POLL_S apart in a thread of its own while allowed (``allow(hwnd)`` with DBD's
    window; ``allow(None)`` = no look at all). ``state`` is the latest look (EMPTY when not allowed or DBD is not in
    front), ``changes`` counts its changes (the card redraws on a new count). ``poll`` replaces the Windows look in
    tests."""

    def __init__(self, poll=None):
        self._poll = poll
        self.state = EMPTY
        self.changes = 0
        self._hwnd = None
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._thread = None
        self._failed = False

    @property
    def allowed(self) -> bool:
        return bool(self._hwnd)

    def allow(self, hwnd) -> None:
        """Looks may happen for DBD's window ``hwnd`` (None / 0 = stop looking, state empty at once)."""
        hwnd = int(hwnd) if hwnd else None
        if hwnd == self._hwnd:
            return
        self._hwnd = hwnd
        if hwnd is None:
            self._set(EMPTY)
            return
        if self._thread is None:
            self._thread = threading.Thread(target=self._run, daemon=True, name="inputs")
            self._thread.start()
        self._wake.set()

    def stop(self) -> None:
        self._hwnd = None
        self._stop.set()
        self._wake.set()

    def _set(self, st: InputState) -> None:
        if st != self.state:
            self.state = st
            self.changes += 1

    def look(self) -> None:
        """One look now (the thread's step; tests call it directly)."""
        hwnd = self._hwnd
        if not hwnd:
            self._set(EMPTY)
            return
        if self._poll is None:
            self._poll = Win32Poll() if IS_WIN else (lambda _h: None)
        st = self._poll(hwnd)
        self._set(EMPTY if st is None or not self._hwnd else st)

    def _run(self) -> None:
        while not self._stop.is_set():
            if not self._hwnd:
                self._set(EMPTY)
                self._wake.wait(IDLE_S)
                self._wake.clear()
                continue
            try:
                self.look()
            except Exception as e:                    # never what was pressed – only the kind of failure
                if not self._failed:
                    self._failed = True
                    log.warning("Eingaben: Abfrage fehlgeschlagen (%s)", type(e).__name__)
                self._set(EMPTY)
                self._stop.wait(IDLE_S)
                continue
            self._stop.wait(POLL_S)
