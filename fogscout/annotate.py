"""Drawings on a picture (1.12, user: "ein gutes Bearbeitungstool für Videos und Screenshots"): arrows, lines, boxes,
ellipses, freehand and text, shared by the screenshot editor (imageedit / qt_image) and the clip editor (clipedit
draws them into a transparent picture that ffmpeg lays over the video). Pure PIL – no Qt.

Positions are fractions of the picture (0..1), sizes fractions of its height, so a shape drawn on the preview lands
on the same spot of the full picture. Every shape is drawn three times larger on a tile of its own and scaled down
(smooth edges without drawing the whole picture three times larger), with a dark outline that keeps it readable on
light and dark game pictures.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

from PIL import Image, ImageDraw

KINDS = ("arrow", "line", "rect", "ellipse", "free", "text")
COLOURS = ("#ffd23f", "#ff4d4d", "#4dabff", "#5ee27a", "#ffffff", "#000000")   # yellow first: DBD's own accent
DEFAULT_SIZE = 0.006            # stroke as a fraction of the picture height (≈ 9 px on 1440p)
TEXT_SIZE = 0.05                # text height as a fraction of the picture height
SIZES = (0.003, 0.006, 0.010, 0.016)
TEXT_SIZES = (0.03, 0.05, 0.08, 0.12)
SS = 3                          # supersampling of a shape's tile
OUTLINE = (0, 0, 0, 170)        # the dark rim around every stroke


@dataclass
class Shape:
    kind: str                                   # one of KINDS
    pts: list = field(default_factory=list)     # [(x, y)] fractions: arrow/line/rect/ellipse two, free many, text one
    colour: str = COLOURS[0]
    size: float = DEFAULT_SIZE                  # stroke (text: height) as a fraction of the picture height
    text: str = ""
    t0: float | None = None                     # video only: shown from/to (seconds of the recording), None = always
    t1: float | None = None

    def moved(self, dx: float, dy: float) -> "Shape":
        return replace(self, pts=[(x + dx, y + dy) for x, y in self.pts])

    def shown_at(self, t: float) -> bool:
        return (self.t0 is None or t >= self.t0) and (self.t1 is None or t <= self.t1)


def _rgba(colour: str, alpha: int = 255) -> tuple:
    c = colour.lstrip("#")
    if len(c) != 6:
        return 255, 210, 63, alpha
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), alpha


def _px(shape: Shape, w: int, h: int) -> list:
    return [(x * w, y * h) for x, y in shape.pts]


def _font(px: int):
    from .skin import inter
    return inter("Bold", max(6, int(px)))


def text_box(shape: Shape, w: int, h: int) -> tuple:
    """(x0, y0, x1, y1) of a text shape in pixels: the anchor is its top-left corner."""
    if not shape.pts:
        return 0, 0, 0, 0
    from .overlay_win32 import _char_len
    size = max(6, int(shape.size * h))
    font = _font(size)
    lines = (shape.text or " ").split("\n")
    width = max(sum(_char_len(font, ch) for ch in line) for line in lines)
    x, y = shape.pts[0][0] * w, shape.pts[0][1] * h
    pad = size * 0.12
    return x - pad, y - pad, x + width + pad, y + size * 1.25 * len(lines) + pad


def bounds(shape: Shape, w: int, h: int) -> tuple:
    """Pixel box (x0, y0, x1, y1) the shape covers, its stroke and outline included."""
    if shape.kind == "text":
        return text_box(shape, w, h)
    pts = _px(shape, w, h)
    if not pts:
        return 0, 0, 0, 0
    s = max(1.0, shape.size * h)
    m = s * (6.0 if shape.kind == "arrow" else 1.5) + 2
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m


def hit(shape: Shape, x: float, y: float, w: int, h: int, slack: float = 6) -> bool:
    """Is the pixel (x, y) on the shape (for picking it in the editor)?"""
    x0, y0, x1, y1 = bounds(shape, w, h)
    if not (x0 - slack <= x <= x1 + slack and y0 - slack <= y <= y1 + slack):
        return False
    if shape.kind in ("text", "rect", "ellipse"):
        return True
    pts = _px(shape, w, h)
    tol = max(slack, shape.size * h * 1.5)
    return any(_seg_dist(x, y, a, b) <= tol for a, b in zip(pts, pts[1:])) or (
        len(pts) == 1 and math.dist((x, y), pts[0]) <= tol)


def _seg_dist(px, py, a, b) -> float:
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.dist((px, py), a)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.dist((px, py), (ax + t * dx, ay + t * dy))


def _arrow_head(a, b, s):
    """Points of the arrow's head at ``b`` for a stroke ``s`` wide."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    length, spread = s * 5.0, math.radians(30)
    return [b, (b[0] - length * math.cos(ang - spread), b[1] - length * math.sin(ang - spread)),
            (b[0] - length * math.cos(ang + spread), b[1] - length * math.sin(ang + spread))]


