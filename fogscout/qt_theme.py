"""Colours and style sheet of the Qt control window (pure, no Qt import: testable without a display).

The palette is the original one of the program (theme.DARK, user's wish 1.51: "Farben wie am Anfang"): greys
#1e1f22 / #2b2d31, gold accent #c9a227, DBD red for selections; the status colours are theme.DOT.
"""
from __future__ import annotations

import colorsys
import os
import tempfile
from functools import lru_cache

from .i18n import N_
from .theme import DARK, DOT

ZOOMS = (0.9, 1.0, 1.1, 1.25, 1.5)        # setting ui_zoom: text size of the window

PALETTE = {
    True: dict(DARK, card=DARK["panel"], nav=DARK["panel"], nav_sel=DARK["bg"], btn=DARK["hover"],
               btn_hover=DARK["press"], press="#2f3136", sel_bg=DARK["press"], btn_dis="#2b2d31", fg_dis="#6a6e75", on_accent="#1a1406",
               bar=DARK["field"], head="#ffffff", accent_hover="#d8b43a", danger="#ff9a94"),
    False: {"bg": "#f3f3f4", "panel": "#ffffff", "field": "#ffffff", "border": "#d6d7da", "fg": "#1b1c1e",
            "dim": "#5f636a", "accent": "#8a6a12", "select": "#7a1f1f", "hover": "#e9eaec", "press": "#dcdde0", "sel_bg": "#dcdde0",
            "card": "#ffffff", "nav": "#e9eaec", "nav_sel": "#f3f3f4", "btn": "#ffffff", "btn_hover": "#e9eaec",
            "btn_dis": "#f3f3f4", "fg_dis": "#a2a5aa", "on_accent": "#ffffff", "bar": "#e4e5e8", "head": "#000000",
            "accent_hover": "#76590f", "danger": "#b42a22"},
}
# 1.22.3 (audit prompt.md, contrast measured with contrast()): colours of state and of the editor's media, per
# mode – until then the dark values (theme.DOT, white playhead, orange marks) were used on light pages too (white
# on white 1.0:1, warnings 2.5:1). Text colours >= 4.5:1 on card/bg/field/panel and on their own 12 % pill tint.
STATE = {
    True: {"ok": "#56d364", "warn": "#e3b341", "err": "#ff7b72", "info": "#79c0ff", "idle": DOT["idle"],
           "playhead": "#ffffff", "mark": "#e8a33d", "media_bg": DARK["field"], "on_select": "#ffffff"},
    False: {"ok": "#116329", "warn": "#7d4e00", "err": "#a40e26", "info": "#0550ae", "idle": "#5f636a",
            "playhead": "#1b1c1e", "mark": "#a15c00", "media_bg": DARK["field"], "on_select": "#ffffff"},
}
STATE_KINDS = ("ok", "warn", "err", "info")
PILL_TINT = 0.12


