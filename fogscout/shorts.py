"""1.20 (user: "Hochformat für Shorts" – max. 3 min, Vorlagen „Unscharfer Hintergrund“ (Standard) und „Zuschnitt
9:16“, Titel oben + Untertitel unten): the vertical short as data, its texts as pictures and the ffmpeg filters that
lay the finished cut onto a 1080×1920 canvas. Pure: no Qt, the texts are PIL images (the preview pastes the same
pictures the export overlays).

Times of subtitles are seconds of the *finished* clip (output time) – a subtitle belongs to what is seen, not to a
moment of the recording."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

W, H = 1080, 1920                 # the canvas of a short
MAX_S = 180.0                     # YouTube Shorts take up to 3 min (since Oct. 2024)
MAX_FPS = 60.0
LAYOUTS = ("blur", "crop")        # "Unscharfer Hintergrund" (whole game picture in the middle) / "Zuschnitt 9:16"
TITLE_SIZES = (0.035, 0.045, 0.06)  # share of the canvas height (small / medium / large)
SUB_SIZE = 0.042
TITLE_Y = 0.17                    # centre of the title, share of the canvas height (upper band)
SUB_Y = 0.80                      # centre of a subtitle (lower band)
TEXT_W = 0.88                     # a line wraps at this share of the width
STROKE = 0.10                     # outline, share of the font size
BLUR = 24                         # boxblur radius of the background (canvas pixels)
DIM = -0.18                       # its brightness (eq)
MAX_TEXT = 200
MAX_SUBS = 200
SUB_DEFAULT_S = 2.0


@dataclass
class Sub:
    t0: float                     # seconds of the finished clip
    t1: float
    text: str


@dataclass
class ShortSpec:
    layout: str = "blur"
    title: str = ""
    title_size: int = 1           # index into TITLE_SIZES
    subs: list = field(default_factory=list)

    def copy(self) -> "ShortSpec":
        return ShortSpec(self.layout, self.title, self.title_size, [Sub(s.t0, s.t1, s.text) for s in self.subs])

    def empty(self) -> bool:
        return self.layout == "blur" and not self.title and not self.subs and self.title_size == 1


def _finite(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def clean_text(t) -> str:
    """One line of at most MAX_TEXT characters (the picture wraps it)."""
    return " ".join(str(t).split())[:MAX_TEXT] if t else ""


def to_dict(spec: ShortSpec | None) -> dict | None:
    if spec is None or spec.empty():
        return None
    return {"layout": spec.layout, "title": spec.title, "title_size": int(spec.title_size),
            "subs": [[round(s.t0, 3), round(s.t1, 3), s.text] for s in spec.subs]}


def from_dict(d) -> ShortSpec | None:
    """Field by field; anything broken drops out (project.validate's rule)."""
    if not isinstance(d, dict):
        return None
    layout = d.get("layout") if d.get("layout") in LAYOUTS else "blur"
    size = d.get("title_size")
    size = int(size) if isinstance(size, int) and 0 <= size < len(TITLE_SIZES) else 1
    subs = []
    for raw in list(d.get("subs") or [])[:MAX_SUBS] if isinstance(d.get("subs"), list) else []:
        if not isinstance(raw, (list, tuple)) or len(raw) < 3:
            continue
        a, b = _finite(raw[0]), _finite(raw[1])
        text = clean_text(raw[2])
        if a is None or b is None or not text or b - a < 0.1 or a < 0:
            continue
        subs.append(Sub(a, min(b, a + MAX_S), text))
    spec = ShortSpec(layout, clean_text(d.get("title")), size, sorted(subs, key=lambda s: s.t0))
    return None if spec.empty() else spec


def fps(src_fps: float) -> float:
    return min(MAX_FPS, src_fps or 30.0)


# ---- texts
def text_picture(text: str, size_px: int, width_px: int):
    """The text as an RGBA picture: Inter Bold, white with a dark outline, wrapped to ``width_px``, centred."""
    from PIL import Image, ImageDraw

    from .skin import inter
    font = inter("Bold", max(8, int(size_px)))
    stroke = max(2, int(size_px * STROKE))
    words, lines, line = text.split(), [], ""
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    for w in words:
        cand = f"{line} {w}".strip()
        if line and probe.textlength(cand, font=font) > width_px:
            lines.append(line)
            line = w
        else:
            line = cand
    if line:
        lines.append(line)
    if not lines:
        return None
    asc, desc = font.getmetrics()
    lh = asc + desc
    widths = [int(probe.textlength(ln, font=font)) for ln in lines]
    pw, ph = max(widths) + 2 * stroke + 4, lh * len(lines) + 2 * stroke + 4
    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (ln, lw) in enumerate(zip(lines, widths)):
        d.text(((pw - lw) / 2, stroke + 2 + i * lh), ln, font=font, fill=(255, 255, 255, 255),
               stroke_width=stroke, stroke_fill=(10, 10, 14, 235))
    return img


def texts(spec: ShortSpec | None, w: int = W, h: int = H) -> list:
    """[(picture, x, y, t0, t1)] – the title (t0/t1 None = always) and the subtitles on a w×h canvas."""
    out = []
    if spec is None:
        return out
    width = int(w * TEXT_W)
    if spec.title:
        pic = text_picture(spec.title, h * TITLE_SIZES[spec.title_size], width)
        if pic is not None:
            out.append((pic, (w - pic.width) // 2, max(0, int(h * TITLE_Y - pic.height / 2)), None, None))
    for s in spec.subs:
        pic = text_picture(s.text, h * SUB_SIZE, width)
        if pic is not None:
            out.append((pic, (w - pic.width) // 2, min(h - pic.height, int(h * SUB_Y - pic.height / 2)), s.t0, s.t1))
    return out


def paste_texts(img, spec: ShortSpec | None, t: float):
    """The preview: ``img`` (the composed short at any size) with the texts shown at output second ``t``."""
    if spec is None or img is None:
        return img
    shown = [x for x in texts(spec, img.width, img.height) if x[3] is None or x[3] <= t < x[4]]
    if not shown:
        return img
    out = img.convert("RGBA")
    for pic, x, y, _a, _b in shown:
        out.alpha_composite(pic, (int(x), int(y)))
    return out.convert("RGB")


# ---- the canvas
def canvas_filters(layout: str, w: int = W, h: int = H, label: str = "s") -> str:
    """A filter chain (one input, one output) that lays the cut onto a w×h canvas: "blur" = the whole picture,
    full width, in the middle over a blurred and darkened copy of itself; "crop" = the middle of the picture
    filling the canvas (the editor's own 9:16 crop, when set, comes before this and fits exactly)."""
    fill = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    if layout == "crop":
        return f"{fill},setsar=1"
    blur = max(2, int(BLUR * h / H))
    return (f"split=2[{label}bg][{label}fg];[{label}bg]{fill},boxblur={blur}:2,eq=brightness={DIM}[{label}b];"
            f"[{label}fg]scale={w}:-2[{label}f];[{label}b][{label}f]overlay=(W-w)/2:(H-h)/2,setsar=1")
