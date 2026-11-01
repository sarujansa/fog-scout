"""Video encoders for the clip editor's exports (1.15, audit of the video system: every re-encoded clip went
through libx264 "veryfast" CRF 18 on the CPU – no HEVC, no graphics-card encoder, no quality or size choice).

Pure: which ffmpeg encoder a choice means and the arguments it takes (``Encoding``), plus two small ffmpeg calls –
``available()`` reads ``ffmpeg -encoders`` once, ``works()`` lets a hardware encoder encode three black frames from
``lavfi`` (no file, no network) so only encoders the driver really provides are offered: ffmpeg's Windows build
lists NVENC, AMF and Quick Sync whether or not the card is there. ``detect()`` keeps the result per ffmpeg binary;
``detect_async()`` runs it off the GUI thread. Only the bundled ffmpeg (obsrec.ffmpeg_exe), only our own clips.

Why not OBS for the export: OBS encodes what it captures, the clips are cut by ffmpeg from the finished files;
imageio-ffmpeg's Windows ffmpeg (7.0.2) carries h264_nvenc/hevc_nvenc, h264_amf/hevc_amf, h264_qsv/hevc_qsv and
libx265 – the Linux build (CI) only libx264/libx265, so nothing here assumes a hardware encoder.
"""
from __future__ import annotations

import re
import subprocess
import threading
from dataclasses import dataclass, replace

from .i18n import N_

CODECS = ("h264", "hevc")
CODEC_LABELS = {"h264": "H.264", "hevc": "HEVC (H.265)"}
QUALITIES = ("fast", "balanced", "high")
QUALITY_LABELS = {"fast": N_("Schnell"), "balanced": N_("Ausgewogen"), "high": N_("Hoch")}
HEIGHTS = (0, 1440, 1080, 720)               # 0 = the recording's own size
HW = ("nvenc", "amf", "qsv")                 # graphics-card encoders, in the order "auto" tries them
HW_LABELS = {"": N_("CPU (x264/x265)"), "auto": N_("Automatisch"), "nvenc": "NVIDIA NVENC", "amf": "AMD AMF",
             "qsv": "Intel Quick Sync"}
ENCODERS = {("h264", ""): "libx264", ("hevc", ""): "libx265",
            ("h264", "nvenc"): "h264_nvenc", ("hevc", "nvenc"): "hevc_nvenc",
            ("h264", "amf"): "h264_amf", ("hevc", "amf"): "hevc_amf",
            ("h264", "qsv"): "h264_qsv", ("hevc", "qsv"): "hevc_qsv"}
# rate control per encoder family and quality: (preset, quality number). CPU: x264 CRF (18 = today's "Genau";
# x265 about +4 for the same look). NVENC: p1–p7 presets with "-cq" (constant quality, 0 kbit/s target). AMF: the
# driver's quality presets with constant QP. Quick Sync: ICQ through -global_quality.
RATES = {
    "libx264": {"fast": ("veryfast", 23), "balanced": ("veryfast", 18), "high": ("medium", 17)},
    "libx265": {"fast": ("veryfast", 27), "balanced": ("veryfast", 22), "high": ("medium", 20)},
    "nvenc": {"fast": ("p3", 28), "balanced": ("p5", 23), "high": ("p6", 20)},
    "amf": {"fast": ("speed", 26), "balanced": ("balanced", 22), "high": ("quality", 19)},
    "qsv": {"fast": ("veryfast", 28), "balanced": ("medium", 23), "high": ("slow", 20)},
}
SELFTEST_TIMEOUT = 20.0                      # s: a hardware encoder without its card fails within a second
SELFTEST_INPUT = "color=c=black:s=320x180:r=30:d=0.2"
_ENCODER_LINE = re.compile(r"^\s*V[A-Z.]{5}\s+([a-z]\w*)", re.M)      # "V....D h264_nvenc   NVIDIA NVENC …"