# Colour themes (since 1.62, user's wish): the accent (and for OLED the dark greys) over the palette above. Every
# accent is checked for contrast (tests/test_qt.py): text on cards >= 4.5:1, text on accent buttons >= 4.5:1.
THEMES = {
    "gold": (N_("Gold (Standard)"), {True: {}, False: {}}),
    "red": (N_("Blutrot"), {
        True: {"accent": "#f07a74", "accent_hover": "#f4938e", "on_accent": "#14070a", "select": "#7a1f1f"},
        False: {"accent": "#a8261f", "accent_hover": "#bf3a33", "on_accent": "#ffffff", "select": "#7a1f1f"}}),
    "blue": (N_("Eisblau"), {
        True: {"accent": "#5aaee8", "accent_hover": "#7cc0ee", "on_accent": "#06121c", "select": "#1d4f80"},
        False: {"accent": "#1d5fa6", "accent_hover": "#2a70bd", "on_accent": "#ffffff", "select": "#1d4f80"}}),
    "green": (N_("Giftgrün"), {
        True: {"accent": "#52c48a", "accent_hover": "#72d4a2", "on_accent": "#04140b", "select": "#1b5e3c"},
        False: {"accent": "#1c7a48", "accent_hover": "#176a3e", "on_accent": "#ffffff", "select": "#1b5e3c"}}),
    "violet": (N_("Lila"), {
        True: {"accent": "#b48cf0", "accent_hover": "#c3a2f4", "on_accent": "#12081f", "select": "#4e2f86"},
        False: {"accent": "#6b3fb3", "accent_hover": "#7c50c4", "on_accent": "#ffffff", "select": "#4e2f86"}}),
    "custom": (N_("Eigene Farbe"), None),         # 1.63: settings accent_custom, made readable by derive_accent
}
# The palette below the theme list (1.63, user's wish): one click = this colour as own accent (theme "custom").
# Base colours; derive_accent makes each one readable in dark, light and OLED.
# 1.23 (audit, prompt.md, Phase 3 design system): the window's sizes in one place, px at 100 % – TYPE scales with
# the text zoom (ui_zoom), RADIUS and PAD_CARD do not. stylesheet(), qt_editor.editor_qss() and the cards take them
# from here; a radius of half an element's own height (round handles, swatches) stays where the element is styled.
TYPE = {"label": 11, "small": 12, "body": 13, "nav": 14, "big": 16, "h1": 21, "display": 22}
RADIUS = {"xs": 2, "bar": 3, "s": 4, "m": 6, "l": 8, "xl": 10}
PAD_CARD = (14, 12, 14, 12)               # a card's content: left, top, right, bottom
ICON = {"s": 14, "m": 16, "l": 20}         # 1.24: glyph sizes (qt_icons) – in text, on buttons, the brand
SWATCHES = ("#c9a227", "#e08a1e", "#e8692a", "#d93a32", "#b0203a", "#e0508f", "#c040c0", "#8a5cf0",
            "#4f5fe0", "#2f8fe0", "#1fb5c9", "#17a38a", "#3cae4f", "#8cbf26")
CUSTOM_DEFAULT = "#2f8fe0"
MIN_CONTRAST = 4.5
# OLED black (1.62.1, user: "mit OLED mehr Farbkombis"): a switch of its own, true black instead of the dark greys
# – with every accent; the light mode stays as it is
OLED = {"bg": "#000000", "panel": "#0d0d0f", "field": "#0a0a0b", "card": "#0d0d0f", "nav": "#0d0d0f",
        "nav_sel": "#000000", "btn": "#1a1b1e", "btn_hover": "#26282c", "hover": "#1a1b1e", "press": "#33363b", "sel_bg": "#26282c",
        "border": "#26282a", "bar": "#141416", "btn_dis": "#0d0d0f"}
_theme, _oled, _custom, _dark, _zoom = "gold", False, CUSTOM_DEFAULT, True, 1.0


def set_theme(key: str, oled: bool = False, custom: str | None = None):
    """The colour theme the window uses from now on (settings color_theme, oled_black, accent_custom; unknown =
    gold, a broken own colour = CUSTOM_DEFAULT)."""
    global _theme, _oled, _custom
    _theme = key if key in THEMES else "gold"
    _oled = bool(oled)
    _custom = norm_hex(custom) or CUSTOM_DEFAULT


def set_dark(dark: bool, zoom: float | None = None):
    """1.22.3: the mode (and text zoom) the window shows now (MainWindow.apply_theme) – for what is coloured or
    sized without a page at hand (status pill, value colours of the facts, the overlay preview's note, the clip
    editor's own style sheet)."""
    global _dark, _zoom
    _dark = bool(dark)
    if zoom is not None:
        _zoom = float(zoom)


def current_dark() -> bool:
    return _dark


def current_zoom() -> float:
    return _zoom


def look_key() -> tuple:
    """1.24.5 (phase 2, measured): what colours(current_dark()) depends on – a cheap key for callers that only need
    to know whether the colours changed (qt_common.set_glyph runs on every refresh; building the palette there cost
    ~30 µs a call)."""
    return _dark, _theme, _oled, _custom


def colours(dark: bool) -> dict:
    """The palette of the current theme: PALETTE with the theme's accent over it, OLED black when dark; the state
    and media colours of STATE."""
    c = dict(PALETTE[bool(dark)])
    c.update(STATE[bool(dark)])
    if dark and _oled:
        c.update(OLED)
    if _theme == "custom":
        c.update(derive_accent(_custom, bool(dark), c["card"], c["bg"], c["nav"]))
    else:
        c.update(THEMES[_theme][1][bool(dark)])
    c["handle"] = _handle(c)
    return c


