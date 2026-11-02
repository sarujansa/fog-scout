"""1.21 (user: "eigene Tonspur" – eine Spur A2, Spielton automatisch leiser unter der Musik mit Regler, Ausblenden am
Ende): music or commentary from the user's own files under the game sound. Pure: the track as data and the ffmpeg
filters that lay it under a cut – the export and the preview's sound use the same chain.

Times: ``at`` = second of the *finished* clip where an audio clip starts (output time, like the short's
subtitles); ``start``/``end`` = the part of the file it plays. Clips on the track never overlap."""
from __future__ import annotations

import math
import os
from dataclasses import dataclass, field

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".opus", ".flac", ".wma", ".mp4", ".mkv", ".mov", ".webm")
DUCKS = {                      # sidechaincompress settings: the game sound gets quieter while the music plays
    "off": None,
    "light": (0.10, 3.0),
    "medium": (0.05, 6.0),
    "strong": (0.02, 12.0),
}
DUCK_ORDER = ("off", "light", "medium", "strong")
FADE_MAX = 5.0
VOL_MAX = 2.0                  # 200 %
MAX_CLIPS = 50
MIN_LEN = 0.1
RATE = 48000


@dataclass
class AudioClip:
    path: str
    at: float                  # output second where it starts
    start: float               # second of the file
    end: float
    volume: float = 1.0

    @property
    def length(self) -> float:
        return max(0.0, self.end - self.start)


@dataclass
class MusicSpec:
    clips: list = field(default_factory=list)
    game_vol: float = 1.0
    music_vol: float = 0.8
    duck: str = "medium"
    fade_in: float = 0.0
    fade_out: float = 2.0

    def copy(self) -> "MusicSpec":
        return MusicSpec([AudioClip(c.path, c.at, c.start, c.end, c.volume) for c in self.clips], self.game_vol,
                         self.music_vol, self.duck, self.fade_in, self.fade_out)

    def empty(self) -> bool:
        return not self.clips and self == MusicSpec()