@dataclass(frozen=True)
class Encoding:
    """What the user picked for a re-encoded clip. ``hw`` "" = CPU, "auto" = the first graphics-card encoder that
    works, else one of HW. ``resolve()`` turns a wish into what this PC can do."""
    codec: str = "h264"
    quality: str = "balanced"
    height: int = 0
    hw: str = ""

    @property
    def family(self) -> str:
        return self.hw if self.hw in HW else self.encoder

    @property
    def encoder(self) -> str:
        return ENCODERS.get((self.codec, self.hw if self.hw in HW else ""), "libx264")

    def resolve(self, avail: dict | None) -> "Encoding":
        """The encoding this PC can do: "auto" → the first working hardware encoder (none: CPU), a hardware encoder
        that does not work → CPU, HEVC without libx265 → H.264. ``avail`` from detect() (None = nothing known: CPU)."""
        avail = avail or {}
        codec = self.codec if self.codec in CODECS else "h264"
        quality = self.quality if self.quality in QUALITIES else "balanced"
        height = int(self.height) if int(self.height or 0) in HEIGHTS else 0
        hw = self.hw
        if hw == "auto":
            hw = next((h for h in HW if avail.get(ENCODERS[(codec, h)])), "")
        elif hw not in HW or not avail.get(ENCODERS[(codec, hw)]):
            hw = ""
        if not hw and codec == "hevc" and avail and not avail.get("libx265", True):
            codec = "h264"
        return Encoding(codec, quality, height, hw)

    def target_height(self, src_h: int) -> int:
        """The picture height to encode (0 = as it is): never larger than the recording, always even."""
        h = int(self.height or 0)
        if h <= 0 or (src_h and h >= src_h):
            return 0
        return h // 2 * 2

    def video_args(self, kbps: int | None = None) -> list:
        """ffmpeg's video arguments: constant quality by ``quality``, or ``kbps`` for a size-fitted clip (the Discord
        mode, every encoder takes -b:v/-maxrate/-bufsize). The CPU default equals the arguments of 1.5.1–1.14."""
        enc = self.encoder
        fam = self.family
        preset, q = RATES[fam][self.quality if self.quality in QUALITIES else "balanced"]
        args = ["-c:v", enc]
        if fam == "libx264":
            args += ["-preset", preset] + (["-crf", str(q)] if kbps is None else [])
        elif fam == "libx265":
            args += ["-preset", preset] + (["-crf", str(q)] if kbps is None else []) + ["-tag:v", "hvc1"]
        elif fam == "nvenc":
            args += ["-preset", preset, "-tune", "hq", "-rc", "vbr"] + (
                ["-cq", str(q), "-b:v", "0"] if kbps is None else [])
        elif fam == "amf":
            args += ["-quality", preset] + (["-rc", "cqp", "-qp_i", str(q), "-qp_p", str(q)] if kbps is None
                                             else ["-rc", "vbr_peak"])
        elif fam == "qsv":
            args += ["-preset", preset] + (["-global_quality", str(q)] if kbps is None else [])
        if kbps is not None:
            args += ["-b:v", f"{int(kbps)}k", "-maxrate", f"{int(kbps * 1.1)}k", "-bufsize", f"{int(kbps) * 2}k"]
        args += ["-pix_fmt", "nv12" if fam == "qsv" else "yuv420p"]
        if self.codec == "hevc" and fam != "libx265":
            args += ["-tag:v", "hvc1"]                   # HEVC in MP4 that Windows and Apple players open
        return args

    def summary(self, translate=lambda s: s) -> str:
        """"H.264 · NVIDIA NVENC · Ausgewogen · 1080p" for the save card's line."""
        bits = [CODEC_LABELS.get(self.codec, self.codec), translate(HW_LABELS.get(self.hw if self.hw in HW else "", "")),
                translate(QUALITY_LABELS.get(self.quality, self.quality))]
        if self.height:
            bits.append(f"{int(self.height)}p")
        return " · ".join(b for b in bits if b)


