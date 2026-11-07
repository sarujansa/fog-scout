"""1.44.1 (user: „nicht zufrieden mit dem Verschieben der UI-Elemente“ – springt, rastet falsch, fummelig): an
element put somewhere by hand keeps that place – the latest drop wins a collision, a map past the bar's edge is
free (its middle decides), a right click puts one element back, the edit frame is grabbable everywhere."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import layout, overlay_render  # noqa: E402
from fogscout.app_sysinfo import SysInfo  # noqa: E402

import test_uimodel  # noqa: E402

app_root = test_uimodel.app_root                 # the same fixture (a program folder with maps for the App)


def test_an_own_place_is_in_the_bar_only_with_its_middle_in_it():
    gw, gh = 3440, 1440
    bar = layout.bar_width(gw, gh)                                             # 440
    assert layout.bar_side("custom", 100, 200, 0, gw, bar) == "left"
    assert layout.bar_side("custom", 380, 200, 0, gw, bar) is None             # reaches in, middle outside: free
    assert layout.bar_side("custom", 300, 200, 0, gw, bar) == "left"           # middle at 400: still in it
    assert layout.bar_side("custom", gw - 300, 200, 0, gw, bar) == "right"
    assert layout.bar_side("custom", gw - 580, 200, 0, gw, bar) is None
    assert layout.bar_side("auto", 1500, 200, 0, gw, bar) == "left"            # the corners as before


def test_the_latest_drop_comes_first_when_elements_collide():
    s = object.__new__(SysInfo)
    s._el_shift = {"music": (0, 40), "today": (0, -10)}
    boxes = [("hud", (0, 0, 10, 10)), ("today", (0, 0, 10, 10)), ("music", (0, 0, 10, 10))]
    assert [n for n, _b in s._el_priority(boxes)] == ["hud", "today", "music"]   # nothing dropped: as before
    s._el_dropped("music")
    s._el_dropped("today")
    assert s._el_shift == {} and s._drop_order == ["today", "music"]
    assert [n for n, _b in s._el_priority(boxes)] == ["today", "music", "hud"]
    s._el_dropped("music")
    assert [n for n, _b in s._el_priority(boxes)] == ["music", "today", "hud"]
    shift = layout.resolve(s._el_priority([("today", (0, 0, 100, 50)), ("music", (0, 20, 100, 50))]), [],
                           (0, 0, 3440, 1440), None, 8)
    assert "music" not in shift and "today" in shift                            # the one just put there stays


def test_the_edit_frame_can_be_grabbed_everywhere_and_keeps_its_size():
    from PIL import Image
    pic = Image.new("RGBA", (120, 60), (0, 0, 0, 0))
    pic.putpixel((60, 30), (255, 255, 255, 255))
    out = overlay_render.add_border(pic, "HEUTE")
    assert out.size == (120, 60)
    assert out.getchannel("A").getextrema()[0] > 0                             # no pixel lets the mouse through
    assert out.getpixel((60, 30))[:3] == (255, 255, 255)                       # the content stays on top


def test_a_right_click_puts_one_element_back_and_a_drop_ticks_at_once(app_root):
    from fogscout.app import App
    from fogscout.config import DEFAULTS
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app._game_rect = lambda: (0, 0, 3440, 1440)
        o = app.settings["overlay"]
        ticks = []
        real = app._tick_overlay
        app._tick_overlay = lambda **kw: (ticks.append(1), real(**kw))[1]
        app._music_own_place(0.3, 0.4)
        app._today_own_place(0.6, 0.2)
        assert o["media_pos"] == o["today_pos"] == "custom" and len(ticks) == 2
        assert app._drop_order[:2] == ["today", "music"]
        app._el_reset("music")
        assert o["media_pos"] == DEFAULTS["overlay"]["media_pos"] and o["media_xy"] == DEFAULTS["overlay"]["media_xy"]
        assert o["today_pos"] == "custom" and "music" not in app._drop_order        # the other stays
        app.undo_layout()
        assert o["media_pos"] == "custom"                                           # one undo step
        app.settings.set("sysinfo", "custom")
        app._el_reset("hud")
        assert app.settings.get("sysinfo") == DEFAULTS["sysinfo"]
        o["anchor"] = "custom"
        app._el_reset("map")
        assert o["anchor"] == "auto"
        app._el_reset("nothing")                                                    # unknown: ignored
    finally:
        app.quit()


# ---- 1.44.2: the preview on the page "Overlay"
import test_qt  # noqa: E402

qapp, keep = test_qt.qapp, test_qt.keep          # the same fixtures (a QApplication, widgets deleted after the test)


def test_a_drag_in_the_preview_keeps_only_its_newest_step():
    from fogscout.app_qt import QtShell, coalesce_slot
    import queue
    assert coalesce_slot("act", ("ov.preview", ("place", "music", 1, 2))) == ("ov.preview", "place", "music")
    assert coalesce_slot("act", ("ov.preview", ("limit", "left", "top", 3))) == ("ov.preview", "limit", "left", "top")
    assert coalesce_slot("act", ("ov.preview", ("select", "music"))) is None       # a click always counts
    assert coalesce_slot("act", ("ov.preview", ("nudge", 1, 0))) is None           # each arrow key counts
    assert coalesce_slot("answer", True) is None
    shell = object.__new__(QtShell)
    shell.events = queue.Queue()
    for i in range(60):
        shell._qt_post("act", ("ov.preview", ("place", "music", i, 0)))
    shell._qt_post("act", ("ov.preview", ("place", "hud", 5, 5)))
    shell._qt_post("act", ("ov.preview", ("select", "map")))
    queued = [shell.events.get_nowait() for _ in range(shell.events.qsize())]
    assert [q[1] for q in queued] == ["act_latest", "act_latest", "act"]           # one per element, in order
    assert shell._act_latest[queued[0][2]] == ("ov.preview", ("place", "music", 59, 0))   # the newest step


def test_a_drag_commits_once_per_pass_and_ends_where_the_mouse_let_go(app_root):
    from fogscout.app import App
    app = App(str(app_root), simulate=str(app_root / "sim"))
    try:
        app._game_rect = lambda: (0, 0, 3440, 1440)
        app.toggle_edit()
        app._drain_events()
        commits = []
        pick = app._preview_pick_now
        app._preview_pick_now = lambda v: (commits.append(v), pick(v))[1]
        for i in range(60):                                  # the mouse moves faster than the window drains
            app._qt_post("act", ("ov.preview", ("place", "music", 2900 + i * 3, 900)))
            if i % 5 == 4:
                app._drain_events()
        app._drain_events()
        assert len(commits) == 12 and commits[-1] == ("place", "music", 2900 + 59 * 3, 900)   # was 60
        assert app.settings["overlay"]["media_pos"] == "custom"
    finally:
        app.quit()


def _view(keep, layers, pics, **extra):
    import queue
    from fogscout import qt_window
    posted = queue.Queue()
    view = keep(qt_window.PreviewView("ov.preview", lambda a, arg=None: posted.put((a, arg))))
    view.resize(1000, 460)
    data = {"screen": (3440, 1440), "bar": 440, "rect": (20, 20, 300, 400, 400), "opacity": 1.0, "pics": pics,
            "layers": layers, "editing": True}
    data.update(extra)
    view.show_state({"data": data, "visible": True})
    view.show()
    return view, posted, data


def test_the_preview_takes_the_mouse_on_the_visible_part_only(qapp, keep):
    from PIL import Image
    card = Image.new("RGBA", (600, 100), (0, 0, 0, 0))                  # a card padded to a wide column …
    card.paste(Image.new("RGBA", (200, 100), "white"), (400, 0))        # … visible only on its right third
    view, _posted, _d = _view(keep, [("map", 2000, 300, 300, 400), ("music", 1900, 600, 600, 100)],
                              {"map": Image.new("RGBA", (300, 400), "blue"), "music": card})
    assert view.layer_at(2350, 650)[0] == "music"
    assert view.layer_at(2100, 650)[0] == "map"                         # the map below the card's empty edge
    tiny = Image.new("RGBA", (10, 10), "white")
    view2, _p, _d = _view(keep, [("hud", 3000, 100, 10, 10)], {"hud": tiny})
    s = view2._frame()[2]
    assert view2.layer_at(3005 + 10 / s, 105)[0] == "hud"               # never smaller than HIT_MIN widget px


def test_the_preview_shows_where_a_dragged_element_lands_and_snaps_to_where_others_were(qapp, keep):
    from PIL import Image
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    pics = {n: Image.new("RGBA", (200, 100), "white") for n in ("hud", "music")}
    layers = [("hud", 3100, 20, 300, 200), ("music", 3100, 300, 300, 100)]
    view, posted, data = _view(keep, layers, pics, selected="music")
    ox, oy, s = view._frame()

    def at(x, y):
        return QPoint(round(ox + x * s), round(oy + y * s))
    QTest.mousePress(view, Qt.LeftButton, Qt.NoModifier, at(3150, 320))
    assert view._snap_from == tuple(layers)
    QTest.mouseMove(view, at(3150, 1020))
    assert view._landing() is None                                    # the App has not answered yet: no frame
    moved = [("hud", 2600, 20, 300, 200), ("music", 3100, 900, 300, 100)]   # the App's places now (reflowed)
    view.show_state({"data": dict(data, layers=moved), "visible": True})
    assert view._landing() == ("music", 3100, 900, 300, 100)          # dashed frame: it lands there
    assert view._snap_from == tuple(layers)                           # snapping still to where the others were
    view.grab()                                                       # paints the frame
    QTest.mouseRelease(view, Qt.LeftButton, Qt.NoModifier, at(3150, 1020))
    assert view._landing() is None                                    # dropped: no frame any more
    sent = [posted.get_nowait() for _ in range(posted.qsize())]
    assert sent[-1][1][1][:2] == ("place", "music") and not any(v[1][1][0] == "select" for v in sent)
