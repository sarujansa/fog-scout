"""The overlay's pictures, drawn with PIL – no window, no Win32 (1.38.34, project review ARCH-3: split from
overlay_win32.py, which keeps the layered windows). The map card (``compose``, ``map_body``, ``add_info``,
``info_card``), the HUD and music cards (``render_hud``, ``music_*``, ``upnext_*``, ``progress_strip``), backdrops,
guide lines, the glyph cache that draws text exactly like ``ImageDraw.text`` (``_draw_run``), fonts and fallbacks
(``font_for``, ``FALLBACK_FONTS``) and the premultiplied BGRA the windows push. overlay_win32 re-exports every name,
so ``from .overlay_win32 import compose`` keeps working; new code imports from here.
"""
from __future__ import annotations

import math
import re
import time
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .mapimage import FONT as FIRA
from .overlay import BACKDROP

BORDER = (224, 176, 0, 255)


@lru_cache(maxsize=64)
def _font(size: int, heavy: bool = False):
    names = ("seguibl.ttf",) if heavy else ()             # Segoe UI Black: as heavy as the map titles
    for name in names + ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


@lru_cache(maxsize=64)
def fira(size: int):
    """Fira Sans ExtraBold at ``size`` (the map titles' font), loaded once per size (1.2.13: the HUD and the music
    card are redrawn every second – the font, its glyphs and their widths are cached, see _draw_run)."""
    try:
        return ImageFont.truetype(FIRA, size)
    except OSError:
        return _font(size)


# 1.8.25 (user: "andere Sprachen werden bei ‚Als nächstes' nicht korrekt angezeigt (russisch)"): the Inter fonts of
# the modern styles are a Latin subset, Fira has Latin/Greek/Cyrillic but no CJK – a character a font lacks is drawn
# with the first of these that has it (Windows' own fonts, DejaVu/Noto elsewhere), on the same baseline
FALLBACK_FONTS = ("segoeuib.ttf", "segoeui.ttf", "msyhbd.ttc", "msyh.ttc", "YuGothB.ttc", "YuGothM.ttc", "malgunbd.ttf",
                  "malgun.ttf", "Nirmala.ttf", "seguisym.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf",
                  "NotoSansCJK-Bold.ttc", "NotoSansCJK-Regular.ttc", "NotoSans-Bold.ttf")
_HAS: dict = {}                    # (font file, size, char) -> the font has a glyph for it
_GLYPHS: dict = {}                 # (font, char, stroke, x fraction) -> (L mask, offset) as ImageDraw.text uses it
_CHAR_LEN: dict = {}               # (font, char) -> textlength
# the keys hold the font itself, not id(font): a font freed by skin.inter's cache left its id to the next font
# (1.12 review: text drawings at every canvas size – other glyphs and widths, garbled text, also in the overlay)
GLYPHS_KEPT = 6000                 # the caches start over beyond this (a few hundred entries in practice)


def _font_key(font):
    return (getattr(font, "path", None) or id(font), getattr(font, "size", 0))


def _has_glyph(font, ch: str) -> bool:
    """Does ``font`` draw ``ch`` itself? A missing character comes out as the font's "notdef" glyph – the same
    picture as a code point no font maps (U+FFFF); white space always counts as there."""
    key = _font_key(font) + (ch,)
    hit = _HAS.get(key)
    if hit is None:
        if ch.isspace() or ord(ch) < 0x80:
            hit = True
        else:
            try:
                mine, notdef = font.getmask(ch), font.getmask("\uffff")
                hit = not (mine.size == notdef.size and bytes(mine) == bytes(notdef))
            except Exception:
                hit = True
        if len(_HAS) > GLYPHS_KEPT:
            _HAS.clear()
        _HAS[key] = hit
    return hit


@lru_cache(maxsize=256)
def _fallback_font(name: str, size: int):
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return None


def font_for(font, ch: str):
    """``font`` when it has ``ch``, else the first fallback that has it (Fira first: same look for Greek/Cyrillic),
    else ``font`` (its "notdef" box)."""
    if _has_glyph(font, ch):
        return font
    size = int(getattr(font, "size", 0) or 0)
    if size <= 0:
        return font
    path = str(getattr(font, "path", ""))
    first = (fira(size),)
    if "Inter-" in path:                           # the modern styles: Segoe UI in the same weight looks closest
        weight = "seguisb.ttf" if "SemiBold" in path else "segoeuib.ttf" if "Bold" in path else "segoeui.ttf"
        first = (_fallback_font(weight, size), fira(size))
    for cand in first + tuple(_fallback_font(n, size) for n in FALLBACK_FONTS):
        if cand is not None and cand is not font and _has_glyph(cand, ch):
            return cand
    return font


@lru_cache(maxsize=256)
def _ascent(font) -> int:
    try:
        return int(font.getmetrics()[0])
    except Exception:
        return 0


def _char_len(font, ch: str) -> float:
    key = (font, ch)
    n = _CHAR_LEN.get(key)
    if n is None:
        if len(_CHAR_LEN) > GLYPHS_KEPT:
            _CHAR_LEN.clear()
        n = _CHAR_LEN[key] = font_for(font, ch).getlength(ch)
    return n


def _glyph(font, ch: str, stroke: int, fx: float):
    """Pillow's own mask of ``ch`` (with ``stroke``) at the fractional x start ``fx`` – exactly what
    ImageDraw.text((x, y), ch, …) draws, cached per font/char/stroke/fraction (the fractions repeat: the same
    text starts at the same x every second)."""
    key = (font, ch, stroke, fx)
    hit = _GLYPHS.get(key)
    if hit is None:
        try:
            mask, off = font.getmask2(ch, "L", stroke_width=stroke, start=(fx, 0), stroke_filled=True)
        except TypeError:                                  # Pillow before stroke_filled
            mask, off = font.getmask2(ch, "L", stroke_width=stroke, start=(fx, 0))
        tile = Image.new("L", tuple(mask.size))
        tile.im.paste(mask, (0, 0) + tuple(mask.size))
        if len(_GLYPHS) > GLYPHS_KEPT:
            _GLYPHS.clear()
        hit = _GLYPHS[key] = (tile, (int(off[0]), int(off[1])))
    return hit


def _draw_run(pic: Image.Image, x: float, y: float, text: str, font, fill, stroke: int = 0,
              stroke_fill=None, track: float = 0) -> float:
    """``text`` drawn character by character like ``d.text((x, y), ch, …); x += d.textlength(ch) + track`` (no
    kerning – the look chosen in 1.49; ``track`` = letter spacing of the info lines), from the glyph cache;
    returns the x after the text. Pixel for pixel the same as ImageDraw.text
    (test_text_is_drawn_exactly_like_character_by_character), a fraction of its time."""
    d = ImageDraw.Draw(pic)
    iy = int(y)
    same = stroke and fill == stroke_fill          # ImageDraw.text draws the fill only when it differs
    for ch in text:
        ix, fx = int(x), math.modf(x)[0]
        f = font_for(font, ch)                     # 1.8.25: a character the font lacks from a fallback font
        jy = iy + (_ascent(font) - _ascent(f) if f is not font else 0)          # … on the same baseline
        if stroke:
            tile, off = _glyph(f, ch, stroke, fx)
            d.bitmap((ix + off[0], jy + off[1]), tile, fill=stroke_fill)
        if not same:
            tile, off = _glyph(f, ch, 0, fx)
            d.bitmap((ix + off[0], jy + off[1]), tile, fill=fill)
        x += _char_len(font, ch) + track
    return x


def body_cols(img: Image.Image, split: int | None):
    """1.8.24 (user: "die Map wird nicht grösser"): columns (x0, x1) of what is drawn below the map's name – the
    transparent strips beside it made the picture as wide as the black bar while the map itself took two thirds
    of it (Coal Tower: 270 of 406 px), so it could not grow. None = keep the whole width."""
    if not split or not 0 < split < img.height:
        return None
    box = img.crop((0, split, img.width, img.height)).getchannel("A").getbbox()
    return (box[0], box[2]) if box and box[2] - box[0] < img.width else None


