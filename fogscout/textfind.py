"""Text on a still of the recording (1.41.1, editor package "smart censoring", step 2): the local PP-OCR detector
(fullscan.TextDetector – offline, the model the program ships) finds the text boxes, pieces of one line are joined,
boxes already hidden are left out, and they are shown as numbered suggestions. On a click (only with „Standbilder an
Claude“) Claude gets the picture – the censored boxes hidden – with the suggestions drawn in and numbered, and answers
with numbers only: which of them show player names, chat or a friend list. Nothing is read out of the picture here
(no OCR text, only where text is), nothing leaves the PC without that click.

Boxes are fractions of the picture [x, y, w, h], like the censor boxes (clipedit.censor_graph)."""
from __future__ import annotations

import os
import threading

MODEL = "ch_PP-OCRv4_det_infer.onnx"
MAX_SUGGEST = 24                 # suggestions at most (the biggest first – a still full of small text stays usable)
JOIN_GAP = 0.012                 # pieces of one line closer than this share of the width become one box
PAD = 0.004                      # each box grows by this share of the picture on every side
COVERED = 0.6                    # a suggestion this much inside a box already there is left out
MAX_SHARE = 0.25                 # a "text box" bigger than this share of the picture is not text

SYSTEM = ("You help a Dead by Daylight player hide private text in a still of their recording before it is "
          "shared. The picture shows numbered rectangles around text that a local detector found. Say which "
          "numbers cover player names, chat messages or a friend list – not the game's own labels, prompts, "
          "timers or perk/item names. Areas already hidden are blurred or black. 'summary' is one short sentence "
          "in the language given. When none of them is private, return an empty list.")

SCHEMA = {"type": "object", "additionalProperties": False, "required": ["summary", "names"],
          "properties": {"summary": {"type": "string"},
                         "names": {"type": "array", "items": {"type": "integer"}}}}


def _overlap(a, b) -> float:
    """The share of box ``a`` that lies inside box ``b``."""
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return max(0.0, w) * max(0.0, h) / max(1e-9, a[2] * a[3])


def _same_line(a, b) -> bool:
    """Pieces of one line of text: about the same height, at least half of it side by side."""
    if max(a[3], b[3]) > 2 * min(a[3], b[3]):
        return False
    top, bottom = max(a[1], b[1]), min(a[1] + a[3], b[1] + b[3])
    return bottom - top >= 0.5 * min(a[3], b[3])


def _gap(a, b) -> float:
    return max(a[0], b[0]) - min(a[0] + a[2], b[0] + b[2])


def join(boxes_px, width: int, height: int, existing=()) -> list:
    """Detector boxes (x0, y0, x1, y1 in pixels) → fraction boxes: pieces of one line joined, padded, cut to the
    picture, the ones mostly inside an ``existing`` box (already hidden) and implausibly big ones left out, the
    biggest MAX_SUGGEST in reading order (top to bottom, left to right)."""
    if width <= 0 or height <= 0:
        return []
    boxes = []
    for x0, y0, x1, y1 in boxes_px:
        box = [x0 / width, y0 / height, (x1 - x0) / width, (y1 - y0) / height]
        if x1 > x0 and y1 > y0 and box[2] * box[3] <= MAX_SHARE:     # a huge one first out – it would swallow
            boxes.append(box)                                          # every line it touches
    joined = True
    while joined:                                     # until nothing more joins (a line in many pieces)
        joined = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if _same_line(a, b) and _gap(a, b) <= JOIN_GAP:
                    x0, y0 = min(a[0], b[0]), min(a[1], b[1])
                    x1, y1 = max(a[0] + a[2], b[0] + b[2]), max(a[1] + a[3], b[1] + b[3])
                    boxes[i] = [x0, y0, x1 - x0, y1 - y0]
                    del boxes[j]
                    joined = True
                    break
            if joined:
                break
    out = []
    for x, y, w, h in boxes:
        x0, y0 = max(0.0, x - PAD), max(0.0, y - PAD)
        x1, y1 = min(1.0, x + w + PAD), min(1.0, y + h + PAD)
        box = [round(x0, 5), round(y0, 5), round(x1 - x0, 5), round(y1 - y0, 5)]
        if box[2] * box[3] > MAX_SHARE or any(_overlap(box, e[:4]) >= COVERED for e in existing):
            continue
        out.append(box)
    out = sorted(out, key=lambda b: -b[2] * b[3])[:MAX_SUGGEST]
    return sorted(out, key=lambda b: (round(b[1], 2), b[0]))


def numbered(img, boxes):
    """A copy of ``img`` with each suggestion drawn as a rectangle and its number (1 …) right of it, vertically
    centred – stacked lines of names keep their numbers apart (above the box they covered the line before). What
    Claude sees."""
    from PIL import ImageDraw, ImageFont
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    size = max(12, h // 40)
    try:
        font = ImageFont.load_default(size=size)
    except TypeError:                                # an old Pillow without sizes
        font = ImageFont.load_default()
    for n, (x, y, bw, bh) in enumerate(boxes, 1):
        x0, y0, x1, y1 = int(x * w), int(y * h), int((x + bw) * w), int((y + bh) * h)
        draw.rectangle((x0, y0, x1, y1), outline=(255, 0, 255), width=max(2, h // 400))
        label = str(n)
        tw = int(draw.textlength(label, font=font)) + 6
        lx = x1 + 3 if x1 + 3 + tw <= w else max(0, x0 - 3 - tw)     # left of it at the right edge
        ly = min(max(0, (y0 + y1) // 2 - (size + 4) // 2), max(0, h - size - 4))
        draw.rectangle((lx, ly, lx + tw, ly + size + 4), fill=(255, 0, 255))
        draw.text((lx + 3, ly + 1), label, fill=(255, 255, 255), font=font)
    return out


def blocks(n: int, language: str, block) -> list:
    """The user content: how many boxes, the language, the picture."""
    return [{"type": "text", "text": f"{n} numbered boxes (1 to {n}). Answer 'summary' in {language}."}, block]


def parse(data, n: int) -> tuple[str, list]:
    """(summary, [0-based indices]) – only whole numbers 1 … ``n``, each once, in Claude's order. ValueError when
    'names' is not a list."""
    items = data.get("names") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise ValueError("names")
    out = []
    for v in items:
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= n or v - 1 in out:
            continue
        out.append(v - 1)
    summary = data.get("summary") if isinstance(data.get("summary"), str) else ""
    return summary.strip()[:300], out


class Finder:
    """The detector, loaded once on first use (in the calling thread – never the window's) and kept; ``find`` is
    safe from one thread at a time. ``models_dir`` = the program's models folder."""

    def __init__(self, models_dir: str):
        self.path = os.path.join(models_dir or "", MODEL)
        self._det = None
        self._lock = threading.Lock()

    def available(self) -> bool:
        return os.path.isfile(self.path)

    def find(self, img, existing=()) -> list:
        """Suggestions for the PIL picture ``img`` (see join)."""
        import numpy as np
        with self._lock:
            if self._det is None:
                from .fullscan import TextDetector
                self._det = TextDetector(self.path, threads=2)
            rgb = np.asarray(img.convert("RGB"))
            found = self._det.boxes(np.ascontiguousarray(rgb[:, :, ::-1]))
        return join(found, img.width, img.height, existing)