HANDLE_CONTRAST = 3.0     # 1.25: grips and scroll handles are controls – >= 3:1 on page and card (WCAG 1.4.11)


def _handle(c: dict) -> str:
    """1.25 (audit: scroll handles at 1.1–1.5:1, card grips 1.3:1 – invisible in light mode and OLED): the resting
    colour of a grip, a scroll handle and a slider knob's edge – the dim text colour over the page, only as strong as
    it must be to reach HANDLE_CONTRAST on both the page and a card (hover: the dim colour itself)."""
    for step in range(30, 101, 5):
        colour = blend(c["dim"], c["bg"], step / 100)
        if all(contrast(colour, bg) >= HANDLE_CONTRAST for bg in (c["bg"], c["card"])):
            return colour
    return c["dim"]


def norm_hex(text) -> str | None:
    """'#rrggbb' (lower case) or None for anything else ('#abc' is widened)."""
    t = str(text or "").strip().lower().lstrip("#")
    if len(t) == 3:
        t = "".join(ch * 2 for ch in t)
    if len(t) != 6 or any(ch not in "0123456789abcdef" for ch in t):
        return None
    return "#" + t


def luminance(colour: str) -> float:
    """Relative luminance (WCAG 2)."""
    c = hex_colour(colour).lstrip("#")
    out = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255
        out.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _hls_hex(h, lum, s) -> str:
    r, g, b = colorsys.hls_to_rgb(h, min(1.0, max(0.0, lum)), s)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


@lru_cache(maxsize=64)
def derive_accent(base: str, dark: bool, *backgrounds: str) -> dict:
    """accent / accent_hover / on_accent / select from any colour (1.63, own colour + palette): same hue, the
    lightness moved just as far as needed – accent on every background >= 4.5:1, text on the accent button (and
    its hover) >= 4.5:1, white on the selection >= 4.5:1. A colour that is readable already stays as it is."""
    c = norm_hex(base) or CUSTOM_DEFAULT
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, lum, s = colorsys.rgb_to_hls(r, g, b)
    ink = "#000000" if dark else "#ffffff"           # text on the accent button

    def ok(colour):
        return (all(contrast(colour, bg) >= MIN_CONTRAST for bg in backgrounds)
                and contrast(ink, colour) >= MIN_CONTRAST)

    step = 0.01 if dark else -0.01                   # dark: lighter; light: darker – both end at white / black
    accent = _hls_hex(h, lum, s)
    for _n in range(101):
        if ok(accent):
            break
        lum = min(1.0, max(0.0, lum + step))
        accent = _hls_hex(h, lum, s)
    hover_l = lum + 0.07 if dark else lum - 0.06     # hover away from the background: stays readable
    hover = _hls_hex(h, hover_l, s)
    if contrast(ink, hover) < MIN_CONTRAST:
        hover = accent
    sel_l = 0.30
    select = _hls_hex(h, sel_l, min(s, 0.6))
    while contrast("#ffffff", select) < MIN_CONTRAST and sel_l > 0:
        sel_l -= 0.02
        select = _hls_hex(h, sel_l, min(s, 0.6))
    return {"accent": accent, "accent_hover": hover, "on_accent": ink, "select": select}


def hex_colour(c) -> str:
    """'#rrggbb' from an (r, g, b[, a]) tuple (sysinfo / overlay colours) or a '#rrggbb' string."""
    if isinstance(c, str):
        return c
    return "#{:02x}{:02x}{:02x}".format(*c[:3])


def blend(colour: str, over: str, alpha: float) -> str:
    """'#rrggbb' of ``colour`` at ``alpha`` over ``over`` (what a tint looks like on a card)."""
    a, b = hex_colour(colour).lstrip("#"), hex_colour(over).lstrip("#")
    return "#" + "".join(f"{round(int(b[i:i + 2], 16) + (int(a[i:i + 2], 16) - int(b[i:i + 2], 16)) * alpha):02x}"
                         for i in (0, 2, 4))


