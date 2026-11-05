"""1.38: the HUD's name places (hudnames) – measured on the user's screenshots, no Claude."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, hudnames, imageedit  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "data", "end", "spectate.jpg")
NAMES_PX = (336, 297, 432, 497)          # the pixelated names in spectate.jpg (1720×720), left, top, right, bottom
TOP_NAME_PX = (825, 15, 885, 45)         # the watched player's name


def _inside(rect_px, box, size):
    x0, y0, x1, y1 = rect_px
    w, h = size
    bx, by, bw, bh = box
    return bx * w <= x0 and by * h <= y0 and (bx + bw) * w >= x1 and (by + bh) * h >= y1


def test_the_spectate_boxes_cover_the_names_of_the_users_screenshot_the_match_box_does_not():
    from PIL import Image
    size = Image.open(DATA).size
    assert size == (1720, 720)
    left, top = hudnames.boxes("spectate", size)
    assert _inside(NAMES_PX, left, size) and _inside(TOP_NAME_PX, top, size)
    match, = hudnames.boxes("match", size)
    assert not _inside(NAMES_PX, match, size)              # the upper names sit above the match box
    assert match == pytest.approx(clipedit.names_box(*size), abs=1e-3)   # the same box as the clip editor's


def test_the_boxes_follow_the_game_picture_in_any_window():
    wide = hudnames.boxes("spectate", (3440, 1440))[0]        # black bars left and right
    full = hudnames.boxes("spectate", (2560, 1440))[0]        # 16:9 only
    narrow = hudnames.boxes("spectate", (1440, 1440))[0]      # bars top and bottom
    assert full == pytest.approx((0.085, 0.395, 0.10, 0.31))
    assert wide[0] == pytest.approx((440 + 0.085 * 2560) / 3440, abs=1e-3) and wide[1] == full[1]
    assert narrow[0] == full[0] and narrow[1] == pytest.approx((315 + 0.395 * 810) / 1440, abs=1e-3)
    assert hudnames.boxes("lobby", (100, 100)) == []


def test_boxes_already_there_are_not_added_twice():
    b = hudnames.boxes("spectate", (3440, 1440))
    once = hudnames.add([], b)
    assert hudnames.add(once, b) == once and len(once) == 2


@pytest.fixture
def qapp():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_window
    return qt_window.application()


def test_the_image_editor_places_them_on_a_turned_picture_too(qapp, tmp_path):
    from PIL import Image
    from fogscout.qt_image import ImageWindow
    path = tmp_path / "shot.png"
    Image.new("RGB", (1720, 720), (90, 80, 60)).save(path)
    win = ImageWindow(str(path), str(tmp_path / "out"))
    try:
        win._names_spectate()
        straight = list(win.edit.censor)
        assert straight == [imageedit.clamp_box(b) for b in hudnames.boxes("spectate", (1720, 720))]
        win._names_spectate()                                  # twice: nothing new, no undo step
        assert win.edit.censor == straight and len(win.undo_stack) == 1
        win.undo()
        win.turn(1)                                            # a quarter turn first, then the names
        win._names_spectate()
        want = imageedit.turned(imageedit.ImageEdit(censor=straight), 1, (1720, 720)).censor
        got = [v for b in win.edit.censor for v in b]
        assert got == pytest.approx([v for b in want for v in b], abs=1e-3)
    finally:
        win.close()
