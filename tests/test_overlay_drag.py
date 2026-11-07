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