def rgba(colour: str, alpha: float) -> str:
    c = hex_colour(colour).lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return f"rgba({r}, {g}, {b}, {round(alpha * 255)})"


def dot_colour(style: str, dark: bool | None = None) -> str:
    """Colour of a status kind as used by status.DOT_STYLE ('ok', 'warn', 'err', 'info', 'idle') – 1.22.3: the
    one of the mode shown (STATE), readable on light pages too."""
    c = colours(_dark if dark is None else dark)
    return c[style] if style in STATE_KINDS else c["idle"]


def readable(colour, dark: bool | None = None, bg: str | None = None) -> str:
    """1.22.3: ``colour`` as text on a card of the mode shown: a status colour of theme.DOT becomes the mode's own
    (STATE); any other one keeps its hue and gets just as much lighter (dark) or darker (light) as it takes for
    >= MIN_CONTRAST – the overlay's pastel ping/temperature colours were 1.4–2.8:1 on white."""
    dark = _dark if dark is None else bool(dark)
    c = colours(dark)
    hx = hex_colour(colour).lower()
    for kind in STATE_KINDS:
        if hx == DOT[kind]:
            return c[kind]
    bg = bg or c["card"]
    if contrast(hx, bg) >= MIN_CONTRAST:
        return hx
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, lum, s = colorsys.rgb_to_hls(r, g, b)
    step = 0.01 if dark else -0.01
    out = hx
    for _n in range(101):
        lum = min(1.0, max(0.0, lum + step))
        out = _hls_hex(h, lum, s)
        if contrast(out, bg) >= MIN_CONTRAST:
            break
    return out


ICON_DIR = os.path.join(tempfile.gettempdir(), "fogscout-ui")


