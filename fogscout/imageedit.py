"""Screenshot editing (1.12, user: "Bearbeitungstool top machen" – crop & rotate, draw & text, censor & colour,
share): one ``ImageEdit`` describes every change, ``render`` applies it to the untouched original, so each step can
be undone and nothing is ever written over the source file (Steam's screenshots stay as they are). Pure PIL.

Coordinates: crop box, censor boxes and drawings are fractions of the turned picture (after rotate/flip, before the
crop) – they stay on what they mark when the crop changes; turning the picture turns them along (``turned``).
Order: turn → colour → censor → drawings → crop.
"""
from __future__ import annotations

import copy
import os
import re
from dataclasses import dataclass, field

from PIL import Image, ImageEnhance, ImageFilter

from . import annotate

CENSOR_STYLES = ("pixel", "blur", "black")
ASPECTS = (("free", None), ("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:3", 4 / 3), ("4:5", 4 / 5))
FORMATS = ("png", "jpg")
JPG_QUALITY = 92
PNG_LEVEL = 3                   # zlib level: 6 (Pillow's default) took 4× as long on a 3440×1440 picture
ADJUST_RANGE = (0.2, 2.0)       # brightness/contrast/saturation factors offered (1 = unchanged)


@dataclass
class ImageEdit:
    rotate: int = 0                              # quarter turns clockwise (0–3)
    flip_h: bool = False
    flip_v: bool = False
    crop: tuple | None = None                    # (x, y, w, h) fractions of the turned picture
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    censor: list = field(default_factory=list)   # [(x, y, w, h)] fractions of the turned picture
    censor_style: str = "pixel"
    shapes: list = field(default_factory=list)   # [annotate.Shape] on the turned picture

    def copy(self) -> "ImageEdit":
        return copy.deepcopy(self)

    def changed(self) -> bool:
        return self != ImageEdit()


def clamp_box(box, min_size: float = 0.01) -> tuple:
    """A fraction box kept inside the picture and at least ``min_size`` wide and tall."""
    x, y, w, h = (float(v) for v in box)
    if w < 0:
        x, w = x + w, -w
    if h < 0:
        y, h = y + h, -h
    w, h = max(min_size, min(1.0, w)), max(min_size, min(1.0, h))
    return max(0.0, min(1.0 - w, x)), max(0.0, min(1.0 - h, y)), w, h


def aspect_box(box, ratio: float | None, size: tuple) -> tuple:
    """``box`` (fractions) shrunk around its centre to ``ratio`` (width/height in pixels of a picture ``size``)."""
    x, y, w, h = clamp_box(box)
    if not ratio:
        return x, y, w, h
    pw, ph = size
    cur = (w * pw) / max(1e-9, h * ph)
    if cur > ratio:                              # too wide: narrower
        nw = h * ph * ratio / pw
        x, w = x + (w - nw) / 2, nw
    else:
        nh = w * pw / ratio / ph
        y, h = y + (h - nh) / 2, nh
    return clamp_box((x, y, w, h), 0.001)


def _turn_point(x: float, y: float, quarters: int) -> tuple:
    for _i in range(quarters % 4):                # one quarter clockwise: (x, y) -> (1 - y, x)
        x, y = 1.0 - y, x
    return x, y


def _turn_box(box, quarters: int) -> tuple:
    x, y, w, h = box
    a = _turn_point(x, y, quarters)
    b = _turn_point(x + w, y + h, quarters)
    return min(a[0], b[0]), min(a[1], b[1]), abs(b[0] - a[0]), abs(b[1] - a[1])


def _flip_point(x: float, y: float, horizontal: bool) -> tuple:
    return (1.0 - x, y) if horizontal else (x, 1.0 - y)


def _flip_box(box, horizontal: bool) -> tuple:
    x, y, w, h = box
    return (1.0 - x - w, y, w, h) if horizontal else (x, 1.0 - y - h, w, h)


def turned(edit: ImageEdit, quarters: int, size: tuple = (1, 1)) -> ImageEdit:
    """``edit`` with the picture (now ``size`` = turned width, height) turned ``quarters`` clockwise more – crop,
    censor boxes and drawings turn along, strokes and text keep their size in pixels."""
    out = edit.copy()
    q = quarters % 4
    out.rotate = (edit.rotate + q) % 4
    if out.crop:
        out.crop = _turn_box(out.crop, q)
    out.censor = [_turn_box(b, q) for b in out.censor]
    w, h = max(1, size[0]), max(1, size[1])
    for s in out.shapes:
        s.pts = [_turn_point(x, y, q) for x, y in s.pts]
        if q % 2:                               # sizes are fractions of the height – the old width now
            s.size = s.size * h / w
    return out