def compose(img: Image.Image, height: int, caption: str, transparent: bool, border: bool,
            text_h: int = 0, split: int | None = None, cols=None) -> Image.Image:
    """Scaled map + optional caption bar (+ edit border) as one RGBA picture; ``text_h``: height the
    caption is sized for (stacked floors: one floor), 0 = ``height``. ``split``: first row of the map below the
    name drawn into the picture (mapimage.title_split) – the name is then scaled by ``text_h`` like the lines
    below the map, the map alone by ``height`` (1.65.4, user: the map's size freely, the name stays). ``cols``
    (1.8.24, body_cols): the map cut to what is drawn – the same for every frame of an animation."""
    if split and text_h and text_h != height and 0 < split < img.height:
        title = img.crop((0, 0, img.width, split))
        body = img.crop((cols[0] if cols else 0, split, cols[1] if cols else img.width, img.height))
        tb = title.getchannel("A").getbbox()        # 1.2.7: the name itself, not the empty strip beside it – the
        if tb:                                      # whole strip made the overlay as wide as the name's size, and
            title = title.crop((tb[0], 0, tb[2], split))     # the lines below were shrunk for nothing
        th = max(1, round(split * text_h / img.height))
        bh = max(1, round(body.height * height / img.height))
        title = title.resize((max(1, round(title.width * text_h / img.height)), th), Image.LANCZOS)
        body = body.resize((max(1, round(body.width * height / img.height)), bh), Image.LANCZOS)
        w = max(title.width, body.width)
        pic = Image.new("RGBA", (w, th + bh), (0, 0, 0, 0))
        pic.alpha_composite(title, ((w - title.width) // 2, 0))
        pic.alpha_composite(body, ((w - body.width) // 2, th))
        height = pic.height
    else:
        w = max(1, round(img.width * height / img.height))
        pic = img.resize((w, height), Image.LANCZOS)
    if not transparent:
        bg = Image.new("RGBA", pic.size, BACKDROP + (255,))
        bg.alpha_composite(pic)
        pic = bg
    if caption:
        size = max(12, (text_h or height) // 34)
        font = _font(size)
        x0, y0, x1, y1 = ImageDraw.Draw(pic).textbbox((0, 0), caption, font=font)
        cap_h = (y1 - y0) + size // 2 + 4
        cap_w = min(w, (x1 - x0) + size + 4)
        canvas = Image.new("RGBA", (w, height + cap_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(canvas)
        d.rectangle([0, 0, cap_w - 1, cap_h - 1], fill=(20, 20, 22, 235))
        d.text((size // 2 + 2 - x0, (cap_h - (y1 - y0)) // 2 - y0), caption, font=font, fill=(242, 242, 242, 255))
        canvas.alpha_composite(pic, (0, cap_h))
        pic = canvas
    if border:
        add_border(pic)
    return pic


def map_body(img: Image.Image, height: int, split: int | None) -> Image.Image:
    """1.3.1: the map alone for the styled cards (skin.map_card): the name drawn into the picture is cut off
    (``split`` = mapimage.title_split) and the empty transparent margins go, scaled so that the map is
    ``height`` tall like compose() would make it (the whole picture's height, name included)."""
    body = img.crop((0, split, img.width, img.height)) if split and 0 < split < img.height else img
    box = body.getchannel("A").getbbox()
    if box:
        body = body.crop(box)
    bh = max(1, round(body.height * height / img.height))
    return body.resize((max(1, round(body.width * bh / body.height)), bh), Image.LANCZOS)


GRAB_SURFACE = (12, 12, 16, 70)      # 1.44.1: under an element in edit mode – grabbable everywhere


def add_border(pic: Image.Image, label: str = "") -> Image.Image:
    """The yellow frame of the edit mode; ``label`` (1.64.7, user: "keinen Plan, was ich verschiebe") names the
    element on a tag inside the frame's top left – size and place stay exactly the same (no jump after "Fertig").
    1.44.1: a faint dark surface under the whole element – a layered window takes the mouse only where a pixel is
    not fully transparent, so before only the letters and the frame could be grabbed (not the gaps between)."""
    if pic.mode == "RGBA":
        under = Image.new("RGBA", pic.size, GRAB_SURFACE)
        under.alpha_composite(pic)
        pic.paste(under)
    d = ImageDraw.Draw(pic)
    d.rectangle([0, 0, pic.width - 1, pic.height - 1], outline=BORDER, width=3)
    if label:
        font = fira(15)                  # 1.46.4: cached, was loaded from the file on every frame drawn
        tw = min(pic.width, int(d.textlength(label, font=font)) + 12)
        asc, desc = font.getmetrics()
        th = min(pic.height, asc + desc + 6)
        d.rectangle([0, 0, tw - 1, th - 1], fill=BORDER)
        d.text((6, 3), label, font=font, fill=(20, 16, 4, 255))
    return pic


INFO_TIMER = (255, 255, 255, 255)
TIMER_GAP = 2.5                    # the gap below the timer, in row gaps (1.2.7, user: too close)
DIM_LABEL = (150, 156, 170, 255)   # = sysinfo.DIM: a row starting with it is "label: values" (column, 1.64.7)
TITLE_SCALE = 1.15                 # the music card's title, a bit larger than the artist below it
INFO_SERVER = (178, 184, 248, 255)     # light tone of the map colour
INFO_DOT = (74, 222, 128, 255)         # "connected"
INFO_WARN = (251, 191, 36, 255)        # doubtful detection
INFO_MEMO = (236, 238, 245, 255)       # 1.8.54: the own note on the map
PING_GOOD, PING_OK = 60, 120           # ms: green up to here, amber up to here, red above
PING_COLOURS = ((134, 239, 172, 255), (251, 191, 36, 255), (248, 113, 113, 255))


def ping_colour(ms: float):
    return PING_COLOURS[0] if ms <= PING_GOOD else PING_COLOURS[1] if ms <= PING_OK else PING_COLOURS[2]


def _content_bottom(pic: Image.Image) -> int:
    """Last row with visible map pixels (map pictures often have an empty transparent margin below)."""
    a = np.asarray(pic.getchannel("A"))
    rows = np.flatnonzero((a > 24).any(axis=1))
    return int(rows[-1]) + 1 if rows.size else pic.height


def _tracked_width(d, text, font, track):
    return sum(d.textlength(c, font=font) for c in text) + track * max(0, len(text) - 1)


def add_info(pic: Image.Image, timer: str, server: str, height: int, backdrop: bool = False,
             ping: float | None = None, status=(), note: str = "", record: str = "",
             beside: bool = False, rec=None, memo=()) -> Image.Image:
    """Round timer, connected server and its ping below the map, styled like the map title: white heavy
    digits with a soft shadow (no box); below them a green "connected" dot with the region in small
    caps, and the ping coloured by quality. The ping is only shown together with a server.
    ``status``: lines of the waiting card (no map on screen) – first one white, the others dimmer.
    ``note``: a warning in amber right below the timer (doubtful detection).
    ``record``: own results on this map (stats page), dimmer, below the timer/note.
    ``memo``: lines of the own note on this map (1.8.54, mapnotes), white, below the record – as written.
    ``backdrop``: the map sits on a dark rectangle (transparent edge off) – extend it behind the info.
    ``beside``: the block goes right of the map, centred in height (low wide bar above/below the picture).
    ``rec``: OBS records – True = the red dot right of the timer is on, False = off phase of the blink (1.5.2,
    user: "rechts von der Rundenzeit blinkend"), None = not recording."""
    if not server:
        ping = None
    if not timer and not server and not status and not note and not record and not memo:
        return pic
    d0 = ImageDraw.Draw(pic)
    tfont, sfont = _font(max(22, height // 11), heavy=True), _font(max(14, height // 24))
    track = max(1, height // 220)
    dot = max(7, height // 44)
    gap = max(4, height // 64)
    # rows: (kind, [(text, colour), ...] segments, font); small rows are tracked caps
    rows = []
    if timer:
        rows.append(("timer", [(timer, INFO_TIMER)], tfont))
    if note:
        rows.append(("note", [(note.upper(), INFO_WARN)], sfont))
    if record:
        rows.append(("record", [(record.upper(), INFO_SERVER)], sfont))
    for line in memo:                          # 1.8.54: as written – no caps, no tracking
        rows.append(("memo", [(line, INFO_MEMO)], sfont))
    for i, line in enumerate(status):          # waiting card: above the server, like the timer on the map
        rows.append(("status", [(line.upper(), INFO_TIMER if i == 0 else INFO_SERVER)], sfont))
    if server:
        rows.append(("server", [(server.upper(), INFO_SERVER)], sfont))
    if ping is not None:
        rows.append(("ping", [("PING ", INFO_SERVER), (f"{ping:.0f} MS", ping_colour(ping))], sfont))
    boxes, widths = [], []
    for kind, segs, font in rows:
        text = "".join(t for t, _ in segs)
        if kind == "timer":                      # 1.5.4 (user: "wird immer grösser und kleiner"): the digits are
            text = re.sub(r"\d", "0", text).rjust(5, "0")   # proportional – measure with the widest so the field and the
        elif kind == "ping":                     # dot never move; 1.8.28: at least "00:00", the ping three digits
            text = re.sub(r"\d+", "000", text)
        boxes.append(d0.textbbox((0, 0), text if kind == "timer" else text or "0", font=font))   # dot never move
        if kind == "timer":
            widths.append(boxes[-1][2] - boxes[-1][0])
        elif kind == "memo":
            widths.append(int(d0.textlength(text, font=font)))
        else:
            widths.append(int(_tracked_width(d0, text, font, track)) + (2 * dot if kind == "server" else 0))
    heights = [b[3] - b[1] for b in boxes]
    # 1.2.7 (user's screenshot: the lines sat right under the timer): more room after the big timer digits
    gaps = [int(TIMER_GAP * gap) if kind == "timer" else gap for kind, _s, _f in rows[:-1]]
    block_h = sum(heights) + sum(gaps)
    width = max([pic.width] + [w + 2 * gap for w in widths])
    # text layer for the info block only (shadow = blurred dark copy, like the title of the map pictures)
    blur = max(2, height // 150)
    pad = 3 * blur
    off = max(1, height // 220)
    layer_w, layer_h = width, block_h + 2 * pad
    top = max(pad, _content_bottom(pic) + 3 * gap)      # right under the visible map, not its empty margin
    left = 0
    halo = max(1, height // 200)                         # dark outline in the shadow: readable over bright game
    if beside:
        layer_w = max(widths) + 2 * gap
        if rec is not None and timer:                     # room for the recording dot right of the timer
            layer_w += 4 * max(5, heights[0] // 5) + gap
        left = pic.width + gap
        canvas_h = max(pic.height, layer_h + 2 * off)
        top = (canvas_h - layer_h) // 2 + pad
        canvas = Image.new("RGBA", (left + layer_w + off, canvas_h), BACKDROP + (255,) if backdrop else (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (width, max(pic.height, top + block_h + pad + 2 * off)),
                           BACKDROP + (255,) if backdrop else (0, 0, 0, 0))
    canvas.alpha_composite(pic, (0, (canvas.height - pic.height) // 2 if beside else 0))
    dark = (0, 0, 0, 230)

    def draw(im, shadow):
        d = ImageDraw.Draw(im)
        y = pad
        for (kind, segs, font), (x0, y0, x1, y1), w, h in zip(rows, boxes, widths, heights):
            if kind == "timer":
                d.text(((layer_w - w) // 2 - x0, y - y0), segs[0][0], font=font,
                       fill=dark if shadow else segs[0][1],
                       stroke_width=2 * halo if shadow else 0, stroke_fill=dark)
                if rec and not shadow:
                    r = max(5, h // 5)
                    rec_dot(d, (layer_w - w) // 2 + w + 2 * r + gap, y + h // 2, r)
            else:
                x = (layer_w - w) // 2
                if kind == "server":
                    grow = halo if shadow else 0
                    cy = y + h // 2
                    d.ellipse([x - grow, cy - dot // 2 - grow, x + dot + grow, cy - dot // 2 + dot + grow],
                              fill=dark if shadow else INFO_DOT)
                    x += 2 * dot
                for text, colour in segs:
                    x = _draw_run(im, x, y - y0, text, font, dark if shadow else colour, halo if shadow else 0,
                                  dark, 0 if kind == "memo" else track)
            y += h + (int(TIMER_GAP * gap) if kind == "timer" else gap)

    shadow = Image.new("RGBA", (layer_w, layer_h), (0, 0, 0, 0))
    draw(shadow, True)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    text = Image.new("RGBA", (layer_w, layer_h), (0, 0, 0, 0))
    draw(text, False)
    canvas.alpha_composite(shadow, (left + off, top - pad + 2 * off))
    canvas.alpha_composite(text, (left, top - pad))
    return canvas


def premultiplied_bgra(img: Image.Image) -> bytes:
    """Pixels for UpdateLayeredWindow: colour multiplied by alpha, in B G R A order. 1.6.1: Pillow's own "RGBa"
    mode does it in C – the same bytes as the numpy version (test), 6.4 → 1.6 ms for a 420×560 map, and this runs
    for every window whose picture changes (the map with its timer every second)."""
    return img.convert("RGBA").convert("RGBa").tobytes("raw", "BGRa")


def premultiplied_bgra_numpy(img: Image.Image) -> bytes:
    """Reference for the test: the numpy version used until 1.6."""
    a = np.asarray(img.convert("RGBA"), dtype=np.uint16)
    rgb = (a[:, :, :3] * a[:, :, 3:4] + 127) // 255
    out = np.empty(a.shape, dtype=np.uint8)
    out[:, :, 0] = rgb[:, :, 2]
    out[:, :, 1] = rgb[:, :, 1]
    out[:, :, 2] = rgb[:, :, 0]
    out[:, :, 3] = a[:, :, 3]
    return out.tobytes()


def render_hud(rows, height: int) -> Image.Image:
    """System values (sysinfo.hud_rows) in Fira Sans ExtraBold like the map titles (user's choice of five
    variants, 1.49: labels grey, values bright, same font and size, no letter spacing) with the soft shadow of
    the info block, left-aligned; ``height``: game height."""
    size = max(13, height // 60)
    font = fira(size)
    gap = max(3, height // 160)
    blur = max(2, height // 300)
    pad = 3 * blur
    halo = max(1, height // 400)
    # 1.64.7 (user: "alles schön untereinander"): rows of label + values start their values in one column
    labelled = [len(row) >= 2 and row[0][1] == DIM_LABEL and row[0][0].strip() for row in rows]
    col = max((int(_run_len(font, row[0][0])) for row, lab in zip(rows, labelled) if lab), default=0)
    texts = ["".join(t for t, _ in (row[1:] if lab else row)) for row, lab in zip(rows, labelled)]
    widths = [int(_run_len(font, t)) + (col if lab else 0) for t, lab in zip(texts, labelled)]
    asc, desc = font.getmetrics()
    line_h = asc + desc
    w = max(widths, default=0) + 2 * pad
    h = len(rows) * line_h + gap * max(0, len(rows) - 1) + 2 * pad
    dark = (0, 0, 0, 230)

    def draw(im, shadow):
        y = pad
        for row, lab in zip(rows, labelled):
            x = pad
            for i, (text, colour) in enumerate(row):
                if lab and i == 1:
                    x = pad + col                      # the values' column
                x = _draw_run(im, x, y, text, font, dark if shadow else colour, halo if shadow else 0, dark)
            y += line_h + gap

    pic = Image.new("RGBA", (max(1, w), max(1, h)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", pic.size, (0, 0, 0, 0))
    draw(shadow, True)
    pic.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)), (0, 0))
    draw(pic, False)
    return pic


def _run_len(font, text: str) -> float:
    """Width of ``text`` drawn character by character (_draw_run), from the width cache."""
    return sum(_char_len(font, ch) for ch in text)


def progress_strip(width: int, elapsed: float, total: float, height: int, accent=None,
                   remaining: bool = False) -> Image.Image:
    """The song's progress (1.64.7, user's screenshot of Spotify): "1:10 ──────── 2:56" – times grey, the bar
    white on a faint track, with the soft dark edge of the other text. ``height``: game height. 1.2.4: ``accent``
    = colour of the bar (from the cover), ``remaining`` = time left on the right ("−1:46") instead of the length."""
    from .media import clock
    size = max(11, height // 75)
    font = fira(size)
    blur = max(2, height // 300)
    pad = 3 * blur
    halo = max(1, height // 400)
    left, right = clock(elapsed), ("\u2212" + clock(total - elapsed) if remaining else clock(total))
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widest = re.sub(r"\d", "0", clock(total))             # 1.8.28: the fields never move while the time runs
    lw, rw = d0.textlength(widest, font=font), d0.textlength(("\u2212" if remaining else "") + widest, font=font)
    asc, desc = font.getmetrics()
    h = asc + desc + 2 * pad
    w = max(int(lw + rw) + 6 * size, width)
    gap = max(6, size // 2)
    x0, x1 = pad + lw + gap, w - pad - rw - gap
    bar = max(3, height // 360)
    cy = h // 2
    frac = 0.0 if total <= 0 else min(1.0, max(0.0, elapsed / total))
    dark = (0, 0, 0, 230)
    pic = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", pic.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    for x, t in ((pad, left), (w - pad - rw, right)):
        ds.text((x, pad), t, font=font, fill=dark, stroke_width=halo, stroke_fill=dark)
    ds.rounded_rectangle((x0 - halo, cy - bar / 2 - halo, x1 + halo, cy + bar / 2 + halo), radius=bar, fill=dark)
    pic.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(pic)
    d.text((pad, pad), left, font=font, fill=DIM_LABEL)
    d.text((w - pad - rw, pad), right, font=font, fill=DIM_LABEL)
    d.rounded_rectangle((x0, cy - bar / 2, x1, cy + bar / 2), radius=bar, fill=(255, 255, 255, 70))
    if frac > 0:
        d.rounded_rectangle((x0, cy - bar / 2, x0 + (x1 - x0) * frac, cy + bar / 2), radius=bar,
                            fill=tuple(accent[:3]) + (235,) if accent else (255, 255, 255, 235))
    return pic


CARD_BACKDROP = (14, 14, 18, 165)    # the music card's own dark area (1.2.4): readable over a bright game picture
CARD_EDGE = (118, 118, 130, 200)      # 1.2.20: its thin frame – the area alone vanishes on the black bars (user:
                                      # "trotz schwarzem Hintergrund den Rahmen von der Map sehen")


def backdrop(pic: Image.Image, height: int, pad: int = 0, radius: int = 0) -> Image.Image:
    """``pic`` on a dark half-transparent area with rounded corners and a thin lighter frame (1.2.4, user's pick:
    "Hintergrund-Kachel"; since 1.2.4 also behind the map and the system values, user: "Hintergrund dahinter, für
    jedes UI-Element"; frame since 1.2.20). ``height``: game height (sets padding and corners unless given)."""
    pad = pad or max(4, height // 160)
    radius = radius or max(6, height // 90)
    out = Image.new("RGBA", (pic.width + 2 * pad, pic.height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, out.width - 1, out.height - 1), radius=radius,
                                          fill=CARD_BACKDROP, outline=CARD_EDGE, width=max(1, radius // 7))
    out.alpha_composite(pic, (pad, pad))
    return out


def map_backdrop(pics, text_h: int) -> list:
    """The map window's pictures (all frames of one map) on the dark area: cut to what all of them show (map
    pictures have empty transparent margins), the same size for every frame; ``text_h``: size of its lines."""
    box = None
    for pic in pics:
        b = pic.getchannel("A").getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    pad, radius = backdrop_pad(text_h), max(8, text_h // 30)
    return [backdrop(pic.crop(box) if box else pic, 0, pad, radius) for pic in pics]


def backdrop_pad(text_h: int) -> int:
    """Edge of the dark area around the map (map_backdrop)."""
    return max(6, text_h // 45)


def _below(pic: Image.Image, strip: Image.Image, centred: bool) -> Image.Image:
    """``strip`` under ``pic`` (overlapping by the shadow pad, like the text rows)."""
    out = Image.new("RGBA", (max(pic.width, strip.width), pic.height + strip.height), (0, 0, 0, 0))
    out.alpha_composite(pic, ((out.width - pic.width) // 2 if centred else 0, 0))
    out.alpha_composite(strip, ((out.width - strip.width) // 2 if centred else 0, pic.height))
    return out


FIT_MIN = 0.6               # a long title is set down to this share of its size before it wraps (1.65.2)


def fit_lines(rows, height: int, scales=None):
    """Each row as a picture no wider than a line of media.MAX_CHARS characters (1.65.2, user: "lieber die
    Schrift kleiner statt Zeilenumbruch"): a longer row gets smaller text, down to FIT_MIN; only what is still
    too long wraps (media.wrap) at that size. ``scales``: size factor per row (the title is a bit larger)."""
    from .media import ARTIST_LINES, TITLE_LINES, wrap
    out = []
    for i, row in enumerate(rows):
        scale = scales[i] if scales else 1.0
        h = int(height * scale)
        im = render_hud([row], h)
        colour = row[-1][1] if row else (255, 255, 255, 255)
        max_w = _line_cap(h)
        if im.width <= max_w or len(row) != 1:
            out.append(im)
            continue
        f = max(FIT_MIN, max_w / im.width)
        small = render_hud([row], max(1, int(h * f)))
        if small.width <= max_w * 1.02:
            out.append(small)
            continue
        text = row[0][0]                                 # still too long: wrap at the smallest size
        chars = max(8, int(len(text) * max_w / small.width))
        lines = wrap(text, chars, TITLE_LINES if i == 0 else ARTIST_LINES)
        out += [render_hud([[(line, colour)]], max(1, int(h * f))) for line in lines]
    return out


@lru_cache(maxsize=128)
def _line_cap(h: int) -> int:
    """Width of a line of media.MAX_CHARS characters at ``h`` (fit_lines' limit), measured once per size."""
    from .media import MAX_CHARS
    return render_hud([[("n" * MAX_CHARS, (255, 255, 255, 255))]], h).width


def _stack(lines, pad: int, centred: bool) -> Image.Image:
    """Line pictures of render_hud one below the other; ``pad``: their shadow margin (it overlaps)."""
    if not lines:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    w = max(im.width for im in lines)
    h = sum(im.height - pad for im in lines) + pad
    pic = Image.new("RGBA", (w, max(1, h)), (0, 0, 0, 0))
    y = 0
    for im in lines:
        pic.alpha_composite(im, ((w - im.width) // 2 if centred else 0, y))
        y += im.height - pad
    return pic


def cover_radius(look, side: int, default: int) -> int:
    """Corner radius of the music card's cover (1.8.24, user: "zwischen runden und eckigen Bildern"): ``look``
    "cover_round" = a circle, "cover_square" = square corners, neither = the style's own (``default``)."""
    if "cover_round" in look:
        return side // 2
    if "cover_square" in look:
        return 0
    return default


def render_music_compact(rows, cover, height: int, look=()) -> Image.Image:
    """Music card "Kompakt" (1.64): the cover left of the title/artist rows, as tall as the two lines."""
    text = _stack(fit_lines(rows, height), 3 * max(2, height // 300), False)
    if cover is None:
        return text
    size = max(13, height // 60)
    blur = max(2, height // 300)
    pad = 3 * blur
    side = max(16, text.height - 2 * pad)
    art = cover.convert("RGBA").resize((side, side), Image.LANCZOS)
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, side - 1, side - 1),
                                           radius=cover_radius(look, side, max(2, size // 4)), fill=255)
    art.putalpha(mask)
    gap = max(6, size // 2)
    pic = Image.new("RGBA", (pad + side + gap + text.width - pad, max(text.height, side + 2 * pad)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", pic.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 200), (pad, pad), mask)
    pic.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
    pic.alpha_composite(art, (pad, pad))
    pic.alpha_composite(text, (pad + side + gap - pad, 0))
    return pic


def render_music(rows, cover, height: int, style: str = "big", progress=None, look=(), upnext=None,
                 upnext_pos: str = "below", anim=None) -> Image.Image:
    """"Läuft gerade": style "big" (1.64.7, user's choice "A") = the cover big on top, below it the title (a bit
    larger) and the artist, centred; "compact" = the card of 1.64 (cover left). Text like the system values, the
    cover slightly rounded with the same soft shadow. ``look`` (1.2.4): "accent" = bar in the cover's colour,
    "remaining" = time left, "backdrop" = on a dark area. ``upnext`` (1.8) = (label, ((title, artist), …)) of the
    Spotify queue, below the song or to its right (``upnext_pos``). = music_card(music_body(…)); HudWindow keeps
    the body (cover and text) and draws only the progress strip anew every second (1.2.13)."""
    return music_card(music_body(rows, cover, height, style, look), height, style, progress, look, upnext, upnext_pos,
                      anim)


def music_picture(rows, height: int, cover=None, style="big", progress=None, look=(), skin="classic", accent=None,
                  upnext=None, upnext_pos="below", anim=None, bodies: dict | None = None,
                  min_w: int = 0, min_h: int = 0) -> Image.Image:
    """The music card in any overlay style – what HudWindow.render draws for it (1.8.1, shared with the song
    change's cross-fade). ``bodies``: a small cache {body key: (music_body, cover)} for the classic style, whose
    cover + text part is costly (fit_lines) and does not change while a song plays. ``min_w`` (1.8.28): the
    picture is at least this wide (the App's steady width per element – a shorter title moves nothing)."""
    progress = (int(progress[0]), int(progress[1])) if progress else None
    look = tuple(sorted(look))
    if skin != "classic":
        from . import skin as skins
        return skins.music(rows, cover, height, skin, progress, look, accent, style, upnext, upnext_pos, anim,
                           min_w=min_w, min_h=min_h)
    key = (tuple(tuple(r) for r in rows), int(height), id(cover), style, "accent" in look,
           tuple(k for k in look if k.startswith("cover_")))          # 1.8.24: the cover's shape
    if bodies is None:
        bodies = {}
    if key not in bodies:
        if len(bodies) >= 2:                                 # old and new song of a cross-fade, no more
            bodies.pop(next(iter(bodies)))
        bodies[key] = (music_body(rows, cover, height, style, look), cover)   # cover kept: id stays
    return music_card(bodies[key][0], height, style, progress, look, upnext, upnext_pos, anim, min_w, min_h)


def lines_above(pic: Image.Image, lines: Image.Image, text_h: int) -> Image.Image:
    """1.8.34: the classic lines block (add_info on an empty picture) above the map picture, both centred – the
    map's drawn name stays on top of the map itself."""
    gap = max(2, text_h // 60)
    out = Image.new("RGBA", (max(pic.width, lines.width), lines.height + gap + pic.height), (0, 0, 0, 0))
    out.alpha_composite(lines, ((out.width - lines.width) // 2, 0))
    out.alpha_composite(pic, ((out.width - pic.width) // 2, lines.height + gap))
    return out


def pad_to(pic: Image.Image, min_w: int, centred: bool = False, min_h: int = 0) -> Image.Image:
    """``pic`` on a transparent canvas at least ``min_w`` wide and ``min_h`` tall (1.8.28/1.8.30: a classic card at
    its steady size – left-aligned, or centred for the big music layout; at the top)."""
    if pic.width >= min_w and pic.height >= min_h:
        return pic
    out = Image.new("RGBA", (max(pic.width, int(min_w)), max(pic.height, int(min_h))), (0, 0, 0, 0))
    out.alpha_composite(pic, ((out.width - pic.width) // 2 if centred else 0, 0))
    return out


UPNEXT_SCALE = 0.8                  # the "up next" rows, a little smaller than the song's lines (1.8)


def upnext_block(label: str, items, height: int, anim=None) -> Image.Image:
    """"Als nächstes" (1.8): a grey header and one row per coming track – number, title, artist – set like the
    system values. ``anim`` (1.8.1) = ((title, artist), shift): the row that just became the song fades out at
    the top while the others slide up from one row below (shift 0 → 1); the block keeps its final size."""
    from .media import MAX_CHARS, clip
    h = max(1, int(height * UPNEXT_SCALE))
    pad = 3 * max(2, h // 300)

    def row_pic(num, item):
        title, artist = (tuple(item) + ("", ""))[:2]
        row = [(f"{num}  " if num else "   ", DIM_LABEL), (clip(title, MAX_CHARS), (255, 255, 255, 255))]
        if artist:
            row.append((" – " + clip(artist, MAX_CHARS // 2 + 5), DIM_LABEL))
        return render_hud([row], h)

    head = render_hud([[(label, DIM_LABEL)]], h) if label else None
    pics = [row_pic(i, it) for i, it in enumerate(items, 1)]
    if not anim or not pics:
        return _stack(([head] if head else []) + pics, pad, False)
    leaving, shift = anim
    shift = min(1.0, max(0.0, float(shift)))
    pitch = pics[0].height - pad
    w = max([p.width for p in pics] + ([head.width] if head else []))
    rows_h = sum(p.height - pad for p in pics) + pad
    inner = Image.new("RGBA", (w, rows_h), (0, 0, 0, 0))
    off = int(round((1.0 - shift) * pitch))
    gone = row_pic(None, leaving)
    gone.putalpha(gone.getchannel("A").point(lambda v: int(v * (1.0 - shift))))
    _paste(inner, gone, 0, off - pitch)
    y = off
    for p in pics:
        _paste(inner, p, 0, y)
        y += p.height - pad
    if head is None:
        return inner
    out = Image.new("RGBA", (w, head.height - pad + rows_h), (0, 0, 0, 0))
    out.alpha_composite(head, (0, 0))
    out.alpha_composite(inner, (0, head.height - pad))
    return out


def upnext_rows(label: str, items, height: int, room: int) -> int:
    """How many of ``items`` fit as upnext_block rows into ``room`` px of height (1.8.24: the list beside the card
    fills its height) – at least one."""
    if len(items) <= 1:
        return len(items)
    full = upnext_block(label, items, height)
    if full.height <= room:
        return len(items)
    one = upnext_block(label, items[:1], height)
    pitch = (full.height - one.height) / (len(items) - 1)
    return max(1, min(len(items), 1 + int((room - one.height) // pitch))) if pitch > 0 else 1


def _paste(layer: Image.Image, pic: Image.Image, x: int, y: int):
    """``pic`` onto ``layer`` at (x, y), cropped to the layer (alpha_composite refuses what sticks out)."""
    sx, sy = max(0, -x), max(0, -y)
    dx, dy = max(0, x), max(0, y)
    cw, ch = min(pic.width - sx, layer.width - dx), min(pic.height - sy, layer.height - dy)
    if cw <= 0 or ch <= 0:
        return
    layer.alpha_composite(pic, (dx, dy), (sx, sy, sx + cw, sy + ch))


def blend_cards(old: Image.Image, new: Image.Image, t: float, centred: bool) -> Image.Image:
    """Cross-fade between two card pictures (1.8.1): ``old`` at 1 − t, ``new`` at t, on a canvas of the larger
    size, aligned at the top (centred horizontally for the big layout)."""
    t = min(1.0, max(0.0, float(t)))
    w, h = max(old.width, new.width), max(old.height, new.height)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for pic, a in ((old, 1.0 - t), (new, t)):
        if a <= 0.0:
            continue
        layer = pic if a >= 1.0 else pic.copy()
        if a < 1.0:
            layer.putalpha(layer.getchannel("A").point(lambda v, a=a: int(v * a)))
        out.alpha_composite(layer, ((w - pic.width) // 2 if centred else 0, 0))
    return out


def _beside(pic: Image.Image, block: Image.Image, gap: int) -> Image.Image:
    """``block`` to the right of ``pic``, both at the top."""
    out = Image.new("RGBA", (pic.width + gap + block.width, max(pic.height, block.height)), (0, 0, 0, 0))
    out.alpha_composite(pic, (0, 0))
    out.alpha_composite(block, (pic.width + gap, 0))
    return out


def music_body(rows, cover, height: int, style: str, look=()):
    """The part of the music card that stays while a song plays: (picture of cover + text, strip width, accent
    colour or None). Costs the text rendering (fit_lines) – cached by HudWindow.render per song."""
    accent = None
    if "accent" in look:
        from .media import accent as cover_accent
        accent = cover_accent(cover)
    blur = max(2, height // 300)
    pad = 3 * blur
    if style == "compact":
        pic = render_music_compact(rows, cover, height, look)
        return pic, pic.width - 2 * pad, accent
    lines = fit_lines(rows, height, [TITLE_SCALE if i == 0 else 1.0 for i in range(len(rows))])
    side = max(32, height // 6) if cover is not None else 0
    gap = max(4, height // 120) if cover is not None else 0
    text_w = max((im.width for im in lines), default=0)
    text_h = sum(im.height - pad for im in lines) + (pad if lines else 0)
    w = max(side + 2 * pad, text_w)
    h = (pad + side + gap - pad if cover is not None else 0) + text_h
    pic = Image.new("RGBA", (max(1, w), max(1, h)), (0, 0, 0, 0))
    if cover is not None:
        art = cover.convert("RGBA").resize((side, side), Image.LANCZOS)
        mask = Image.new("L", (side, side), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, side - 1, side - 1),
                                               radius=cover_radius(look, side, max(2, side // 14)), fill=255)
        art.putalpha(mask)
        ax = (w - side) // 2
        shadow = Image.new("RGBA", pic.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 200), (ax, pad), mask)
        pic.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))
        pic.alpha_composite(art, (ax, pad))
    y = pad + side + gap - pad if cover is not None else 0
    for im in lines:
        pic.alpha_composite(im, ((w - im.width) // 2, y))
        y += im.height - pad
    return pic, max(side, text_w - 2 * pad), accent


def music_card(body, height: int, style: str, progress=None, look=(), upnext=None,
               upnext_pos: str = "below", anim=None, min_w: int = 0, min_h: int = 0) -> Image.Image:
    """The music card from its body (music_body): the progress strip below it (``progress`` = (elapsed, total)
    seconds), then the Spotify queue ``upnext`` = (label, items) below or to the right (1.8; ``anim`` = the
    sliding rows of a song change, 1.8.1), on the dark area if "backdrop" is in ``look``. Cheap – drawn every
    second while a song plays."""
    pic, strip_w, accent = body
    if progress:
        strip = progress_strip(strip_w, *progress, height, accent if "accent" in look else None,
                               "remaining" in look)
        pic = _below(pic, strip, style != "compact")
    if upnext and upnext[1]:
        items = upnext[1]
        if upnext_pos == "right":                    # 1.8.24: as many rows as fit beside the card
            items = items[:upnext_rows(upnext[0], items, height, pic.height)]
        block = upnext_block(upnext[0], items, height, anim)
        pic = _beside(pic, block, max(6, height // 120)) if upnext_pos == "right" else \
            _below(pic, block, style != "compact")
    if "backdrop" in look:                       # the dark area round the padded picture: the whole card keeps its size
        pad2 = 2 * max(4, height // 160)          # (backdrop's own edge)
        pic = pad_to(pic, min_w - pad2, style != "compact", min_h - pad2)
        return backdrop(pic, height)
    return pad_to(pic, min_w, style != "compact", min_h)


@lru_cache(maxsize=16)
def guide_line(length: int, vertical: bool, dash: int = 14) -> Image.Image:
    """A centre guide line (1.64.5, user: "Mittellinie als Kreuz beim Ausrichten"): 3 px – light dashes on a dark
    edge, visible on bright and dark game pictures alike. 1.46.4: cached – drawn on every tick while arranging only
    to be dropped by set_picture (same key); the picture is only read afterwards, never changed."""
    w, h = (3, length) if vertical else (length, 3)
    pic = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(pic)
    d.rectangle((0, 0, w - 1, h - 1), fill=(0, 0, 0, 150))
    for i in range(0, length, 2 * dash):
        if vertical:
            d.line([(1, i), (1, min(length - 1, i + dash - 1))], fill=(255, 255, 255, 230))
        else:
            d.line([(i, 1), (min(length - 1, i + dash - 1), 1)], fill=(255, 255, 255, 230))
    return pic


REC_DOT = (229, 83, 75, 255)      # 1.4.1: theme.DOT "err" red


def rec_dot(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float):
    """1.4.1/1.5.2: the red "recording" dot with a dark ring – right of the round timer in every style."""
    ring = max(1, int(r // 3))
    d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=(20, 20, 22, 230))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=REC_DOT)


def rec_phase(now: float | None = None) -> bool:
    """Blink of the recording dot: on during even seconds, off during odd ones (1 s period)."""
    return int(time.time() if now is None else now) % 2 == 0


def info_card(timer: str, server: str, ping, note: str, record: str, text_h: int, style: str = "classic",
              accent=None, transparent: bool = True, dark_area: bool = False, rec=None, memo=()) -> Image.Image:
    """1.8.24 (user: "Zeit etc. nicht mehr mit der Map verbunden, eigene Elemente – ich will ab und zu nur die
    eigentliche Map-Grösse ändern"): timer, note, record, server and ping as a card of their own – the same lines
    as below the map, without the map; shared by the overlay (App.info_win) and the preview."""
    if style != "classic":
        from .skin import map_card
        return map_card(None, "", "", timer, note, record, server, ping, (), text_h, style, accent, rec=rec,
                        memo=memo)
    pic = add_info(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), timer, server, text_h, backdrop=not transparent,
                   ping=ping, note=note, record=record, rec=rec, memo=memo)
    return map_backdrop([pic], text_h)[0] if dark_area else pic


# ---- 1.39: the input card ("Eingaben") – keys / mouse or gamepad, drawn from inputs.InputState
INPUT_GAP = 0.14                       # gap between keys, in key widths (u)
INPUT_PAD = 0.30                       # card padding (u)
INPUT_W = 5 + 6 * INPUT_GAP + 1.75     # content: five key columns, a double gap, the mouse
INPUT_H = 3 + 2 * INPUT_GAP            # three key rows
INPUT_RATIO = (INPUT_W + 2 * INPUT_PAD) / (INPUT_H + 2 * INPUT_PAD)    # width / height – the same for both layouts
INPUT_SS = 2                           # drawn at twice the size, then scaled down: smooth round corners
INPUT_BG = (16, 18, 22, 210)
INPUT_IDLE = (255, 255, 255, 26)
INPUT_EDGE = (255, 255, 255, 70)
INPUT_CAP = (225, 228, 235, 215)
INPUT_CAP_DOWN = (18, 18, 20, 255)
PAD_FACE = {"a": (96, 186, 70, 255), "b": (222, 74, 64, 255), "x": (64, 128, 226, 255), "y": (238, 190, 52, 255)}
_INPUT_MEMO: dict = {}
INPUT_KEPT = 128                       # whole cards kept by state (a round has a few dozen different ones)
_INPUT_PATCHES: dict = {}             # idle cards and the patch of each control state drawn so far
INPUT_PATCHES_KEPT = 600


def _input_keys():
    """(id, x, y, w, h, cap) of the keyboard cluster in key units: Q W E R over A S D, SHIFT / CTRL on the left,
    SPACE under A–R."""
    from .inputs import KEYS
    caps = {k: cap for k, _vk, cap in KEYS}
    col = lambda i: i * (1 + INPUT_GAP)      # noqa: E731
    row = col
    out = [(k, col(i + 1), row(0), 1, 1) for i, k in enumerate(("q", "w", "e", "r"))]
    out += [("shift", col(0), row(1), 1, 1)] + [(k, col(i + 1), row(1), 1, 1) for i, k in enumerate(("a", "s", "d"))]
    out += [("ctrl", col(0), row(2), 1, 1), ("space", col(1), row(2), 4 + 3 * INPUT_GAP, 1)]
    return [(k, x, y, w, h, caps[k]) for k, x, y, w, h in out]


def _cap_font(size: float):
    from .skin import inter
    return inter("Bold", max(6, int(size)))


def _centred_text(d, cx, cy, text, font, fill):
    if not text:
        return
    box = d.textbbox((0, 0), text, font=font)
    d.text((cx - (box[0] + box[2]) / 2, cy - (box[1] + box[3]) / 2), text, font=font, fill=fill)


def _draw_keyboard(d, pic, st, u, ox, oy, accent):
    down = st.keys
    for k, x, y, w, h, cap in _input_keys():
        x0, y0 = ox + x * u, oy + y * u
        box = [x0, y0, x0 + w * u, y0 + h * u]
        on = k in down
        d.rounded_rectangle(box, radius=0.18 * u, fill=accent if on else INPUT_IDLE,
                            outline=None if on else INPUT_EDGE, width=max(1, int(0.04 * u)))
        _centred_text(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, cap,
                      _cap_font((0.42 if len(cap) == 1 else 0.24) * u), INPUT_CAP_DOWN if on else INPUT_CAP)
    # the mouse: a rounded body, the top split into left / right, the wheel button in the middle
    mx, mw, mh = ox + (5 + 6 * INPUT_GAP) * u, 1.75 * u, INPUT_H * u
    body = [mx, oy, mx + mw, oy + mh]
    split = oy + 1.35 * u
    mask = Image.new("L", pic.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(body, radius=0.85 * u, fill=255)
    fill = Image.new("RGBA", pic.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fill)
    fd.rectangle(body, fill=INPUT_IDLE)
    for k, x0, x1 in (("lmb", mx, mx + mw / 2), ("rmb", mx + mw / 2, mx + mw)):
        if k in down:
            fd.rectangle([x0, oy, x1, split], fill=accent)
    pic.alpha_composite(Image.composite(fill, Image.new("RGBA", pic.size, (0, 0, 0, 0)), mask))
    line = max(1, int(0.04 * u))
    d.rounded_rectangle(body, radius=0.85 * u, outline=INPUT_EDGE, width=line)
    d.line([mx, split, mx + mw, split], fill=INPUT_EDGE, width=line)
    d.line([mx + mw / 2, oy, mx + mw / 2, split], fill=INPUT_EDGE, width=line)
    wx, ww = mx + mw / 2, 0.30 * u
    wheel = [wx - ww / 2, oy + 0.32 * u, wx + ww / 2, oy + 0.95 * u]
    d.rounded_rectangle(wheel, radius=ww / 2, fill=accent if "mmb" in down else (34, 36, 42, 255),
                        outline=INPUT_EDGE, width=line)


def _draw_gamepad(d, st, u, ox, oy, accent):
    line = max(1, int(0.04 * u))
    small = _cap_font(0.24 * u)

    def at(x, y):
        return ox + x * u, oy + y * u

    for name, x0, x1, value, rtl in (("LT", 0.2, 2.3, st.lt, False), ("RT", INPUT_W - 2.3, INPUT_W - 0.2, st.rt,
                                                                          True)):
        a, b = at(x0, 0.0), at(x1, 0.34)
        d.rounded_rectangle([a[0], a[1], b[0], b[1]], radius=0.1 * u, fill=INPUT_IDLE, outline=INPUT_EDGE,
                            width=line)
        if value > 0:
            wfill = (b[0] - a[0]) * value
            fx0, fx1 = (b[0] - wfill, b[0]) if rtl else (a[0], a[0] + wfill)
            d.rounded_rectangle([fx0, a[1], fx1, b[1]], radius=0.1 * u, fill=accent)
        _centred_text(d, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, name, small,
                      INPUT_CAP_DOWN if value >= 0.5 else INPUT_CAP)
    for k, x0, x1 in (("lb", 0.2, 2.3), ("rb", INPUT_W - 2.3, INPUT_W - 0.2)):
        a, b = at(x0, 0.48), at(x1, 0.88)
        on = k in st.pad
        d.rounded_rectangle([a[0], a[1], b[0], b[1]], radius=0.2 * u, fill=accent if on else INPUT_IDLE,
                            outline=None if on else INPUT_EDGE, width=line)
        _centred_text(d, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, k.upper(), small,
                      INPUT_CAP_DOWN if on else INPUT_CAP)
    for k, x in (("back", 3.3), ("start", INPUT_W - 3.3 - 0.5)):
        a, b = at(x, 1.15), at(x + 0.5, 1.41)
        d.rounded_rectangle([a[0], a[1], b[0], b[1]], radius=0.13 * u, fill=accent if k in st.pad else INPUT_IDLE,
                            outline=INPUT_EDGE, width=line)
    for k, (cx, cy), r, knob, travel, sx, sy in (("ls", (1.25, 2.3), 0.78, 0.36, 0.42, st.lx, st.ly),
                                                 ("rs", (4.65, 2.62), 0.62, 0.30, 0.32, st.rx, st.ry)):
        c = at(cx, cy)
        d.ellipse([c[0] - r * u, c[1] - r * u, c[0] + r * u, c[1] + r * u], fill=INPUT_IDLE,
                  outline=accent if k in st.pad else INPUT_EDGE, width=line * (3 if k in st.pad else 1))
        kx, ky = c[0] + sx * travel * u, c[1] - sy * travel * u
        moved = k in st.pad or sx or sy
        d.ellipse([kx - knob * u, ky - knob * u, kx + knob * u, ky + knob * u],
                  fill=accent if moved else (60, 63, 72, 255), outline=INPUT_EDGE, width=line)
    cx, cy = at(2.95, 2.62)
    arm, half = 0.55 * u, 0.19 * u
    for k, box in (("up", [cx - half, cy - arm, cx + half, cy - half]), ("down", [cx - half, cy + half, cx + half,
                                                                                    cy + arm]),
                   ("left", [cx - arm, cy - half, cx - half, cy + half]),
                   ("right", [cx + half, cy - half, cx + arm, cy + half])):
        d.rectangle(box, fill=accent if k in st.pad else INPUT_IDLE, outline=INPUT_EDGE, width=line)
    d.rectangle([cx - half, cy - half, cx + half, cy + half], fill=INPUT_IDLE)
    face = _cap_font(0.34 * u)
    bx, by = at(6.35, 2.12)
    for k, dx, dy in (("y", 0, -0.6), ("a", 0, 0.6), ("x", -0.6, 0), ("b", 0.6, 0)):
        x, y, r = bx + dx * u, by + dy * u, 0.32 * u
        on = k in st.pad
        d.ellipse([x - r, y - r, x + r, y + r], fill=PAD_FACE[k] if on else INPUT_IDLE,
                  outline=None if on else INPUT_EDGE, width=line)
        _centred_text(d, x, y, k.upper(), face, INPUT_CAP_DOWN if on else PAD_FACE[k])


def input_size(height: int) -> tuple:
    """(w, h) of the input card at ``height`` px – the same for keyboard and gamepad (switching moves nothing)."""
    h = max(24, int(height))
    return int(round(h * INPUT_RATIO)), h


def _input_full(st, layout: str, w: int, h: int, acc, backdrop: bool) -> Image.Image:
    """The whole card drawn for ``st`` (supersampled, box-filtered down: a control changes only its own pixels)."""
    S = INPUT_SS
    pic = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(pic)
    u = h * S / (INPUT_H + 2 * INPUT_PAD)
    if backdrop:
        d.rounded_rectangle([0, 0, pic.width - 1, pic.height - 1], radius=0.35 * u, fill=INPUT_BG)
    ox = (pic.width - INPUT_W * u) / 2
    oy = INPUT_PAD * u
    if layout == "gamepad":
        _draw_gamepad(d, st, u, ox, oy, acc)
    else:
        _draw_keyboard(d, pic, st, u, ox, oy, acc)
    return pic.reduce(S)


def _input_controls(layout: str):
    """(name, unit box (x, y, w, h), part(st) -> hashable, state(part) -> InputState) of every control that can
    change – a control's part is what the card shows of it; ``state`` = an InputState with only that part."""
    from .inputs import KEY_IDS, MOUSE_IDS, InputState, stick_steps
    E = frozenset()
    if layout != "gamepad":
        out = [(k, (x, y, w, h), (lambda st, k=k: k in st.keys),
                (lambda part, k=k: InputState(keys=frozenset({k}) if part else E)))
               for k, x, y, w, h, _cap in _input_keys()]
        out.append(("mouse", (5 + 6 * INPUT_GAP, 0, 1.75, INPUT_H),
                    lambda st: tuple(sorted(st.keys & frozenset(MOUSE_IDS))),
                    lambda part: InputState(keys=frozenset(part))))
        assert all(k in KEY_IDS for k, *_r in out if k != "mouse")
        return out
    W = INPUT_W
    out = []
    for k, box in (("lb", (0.2, 0.48, 2.1, 0.4)), ("rb", (W - 2.3, 0.48, 2.1, 0.4)),
                   ("back", (3.3, 1.15, 0.5, 0.26)), ("start", (W - 3.8, 1.15, 0.5, 0.26)),
                   ("y", (6.03, 1.2, 0.64, 0.64)), ("a", (6.03, 2.4, 0.64, 0.64)),
                   ("x", (5.43, 1.8, 0.64, 0.64)), ("b", (6.63, 1.8, 0.64, 0.64))):
        out.append((k, box, (lambda st, k=k: k in st.pad), (lambda part, k=k: InputState(pad=frozenset({k}) if part
                                                                                          else E))))
    dirs = frozenset(("up", "down", "left", "right"))
    out.append(("dpad", (2.4, 2.07, 1.1, 1.1), lambda st: tuple(sorted(st.pad & dirs)),
                lambda part: InputState(pad=frozenset(part))))
    out.append(("lt", (0.2, 0.0, 2.1, 0.34), lambda st: round(st.lt * 8), lambda q: InputState(lt=q / 8)))
    out.append(("rt", (W - 2.3, 0.0, 2.1, 0.34), lambda st: round(st.rt * 8), lambda q: InputState(rt=q / 8)))
    out.append(("ls", (0.47, 1.52, 1.56, 1.56), lambda st: (stick_steps(st.lx, st.ly), "ls" in st.pad),
                lambda part: InputState(lx=part[0][0], ly=part[0][1], pad=frozenset({"ls"}) if part[1] else E)))
    out.append(("rs", (4.03, 2.0, 1.24, 1.24), lambda st: (stick_steps(st.rx, st.ry), "rs" in st.pad),
                lambda part: InputState(rx=part[0][0], ry=part[0][1], pad=frozenset({"rs"}) if part[1] else E)))
    return out


INPUT_EDGE_PX = 2                      # pixels around a control's box that its patch takes along


def _input_box(box, w: int, h: int) -> tuple:
    """A control's unit box → its pixel box on the card (with INPUT_EDGE_PX), clipped to the card."""
    u = h / (INPUT_H + 2 * INPUT_PAD)
    ox, oy = (w - INPUT_W * u) / 2, INPUT_PAD * u
    x, y, bw, bh = box
    m = INPUT_EDGE_PX
    return (max(0, int(ox + x * u) - m), max(0, int(oy + y * u) - m),
            min(w, int(math.ceil(ox + (x + bw) * u)) + m), min(h, int(math.ceil(oy + (y + bh) * u)) + m))


def input_card(st, layout: str, height: int, accent=None, backdrop: bool = True) -> Image.Image:
    """1.39: the card "Eingaben" – ``st`` (inputs.InputState) as a keyboard cluster with the mouse or as a gamepad
    (``layout``), ``height`` px tall, held keys in ``accent``. Always the same size for a height (never breathes).
    Put together from the idle card and one patch per control that shows something (each patch drawn once, the
    first time that control is in that state) – a new state costs a few pastes, not a whole drawing; the result is
    the same as drawing the whole card (test_the_input_card_from_patches_is_the_whole_drawing). Returns a copy."""
    from .skin import accent_rgba
    acc = accent_rgba(accent)
    w, h = input_size(height)
    layout = "gamepad" if layout == "gamepad" else "keyboard"
    base_key = (layout, w, h, acc, bool(backdrop))
    controls = _input_controls(layout)
    parts = tuple((name, part(st)) for name, _box, part, _state in controls)
    key = (base_key, tuple(p for p in parts if p[1]))
    hit = _INPUT_MEMO.get(key)
    if hit is not None:
        _INPUT_MEMO[key] = _INPUT_MEMO.pop(key)                       # recently used: kept longest
        return hit.copy()
    base = _INPUT_PATCHES.get(base_key)
    if base is None:
        from .inputs import EMPTY
        base = _INPUT_PATCHES[base_key] = _input_full(EMPTY, layout, w, h, acc, backdrop)
    out = base.copy()
    for (name, box, _part, state), (_n, value) in zip(controls, parts):
        if not value:
            continue
        pkey = (base_key, name, value)
        patch = _INPUT_PATCHES.get(pkey)
        if patch is None:
            px = _input_box(box, w, h)
            pic = _input_full(state(value), layout, w, h, acc, backdrop).crop(px)
            # only the pixels this control changes: neighbouring boxes may overlap by their edge, and a patch must
            # never put an idle edge over a held neighbour
            changed = np.any(np.asarray(pic) != np.asarray(base.crop(px)), axis=2)
            patch = _INPUT_PATCHES[pkey] = (px, pic, Image.fromarray((changed * 255).astype(np.uint8), "L"))
        out.paste(patch[1], patch[0][:2], patch[2])
    _INPUT_MEMO[key] = out
    while len(_INPUT_MEMO) > INPUT_KEPT:
        _INPUT_MEMO.pop(next(iter(_INPUT_MEMO)))
    while len(_INPUT_PATCHES) > INPUT_PATCHES_KEPT:
        _INPUT_PATCHES.pop(next(iter(_INPUT_PATCHES)))
    return out.copy()
