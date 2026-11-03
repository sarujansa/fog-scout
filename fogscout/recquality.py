"""1.29 (user: "Ich will OBS-Aufnahmen mit guter Qualität" – blurry/mushy, "einfach das Beste"): how good is OBS's
recording, why not, and what to change. Pure – the values come from Recorder._poll (obs_status), nothing here talks
to OBS. Recorder.apply_quality writes the plan made here, only on the user's click.

Measured: the bitrate of the recording on air (GetRecordStatus outputBytes / outputDuration, after MEASURE_AFTER_S)
→ bits per pixel and frame (bpp). H.264 needs about GOOD_BPP for a fast game like DBD to stay sharp, below
MUSHY_BPP it smears; HEVC/AV1 do the same with EFFICIENT × as many bits.

What a click can set (obs-websocket 5): the output size and frame rate (SetVideoSettings), and in OBS's simple
output mode the recording quality and encoder (SetProfileParameter, QUALITY_KEYS only); in the advanced mode the
rescale switch. The advanced mode's encoder settings (rate control, CQP, bitrate) live in OBS's recordEncoder.json –
no request sets them, so steps() tells the user where to click."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .i18n import _
from .obsrec import QUALITY_KEYS, encoder_label

MEASURE_AFTER_S = 20.0          # the first seconds of a file (header, keyframe) say little about its rate
GOOD_BPP = 0.08                 # H.264: ≈ 18 Mbit/s at 2560×1440@60 – sharp
MUSHY_BPP = 0.05                # below: smeared in motion (≈ 11 Mbit/s at 2560×1440@60)
EFFICIENT = 0.6                 # HEVC/AV1 need this share of H.264's bits
GOOD_FPS = 59.0                 # 60 (or 59.94) frames per second
TARGET_FPS = 60
SKIP_SHARE = 0.01               # more skipped frames than this: the encoder cannot keep up

SIMPLE_BEST = "HQ"              # simple mode: "Kaum unterscheidbare Qualität" (Stream/Small/HQ/Lossless)
SIMPLE_NVENC = "nvenc"          # simple mode's NVENC H.264 – only when an NVIDIA driver is installed

@dataclass
class Verdict:
    level: str = ""             # "" (nothing known) / ok / warn / err – the card's state colour
    words: str = ""             # one line for the card
    hints: list = field(default_factory=list)       # what is wrong, one sentence each
    fixable: bool = False       # a click can change something (plan() is not empty)
    mbps: float | None = None   # measured, None = not yet


def bitrate_mbps(nbytes, seconds) -> float | None:
    """Megabits per second of a file of ``nbytes`` after ``seconds`` – None before MEASURE_AFTER_S."""
    try:
        nbytes, seconds = float(nbytes or 0), float(seconds or 0)
    except (TypeError, ValueError):
        return None
    if seconds < MEASURE_AFTER_S or nbytes <= 0:
        return None
    return nbytes * 8 / seconds / 1e6


def bpp(mbps, width, height, fps) -> float | None:
    """Bits per pixel and frame."""
    if not mbps or not width or not height or not fps:
        return None
    return mbps * 1e6 / (float(width) * float(height) * float(fps))


def efficient(encoder: str) -> bool:
    """HEVC/AV1 (encoder_label of either the raw name or the label)."""
    e = encoder or ""
    return "HEVC" in e or "AV1" in e or "hevc" in e.lower() or "av1" in e.lower()


def _cpu(d) -> bool:
    return "(CPU)" in (d.get("encoder") or "")


def _simple(d) -> bool:
    return (d.get("mode") or "").lower() == "simple"


def _scaled(d) -> bool:
    bw, bh, w, h = (int(d.get(k) or 0) for k in ("base_width", "base_height", "width", "height"))
    return bool(bw and bh and w and h and (w < bw or h < bh))


def _rescaled(d) -> bool:
    return not _simple(d) and str(d.get("rescale") or "").lower() == "true"


def _slow_fps(d) -> bool:
    fps = float(d.get("fps") or 0)
    return 0 < fps < GOOD_FPS


def _skips(d) -> bool:
    total = int(d.get("output_total") or 0)
    return total > 0 and int(d.get("output_skipped") or 0) / total > SKIP_SHARE


def nvidia_present() -> bool:
    """An NVIDIA driver is installed (nvml.dll in System32 – the file is only looked at, never loaded here)."""
    root = os.environ.get("SystemRoot", r"C:\Windows")
    return os.name == "nt" and os.path.isfile(os.path.join(root, "System32", "nvml.dll"))


def verdict(d: dict) -> Verdict:
    """The card's line about quality from an obs_status dict (Recorder._poll)."""
    v = Verdict()
    if not d or not d.get("connected"):
        return v
    hints = []
    quality = (d.get("quality") or "").lower()
    if _simple(d) and quality in ("stream", "small"):
        hints.append(_("OBS nimmt mit der Qualität „wie Stream“ bzw. „klein“ auf – „Kaum unterscheidbare Qualität“ "
                       "ist viel schärfer."))
    if _scaled(d) or _rescaled(d):
        hints.append(_("OBS skaliert das Bild herunter ({base} → {out}) – das macht es weich.",
                       base=f"{d.get('base_width')}×{d.get('base_height')}",
                       out=f"{d.get('width')}×{d.get('height')}"))
    if _slow_fps(d):
        hints.append(_("OBS nimmt mit {fps} Bildern pro Sekunde auf – 60 wirken in Bewegung viel klarer.",
                       fps=f"{float(d.get('fps')):g}"))
    if _cpu(d) and _skips(d):
        hints.append(_("Der CPU-Encoder kommt nicht mit (übersprungene Bilder) – den Encoder der Grafikkarte nehmen."))
    mbps = bitrate_mbps(d.get("bytes"), d.get("seconds")) if d.get("recording") else None
    v.mbps = mbps
    size = ""
    if d.get("width") and d.get("height"):
        size = f"{d['width']}×{d['height']}" + (f"@{float(d['fps']):g}" if d.get("fps") else "")
    level = "ok" if not hints else "warn"
    if mbps is not None:
        b = bpp(mbps, d.get("width"), d.get("height"), d.get("fps"))
        f = EFFICIENT if efficient(d.get("encoder") or "") else 1.0
        if b is not None and b < MUSHY_BPP * f:
            level, word = "err", _("matschig")
            hints.append(_("Die Bitrate ist für dieses Bild zu niedrig – die Ratensteuerung des Encoders auf "
                           "CQP 18 stellen (siehe Anleitung)."))
        elif b is not None and b < GOOD_BPP * f:
            level, word = ("warn", _("knapp"))
            hints.append(_("Die Bitrate reicht knapp – mit CQP 18 bleibt das Bild auch in schnellen Szenen scharf."))
        else:
            word = _("gut") if not hints else _("Einstellungen prüfen")
        v.words = _("Qualität: {word} – {mbps} Mbit/s bei {size}", word=word, mbps=f"{mbps:.0f}",
                    size=size or "?")
    elif hints:
        v.words = _("Qualität: Einstellungen prüfen")
    else:
        v.words = _("Qualität: gemessen wird während einer Aufnahme")
        level = ""
    v.level, v.hints = level, hints
    v.fixable = bool(plan(d))
    return v


