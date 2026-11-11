"""Program icon: pictures from fogscout/assets, one file per size.

    python -m fogscout.icon PATH.ico     -> writes a multi-size .ico (16 … 256 px)

1.50.2 (Saru: "die Icons sollten in einer höheren Qualität sein, ich bin mit allen 4 nicht zufrieden"): the icon
belongs to one family with Fog Forge, Fog Translate and Fog Launch – the same dark tile with depth, warm glow, soft
fog and amber; the scout's picture stays the compass star. The pictures come from the shared source in the
fog-forge repository (tools/icons/, rendered by Chromium from SVG), so this module no longer draws: each size in
SIZES is its own file, and 16–32 px are a simpler variant (no fog, larger star) that stays sharp in the taskbar.
Until 1.50.1 the icon was drawn here with PIL (compass star over lavender fog). The file carries ICON_VERSION in its
name: Windows caches shortcut and taskbar icons by path and would keep showing the old picture out of a replaced
file; the old files go with the old shortcuts (autostart.install).
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw

ICON_VERSION = 3
FILE = f"fogscout-{ICON_VERSION}.ico"
OLD_FILES = ("fogscout-2.ico", "fogscout.ico", "dbdmapscout.ico")   # earlier pictures (1.50.1 / 1.9 / until 1.8.91)
BG = (20, 28, 33, 255)             # the tile's dark ground (ring around the tray dots)
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
PICTURES = (16, 20, 24, 32, 40, 48, 64, 128, 256, 512)   # assets/icon-<n>.png; up to 32 the small variant
SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]
_CACHE: dict[int, Image.Image] = {}


def _picture(n: int) -> Image.Image:
    if n not in _CACHE:
        with Image.open(os.path.join(ASSETS, f"icon-{n}.png")) as img:
            _CACHE[n] = img.convert("RGBA")
    return _CACHE[n]


def draw(size: int = 256) -> Image.Image:
    """The icon at ``size`` px: its own picture when there is one, else the next larger one scaled down (the
    small variant only for sizes up to 32, where it was made for)."""
    exact = size if size in PICTURES else None
    if exact:
        return _picture(exact).copy()
    larger = [n for n in PICTURES if n >= size and (n > 32 or size <= 32)]
    source = _picture(larger[0] if larger else PICTURES[-1])
    return source.resize((size, size), Image.LANCZOS)


REC = (229, 83, 75, 255)      # 1.4.1: recording dot top right (theme.DOT "err" red)


def draw_status(size: int, colour: str | None, rec: bool = False) -> Image.Image:
    """1.3.6: the icon with a status dot bottom right (tray), ringed in the icon's dark ground; 1.4.1: a red
    dot top right while a round is being recorded."""
    img = draw(size)
    if not colour and not rec:
        return img
    s = 4 * size
    over = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    if colour:
        r, ring = 0.25 * s, 0.06 * s
        cx = cy = s - r - ring
        d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=BG)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    if rec:
        r, ring = 0.19 * s, 0.06 * s
        cx, cy = s - r - ring, r + ring
        d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=BG)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=REC)
    img.alpha_composite(over.resize((size, size), Image.LANCZOS))
    return img


def ico_bytes() -> bytes:
    """Every size from its own picture (saving one big picture with ``sizes`` would scale it down instead)."""
    from io import BytesIO
    buf = BytesIO()
    pictures = [draw(n) for n in SIZES]
    pictures[-1].save(buf, format="ICO", sizes=[(n, n) for n in SIZES], append_images=pictures[:-1])
    return buf.getvalue()


def save_ico(path: str) -> None:
    with open(path, "wb") as fh:
        fh.write(ico_bytes())


def ensure_ico(root: str) -> str:
    """The icon file for the taskbar and the shortcuts in ``root`` (FILE): written once when missing or empty
    (the picture's version is in the name, so an existing file is this picture; drawing the nine sizes takes
    ~180 ms, not spent at every start). Written through a temporary file, so a crash leaves no half file."""
    path = os.path.join(root, FILE)
    try:
        if os.path.getsize(path) > 0:
            return path
    except OSError:
        pass
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(ico_bytes())
    os.replace(tmp, path)
    return path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python -m fogscout.icon PATH.ico")
    save_ico(sys.argv[1])
