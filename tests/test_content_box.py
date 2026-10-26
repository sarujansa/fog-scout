"""1.12.6: black borders of a recording (clipedit.content_box/refine_box) – the clip editor shows and saves the game
part only. Pure: pictures made with PIL, no ffmpeg."""
import os
import random
import sys

import pytest
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit  # noqa: E402


def frame(size, box, seed, dark_top=0, colour=None):
    """A picture of ``size`` with game-like noise inside ``box`` (pixels x0, y0, x1, y1) and black around it;
    ``dark_top`` rows of the game part stay nearly black (a dark ceiling)."""
    rnd = random.Random(seed)
    img = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    for _ in range(400):
        x, y = rnd.randrange(x0, x1), rnd.randrange(y0 + dark_top, y1)
        c = colour or (rnd.randrange(30, 200), rnd.randrange(20, 160), rnd.randrange(10, 120))
        d.rectangle((x, y, min(x1 - 1, x + 12), min(y1 - 1, y + 9)), fill=c)
    d.rectangle((x0, y0 + dark_top, x1 - 1, y0 + dark_top + 1), fill=(60, 50, 40))    # edges of the game part
    d.rectangle((x0, y1 - 2, x1 - 1, y1 - 1), fill=(60, 50, 40))
    d.rectangle((x0, y0 + dark_top, x0 + 1, y1 - 1), fill=(60, 50, 40))
    d.rectangle((x1 - 2, y0 + dark_top, x1 - 1, y1 - 1), fill=(60, 50, 40))
    if dark_top:
        d.rectangle((x0, y0, x1 - 1, y0 + dark_top - 1), fill=(8, 7, 9))
    return img


def test_a_game_picture_centred_in_black_is_found():
    """The user's round (1.12.6 screenshot): the game in the middle, black on all four sides."""
    size, box = (216, 108), (30, 19, 186, 89)
    imgs = [frame(size, box, i) for i in range(24)]
    x, y, w, h = clipedit.content_box(imgs)
    assert x == pytest.approx(30 / 216, abs=0.006) and w == pytest.approx(156 / 216, abs=0.012)
    assert y == pytest.approx(19 / 108, abs=0.01) and h == pytest.approx(70 / 108, abs=0.02)


def test_dbd_16_9_in_a_21_9_window_loses_only_its_side_bars():
    size = (344, 144)                                   # 3440×1440 at a tenth: 256 px of game, 44 px bars
    imgs = [frame(size, (44, 0, 300, 144), i) for i in range(12)]
    x, y, w, h = clipedit.content_box(imgs)
    assert (y, h) == (0.0, 1.0)
    assert x == pytest.approx(44 / 344, abs=0.004) and w == pytest.approx(256 / 344, abs=0.008)


def test_a_full_picture_has_no_borders():
    imgs = [frame((192, 108), (0, 0, 192, 108), i) for i in range(10)]
    assert clipedit.content_box(imgs) is None


def test_a_dark_ceiling_over_the_whole_round_is_no_border():
    """Only the top dark (a basement for minutes) – one side, not a pair: the picture is not cut."""
    imgs = [frame((192, 108), (0, 0, 192, 108), i, dark_top=14) for i in range(10)]
    assert clipedit.content_box(imgs) is None


def test_bars_of_unequal_width_are_not_cut():
    """A source at the top left of a bigger canvas (black only right and below) – not a centred picture."""
    imgs = [frame((192, 108), (0, 0, 150, 80), i) for i in range(10)]
    assert clipedit.content_box(imgs) is None


def test_too_few_pictures_with_anything_in_them_are_not_trusted():
    black = Image.new("RGB", (192, 108))
    imgs = [frame((192, 108), (30, 19, 162, 89), i) for i in range(3)] + [black] * 20
    assert clipedit.content_box(imgs) is None
    assert clipedit.content_box([]) is None and clipedit.content_box([None, None]) is None


def test_a_moment_lit_into_a_dark_corner_widens_the_part():
    """One picture alone has a dark top band; the others show it lit – the union keeps the whole game part."""
    size, box = (216, 108), (30, 19, 186, 89)
    imgs = [frame(size, box, 0, dark_top=20)] + [frame(size, box, i) for i in range(1, 8)]
    _x, y, _w, h = clipedit.content_box(imgs)
    assert y == pytest.approx(19 / 108, abs=0.01)


def test_pictures_of_another_size_are_left_out():
    size, box = (216, 108), (30, 19, 186, 89)
    imgs = [frame(size, box, i) for i in range(8)] + [Image.new("RGB", (100, 100), (200, 200, 200))]
    assert clipedit.content_box(imgs) is not None


def test_the_sharper_picture_moves_the_edges_inside_the_game_part():
    """refine_box: the box of small pictures (one pixel ≈ 13 px of 1440p) put on the edges of a 960×540 picture,
    one row/column inside – no black line is left in the clip, and only a pixel of game is lost per side."""
    big, game = (960, 540), (135, 95, 825, 445)
    sharp = frame(big, game, 99)
    coarse = (0.13, 0.17, 0.74, 0.66)                       # a little off, as from 192×108 pictures
    x, y, w, h = clipedit.refine_box(coarse, sharp)
    px = (x * 960, y * 540, (x + w) * 960, (y + h) * 540)
    assert px[0] == pytest.approx(136, abs=0.6) and px[1] == pytest.approx(96, abs=0.6)
    assert px[2] == pytest.approx(824, abs=0.6) and px[3] == pytest.approx(444, abs=0.6)
    inner = sharp.crop(tuple(round(v) for v in px))
    assert min(inner.crop((0, 0, 1, inner.height)).convert("L").getextrema()[1],
               inner.crop((0, 0, inner.width, 1)).convert("L").getextrema()[1]) > clipedit.CONTENT_DARK


def test_a_side_dark_in_the_sharper_picture_keeps_its_place():
    big, game = (960, 540), (135, 95, 825, 445)
    sharp = frame(big, game, 5, dark_top=60)               # this moment: the top of the game part dark
    coarse = (135 / 960, 95 / 540, 690 / 960, 350 / 540)
    x, y, w, h = clipedit.refine_box(coarse, sharp)
    assert y == pytest.approx(95 / 540, abs=1e-9) and h == pytest.approx((444 - 95) / 540, abs=0.002)
    assert clipedit.refine_box(None, sharp) is None
    assert clipedit.refine_box(coarse, Image.new("RGB", big)) == coarse
