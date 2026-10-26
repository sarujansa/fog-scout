"""The picture editor window (qt_image.ImageWindow, 1.12) – review fixes: freeing, keys, undo, crop box, saving."""
import gc
import threading
import weakref

import pytest
from PIL import Image

pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)

from PySide6.QtCore import QPoint, Qt  # noqa: E402
from PySide6.QtGui import QShortcut  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QPushButton  # noqa: E402

from fogscout import annotate, imageedit, qt_image, qt_window  # noqa: E402


def _source(tmp_path, w=400, h=200, name="20261025_1.png"):
    img = Image.new("RGB", (w, h), (90, 120, 150))
    img.paste((200, 30, 30), (0, 0, w // 2, h // 2))           # red top left: turning and mirroring show
    path = tmp_path / name
    img.save(path)
    return path


@pytest.fixture
def app():
    return qt_window.application()


@pytest.fixture
def opened(app, tmp_path):
    """``open_win(path=None, **kw)`` → a shown ImageWindow; all of them are closed after the test."""
    wins = []

    def open_win(path=None, **kw):
        win = qt_image.ImageWindow(str(path or _source(tmp_path)), str(tmp_path / "out"), **kw)
        wins.append(win)
        win.show()
        win.activateWindow()
        QTest.qWaitForWindowExposed(win)
        app.processEvents()
        return win
    yield open_win
    for win in wins:
        win.wait_saved()
        win.close()


def _need_active(win):
    """Shortcuts and keyboard focus only work in the active window: always so offscreen (Linux CI); a desktop may
    refuse a test process the foreground."""
    if not QTest.qWaitForWindowActive(win):
        pytest.skip("the window could not become the active window here")


def _at(win, fx, fy):
    f = win.canvas.frame_rect()
    return QPoint(int(f.left() + f.width() * fx), int(f.top() + f.height() * fy))


def _keys(app, win, key, mods=Qt.NoModifier):
    """A key press as the user makes it: to whatever has the keyboard focus."""
    QTest.keyClick(app.focusWidget() or win, key, mods)
    app.processEvents()


def test_a_closed_editor_is_freed_and_one_still_saving_only_after_its_save(app, tmp_path, monkeypatch):
    """Code review 11: slots that captured the window (lambdas on its own buttons and sliders) kept every closed editor
    – full-size picture, preview, undo steps – alive until Fog Scout quit (~41 MB per 3440×1440 screenshot)."""
    src = _source(tmp_path)
    win = qt_image.ImageWindow(str(src), str(tmp_path / "out"))
    win.show()
    app.processEvents()
    for b in win.findChildren(QPushButton):                  # every kind of slot the window connects, used once
        if b.text() in ("⟳ Rechts drehen", "⇆ Spiegeln"):
            b.click()
    win.tools.setCurrentIndex(1)
    win.draw_btns["arrow"].click()
    win.colour_btns[annotate.COLOURS[2]].click()
    win.sliders["brightness"][0].setValue(130)
    assert win.edit.rotate == 1 and win.edit.flip_h and win.canvas.shape_tool == "arrow"
    assert win.canvas.pen["colour"] == annotate.COLOURS[2] and win.edit.brightness == pytest.approx(1.3)
    win.close()
    app.processEvents()
    ref = weakref.ref(win)
    b = win = None
    gc.collect()
    assert ref() is None

    saved = []
    win = qt_image.ImageWindow(str(src), str(tmp_path / "out"), on_saved=saved.append)
    win.show()
    gate = threading.Event()
    real_save = imageedit.save

    def slow_save(img, path, fmt="png"):
        gate.wait(30)
        return real_save(img, path, fmt)
    monkeypatch.setattr(qt_image.imageedit, "save", slow_save)
    win.save()
    win.close()                                              # closed while the copy is still being written
    ref = weakref.ref(win)
    del win
    gc.collect()
    gate.set()
    assert ref() is not None                                 # kept until the save is picked up …
    ref().wait_saved()
    assert len(saved) == 1 and Image.open(saved[0]).size == (400, 200)   # … so the App still hears of it
    gc.collect()
    assert ref() is None


def test_ctrl_y_and_ctrl_shift_z_redo(app, opened):
    """Code review 12: Ctrl+Y was registered twice (QKeySequence.Redo is Ctrl+Y on Windows/offscreen, plus "Ctrl+Y"):
    Qt calls that ambiguous and fired neither – the documented redo key did nothing."""
    win = opened()
    keys = [k.toString() for sc in win.findChildren(QShortcut) for k in sc.keys()]
    assert len(keys) == len(set(keys)) and "Ctrl+Y" in keys and "Ctrl+Shift+Z" in keys
    _need_active(win)
    win.canvas.add_box((0.1, 0.1, 0.2, 0.2))
    _keys(app, win, Qt.Key_Z, Qt.ControlModifier)
    assert win.edit.censor == []
    _keys(app, win, Qt.Key_Y, Qt.ControlModifier)
    assert win.edit.censor == [(0.1, 0.1, 0.2, 0.2)]
    _keys(app, win, Qt.Key_Z, Qt.ControlModifier)
    _keys(app, win, Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier)
    assert win.edit.censor == [(0.1, 0.1, 0.2, 0.2)]


def test_undo_and_reset_bring_the_censor_style_box_along(opened):
    """Code review 15: after undo or 'Alles zurücksetzen' the box still said 'Schwarz' while the copy was saved
    pixelated – and picking 'Schwarz' again did nothing (already shown)."""
    win = opened()
    style = win.censor_style
    win.canvas.add_box((0.6, 0.6, 0.2, 0.2))
    style.setCurrentIndex(style.findData("black"))
    assert win.edit.censor_style == "black"
    win.undo()
    assert win.edit.censor_style == "pixel" and style.currentData() == "pixel" and win.canvas.style == "pixel"
    win.redo()
    assert style.currentData() == "black"
    win.reset_all()
    assert style.currentData() == "pixel"
    win.canvas.add_box((0.6, 0.6, 0.2, 0.2))
    style.setCurrentIndex(style.findData("black"))
    assert win.edit.censor_style == "black"
    assert win.result().getpixel((280, 140)) == (0, 0, 0)    # the middle of the box: black, not blocks


def test_a_click_on_the_picture_takes_the_keys_back_from_the_text_field(app, opened):
    """Code review 24: the window took no focus, so after typing a text and clicking the picture the text field kept
    the keys – Ctrl+Z/Ctrl+C/Delete did nothing (or edited the text) instead of what the hint line promises."""
    win = opened()
    _need_active(win)
    win.turn(1)
    win.tools.setCurrentIndex(1)
    win.draw_btns["text"].click()
    QTest.mouseClick(win.draw_text, Qt.LeftButton)
    QTest.keyClicks(win.draw_text, "GG")
    QTest.mouseClick(win.canvas, Qt.LeftButton, Qt.NoModifier, _at(win, 0.2, 0.2))
    app.processEvents()
    assert [s.text for s in win.edit.shapes] == ["GG"]
    assert app.focusWidget() is not win.draw_text
    _keys(app, win, Qt.Key_C, Qt.ControlModifier)
    copied = app.clipboard().image()
    assert (copied.width(), copied.height()) == win.result().size == (200, 400)
    _keys(app, win, Qt.Key_Z, Qt.ControlModifier)
    assert win.edit.shapes == [] and win.edit.rotate == 1    # the text undone, the turn kept
    _keys(app, win, Qt.Key_Y, Qt.ControlModifier)
    assert [s.text for s in win.edit.shapes] == ["GG"]
    win.canvas.shape_sel = 0
    _keys(app, win, Qt.Key_Delete)
    assert win.edit.shapes == []
    QTest.mouseClick(win.draw_text, Qt.LeftButton)
    assert app.focusWidget() is win.draw_text
    QTest.keyClick(win.draw_text, Qt.Key_Return)
    assert app.focusWidget() is not win.draw_text            # Enter: done typing, the keys go back too


def test_the_crop_ratio_box_follows_undo_and_turning(opened):
    """Code review 34: undo of a ratio change or a quarter turn left the box (and the canvas' ratio lock) on the old
    ratio – the next corner drag snapped the crop to it."""
    win = opened()
    box = win.crop_box
    box.setCurrentIndex(box.findData("16:9"))
    box.setCurrentIndex(box.findData("1:1"))
    win.undo()
    assert box.currentData() == "16:9" and win.canvas.crop_ratio == pytest.approx(16 / 9)
    win.turn(1)
    x, y, w, h = win.edit.crop
    assert (w * 200) / (h * 400) == pytest.approx(9 / 16, rel=0.02)
    assert box.currentData() == "9:16" and win.canvas.crop_ratio == pytest.approx(9 / 16)
    win.undo()
    assert box.currentData() == "16:9"
    box.setCurrentIndex(box.findData("4:3"))
    win.turn(1)                                               # 3:4 is not offered: free
    assert box.currentData() == "free" and win.canvas.crop_ratio is None
    win.undo()
    assert box.currentData() == "4:3"
    box.setCurrentIndex(box.findData("free"))
    win.canvas.crop = (0.1, 0.1, 0.5, 0.7)                    # dragged freely
    win.canvas.crop_changed.emit()
    win.turn(1)
    win.undo()
    assert box.currentData() == "free" and win.edit.crop == (0.1, 0.1, 0.5, 0.7)


def test_a_free_crop_stays_free_after_undo_and_turning(app, tmp_path, opened):
    """Code review 34, second pass: the box followed undo/turn to any offered ratio the crop matched – a free crop
    of a 16:9 picture starts as exactly 16:9, so undo or a turn locked corner drags to 16:9/9:16, never picked."""
    win = opened(_source(tmp_path, 400, 225))
    box = win.crop_box
    box.setCurrentIndex(box.findData("free"))
    assert win.edit.crop == (0, 0, 1, 1)
    win.canvas.crop = (0.1, 0.1, 0.5, 0.7)                    # dragged freely
    win.canvas.crop_changed.emit()
    win.undo()                                                # back to the full frame: 16:9 by chance
    assert box.currentData() == "free" and win.canvas.crop_ratio is None
    assert win.canvas.crop_edit
    QTest.mousePress(win.canvas, Qt.LeftButton, Qt.NoModifier, _at(win, 0.999, 0.999))
    QTest.mouseMove(win.canvas, _at(win, 0.4, 0.95))           # the bottom right corner to a tall box
    QTest.mouseRelease(win.canvas, Qt.LeftButton, Qt.NoModifier, _at(win, 0.4, 0.95))
    app.processEvents()
    x, y, w, h = win.edit.crop
    assert (w * 400) / (h * 225) < 1.0                        # not snapped to 16:9
    win.undo()
    win.turn(1)
    assert box.currentData() == "free" and win.canvas.crop_ratio is None
    win.undo()
    box.setCurrentIndex(box.findData("none"))
    assert win.edit.crop is None
    win.undo()                                                # the free crop back: still free
    assert win.edit.crop == (0, 0, 1, 1) and box.currentData() == "free"
    box.setCurrentIndex(box.findData("16:9"))                 # a ratio the user picked comes back with its crop
    box.setCurrentIndex(box.findData("none"))
    win.undo()
    assert box.currentData() == "16:9" and win.canvas.crop_ratio == pytest.approx(16 / 9)


def test_two_editors_saving_at_once_never_share_a_file(tmp_path, opened, monkeypatch):
    """Code review 35/48: both editors of one screenshot picked the same free name before either had written it –
    one said 'Gespeichert' with the other's picture, the other failed."""
    src = _source(tmp_path)
    saved = []
    a, b = opened(src, on_saved=saved.append), opened(src, on_saved=saved.append)
    a.turn(1)
    b.flip(True)
    gate, started = threading.Event(), []
    real_save = imageedit.save

    def held_save(img, path, fmt="png"):
        started.append(path)
        gate.wait(30)
        return real_save(img, path, fmt)
    monkeypatch.setattr(qt_image.imageedit, "save", held_save)
    a.save()
    b.save()                                                  # before a's copy exists
    gate.set()
    a.wait_saved()
    b.wait_saved()
    assert len(saved) == 2 and saved[0] != saved[1], (a.status.text(), b.status.text())
    assert Image.open(saved[0]).size == (200, 400)            # a: turned
    pic = Image.open(saved[1])
    assert pic.size == (400, 200) and pic.getpixel((390, 10)) == (200, 30, 30)   # b: mirrored
    assert "Gespeichert" in a.status.text() and "Gespeichert" in b.status.text()
    assert qt_image._SAVING == {}


def test_typing_a_text_is_one_undo_step(app, opened):
    """Code review 36: every key typed into a text drawing was one undo step – a sentence pushed the crop and the
    censor boxes out of the 60 kept steps."""
    win = opened()
    win.crop_box.setCurrentIndex(win.crop_box.findData("16:9"))
    win.canvas.add_box((0.1, 0.1, 0.2, 0.2))
    win.tools.setCurrentIndex(1)
    win.draw_btns["text"].click()
    QTest.mouseClick(win.canvas, Qt.LeftButton, Qt.NoModifier, _at(win, 0.5, 0.5))
    assert len(win.undo_stack) == 3 and win.canvas.selected_shape().kind == "text"
    QTest.mouseClick(win.draw_text, Qt.LeftButton)
    win.draw_text.selectAll()
    sentence = "Hier stand der Killer die ganze Zeit hinter dem Generator!!"
    QTest.keyClicks(win.draw_text, sentence)
    assert [s.text for s in win.edit.shapes] == [sentence] and len(win.undo_stack) == 4
    QTest.keyClick(win.draw_text, Qt.Key_Return)              # done typing: the next text is a step of its own
    QTest.mouseClick(win.draw_text, Qt.LeftButton)
    QTest.keyClicks(win.draw_text, "?")
    assert len(win.undo_stack) == 5
    win.undo()
    assert [s.text for s in win.edit.shapes] == [sentence]
    QTest.keyClicks(win.draw_text, "x")                       # after an undo: a new step, the redo is gone
    assert len(win.undo_stack) == 5 and not win.redo_stack
    for _i in range(len(win.undo_stack)):
        win.undo()
    assert win.edit.crop is None and win.edit.censor == [] and win.edit.shapes == []


def test_pen_changes_only_touch_a_drawing_shown_as_picked(app, opened):
    """Code review 37: with the draw tool off (the picked frame is not drawn then) colour, size and 'Zeichnung
    entfernen' still changed the drawing picked earlier; choosing the size already shown did nothing."""
    win = opened()
    win.tools.setCurrentIndex(1)
    win.draw_btns["arrow"].click()
    win.canvas._new_shape(annotate.Shape("arrow", [(0.2, 0.5), (0.6, 0.5)], win.canvas.pen["colour"],
                                         win.canvas.pen["size"]))
    first = (annotate.COLOURS[0], annotate.SIZES[1])
    assert [(s.colour, s.size) for s in win.edit.shapes] == [first] and win.canvas.shape_sel == 0
    win.draw_btns["arrow"].click()                            # tool off
    win.colour_btns[annotate.COLOURS[3]].click()
    win.draw_size_box.setCurrentIndex(3)                      # the user picks "Sehr dick" (as a pick emits it)
    win.draw_size_box.activated.emit(3)
    win._draw_remove()
    assert [(s.colour, s.size) for s in win.edit.shapes] == [first]
    win.draw_btns["arrow"].click()
    QTest.mouseClick(win.canvas, Qt.LeftButton, Qt.NoModifier, _at(win, 0.4, 0.5))   # pick the arrow again
    assert win.canvas.shape_sel == 0 and len(win.edit.shapes) == 1
    win.draw_size_box.activated.emit(3)                       # the user picks the size the box already shows
    assert win.edit.shapes[0].size == annotate.SIZES[3]
    win.tools.setCurrentIndex(2)                              # leaving the tab: nothing stays picked either
    win.tools.setCurrentIndex(1)
    win.colour_btns[annotate.COLOURS[4]].click()
    assert win.edit.shapes[0].colour == annotate.COLOURS[0] and win.canvas.pen["colour"] == annotate.COLOURS[4]


def test_an_unreadable_picture_offers_no_tools(tmp_path, opened):
    """Code review 40: the crop box and 'Rahmen bearbeiten' stayed usable on 'Bild nicht lesbar' and raised
    AttributeError (no picture to measure)."""
    bad = tmp_path / "broken.png"
    bad.write_bytes(b"not a picture")
    win = opened(bad)
    assert "nicht lesbar" in win.status.text() and not win.tools.isEnabled()
    win.crop_box.blockSignals(True)
    win.crop_box.setCurrentIndex(win.crop_box.findData("1:1"))
    win.crop_box.blockSignals(False)
    win._crop_picked(0)
    win.crop_btn.setChecked(True)
    win._crop_tool()
    assert win.edit.crop is None and win.result() is None


def test_a_slider_move_right_after_undo_is_a_step_of_its_own(opened):
    """Code review 42: within 120 ms after Ctrl+Z (the slider's redraw timer still running) a slider move got no undo
    step and kept the stale redo – the next undo took it back together with the step before."""
    win = opened()
    sl = win.sliders["brightness"][0]
    win.canvas.add_box((0.1, 0.1, 0.2, 0.2))
    sl.setValue(150)
    win.undo()
    assert win._adjust_timer.isActive() and win.edit.brightness == 1.0
    sl.setValue(60)
    assert len(win.undo_stack) == 2 and not win.redo_stack
    win.undo()
    assert win.edit.brightness == 1.0 and win.edit.censor == [(0.1, 0.1, 0.2, 0.2)]


def test_a_picture_too_large_for_pillow_is_unreadable_not_a_crash(tmp_path, opened, monkeypatch):
    """Code review 21: Pillow refuses pictures over 2 × MAX_IMAGE_PIXELS with DecompressionBombError (no OSError) –
    the editor raised out of the double-click instead of saying 'Bild nicht lesbar'."""
    src = _source(tmp_path)
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 1000)     # 400×200 = 80 000 px > 2 × 1000
    win = opened(src)
    assert "nicht lesbar" in win.status.text() and not win.save_btn.isEnabled() and win.result() is None