@lru_cache(maxsize=32)
def ui_icon(name: str, colour: str) -> str:
    """1.8.8: a small picture for the style sheet (``check`` = tick of a ticked box, ``arrow`` = the chevron of a
    choice box) in ``colour``, drawn with Pillow at 16 px and 32 px (Qt takes ``@2x`` on a high-DPI screen); the
    path with forward slashes, "" when it cannot be written (Qt then draws nothing there)."""
    try:
        from PIL import Image, ImageDraw
        os.makedirs(ICON_DIR, exist_ok=True)
        base = os.path.join(ICON_DIR, f"{name}-{hex_colour(colour).lstrip('#')}")
        rgb = tuple(int(hex_colour(colour).lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        for scale, suffix in ((1, ""), (2, "@2x")):
            size, ss = 16 * scale, 8                           # drawn 8× larger, then scaled down: smooth edges
            big = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(big)
            u = size * ss / 16
            if name == "check":
                d.line([(3.5 * u, 8.5 * u), (6.5 * u, 11.5 * u), (12.5 * u, 4.5 * u)], fill=rgb + (255,),
                       width=round(2.2 * u), joint="curve")
            elif name == "dash":                               # 1.8.75: a group with some regions ticked
                d.line([(4 * u, 8 * u), (12 * u, 8 * u)], fill=rgb + (255,), width=round(2.2 * u))
            else:                                              # arrow: a chevron pointing down
                d.line([(4 * u, 6 * u), (8 * u, 10 * u), (12 * u, 6 * u)], fill=rgb + (255,), width=round(1.8 * u),
                       joint="curve")
            big.resize((size, size), Image.LANCZOS).save(base + suffix + ".png")
        return (base + ".png").replace("\\", "/")
    except Exception:
        return ""


def stylesheet(dark: bool, zoom: float = 1.0) -> str:
    """The whole window's QSS. Font sizes in px scale with the setting ui_zoom (Qt adds the screen scaling)."""
    c = colours(dark)

    def px(size):
        return f"{max(8, round(size * zoom))}px"

    return f"""
* {{ font-family: 'Segoe UI Variable Text', 'Segoe UI', 'Inter', sans-serif; font-size: {px(TYPE['body'])}; color: {c['fg']};
    placeholder-text-color: {c['dim']}; }}  /* 1.25: with `color` set, Qt drew placeholders as fg at 50 % (3.3:1) */
QMainWindow, QWidget#page, QStackedWidget, QScrollArea, QScrollArea > QWidget > QWidget {{ background: {c['bg']}; }}
QListWidget#nav {{ background: {c['nav']}; border: none; padding: 10px 6px; outline: 0; font-size: {px(TYPE['nav'])}; }}
QListWidget#nav::item {{ padding: 8px 12px; border-radius: {RADIUS['m']}px; margin: 1px 0; color: {c['dim']};
    border-left: 3px solid transparent; }}  /* same place selected or not */
QListWidget#nav::item:selected {{ background: {c['nav_sel']}; color: {c['accent']}; border-left: 3px solid {c['accent']};
    border-top-left-radius: 0; border-bottom-left-radius: 0; }}  /* 1.25: a straight mark, not a "(" */
QListWidget#nav::item:hover:!selected {{ background: {c['hover']}; color: {c['fg']}; }}
QFrame[class="card"] {{ background: {c['card']}; border: 1px solid {c['border']}; border-radius: {RADIUS['xl']}px; }}
QFrame[class="card"] QLabel {{ background: transparent; }}
QFrame[class="card"][dragging="true"], QFrame[class="card"][found="true"] {{ border: 1px solid {c['accent']}; }}
QFrame[class="card"][link="true"]:hover {{ border: 1px solid {c['accent']}; }}
QWidget#navside {{ background: {c['nav']}; }}
QPushButton#navsearch {{ margin: 12px 10px 2px 10px; background: {c['field']}; border: 1px solid {c['border']};
    border-radius: {RADIUS['m']}px; padding: 5px 8px; text-align: left; color: {c['dim']}; }}  /* 1.38.55: a search button */
QPushButton#navsearch:hover {{ background: {c['hover']}; color: {c['fg']}; }}
QPushButton#navsearch:pressed {{ background: {c['press']}; }}
QPushButton#navsearch:focus {{ border: 1px solid {c['accent']}; }}
QPushButton#navsearchbtn {{ background: transparent; border: none; margin-top: 10px; padding: 8px; }}
QPushButton#navsearchbtn:hover {{ background: {c['hover']}; }}
QPushButton#navsearchbtn:focus {{ border: 1px solid {c['accent']}; }}
QWidget#navbrand {{ background: {c['nav']}; }}  /* 1.24: the program's name above the navigation */
QLabel#brandname {{ font-size: {px(TYPE['big'])}; font-weight: 700; color: {c['head']}; }}
QFrame#navstatus {{ background: {c['nav']}; border: none; border-top: 1px solid {c['border']}; border-radius: 0; }}
QFrame#navstatus:hover {{ background: {c['hover']}; }}  /* 1.24: what Fog Scout does now, every page */
QFrame#navstatus:focus {{ border: 1px solid {c['accent']}; }}
QLabel#navstatustext {{ color: {c['fg']}; font-size: {px(TYPE['small'])}; background: transparent; }}
QLabel[class="subtitle"] {{ color: {c['dim']}; font-size: {px(TYPE['body'])}; }}  /* 1.24: a page's purpose */
QLabel[class="dim"] {{ color: {c['dim']}; font-size: {px(TYPE['small'])}; }}
QLabel[class="hint"] {{ color: {c['dim']}; font-size: {px(TYPE['small'])}; }}  /* 1.17.1: qt_pages.HintLabel – line length */
QLabel[class="h1"] {{ font-size: {px(TYPE['h1'])}; font-weight: 700; color: {c['head']}; }}
QLabel[class="map"] {{ font-family: 'Fira Sans ExtraBold', 'Segoe UI'; font-size: {px(TYPE['display'])}; color: {c['head']}; }}
QLabel[class="h2"] {{ font-size: {px(TYPE['small'])}; font-weight: 700; color: {c['fg']}; letter-spacing: 0.8px; }}  /* 1.17: the accent marks state, not every title */
QLabel[class="big"] {{ font-size: {px(TYPE['big'])}; font-weight: 700; color: {c['head']}; }}
QDialog#message {{ background: {c['bg']}; }}  /* 1.8.44: App._ask/_inform */
QTabWidget::pane {{ border: none; border-top: 1px solid {c['border']}; top: -1px; }}  /* 1.25: a line under the tabs –
   the rounded frame was drawn with open corners at 100/125 % and boxed cards a second time */
QTabWidget#formtabs::pane {{ background: {c['card']}; border: 1px solid {c['border']}; border-radius: {RADIUS['xl']}px; top: -1px;
    border-top-left-radius: 0; }}
QTabWidget#formtabs[found="true"]::pane {{ border: 1px solid {c['accent']}; }}
QTabWidget#formtabs QWidget#page {{ background: {c['card']}; }}
QTabWidget#formtabs > QTabBar::tab {{ font-weight: 600; padding: 8px 16px; }}
QTabBar::tab {{ background: transparent; color: {c['dim']}; padding: 7px 14px; border: none; }}
QTabBar[dense="true"]::tab {{ padding: 7px 9px; }}  /* 1.8.46/1.8.48: rows with many tabs (statistics) */
QTabBar::tab:selected {{ color: {c['accent']}; border-bottom: 2px solid {c['accent']}; }}
QTabBar::tab:hover:!selected {{ color: {c['fg']}; }}
QTabWidget#segments::pane {{ border: none; top: 0; }}  /* 1.11.14: the statistics' groups as a segment switch */
QTabBar#segbar::tab {{ background: transparent; color: {c['dim']}; border: 1px solid transparent; border-radius: {RADIUS['m']}px;
    padding: 5px 14px; margin: 0 4px 6px 0; }}
QTabBar#segbar::tab:selected {{ background: {c['btn_hover']}; color: {c['head']}; border: 1px solid {c['border']};
    font-weight: 600; }}  /* 1.17: a raised segment instead of a gold slab */
QTabBar#segbar::tab:hover:!selected {{ background: {c['hover']}; color: {c['fg']}; }}
QLabel[class="kpi"] {{ font-size: {px(TYPE['display'])}; font-weight: 700; color: {c['head']}; }}
QLabel[class="sub"] {{ color: {c['dim']}; font-size: {px(TYPE['label'])}; font-weight: 700; letter-spacing: 1px; padding-top: 6px; }}
QLabel[class="note"] {{ color: {c['warn']}; }}
QLabel#thumb {{ background: {c['media_bg']}; border-radius: {RADIUS['l']}px; }}  /* map pictures need a dark backdrop */
QFrame[class="tile"] {{ background: {c['card']}; border: 1px solid {c['border']}; border-radius: {RADIUS['l']}px; }}
QFrame[class="tile"]:hover {{ background: {c['hover']}; }}
QFrame[class="tile"]:focus {{ background: {c['hover']}; border: 1px solid {c['accent']}; }}  /* 1.8.72: arrows walk the tiles */
QFrame[class="tile"][current="true"] {{ border: 2px solid {c['accent']}; }}
QFrame[class="tile"] QLabel {{ background: transparent; border: none; }}
QFrame[class="tile"] QLabel#tilepic {{ background: {c['media_bg']}; border-radius: {RADIUS['m']}px; }}
QLabel[class="tile"] {{ font-size: {px(TYPE['small'])}; font-weight: 600; color: {c['head']}; }}
QLabel[class="tileinfo"] {{ font-size: {px(TYPE['label'])}; color: {c['dim']}; }}
QLabel[state="ok"] {{ color: {c['ok']}; }}  /* 1.24: state words – always beside a sign, never colour alone; after every QLabel class
   rule, so a dim/hint/big label keeps its size and takes the state's colour */
QLabel[state="warn"] {{ color: {c['warn']}; }}
QLabel[state="err"] {{ color: {c['err']}; }}
QLabel[state="off"] {{ color: {c['dim']}; }}
QListWidget#paletterows {{ background: transparent; border: none; outline: 0; }}  /* 1.26: the palette's rows */
QListWidget#realms {{ border: 1px solid {c['border']}; border-radius: {RADIUS['l']}px; padding: 4px; outline: 0; }}
QListWidget#realms::item {{ padding: 7px 0; border-radius: {RADIUS['m']}px; }}
QListWidget#realms::item:selected {{ background: {c['nav_sel']}; }}
QListWidget#realms::item:hover:!selected {{ background: {c['hover']}; }}
QFrame#roundrow {{ border-radius: {RADIUS['m']}px; }}  /* 1.17.1: overview "Letzte Runden" – a row opens the round */
QFrame#roundrow:hover {{ background: {c['hover']}; }}
QPushButton#fold {{ background: transparent; border: 1px solid transparent; padding: 2px 6px 2px 0; color: {c['dim']}; }}
QPushButton#fold:hover {{ color: {c['fg']}; }}
QPushButton#fold:focus {{ border-color: {c['accent']}; }}
QPushButton#rowplay {{ background: transparent; border: 1px solid transparent; padding: 0 6px; color: {c['dim']}; }}
QPushButton#rowplay:hover {{ color: {c['accent']}; border-color: {c['border']}; }}
QPushButton#rowplay:focus {{ border-color: {c['accent']}; }}  /* 1.22.3: the ID rule hid the keyboard focus */
QLabel#pill {{ border-radius: {RADIUS['xl']}px; padding: 3px 12px; font-size: {px(TYPE['small'])}; font-weight: 600; }}
QPushButton {{ background: {c['btn']}; border: 1px solid {c['border']}; border-radius: {RADIUS['m']}px; padding: 6px 14px; }}
QPushButton:hover {{ background: {c['btn_hover']}; }}
QPushButton:pressed {{ background: {c['press']}; }}
QPushButton:disabled {{ background: transparent; color: {c['fg_dis']}; border-color: {c['border']}; }}  /* keeps its shape */
QPushButton:focus {{ border-color: {c['accent']}; }}  /* 1.8.72: the keyboard focus is visible (was: like unfocused) */
QPushButton#primary {{ background: {c['accent']}; color: {c['on_accent']}; border: 1px solid {c['accent']}; font-weight: 700; }}
QPushButton#primary:hover {{ background: {c['accent_hover']}; }}
QPushButton#primary:pressed {{ background: {c['accent']}; border-color: {c['head']}; }}
QPushButton#primary:focus {{ border-color: {c['head']}; }}
QPushButton#primary:disabled {{ background: transparent; color: {c['fg_dis']}; border-color: {c['border']};
    font-weight: 600; }}  /* 1.22.3: the ID rule outranked :disabled – a disabled primary looked active */
QPushButton#danger {{ color: {c['danger']}; }}  /* 1.12.3: deletes or resets data (uimodel.danger) */
QPushButton#danger:hover {{ border-color: {c['danger']}; }}
QPushButton#danger:disabled {{ color: {c['fg_dis']}; border-color: {c['border']}; }}
QPushButton[class="seg"] {{ background: transparent; color: {c['dim']}; border-color: transparent; }}  /* 1.17 */
QPushButton[class="seg"]:hover {{ background: {c['hover']}; color: {c['fg']}; }}
QPushButton[class="seg"]:checked {{ background: {c['btn_hover']}; color: {c['head']}; border-color: {c['border']}; font-weight: 600; }}
QPushButton[class="seg"]:focus {{ border-color: {c['accent']}; }}  /* 1.22.3: the transparent border hid the focus */
QPushButton[class="seg"]:disabled {{ color: {c['fg_dis']}; }}
QProgressBar {{ background: {c['bar']}; border: none; border-radius: {RADIUS['bar']}px; max-height: 6px; min-height: 6px; }}
QProgressBar::chunk {{ background: {c['accent']}; border-radius: {RADIUS['bar']}px; }}
QProgressBar#factbar {{ max-height: 4px; min-height: 4px; border-radius: {RADIUS['xs']}px; }}
QProgressBar#factbar::chunk {{ background: {c['dim']}; border-radius: {RADIUS['xs']}px; }}  /* 1.17: ratio, not state */
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {c['handle']}; border-radius: {RADIUS['s']}px; min-height: 30px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar[idle="true"]::handle:vertical {{ background: transparent; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}  /* 1.17: like the vertical one */
QScrollBar::handle:horizontal {{ background: {c['handle']}; border-radius: {RADIUS['s']}px; min-width: 30px; }}
QScrollBar::handle:hover, QScrollBar::handle:pressed {{ background: {c['dim']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QTreeWidget {{ border: 1px solid {c['border']}; border-radius: {RADIUS['l']}px; padding: 4px; }}
QTreeWidget::item {{ padding: 3px 6px; }}
QHeaderView::section {{ padding: 3px 6px; }}
QTreeWidget::item:selected {{ background: {c['select']}; color: {c['on_select']}; }}
QTreeWidget::item:hover:!selected {{ background: {c['hover']}; }}  /* 1.24: the row under the mouse */
QTreeView::indicator {{ width: 16px; height: 16px; border: 1px solid {c['dim']}; border-radius: {RADIUS['s']}px;
    background: {c['field']}; }}  /* 1.8.75: the server regions' tick boxes like the page's (were Fusion's glyphs) */
QTreeView::indicator:hover {{ border-color: {c['accent']}; }}
QTreeView::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']};
    image: url("{ui_icon('check', c['on_accent'])}"); }}
QTreeView::indicator:indeterminate {{ border-color: {c['accent']}; image: url("{ui_icon('dash', c['accent'])}"); }}
QLineEdit {{ border: 1px solid {c['border']}; border-radius: {RADIUS['m']}px; padding: 5px 8px; }}
QLineEdit:focus {{ border-color: {c['accent']}; }}
QComboBox {{ background: {c['btn']}; border: 1px solid {c['border']}; border-radius: {RADIUS['m']}px; padding: 5px 28px 5px 10px; }}
QComboBox:hover {{ background: {c['btn_hover']}; }}
QComboBox:focus, QComboBox:on {{ border-color: {c['accent']}; }}
QComboBox:disabled {{ background: transparent; color: {c['fg_dis']}; }}
QComboBox:editable {{ background: {c['field']}; }}
QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: center right; width: 24px; border: none; }}
QComboBox::down-arrow {{ image: url("{ui_icon('arrow', c['dim'])}"); width: 12px; height: 12px; }}
QComboBox QAbstractItemView {{ background: {c['panel']}; border: 1px solid {c['border']}; padding: 4px; outline: 0;
    selection-background-color: {c['select']}; selection-color: {c['on_select']}; }}
QCheckBox {{ spacing: 8px; }}
QCheckBox::indicator {{ width: 16px; height: 16px; border: 1px solid {c['dim']}; border-radius: {RADIUS['s']}px;
    background: {c['field']}; }}
QCheckBox::indicator:hover, QCheckBox::indicator:focus {{ border-color: {c['accent']}; }}
QCheckBox::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']};
    image: url("{ui_icon('check', c['on_accent'])}"); }}
QCheckBox::indicator:disabled {{ border-color: {c['fg_dis']}; background: transparent; }}
QCheckBox::indicator:checked:disabled {{ background: {c['border']}; border-color: {c['border']}; }}
QToolTip {{ background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']}; padding: 4px; }}
"""


def palette_roles(dark: bool) -> dict:
    """QPalette roles (name -> colour) for what Qt's Fusion style draws itself: check boxes, sliders, choice
    boxes, text fields and lists – the style sheet only covers cards, buttons and labels."""
    c = colours(dark)
    return {"Window": c["bg"], "WindowText": c["fg"], "Base": c["field"], "AlternateBase": c["panel"],
            "Text": c["fg"], "Button": c["btn"], "ButtonText": c["fg"], "Highlight": c["accent"],
            "HighlightedText": c["on_accent"], "ToolTipBase": c["panel"], "ToolTipText": c["fg"],
            "PlaceholderText": c["dim"], "Light": c["hover"], "Midlight": c["border"], "Mid": c["border"],
            "Dark": c["bg"], "Shadow": "#000000", "BrightText": "#ffffff", "Link": c["accent"]}


def bar_style(colour) -> str:
    """Style of one value bar in the colour of its value (temperature, ping)."""
    return f"QProgressBar::chunk {{ background: {hex_colour(colour)}; border-radius: {RADIUS['bar']}px; }}"


def pill_style(style: str, dark: bool | None = None) -> str:
    col = dot_colour(style, dark)
    return f"background: {rgba(col, PILL_TINT)}; color: {col};"