def flipped(edit: ImageEdit, horizontal: bool, size: tuple = (1000, 1000)) -> ImageEdit:
    """``edit`` mirrored once more (left/right or up/down), its boxes and drawings along (``size``: the turned
    picture, for the width of a text)."""
    out = edit.copy()
    if horizontal:
        out.flip_h = not out.flip_h
    else:
        out.flip_v = not out.flip_v
    if out.crop:
        out.crop = _flip_box(out.crop, horizontal)
    out.censor = [_flip_box(b, horizontal) for b in out.censor]
    for s in out.shapes:
        if s.kind == "text":                    # text stays readable: only its anchor moves
            pw, ph = max(1, size[0]), max(1, size[1])
            x0, y0, x1, y1 = annotate.text_box(s, pw, ph)
            w, h = (x1 - x0) / pw, (y1 - y0) / ph
            x, y = s.pts[0]
            s.pts = [(1.0 - x - w, y) if horizontal else (x, 1.0 - y - h)]
        else:
            s.pts = [_flip_point(x, y, horizontal) for x, y in s.pts]
    return out


def base(img: Image.Image, edit: ImageEdit) -> Image.Image:
    """The turned (and mirrored) picture all coordinates refer to."""
    out = img.convert("RGB")
    if edit.rotate % 4:
        out = out.transpose({1: Image.ROTATE_270, 2: Image.ROTATE_180, 3: Image.ROTATE_90}[edit.rotate % 4])
    if edit.flip_h:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    if edit.flip_v:
        out = out.transpose(Image.FLIP_TOP_BOTTOM)
    return out


def box_px(box, size: tuple) -> tuple:
    """Fraction box -> whole pixels (x0, y0, x1, y1) inside a picture ``size``, at least 1 px."""
    w, h = size
    x, y, bw, bh = box
    x0, y0 = max(0, min(w - 1, int(round(x * w)))), max(0, min(h - 1, int(round(y * h))))
    x1, y1 = max(x0 + 1, min(w, int(round((x + bw) * w)))), max(y0 + 1, min(h, int(round((y + bh) * h))))
    return x0, y0, x1, y1


def censor_area(img: Image.Image, box, style: str) -> Image.Image:
    """``img`` with ``box`` (fractions) made unreadable: coarse blocks, blurred or black."""
    x0, y0, x1, y1 = box_px(box, img.size)
    part = img.crop((x0, y0, x1, y1))
    pw, ph = part.size
    if style == "black":
        part = Image.new(img.mode, part.size, 0)
    elif style == "blur":
        part = part.filter(ImageFilter.GaussianBlur(max(3, min(pw, ph) // 6)))
    else:
        block = max(4, min(pw, ph) // 8)
        part = part.resize((max(1, pw // block), max(1, ph // block)), Image.BILINEAR).resize((pw, ph), Image.NEAREST)
    out = img.copy()
    out.paste(part, (x0, y0))
    return out


def adjust(img: Image.Image, brightness=1.0, contrast=1.0, saturation=1.0) -> Image.Image:
    lo, hi = ADJUST_RANGE
    for enh, v in ((ImageEnhance.Brightness, brightness), (ImageEnhance.Contrast, contrast),
                   (ImageEnhance.Color, saturation)):
        v = max(lo, min(hi, float(v)))
        if abs(v - 1.0) > 1e-3:
            img = enh(img).enhance(v)
    return img


def render(img: Image.Image, edit: ImageEdit, crop: bool = True) -> Image.Image:
    """The edited picture (RGB). ``crop`` False: everything but the crop (the editor shows the crop box on it)."""
    out = adjust(base(img, edit), edit.brightness, edit.contrast, edit.saturation)
    for box in edit.censor:
        out = censor_area(out, box, edit.censor_style)
    if edit.shapes:
        out = annotate.draw(out, edit.shapes).convert("RGB")
    if crop and edit.crop:
        out = out.crop(box_px(edit.crop, out.size))
    return out


def save(img: Image.Image, path: str, fmt: str = "png") -> str:
    """Write ``img`` as PNG or JPG (temporary file + rename: never a half-written picture); returns the path."""
    fmt = fmt if fmt in FORMATS else "png"
    tmp = path + ".tmp"
    if fmt == "jpg":
        img.convert("RGB").save(tmp, "JPEG", quality=JPG_QUALITY, optimize=True)
    else:
        img.save(tmp, "PNG", compress_level=PNG_LEVEL)
    os.replace(tmp, path)
    return path


def out_name(source: str, fmt: str = "png") -> str:
    """'<source name> – bearbeitet.png' (the file name, no folder)."""
    stem = os.path.splitext(re.split(r"[\\/]", source)[-1])[0][:120] or "Screenshot"   # a Windows path anywhere
    return f"{stem} – bearbeitet.{fmt if fmt in FORMATS else 'png'}"
