"""1.38 (user: "Gerne" – the local name template proposed after 1.37, before Claude): censor boxes over the places
where Dead by Daylight's HUD shows player names – no network, no Claude, nothing read from the game.

Two layouts, both measured on the user's own screenshots (names already pixelated there):
- "match": the survivor list bottom left while playing – clipedit.NAMES_BOX (1.7.4, ≈ 50–82 % of the height),
  the clip editor's „Namen links unten“ since 1.7.2.
- "spectate": while spectating the list sits higher – tests/data/end/spectate.jpg (3440×1440 at half size): the
  four names at x 336–432, y 297–497 of 1720×720 = 9.1–16.6 % of the 16:9 picture's width, 41–69 % of its height
  – and the watched player's name top centre (x 47–52 %, y 2–6 %). The boxes are a little larger: DBD's HUD scale
  can be set. The match box misses the upper two names there.
Lobby and result screen have no fixed places – that is where Claude helps (imageclaude, editorclaude).

``boxes`` gives fractions of the whole picture, the 16:9 game picture centred in it (black bars of an ultrawide
window left and right, of a narrow one top and bottom) – the rule of detector.viewport."""
from __future__ import annotations

from .clipedit import NAMES_BOX

# (x, y, w, h) as fractions of the 16:9 game picture
ZONES = {"match": (NAMES_BOX,),
         "spectate": ((0.085, 0.395, 0.10, 0.31), (0.43, 0.0, 0.14, 0.08))}


def game_rect(width: int, height: int) -> tuple:
    """(x, y, w, h) in pixels of the 16:9 picture inside a ``width`` × ``height`` frame."""
    vw = min(width, height * 16 / 9)
    vh = min(height, width * 9 / 16)
    return (width - vw) / 2, (height - vh) / 2, vw, vh


def boxes(kind: str, size: tuple) -> list:
    """The name boxes of ``kind`` ("match" | "spectate") as fractions (x, y, w, h) of a picture of ``size``."""
    w, h = max(1, int(size[0])), max(1, int(size[1]))
    gx, gy, gw, gh = game_rect(w, h)
    out = []
    for x, y, bw, bh in ZONES.get(kind, ()):
        out.append((round((gx + x * gw) / w, 4), round((gy + y * gh) / h, 4),
                    round(bw * gw / w, 4), round(bh * gh / h, 4)))
    return out


def add(existing, new, same: float = 0.01) -> list:
    """``existing`` boxes plus those of ``new`` not already there (each value within ``same``)."""
    out = [tuple(b) for b in existing]
    for b in new:
        if not any(all(abs(a - c) <= same for a, c in zip(b, o)) for o in out):
            out.append(tuple(b))
    return out