def plan(d: dict, nvidia: bool = False) -> dict:
    """What a click would change: {"video": {SetVideoSettings fields} or absent, "profile": [(cat, name, value)]}.
    Empty = nothing a request can improve (the advanced mode's encoder settings are steps() for the user)."""
    if not d or not d.get("connected"):
        return {}
    out = {}
    video = {}
    if _scaled(d):
        video.update(outputWidth=int(d["base_width"]), outputHeight=int(d["base_height"]))
    if _slow_fps(d):
        video.update(fpsNumerator=TARGET_FPS, fpsDenominator=1)
    if video:
        out["video"] = video
    prof = []
    if _simple(d):
        if (d.get("quality") or "").lower() in ("stream", "small"):
            prof.append(("SimpleOutput", "RecQuality", SIMPLE_BEST))
        if nvidia and (d.get("encoder_raw") or "").lower().startswith("x264"):
            prof.append(("SimpleOutput", "RecEncoder", SIMPLE_NVENC))
    elif _rescaled(d):
        prof.append(("AdvOut", "RecRescale", "false"))
    prof = [p for p in prof if p[:2] in QUALITY_KEYS]           # never more than a click may write
    if prof:
        out["profile"] = prof
    return out


def plan_lines(p: dict) -> list:
    """The plan in words for the question before writing."""
    lines = []
    v = p.get("video") or {}
    if "outputWidth" in v:
        lines.append(_("Ausgabeauflösung = Basisauflösung ({size})", size=f"{v['outputWidth']}×{v['outputHeight']}"))
    if "fpsNumerator" in v:
        lines.append(_("Bildrate 60"))
    for cat, name, value in p.get("profile") or ():
        if name == "RecQuality":
            lines.append(_("Aufnahmequalität „Kaum unterscheidbare Qualität“"))
        elif name == "RecEncoder":
            lines.append(_("Encoder {name}", name=encoder_label(value)))
        elif name == "RecRescale":
            lines.append(_("Aufnahme nicht mehr herunterskalieren"))
    return lines


def steps(mode: str, encoder: str = "") -> list:
    """Click-by-click in OBS for what no request can set."""
    if (mode or "").lower() == "simple":
        return [_("OBS → Einstellungen → Ausgabe (Modus „Einfach“) → Aufnahme:"),
                _("Aufnahmequalität: „Kaum unterscheidbare Qualität, große Dateigröße“"),
                _("Encoder: Hardware (NVENC/AMD/QSV), wenn vorhanden"),
                _("Aufnahmeformat: MKV oder Hybrid-MP4"),
                _("Video: Ausgabeauflösung = Basisauflösung, Bildrate 60")]
    cpu = "(CPU)" in encoder_label(encoder) or "x264" in (encoder or "").lower()
    rows = [_("OBS → Einstellungen → Ausgabe (Modus „Erweitert“) → Reiter „Aufnahme“:"),
            _("Video-Encoder: NVIDIA NVENC H.264 oder HEVC (nicht „Stream-Encoder verwenden“)"),
            _("Ausgabe neu skalieren: aus")]
    if cpu:
        rows += [_("x264: Frequenzsteuerung CRF, Wert 18, Voreinstellung veryfast")]
    else:
        rows += [_("Frequenzsteuerung: CQP, CQ-Level 18 (HEVC 20)"),
                 _("Voreinstellung: P5: Langsam (gute Qualität), Tuning: Hohe Qualität, Mehrfachdurchlauf: zwei "
                   "Durchläufe (Viertelauflösung)"),
                 _("Profil: high (HEVC: main), Keyframe-Intervall: 2 s")]
    rows += [_("Aufnahmeformat: MKV oder Hybrid-MP4"),
             _("Video: Ausgabeauflösung = Basisauflösung, Bildrate 60"),
             _("Danach eine kurze Runde aufnehmen – die Karte zeigt die neue Bitrate.")]
    return rows