def parse_encoders(text: str) -> set:
    """The video encoder names in ``ffmpeg -encoders`` output."""
    return set(_ENCODER_LINE.findall(text or ""))


def _run(args: list, timeout: float, run=None) -> tuple[int, str]:
    if run is not None:
        return run(args)
    try:
        p = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)
    return p.returncode, (p.stdout or b"").decode("utf-8", "replace")


def available(ffmpeg: str, run=None) -> set:
    """The video encoders this ffmpeg was built with (listed, not yet proven to work)."""
    rc, out = _run([ffmpeg, "-hide_banner", "-encoders"], 30, run)
    return parse_encoders(out) if rc == 0 else set()


def works(ffmpeg: str, encoder: str, run=None) -> bool:
    """Three black frames through ``encoder`` to nowhere – a hardware encoder without its card/driver fails here
    (e.g. "Cannot load nvcuda.dll", "No capable devices found") and is then not offered."""
    pix = "nv12" if encoder.endswith("_qsv") else "yuv420p"
    rc, _out = _run([ffmpeg, "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", SELFTEST_INPUT, "-frames:v",
                     "3", "-c:v", encoder, "-pix_fmt", pix, "-f", "null", "-"], SELFTEST_TIMEOUT, run)
    return rc == 0


_KNOWN = {}                                  # ffmpeg path -> {encoder name: works}
_LOCK = threading.Lock()


def detect(ffmpeg: str | None, run=None, force: bool = False) -> dict:
    """{encoder: True/False} for every encoder in ENCODERS: the CPU ones as listed, the hardware ones only when
    works() says so. Kept per ffmpeg binary (the self-tests take a moment each); {} without ffmpeg."""
    if not ffmpeg:
        return {}
    with _LOCK:
        if not force and ffmpeg in _KNOWN:
            return dict(_KNOWN[ffmpeg])
    listed = available(ffmpeg, run)
    out = {}
    for (codec, hw), name in ENCODERS.items():
        if name not in listed:
            out[name] = False
        elif hw:
            out[name] = works(ffmpeg, name, run)
        else:
            out[name] = True
    with _LOCK:
        _KNOWN[ffmpeg] = dict(out)
    return out


def known(ffmpeg: str | None) -> dict | None:
    """What detect() found so far for ``ffmpeg`` (None = not yet run)."""
    with _LOCK:
        return dict(_KNOWN[ffmpeg]) if ffmpeg in _KNOWN else None


def detect_async(ffmpeg: str | None, done, run=None):
    """detect() in a thread, ``done(avail)`` from that thread (callers hand it to their own queue)."""
    def work():
        try:
            done(detect(ffmpeg, run))
        except Exception:                                  # never a dead callback: the editor keeps the CPU
            done({})
    threading.Thread(target=work, name="encoder-detect", daemon=True).start()


def forget():
    """Tests: drop what detect() kept."""
    with _LOCK:
        _KNOWN.clear()


def hw_choices(avail: dict | None, codec: str = "h264") -> list:
    """The encoder choices to offer for ``codec``: [("", CPU), ("nvenc", …) …] – hardware only when it works."""
    out = [("", HW_LABELS[""])]
    for h in HW:
        if (avail or {}).get(ENCODERS[(codec if codec in CODECS else "h264", h)]):
            out.append((h, HW_LABELS[h]))
    return out


def from_settings(settings) -> Encoding:
    """The remembered export choice (settings clip_codec / clip_quality / clip_height / clip_hw)."""
    try:
        height = int(settings.get("clip_height", 0) or 0)
    except (TypeError, ValueError):
        height = 0
    return replace(Encoding(), codec=str(settings.get("clip_codec", "h264") or "h264"),
                   quality=str(settings.get("clip_quality", "balanced") or "balanced"), height=height,
                   hw=str(settings.get("clip_hw", "auto") if settings.get("clip_hw", "auto") is not None else "auto"))
