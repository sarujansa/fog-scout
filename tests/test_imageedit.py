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
