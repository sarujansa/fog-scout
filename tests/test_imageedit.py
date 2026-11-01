"""1.12: drawings (annotate) and the screenshot editor's core (imageedit) – pure PIL."""
import os

import pytest
from PIL import Image

from fogscout import annotate, imageedit


def _picture(w=400, h=200):
    img = Image.new("RGB", (w, h), (40, 40, 40))
    img.paste((200, 30, 30), (0, 0, w // 2, h // 2))           # red top left, the rest dark: turning shows
    return img


def test_shapes_are_drawn_where_their_fractions_say_with_a_dark_rim():
    img = Image.new("RGB", (400, 200), (128, 128, 128))
    out = annotate.draw(img, [annotate.Shape("rect", [(0.25, 0.25), (0.75, 0.75)], "#ff4d4d", 0.02)])
    assert out.size == (400, 200) and out.mode == "RGBA"
    assert out.getpixel((100, 100))[:3] == (255, 77, 77) or out.getpixel((100, 101))[0] > 230   # on the left edge
    assert out.getpixel((200, 100))[:3] == (128, 128, 128)                                     # inside stays
    rim = out.getpixel((100 - 2, 100))[:3]
    assert max(rim) < 128                                                                       # dark outline
    t = annotate.draw(img, [annotate.Shape("text", [(0.1, 0.1)], "#ffffff", 0.2, "Hi")])
    assert (255, 255, 255) in {c for _n, c in t.crop((40, 20, 140, 70)).convert("RGB").getcolors(100000)}
    assert annotate.draw(img, [annotate.Shape("text", [(0.1, 0.1)], "#ffffff", 0.2, "  ")]).getpixel((50, 30))[:3] \
        == (128, 128, 128)                                                                      # empty text: nothing


def test_a_shape_with_times_shows_only_then_and_survives_a_round_trip():
    s = annotate.Shape("arrow", [(0.1, 0.1), (0.9, 0.9)], t0=2.0, t1=5.0)
    assert not s.shown_at(1.0) and s.shown_at(3.0) and not s.shown_at(6.0)
    img = Image.new("RGB", (200, 200), (128, 128, 128))
    assert annotate.draw(img, [s], t=1.0).getpixel((100, 100))[:3] == (128, 128, 128)
    assert annotate.draw(img, [s], t=3.0).getpixel((100, 100))[:3] != (128, 128, 128)
    back = annotate.from_dict(annotate.to_dict(s))
    assert back == s and annotate.from_dict({"kind": "rocket"}) is None and annotate.from_dict({"pts": "x"}) is None
    layer = annotate.layer(200, 100, [s])
    assert layer.mode == "RGBA" and layer.getpixel((5, 95))[3] == 0                 # transparent where nothing is


def test_hit_finds_a_line_near_it_and_not_far_away():
    s = annotate.Shape("line", [(0.0, 0.5), (1.0, 0.5)], size=0.01)
    assert annotate.hit(s, 50, 101, 100, 200) and not annotate.hit(s, 50, 160, 100, 200)
    box = annotate.Shape("rect", [(0.2, 0.2), (0.4, 0.4)])
    assert annotate.hit(box, 30, 30, 100, 100) and not annotate.hit(box, 90, 90, 100, 100)


def test_turning_and_mirroring_move_the_marks_along():
    e = imageedit.ImageEdit(crop=(0.0, 0.0, 0.5, 0.5), censor=[(0.0, 0.0, 0.25, 0.5)],
                            shapes=[annotate.Shape("line", [(0.1, 0.2), (0.3, 0.2)], size=0.01)])
    t = imageedit.turned(e, 1, size=(400, 200))
    assert t.rotate == 1 and t.crop == pytest.approx((0.5, 0.0, 0.5, 0.5))
    assert t.censor[0] == pytest.approx((0.5, 0.0, 0.5, 0.25))
    assert t.shapes[0].pts == [pytest.approx((0.8, 0.1)), pytest.approx((0.8, 0.3))]
    assert t.shapes[0].size == pytest.approx(0.005)                       # 2 px of 200 → 2 px of 400
    assert e.rotate == 0 and e.crop == (0.0, 0.0, 0.5, 0.5)              # the original untouched (undo)
    full = imageedit.turned(imageedit.turned(t, 2), 1)
    assert full.rotate == 0 and full.crop == pytest.approx(e.crop)
    f = imageedit.flipped(e, True)
    assert f.flip_h and f.crop == pytest.approx((0.5, 0.0, 0.5, 0.5))
    assert imageedit.flipped(f, True).crop == pytest.approx(e.crop)


def test_render_turns_adjusts_censors_draws_and_crops_in_that_order():
    img = _picture()
    assert imageedit.render(img, imageedit.ImageEdit()).tobytes() == img.tobytes()
    turned = imageedit.render(img, imageedit.ImageEdit(rotate=1))
    assert turned.size == (200, 400) and turned.getpixel((150, 50)) == (200, 30, 30)       # red now top right
    cropped = imageedit.render(img, imageedit.ImageEdit(crop=(0.0, 0.0, 0.5, 0.5)))
    assert cropped.size == (200, 100) and cropped.getpixel((100, 50)) == (200, 30, 30)
    black = imageedit.render(img, imageedit.ImageEdit(censor=[(0.0, 0.0, 0.5, 0.5)], censor_style="black"))
    assert black.getpixel((50, 50)) == (0, 0, 0) and black.getpixel((300, 150)) == (40, 40, 40)
    noisy = Image.effect_noise((400, 200), 80).convert("RGB")
    pix = imageedit.render(noisy, imageedit.ImageEdit(censor=[(0.0, 0.0, 0.5, 1.0)]))
    assert pix.getpixel((1, 1)) == pix.getpixel((2, 2))                   # blocks: neighbours alike
    assert pix.crop((200, 0, 400, 200)).tobytes() == noisy.crop((200, 0, 400, 200)).tobytes()
    bright = imageedit.render(img, imageedit.ImageEdit(brightness=1.5))
    assert bright.getpixel((300, 150))[0] > 40
    assert imageedit.render(img, imageedit.ImageEdit(crop=(0, 0, 0.5, 0.5)), crop=False).size == (400, 200)


def test_aspect_boxes_and_clamping():
    box = imageedit.aspect_box((0.0, 0.0, 1.0, 1.0), 9 / 16, (1600, 900))
    x, y, w, h = box
    assert (w * 1600) / (h * 900) == pytest.approx(9 / 16, rel=1e-3) and h == pytest.approx(1.0)
    assert x == pytest.approx((1 - w) / 2)
    assert imageedit.clamp_box((0.9, 0.9, 0.5, 0.5)) == pytest.approx((0.5, 0.5, 0.5, 0.5))
    assert imageedit.clamp_box((0.5, 0.5, -0.2, -0.2)) == pytest.approx((0.3, 0.3, 0.2, 0.2))


def test_saving_writes_png_or_jpg_and_names_a_copy(tmp_path):
    img = _picture()
    p = imageedit.save(img, str(tmp_path / "a.png"), "png")
    assert Image.open(p).size == (400, 200) and not os.path.exists(p + ".tmp")
    j = imageedit.save(img, str(tmp_path / "a.jpg"), "jpg")
    assert Image.open(j).format == "JPEG"
    assert imageedit.out_name(r"C:\Steam\screenshots\20261025_1.jpg", "png") == "20261025_1 – bearbeitet.png"


def test_steam_screenshots_are_listed_from_dbds_folder_only_and_newest_first(tmp_path):
    """1.12 (user: "lass es ruhig auf F12"): Steam's DBD folder (app 381210) of every account, only pictures directly
    in it (not Steam's thumbnails, not other games), newest first; the user's own folder replaces it."""
    from fogscout import steamshots
    steam = tmp_path / "Steam"
    dbd = steam / "userdata" / "123" / "760" / "remote" / "381210" / "screenshots"
    other = steam / "userdata" / "123" / "760" / "remote" / "570" / "screenshots"
    (dbd / "thumbnails").mkdir(parents=True)
    other.mkdir(parents=True)
    (steam / "userdata" / "anonymous").mkdir()
    for i, name in enumerate(("a.jpg", "b.png", "notes.txt")):
        p = dbd / name
        p.write_bytes(b"x" * (i + 1))
        os.utime(p, (1000 + i, 1000 + i))
    (dbd / "thumbnails" / "a.jpg").write_bytes(b"t")
    (other / "dota.jpg").write_bytes(b"d")
    dirs = steamshots.shot_dirs(str(steam))
    assert dirs == [str(dbd)]
    shots = steamshots.list_shots(dirs)
    assert [os.path.basename(s.path) for s in shots] == ["b.png", "a.jpg"] and shots[0].size == 2
    assert steamshots.shot_dirs(None) == [] and steamshots.shot_dirs(str(tmp_path / "missing")) == []
    own = tmp_path / "mine"
    own.mkdir()
    assert steamshots.folders(str(own), str(steam)) == [(str(own), "own")]
    assert steamshots.folders(None, str(steam)) == [(str(dbd), "steam")]
    assert steamshots.folders(str(tmp_path / "gone"), str(steam)) == []
    assert steamshots.edit_folder(str(tmp_path)) == str(tmp_path / "Screenshots")
    assert steamshots.edit_folder("").endswith(os.path.join("Pictures", "Fog Scout"))


def test_the_image_window_crops_turns_draws_censors_saves_a_copy_and_undoes(tmp_path):
    """1.12: the screenshot editor end to end (offscreen) – the original file stays untouched, the copy goes into
    the editor's own folder; every step can be undone."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_image, qt_window
    app = qt_window.application()
    src = tmp_path / "steam" / "20261025_1.jpg"
    src.parent.mkdir()
    _picture(400, 200).save(src, quality=95)
    before = src.read_bytes()
    saved = []
    win = qt_image.ImageWindow(str(src), str(tmp_path / "out"), on_saved=saved.append)
    try:
        win.show()
        app.processEvents()
        win.crop_box.setCurrentIndex(win.crop_box.findData("1:1"))
        assert win.edit.crop is not None and win.canvas.crop_edit
        x, y, w, h = win.edit.crop
        assert (w * 400) == pytest.approx(h * 200, rel=0.02)
        win.turn(1)
        assert win.edit.rotate == 1 and win._turned_size() == (200, 400)
        win.canvas._new_shape(annotate.Shape("rect", [(0.1, 0.1), (0.4, 0.3)], "#ff4d4d", 0.01))
        assert len(win.edit.shapes) == 1
        win.canvas.add_box((0.5, 0.5, 0.2, 0.2))
        assert win.edit.censor == [(0.5, 0.5, 0.2, 0.2)]
        win.sliders["brightness"][0].setValue(150)
        win._adjust_timer.stop()
        win._adjust_apply()
        assert win.edit.brightness == pytest.approx(1.5)
        win.save()
        win.wait_saved()
        assert saved and saved[0].startswith(str(tmp_path / "out")) and saved[0].endswith(" – bearbeitet.png")
        out = Image.open(saved[0])
        assert out.size[0] == out.size[1]                                 # the square crop, turned picture
        assert src.read_bytes() == before                                 # the original untouched
        win.copy()
        assert not app.clipboard().image().isNull()
        steps = len(win.undo_stack)
        assert steps >= 5
        for _i in range(steps):
            win.undo()
        assert not win.edit.changed() and win.edit.crop is None and win.crop_box.currentData() == "none"
        win.redo()
        assert win.edit.crop is not None
    finally:
        win.close()


def test_a_picture_that_cannot_be_read_says_so(tmp_path):
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_image, qt_window
    qt_window.application()
    bad = tmp_path / "broken.jpg"
    bad.write_bytes(b"not a picture")
    win = qt_image.ImageWindow(str(bad), str(tmp_path / "out"))
    try:
        assert "nicht lesbar" in win.status.text() and not win.save_btn.isEnabled() and win.result() is None
    finally:
        win.close()


def test_a_big_shape_is_drawn_only_where_its_stroke_is_and_looks_the_same(monkeypatch):
    """1.12 optimisation: a box around the whole picture was one tile three times the picture (3440×1440: 0.8 s,
    ~180 MB); now only the squares its stroke touches are drawn – the same picture (an ellipse may differ in single
    edge pixels: PIL rounds its curve per square)."""
    from PIL import ImageChops
    img = Image.new("RGB", (1600, 900), (90, 90, 90))
    box = annotate.Shape("rect", [(0.05, 0.05), (0.95, 0.95)], "#ff4d4d", 0.008)
    ring = annotate.Shape("ellipse", [(0.1, 0.1), (0.9, 0.9)], "#4dabff", 0.008)
    line = annotate.Shape("line", [(0.0, 0.0), (1.0, 1.0)], size=0.01)
    squares = annotate._squares(box, 0, 0, 1600, 900, 1600, 900)
    grid = len(range(0, 1600, annotate.CHUNK)) * len(range(0, 900, annotate.CHUNK))
    assert 1 < len(squares) < grid * 0.75                                 # the empty inside is skipped
    assert annotate._squares(annotate.Shape("free", [(0, 0), (1, 1)]), 0, 0, 1600, 900, 1600, 900) == \
        [(0, 0, 1600, 900)]                                               # freehand: one tile (cheaper)
    split = annotate.draw(img, [box, ring, line])
    monkeypatch.setattr(annotate, "CHUNK_FROM", 10 ** 12)
    whole = annotate.draw(img, [box, ring, line])
    diff = ImageChops.difference(split, whole).convert("L")
    off = diff.point(lambda v: 255 if v > 24 else 0).histogram()[255]
    assert ImageChops.difference(annotate.draw(img, [box]), annotate.draw(img, [box])).getbbox() is None
    assert off < 0.002 * 1600 * 900 and max(diff.tobytes()) < 128        # no seams, only stray edge pixels


def test_moving_a_drawing_redraws_only_that_drawing_on_the_canvas():
    """1.12 optimisation: while a drawing is drawn or moved, the others stay one cached picture (10 drawings:
    59 → 5 ms per mouse move on the test machine)."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtGui import QImage
    from fogscout import qt_clip, qt_window
    app = qt_window.application()
    view = qt_clip.PreviewView()
    try:
        view.resize(640, 360)
        view.set_frame(QImage(320, 180, QImage.Format_RGB888))
        view.show()
        view.set_shapes([annotate.Shape("arrow", [(0.1 * i, 0.1), (0.1 * i + 0.05, 0.4)]) for i in range(8)])
        view.repaint()
        app.processEvents()
        cached = view._layer
        assert cached is not None
        new = annotate.Shape("rect", [(0.3, 0.5), (0.4, 0.6)])
        view._drag = ("shape_new", (0.3, 0.5), new)
        for k in range(5):
            new.pts[1] = (0.4 + 0.02 * k, 0.6)
            view._preview_new = new
            view.repaint()
        assert view._layer is cached and view._active_shape() is new       # the still ones were not drawn again
        view._drag, view._preview_new = None, None                         # released (as _release_extra does)
        view.shape_sel = 2
        view._drag = ("shape_move", (0.2, 0.1), view.shapes[2])
        view.repaint()
        assert view._active_shape() is view.shapes[2]
        assert view._layer is not cached and repr(view.shapes[2]) not in view._layer[0][2]   # left the cached picture
        view._drag = None
    finally:
        view.close()


def test_the_canvas_shows_a_smaller_copy_but_saving_keeps_every_pixel(tmp_path):
    """1.12 optimisation: a large screenshot is turned and coloured on a copy of at most PREVIEW_MAX on every
    change (3440×1440: ~40 → 9 ms per slider step); crop ratios and the saved picture use the original."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_image, qt_window
    app = qt_window.application()
    src = tmp_path / "big.png"
    _picture(qt_image.PREVIEW_MAX + 480, 1000).save(src)
    saved = []
    win = qt_image.ImageWindow(str(src), str(tmp_path / "out"), on_saved=saved.append)
    try:
        win.show()
        app.processEvents()
        assert max(win.preview.size) == qt_image.PREVIEW_MAX and win.original.size == (qt_image.PREVIEW_MAX + 480,
                                                                                         1000)
        assert win.canvas.image_size() == win.original.size and win.canvas._img.width() == qt_image.PREVIEW_MAX
        win.turn(1)
        assert win.canvas.image_size() == (1000, qt_image.PREVIEW_MAX + 480)
        win.save()
        assert not win.save_btn.isEnabled() and win.status.text() == "Speichert …"   # in a thread, window free
        win.save()                                                         # a second click while saving: ignored
        win.wait_saved()
        assert win.save_btn.isEnabled() and len(saved) == 1
        assert Image.open(saved[0]).size == (1000, qt_image.PREVIEW_MAX + 480)
    finally:
        win.close()
    small = qt_image.ImageWindow.__dict__["_preview_copy"].__func__(_picture(400, 200))
    assert small.size == (400, 200)


# ---------------------------------------------------------------- review fixes (1.12 editing tools)

def _marked(w=400, h=200):
    """A dark picture with one white block (the "name" to censor) at the top left."""
    img = Image.new("RGB", (w, h), (40, 40, 40))
    img.paste((255, 255, 255), (40, 20, 60, 40))
    return img


def test_mirroring_and_then_turning_keeps_a_censor_box_on_what_it_covers():
    """Review #1: base() turns before it mirrors – after a mirror, "Rechts drehen" turned the picture the other way
    while the boxes turned clockwise, and the censored name showed in the saved copy."""
    img = _marked()
    box = (0.1, 0.1, 0.05, 0.1)                                           # exactly the white block
    turns = {1: Image.ROTATE_270, 2: Image.ROTATE_180, 3: Image.ROTATE_90}
    for horizontal in (True, False):
        for q in (1, 2, 3):
            e = imageedit.flipped(imageedit.ImageEdit(), horizontal, img.size)
            e.censor = [imageedit._flip_box(box, horizontal)]
            e.censor_style = "black"
            size = imageedit.base(img, e).size
            t = imageedit.turned(e, q, size)
            mirror = Image.FLIP_LEFT_RIGHT if horizontal else Image.FLIP_TOP_BOTTOM
            expected = img.transpose(mirror).transpose(turns[q])          # what the user did, in that order
            assert imageedit.base(img, t).tobytes() == expected.tobytes(), (horizontal, q)
            out = imageedit.render(img, t)
            assert (255, 255, 255) not in {c for _n, c in out.getcolors(1 << 20)}, (horizontal, q)


def test_text_drawn_at_many_sizes_never_gets_the_glyphs_of_another_font():
    """Review #2/#5: the glyph caches were keyed by id(font); text drawings at every canvas size churn skin.inter's
    64 fonts, a freed font's id went to the next one – other widths and glyphs in the editor, the saved copy and
    the overlay's own text."""
    from PIL import ImageDraw
    from fogscout import skin
    from fogscout.overlay_win32 import _char_len, _draw_run
    shapes = [annotate.Shape("text", [(0.1, 0.1)], "#ffd23f", 0.05, "Killer hier"),
              annotate.Shape("text", [(0.4, 0.6)], "#ffffff", 0.08, "Gen")]
    before = annotate.layer(800, 600, shapes).tobytes()
    for h in range(600, 1151, 10):                                        # a canvas dragged larger
        annotate.layer(800, h, shapes)
    assert annotate.layer(800, 600, shapes).tobytes() == before
    text = "Coal Tower 12:34"
    wrong = []
    for weight, size in [("SemiBold", 15), ("Bold", 18), ("Medium", 13), ("Bold", 24), ("SemiBold", 20)] + \
            [("Bold", s) for s in range(6, 160, 9)]:
        f = skin.inter(weight, size)
        a = Image.new("L", (600, 220))
        _draw_run(a, 4, 4, text, f, 255)
        b = Image.new("L", (600, 220))
        d, x = ImageDraw.Draw(b), 4
        for ch in text:
            d.text((x, 4), ch, font=f, fill=255)
            x += f.getlength(ch)
        if a.tobytes() != b.tobytes() or any(_char_len(f, ch) != f.getlength(ch) for ch in text):
            wrong.append((weight, size))
    assert wrong == []


def test_turning_keeps_a_text_drawing_whole_on_the_picture():
    """Review #7/#14: turning moved only the text's top-left anchor – it became the top-right corner and the
    upright text ran off the picture (1440 px wide after the turn: 64 px of "Killer hier" left)."""
    img = Image.new("RGB", (3440, 1440), (40, 40, 40))
    e = imageedit.ImageEdit(shapes=[annotate.Shape("text", [(0.05, 0.05)], "#ffffff", 0.08, "Killer hier")])

    def ink(pic):
        return pic.convert("L").point(lambda v: 255 if v > 250 else 0).getbbox()

    x0, _y0, x1, _y1 = ink(imageedit.render(img, e))
    for q in (1, 2, 3):
        t = imageedit.turned(e, q, img.size)
        nw, nh = (1440, 3440) if q % 2 else (3440, 1440)
        bx0, by0, bx1, by1 = annotate.text_box(t.shapes[0], nw, nh)
        assert bx0 >= -1e-6 and by0 >= -1e-6 and bx1 <= nw + 1e-6 and by1 <= nh + 1e-6, q
        tx0, _ty0, tx1, _ty1 = ink(imageedit.render(img, t))
        assert abs((tx1 - tx0) - (x1 - x0)) <= 2, q                       # the whole text, not a cut-off part
    mid = imageedit.ImageEdit(shapes=[annotate.Shape("text", [(0.4, 0.45)], "#ffffff", 0.05, "GG")])
    back, size = mid, img.size
    for _i in range(4):                                                   # four turns: where it was
        back = imageedit.turned(back, 1, size)
        size = size[::-1]
    assert back.shapes[0].pts[0] == pytest.approx((0.4, 0.45), abs=0.002)
    assert back.shapes[0].size == pytest.approx(0.05)


def test_a_box_or_ellipse_is_picked_on_its_outline_and_a_new_drawing_can_start_inside():
    """Review #8: the whole inside of a frame counted as on it – no drawing could be started inside a frame around
    the picture, the press moved the frame instead. A frame too small to draw in still counts whole."""
    frame = annotate.Shape("rect", [(0.05, 0.05), (0.95, 0.95)])
    ring = annotate.Shape("ellipse", [(0.1, 0.1), (0.9, 0.9)])
    assert not annotate.hit(frame, 800, 450, 1600, 900) and not annotate.hit(ring, 800, 450, 1600, 900)
    assert annotate.hit(frame, 80, 450, 1600, 900) and annotate.hit(frame, 800, 48, 1600, 900)
    assert annotate.hit(frame, 84, 300, 1600, 900) and not annotate.hit(frame, 120, 300, 1600, 900)
    assert annotate.hit(ring, 160, 450, 1600, 900) and annotate.hit(ring, 800, 92, 1600, 900)
    assert not annotate.hit(ring, 200, 450, 1600, 900)
    small = annotate.Shape("rect", [(0.2, 0.2), (0.4, 0.4)])
    assert annotate.hit(small, 30, 30, 100, 100)


def test_mirroring_a_text_mirrors_its_box_exactly():
    """Review #28: flipped() counted the text box's padding twice – the text landed 2 × pad off its mirror."""
    pw, ph = 3440, 1440
    for size in annotate.TEXT_SIZES:
        s = annotate.Shape("text", [(0.1, 0.1)], "#ffffff", size, "Killer")
        e = imageedit.ImageEdit(shapes=[s])
        x0, y0, x1, y1 = annotate.text_box(s, pw, ph)
        h = annotate.text_box(imageedit.flipped(e, True, (pw, ph)).shapes[0], pw, ph)
        assert h == pytest.approx((pw - x1, y0, pw - x0, y1), abs=1e-6)
        v = annotate.text_box(imageedit.flipped(e, False, (pw, ph)).shapes[0], pw, ph)
        assert v == pytest.approx((x0, ph - y1, x1, ph - y0), abs=1e-6)
        twice = imageedit.flipped(imageedit.flipped(e, True, (pw, ph)), True, (pw, ph))
        assert twice.shapes[0].pts[0] == pytest.approx((0.1, 0.1))


def test_a_pasted_windows_line_break_in_a_text_is_a_line_break():
    """Review #29: "\\r" (a pasted "\\r\\n" stays in the text field) went to Pillow as a character – with the raqm
    layout RuntimeError('raqm_layout() failed') from the canvas and the save thread."""
    img = Image.new("RGB", (400, 200), (90, 90, 90))
    two = annotate.Shape("text", [(0.1, 0.1)], "#ffffff", 0.1, "Killer\nhier")
    plain = annotate.draw(img, [two]).tobytes()
    for text in ("Killer\r\nhier", "Killer\rhier", "Killer\x85hier", "Killer\u2029hier"):
        s = annotate.Shape("text", [(0.1, 0.1)], "#ffffff", 0.1, text)
        assert annotate.text_box(s, 400, 200) == annotate.text_box(two, 400, 200), repr(text)
        assert annotate.draw(img, [s]).tobytes() == plain, repr(text)
    assert annotate.text_lines("a\n") == ["a", ""] and annotate.text_lines("") == [""]


def test_a_16_bit_grey_picture_is_scaled_not_cut_to_white(tmp_path):
    """Review #30: convert("RGB") cuts 16-bit values above 255 – a mid-grey 16-bit PNG was white in the editor,
    the saved copy and the gallery."""
    from fogscout import thumbs
    grey = Image.new("I;16", (60, 40), 40000)                            # 40000 / 65535 ≈ 156 of 255
    assert abs(imageedit.render(grey, imageedit.ImageEdit()).getpixel((5, 5))[0] - 156) <= 1
    assert abs(imageedit.render(grey.convert("I"), imageedit.ImageEdit()).getpixel((5, 5))[0] - 156) <= 1
    p = tmp_path / "grey16.png"
    grey.save(p)
    assert Image.open(p).mode.startswith("I")
    thumb = thumbs.thumbnail(str(p), (30, 20))
    assert abs(thumb.getpixel((5, 5))[0] - 156) <= 1 and thumb.mode == "RGBA"
    assert imageedit.converted(Image.new("L", (4, 4), 77)).getpixel((1, 1)) == (77, 77, 77)


def _bomb(path):
    """A real 1 × 1 PNG whose header says 20000 × 20000 (Image.open reads only the header)."""
    import io
    import struct
    import zlib
    buf = io.BytesIO()
    Image.new("RGB", (1, 1)).save(buf, "PNG")
    b = bytearray(buf.getvalue())
    i = b.find(b"IHDR")
    b[i + 4:i + 12] = struct.pack(">II", 20000, 20000)
    b[i + 17:i + 21] = struct.pack(">I", zlib.crc32(bytes(b[i:i + 17])) & 0xffffffff)
    path.write_bytes(bytes(b))
    return str(path)


def test_one_oversized_picture_never_ends_the_thumbnail_thread(tmp_path, monkeypatch):
    """Review #21: Pillow's DecompressionBombError is no OSError – it ended the loader thread, no tile after it was
    ever made and the gallery polled forever."""
    import time
    import warnings
    from fogscout import thumbs
    bomb = _bomb(tmp_path / "00_big.png")
    good = tmp_path / "a.png"
    Image.new("RGB", (64, 32), (200, 0, 0)).save(good)
    good = str(good)
    loader = thumbs.Loader((32, 32), str(tmp_path / "cache"), name="shot-thumbs")
    assert loader.make(bomb) == (bomb, 0, 0, b"")
    with warnings.catch_warnings():                                      # a picture over MAX_IMAGE_PIXELS only
        warnings.simplefilter("error", Image.DecompressionBombWarning)   # warns – as an error: broken too
        monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 64 * 32 - 1)
        assert loader.make(good) == (good, 0, 0, b"")
    monkeypatch.undo()
    loader.request([bomb, good])
    got = {}
    end = time.time() + 30
    while len(got) < 2 and time.time() < end:
        for path, w, h, _data in loader.take():
            got[path] = (w, h)
        time.sleep(0.01)
    assert got == {bomb: (0, 0), good: (32, 16)}
    loader.make = lambda path: 1 / 0                                      # whatever else goes wrong in one picture
    loader.request([good])
    end = time.time() + 30
    while not (done := loader.take()) and time.time() < end:
        time.sleep(0.01)
    assert done == [(good, 0, 0, b"")] and not loader.busy


def test_saving_uses_its_own_temporary_file_and_leaves_none_behind(tmp_path, monkeypatch):
    """Review #35/#48/#54: one fixed "<name>.tmp" for every save – two editors saving the same name wrote into one
    file; a failed rename and a quit during a save left the temporary file in the folder for good."""
    import threading
    img = _picture()
    out = tmp_path / "shot – bearbeitet.png"
    used = []
    real = os.replace

    def spy(src, dst):
        used.append(os.path.basename(src))
        return real(src, dst)

    monkeypatch.setattr(imageedit.os, "replace", spy)
    for _i in range(2):
        t = threading.Thread(target=imageedit.save, args=(img, str(out)))
        t.start()
        t.join()
    monkeypatch.undo()
    assert len(used) == 2 and used[0] != used[1] and all(imageedit.TMP_NAME.match(n) for n in used)
    assert Image.open(out).size == (400, 200)
    blocked = tmp_path / "taken.png"
    blocked.mkdir()                                                       # the rename fails
    (blocked / "x").write_text("x")
    with pytest.raises(OSError):
        imageedit.save(img, str(blocked))
    assert not [n for n in os.listdir(tmp_path) if n.endswith(".tmp")]
    old = tmp_path / ("left – bearbeitet.png.%d-1.tmp" % os.getpid())     # a save cut off by quitting
    fresh = tmp_path / "busy – bearbeitet.png.9-2.tmp"                    # another window saving right now
    foreign = tmp_path / "notes.png.tmp"
    for p in (old, fresh, foreign):
        p.write_bytes(b"part")
    os.utime(old, (1, 1))
    os.utime(foreign, (1, 1))
    imageedit.save(img, str(out), "jpg")
    assert not old.exists() and fresh.exists() and foreign.exists()


def test_edited_pictures_never_go_into_steams_screenshot_folder(tmp_path, monkeypatch):
    """Review #55: a recordings folder in Steam's DBD screenshot folder made the edited copies land there (on NTFS
    "…/381210/Screenshots" is Steam's own "screenshots") – the hard rule says nothing is ever written there."""
    from fogscout import steamshots
    steam = tmp_path / "Steam"
    area = steam / "userdata" / "123" / "760" / "remote" / "381210"
    shots = area / "screenshots"
    shots.mkdir(parents=True)
    monkeypatch.setattr(steamshots, "steam_path", lambda: str(steam))    # as the registry says on Windows
    own = steamshots.edit_folder(None)
    assert steamshots.edit_folder(str(shots)) == own
    assert steamshots.edit_folder(str(area)) == own
    assert steamshots.edit_folder(str(shots / "OBS")) == own
    link = tmp_path / "rec-link"
    try:
        link.symlink_to(shots, target_is_directory=True)
    except (OSError, NotImplementedError):
        link = None
    if link is not None:
        assert steamshots.edit_folder(str(link)) == own                   # a link into Steam's folder
    rec = tmp_path / "Videos"
    assert steamshots.edit_folder(str(rec)) == str(rec / "Screenshots")
    assert steamshots.edit_folder(str(shots), None) == str(shots / "Screenshots")    # no Steam on this PC


def test_every_visible_pixel_of_a_flat_oval_or_a_frame_picks_it_and_its_middle_does_not():
    """Review #8, second pass: the distance along the ray from the middle is far too large on a flat oval – up to
    half of its drawn stroke picked nothing (and its inside neither), a press on it started a new drawing. And
    Pillow draws the stroke inside the box with square corners: its inner rim and the corner tips must pick it too."""
    import numpy as np
    for (pw, ph), kind, pts, size in [((1000, 419), "ellipse", [(0.10, 0.10), (0.40, 0.18)], 0.006),
                                      ((1600, 670), "ellipse", [(0.40, 0.05), (0.60, 0.12)], 0.006),
                                      ((1600, 900), "ellipse", [(0.05, 0.45), (0.95, 0.56)], 0.006),
                                      ((1600, 900), "ellipse", [(0.30, 0.10), (0.36, 0.90)], 0.006),
                                      ((1600, 900), "ellipse", [(0.05, 0.05), (0.95, 0.95)], 0.016),
                                      ((1600, 900), "rect", [(0.05, 0.05), (0.95, 0.95)], 0.006),
                                      ((1600, 900), "rect", [(0.20, 0.20), (0.80, 0.40)], 0.016)]:
        s = annotate.Shape(kind, pts, "#ff4d4d", size)
        alpha = np.asarray(annotate.layer(pw, ph, [s]))[:, :, 3]
        ys, xs = np.nonzero(alpha > 128)
        missed = [(x, y) for x, y in zip(xs, ys) if not annotate.hit(s, x + 0.5, y + 0.5, pw, ph)]
        assert not missed, (kind, pts, len(missed), len(xs))
        (x0, y0), (x1, y1) = pts
        assert not annotate.hit(s, (x0 + x1) / 2 * pw, (y0 + y1) / 2 * ph, pw, ph), (kind, pts)


def test_a_project_shape_that_the_painter_cannot_draw_is_mended_or_dropped():
    """1.16.1 (audit, reproduced): a colour that is no "#rrggbb", a point or size that is not finite or absurd
    reached annotate.draw from a project file and raised in the paint path."""
    from PIL import Image
    import math
    good = {"kind": "rect", "pts": [[0.1, 0.1], [0.5, 0.5]], "colour": "#zzzzzz", "size": 1e308, "text": ""}
    s = annotate.from_dict(good)
    assert s is not None and s.colour == annotate.COLOURS[0] and s.size == annotate.SIZE_MAX
    for bad in ({"kind": "line", "pts": [[float("nan"), 0.2], [0.5, 0.5]]},
                {"kind": "line", "pts": [[1e9, 0.2], [0.5, 0.5]]}):
        assert annotate.from_dict(bad) is None
    t = annotate.from_dict({"kind": "text", "pts": [[0.2, 0.2]], "text": "x", "size": 1e9, "t0": float("inf")})
    assert t is not None and t.size == annotate.SIZE_MAX and t.t0 is None
    neg = annotate.from_dict({"kind": "arrow", "pts": [[0.2, 0.2], [0.6, 0.6]], "size": -3})
    assert neg is not None and neg.size == annotate.DEFAULT_SIZE and math.isfinite(neg.size)
    img = annotate.draw(Image.new("RGBA", (160, 90), (0, 0, 0, 0)), [s, t, neg])   # draws without raising
    assert img.getbbox() is not None