def _f(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def _clamp(v, lo, hi, default):
    f = _f(v)
    return default if f is None else min(max(f, lo), hi)


def is_audio(path: str) -> bool:
    return os.path.splitext(str(path or ""))[1].lower() in AUDIO_EXTS


def clean(clips) -> list:
    """Sorted by ``at``; a clip that would overlap the one before starts where that one ends."""
    out = []
    for c in sorted(clips, key=lambda c: c.at):
        if c.length < MIN_LEN:
            continue
        at = max(c.at, out[-1].at + out[-1].length) if out else max(0.0, c.at)
        out.append(AudioClip(c.path, round(at, 3), round(c.start, 3), round(c.end, 3), c.volume))
    return out[:MAX_CLIPS]


def to_dict(spec: MusicSpec | None) -> dict | None:
    if spec is None or spec.empty():
        return None
    return {"clips": [[c.path, round(c.at, 3), round(c.start, 3), round(c.end, 3), round(c.volume, 3)]
                      for c in spec.clips],
            "game_vol": round(spec.game_vol, 3), "music_vol": round(spec.music_vol, 3), "duck": spec.duck,
            "fade_in": round(spec.fade_in, 3), "fade_out": round(spec.fade_out, 3)}


def from_dict(d) -> MusicSpec | None:
    """Field by field; a broken clip drops out (project.validate's rule)."""
    if not isinstance(d, dict):
        return None
    clips = []
    for raw in list(d.get("clips") or [])[:MAX_CLIPS] if isinstance(d.get("clips"), list) else []:
        if not isinstance(raw, (list, tuple)) or len(raw) < 4 or not isinstance(raw[0], str) or not raw[0]:
            continue
        at, s, e = _f(raw[1]), _f(raw[2]), _f(raw[3])
        if at is None or s is None or e is None or at < 0 or s < 0 or e - s < MIN_LEN:
            continue
        vol = _clamp(raw[4] if len(raw) > 4 else 1.0, 0.0, VOL_MAX, 1.0)
        clips.append(AudioClip(raw[0], at, s, e, vol))
    spec = MusicSpec(clean(clips), _clamp(d.get("game_vol"), 0.0, VOL_MAX, 1.0),
                     _clamp(d.get("music_vol"), 0.0, VOL_MAX, 0.8),
                     d.get("duck") if d.get("duck") in DUCKS else "medium",
                     _clamp(d.get("fade_in"), 0.0, FADE_MAX, 0.0), _clamp(d.get("fade_out"), 0.0, FADE_MAX, 2.0))
    return None if spec.empty() else spec


def file_seconds(path: str, ffmpeg: str | None = None) -> float:
    """Length of an audio (or video) file's sound; 0 when it has none or cannot be read."""
    from . import clipedit
    info = clipedit.probe(path, ffmpeg)
    return info.duration if info.duration > 0 and info.audio_tracks > 0 else 0.0


# ---- the filters
def window_inputs(spec: MusicSpec | None, w0: float, wl: float) -> list:
    """[(path, file second to seek, seconds to read, delay in the window)] of the clips that sound in the window
    [w0, w0 + wl] of the finished clip (the export: 0..total; the preview: one stretch). Missing files drop out."""
    out = []
    if spec is None:
        return out
    for c in spec.clips:
        a, b = max(c.at, w0), min(c.at + c.length, w0 + wl)
        if b - a < 0.01 or not os.path.isfile(c.path):
            continue
        out.append((c, c.start + (a - c.at), b - a, a - w0))
    return out


def chain(spec: MusicSpec, w0: float, wl: float, total: float, first_input: int, game: str | None,
          tag: str = "") -> tuple[str, str]:
    """(filters, output label): the clips of ``window_inputs`` (ffmpeg inputs ``first_input``…, each already
    seeked) laid at their place, music volume with the fades of the whole cut (in–out over ``total``), and – when
    ``game`` is a label – the game sound at its volume, ducked under the music, both mixed. No clip in the window:
    the game sound at its volume only."""
    placed = window_inputs(spec, w0, wl)
    fmt = f"aresample={RATE},aformat=sample_fmts=fltp:channel_layouts=stereo"
    parts = []
    gvol = f"volume={spec.game_vol:.3f}"
    if not placed:
        if game is None:
            return "", ""
        parts.append(f"{game}{fmt},{gvol}[mx{tag}]")
        return ";".join(parts), f"[mx{tag}]"
    for k, (c, _ss, _t, delay) in enumerate(placed):
        parts.append(f"[{first_input + k}:a]{fmt},volume={c.volume:.3f},adelay={int(round(delay * 1000))}:all=1"
                     f"[mc{tag}{k}]")
    if len(placed) > 1:
        parts.append("".join(f"[mc{tag}{k}]" for k in range(len(placed)))
                     + f"amix=inputs={len(placed)}:normalize=0:duration=longest[mm{tag}]")
        mm = f"[mm{tag}]"
    else:
        mm = f"[mc{tag}0]"
    fi, fo = spec.fade_in, spec.fade_out
    env = [f"{spec.music_vol:.3f}"]
    if fi > 0:
        env.append(f"min(1,(t+{w0:.3f})/{fi:.3f})")
    if fo > 0:
        env.append(f"min(1,max(0,({total:.3f}-(t+{w0:.3f}))/{fo:.3f}))")
    parts.append(f"{mm}apad,atrim=duration={wl:.3f},volume='{'*'.join(env)}':eval=frame[mu{tag}]")
    if game is None:
        return ";".join(parts), f"[mu{tag}]"
    parts.append(f"{game}{fmt},{gvol}[g{tag}]")
    duck = DUCKS.get(spec.duck)
    if duck:
        thr, ratio = duck
        parts.append(f"[mu{tag}]asplit=2[ma{tag}][ms{tag}]")
        parts.append(f"[g{tag}][ms{tag}]sidechaincompress=threshold={thr}:ratio={ratio:g}:attack=20:release=400"
                     f"[gd{tag}]")
        parts.append(f"[gd{tag}][ma{tag}]amix=inputs=2:normalize=0:duration=first[mx{tag}]")
    else:
        parts.append(f"[g{tag}][mu{tag}]amix=inputs=2:normalize=0:duration=first[mx{tag}]")
    return ";".join(parts), f"[mx{tag}]"


def input_args(spec: MusicSpec | None, w0: float, wl: float) -> list:
    """The ffmpeg arguments that read the clips of ``window_inputs`` (only the part each needs)."""
    args = []
    for c, ss, t, _delay in window_inputs(spec, w0, wl):
        args += ["-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", c.path]
    return args