def _draw_strokes(d, shape: Shape, pts, s: float, colour, rim: bool):
    """One pass of the shape on the (supersampled) tile: the rim (wider, dark) or the colour."""
    grow = s * 0.5 + SS * 1.5 if rim else 0
    width = max(1, int(round(s + 2 * grow)))
    if shape.kind in ("line", "arrow", "free") and len(pts) >= 2:
        end = pts[-1]
        if shape.kind == "arrow":                          # the line stops inside the head: no blunt tip
            head = _arrow_head(pts[0], pts[1], s)
            mid = ((head[1][0] + head[2][0]) / 2, (head[1][1] + head[2][1]) / 2)
            end = mid
        line = pts[:-1] + [end] if shape.kind != "free" else pts
        d.line(line, fill=colour, width=width, joint="curve")
        r = width / 2
        for p in (line[0],) + ((line[-1],) if shape.kind != "arrow" else ()):
            d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=colour)       # round caps
        if shape.kind == "arrow":
            head = _arrow_head(pts[0], pts[1], s)
            d.polygon(head, fill=colour, outline=colour, width=max(1, int(round(2 * grow))) if rim else 1)
    elif shape.kind in ("rect", "ellipse") and len(pts) >= 2:
        (x0, y0), (x1, y1) = pts[0], pts[1]
        box = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        box = (box[0] - grow, box[1] - grow, box[2] + grow, box[3] + grow)
        if box[2] - box[0] < 1 or box[3] - box[1] < 1:
            return
        if shape.kind == "rect":
            d.rectangle(box, outline=colour, width=width)
        else:
            d.ellipse(box, outline=colour, width=width)


def _draw_text(tile: Image.Image, shape: Shape, ox: float, oy: float, w: int, h: int):
    from .overlay_win32 import _draw_run
    size = max(6, int(shape.size * h)) * SS
    font = _font(size)
    stroke = max(SS, int(size * 0.09))
    x, y = shape.pts[0][0] * w * SS - ox, shape.pts[0][1] * h * SS - oy
    for i, line in enumerate((shape.text or "").split("\n")):
        _draw_run(tile, x, y + i * size * 1.25, line, font, _rgba(shape.colour), stroke=stroke,
                  stroke_fill=(0, 0, 0, 230))


def draw(img: Image.Image, shapes, t: float | None = None) -> Image.Image:
    """``img`` (any mode) with ``shapes`` on it, as RGBA; ``t`` (video): only shapes shown at that time."""
    out = img.convert("RGBA")
    w, h = out.size
    for shape in shapes:
        if t is not None and not shape.shown_at(t):
            continue
        if shape.kind == "text" and (not shape.pts or not shape.text.strip()):
            continue
        x0, y0, x1, y1 = (int(math.floor(v)) for v in bounds(shape, w, h))
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(w, x1 + 1), min(h, y1 + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        tile = Image.new("RGBA", ((x1 - x0) * SS, (y1 - y0) * SS), (0, 0, 0, 0))
        if shape.kind == "text":
            _draw_text(tile, shape, x0 * SS, y0 * SS, w, h)
        else:
            pts = [((px - x0) * SS, (py - y0) * SS) for px, py in _px(shape, w, h)]
            s = max(1.0, shape.size * h) * SS
            d = ImageDraw.Draw(tile)
            _draw_strokes(d, shape, pts, s, OUTLINE, rim=True)
            _draw_strokes(d, shape, pts, s, _rgba(shape.colour), rim=False)
        tile = tile.resize((x1 - x0, y1 - y0), Image.LANCZOS)
        out.alpha_composite(tile, (x0, y0))
    return out


def layer(width: int, height: int, shapes, t: float | None = None) -> Image.Image:
    """A transparent picture with only ``shapes`` on it (the clip editor lays it over the video)."""
    return draw(Image.new("RGBA", (max(1, width), max(1, height)), (0, 0, 0, 0)), shapes, t)


def to_dict(shape: Shape) -> dict:
    return {"kind": shape.kind, "pts": [list(p) for p in shape.pts], "colour": shape.colour, "size": shape.size,
            "text": shape.text, "t0": shape.t0, "t1": shape.t1}


def from_dict(d: dict) -> Shape | None:
    try:
        kind = str(d.get("kind"))
        if kind not in KINDS:
            return None
        pts = [(float(p[0]), float(p[1])) for p in d.get("pts") or []][:2000]
        t0 = d.get("t0")
        t1 = d.get("t1")
        return Shape(kind, pts, str(d.get("colour") or COLOURS[0]), float(d.get("size") or DEFAULT_SIZE),
                     str(d.get("text") or "")[:500], None if t0 is None else float(t0),
                     None if t1 is None else float(t1))
    except (TypeError, ValueError, IndexError, AttributeError):
        return None
