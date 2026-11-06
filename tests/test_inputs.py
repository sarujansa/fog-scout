"""1.39: the input card "Eingaben" – what is read (only a fixed list of keys, only when allowed and DBD is in front),
how it is drawn (never breathes, patches = the whole drawing) and where it stands."""
import ast
import pathlib
import random

import numpy as np

from fogscout import config, inputs, layout, overlay_render
from fogscout.inputs import EMPTY, InputState, KEY_IDS, PAD_IDS, Reader

PKG = pathlib.Path(__file__).resolve().parent.parent / "fogscout"


def test_only_the_listed_keys_are_ever_asked_for():
    """The hard rule: DBD's default keys and the mouse buttons – no other letter, no digit, no Enter (chat)."""
    assert set(KEY_IDS) == {"q", "w", "e", "r", "shift", "a", "s", "d", "ctrl", "space", "lmb", "rmb", "mmb"}
    vks = {vk for _k, vk, _cap in inputs.KEYS}
    assert vks == {0x51, 0x57, 0x45, 0x52, 0x10, 0x41, 0x53, 0x44, 0x11, 0x20, 0x01, 0x02, 0x04}
    assert 0x0D not in vks and not any(0x30 <= vk <= 0x39 for vk in vks)


def test_the_reader_calls_only_polling_apis_never_a_hook():
    """inputs.py asks Windows only for the key state, the gamepad state and the foreground window – no hook, no
    Raw Input, no message (tests/test_guards.py covers sending input for the whole package)."""
    tree = ast.parse((PKG / "inputs.py").read_text(encoding="utf-8"))
    called = {n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    win = {c for c in called if c[:1].isupper()}
    assert win <= {"GetAsyncKeyState", "XInputGetState", "GetForegroundWindow", "GetAncestor", "WinDLL", "Thread",
                   "Event", "Structure", "POINTER"}
    text = (PKG / "inputs.py").read_text(encoding="utf-8")
    for bad in ("SetWindowsHookEx", "RegisterRawInputDevices", "GetRawInputData", "GetKeyboardState", "ToUnicode",
                "OpenProcess"):
        assert bad not in text


def test_the_dll_comes_from_system32_only():
    text = (PKG / "inputs.py").read_text(encoding="utf-8")
    assert "WinDLL(system_exe(name))" in text and 'WinDLL("xinput' not in text


def test_nothing_is_looked_at_while_not_allowed():
    calls = []
    r = Reader(poll=lambda hwnd: calls.append(hwnd) or InputState(keys=frozenset({"w"})))
    r.look()
    assert calls == [] and r.state == EMPTY
    r._hwnd = 42                                   # allowed (without starting the thread)
    r.look()
    assert calls == [42] and r.state.keys == {"w"}
    n = r.changes
    r.allow(None)                                  # not allowed any more: empty at once, no further look
    r.look()
    assert calls == [42] and r.state == EMPTY and r.changes == n + 1


def test_dbd_not_in_front_reads_as_nothing_held():
    r = Reader(poll=lambda hwnd: None)             # Win32Poll returns None when DBD is not the foreground window
    r._hwnd = 7
    r.state = InputState(keys=frozenset({"w"}))
    r.look()
    assert r.state == EMPTY


def test_gamepad_values_have_dead_zones():
    st = inputs.pad_state(0x1000 | 0x0100, 20, 255, 5000, -32768, 0, 32767)
    assert st.pad == {"a", "lb"} and st.pad_on
    assert st.lt == 0 and st.rt == 1.0                       # below the trigger threshold: 0
    assert st.lx == 0 and st.ly == -1.0 and st.ry == 1.0     # 5000/32767 is inside the stick's dead zone
    assert not inputs.pad_active(inputs.pad_state(0, 10, 10, 1000, -1000, 0, 0))


def test_stick_steps_are_few():
    assert inputs.stick_steps(0, 0) == (0.0, 0.0)
    assert inputs.stick_steps(0.1, 0.95) == (0.0, 1.0)
    assert inputs.stick_steps(0.3, 0.3) == (0.354, 0.354)    # half way, diagonal
    rng = random.Random(3)
    seen = {inputs.stick_steps(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(2000)}
    assert len(seen) <= 1 + 2 * inputs.STICK_DIRS


def test_auto_shows_the_device_used_last():
    c = inputs.DeviceChoice()
    assert c.layout("auto", EMPTY) == "keyboard"
    assert c.layout("auto", InputState(pad=frozenset({"a"}))) == "gamepad"
    assert c.layout("auto", EMPTY) == "gamepad"                          # nothing held: stays
    assert c.layout("auto", InputState(keys=frozenset({"w"}))) == "keyboard"
    assert c.layout("gamepad", InputState(keys=frozenset({"w"}))) == "gamepad"


def _states(rng, n):
    return [InputState(keys=frozenset(k for k in KEY_IDS if rng.random() < 0.35),
                       pad=frozenset(k for k in PAD_IDS if rng.random() < 0.35),
                       lt=rng.random(), rt=rng.choice([0.0, rng.random()]), lx=rng.uniform(-1, 1),
                       ly=rng.uniform(-1, 1), rx=rng.uniform(-1, 1), ry=rng.uniform(-1, 1)) for _ in range(n)]


def test_the_card_never_changes_its_size():
    """Nothing breathes: every state and both layouts have the size of the height."""
    for h in (40, 115, 230):
        size = overlay_render.input_size(h)
        for st in [EMPTY, inputs.SAMPLE] + _states(random.Random(h), 20):
            for lay in ("keyboard", "gamepad"):
                assert overlay_render.input_card(st, lay, h, "#c9a227").size == size


def test_the_input_card_from_patches_is_the_whole_drawing():
    from fogscout.skin import accent_rgba
    rng = random.Random(7)
    for st in _states(rng, 40):
        for lay in ("keyboard", "gamepad"):
            for h in (60, 115):
                got = np.asarray(overlay_render.input_card(st, lay, h, "#5ab0ff"))
                lx, ly = inputs.stick_steps(st.lx, st.ly)
                rx, ry = inputs.stick_steps(st.rx, st.ry)
                shown = InputState(keys=st.keys, pad=st.pad, lt=round(st.lt * 8) / 8, rt=round(st.rt * 8) / 8,
                                   lx=lx, ly=ly, rx=rx, ry=ry)
                w, hh = overlay_render.input_size(h)
                ref = np.asarray(overlay_render._input_full(shown, lay, w, hh, accent_rgba("#5ab0ff"), True))
                assert np.array_equal(got, ref), (lay, h, st)


def test_a_held_key_lights_up():
    idle = overlay_render.input_card(EMPTY, "keyboard", 115, "#ff0000")
    held = overlay_render.input_card(InputState(keys=frozenset({"w"})), "keyboard", 115, "#ff0000")
    diff = np.any(np.asarray(idle) != np.asarray(held), axis=2)
    ys, xs = np.nonzero(diff)
    assert len(xs) and xs.max() - xs.min() < idle.width / 5           # only the W key changed
    r, g, b, _a = held.getpixel((int(xs.mean()), int(ys.min()) + 6))
    assert r > 200 and g < 60 and b < 60


def test_the_card_stands_at_the_bottom_of_its_bar():
    o = dict(config.DEFAULTS["overlay"])
    game = (0, 0, 3440, 1440)
    h = layout.inputs_height(o, game, 17, overlay_render.INPUT_RATIO)
    size = overlay_render.input_size(h)
    x, y = layout.inputs_xy("bottom_right", game, size, 17)
    assert 3000 <= x and x + size[0] <= 3440 and y + size[1] == 1440 - 17
    assert abs((x + size[0] / 2) - (3440 - 220)) <= 1                  # centred in the right bar (440 px)
    x, _y = layout.inputs_xy("bottom_left", game, size, 17)
    assert abs((x + size[0] / 2) - 220) <= 1
    x, y = layout.inputs_xy("bottom_left", (0, 0, 2560, 1440), size, 17)   # no bars: the window's corner
    assert (x, y + size[1]) == (17, 1440 - 17)
    x, y = layout.inputs_xy("custom", game, size, 17, own=(0.5, 0.5))
    assert abs(x + size[0] / 2 - 1720) <= 1 and abs(y + size[1] / 2 - 720) <= 1
    x, y = layout.inputs_xy("custom", game, size, 17, own=(1.0, 1.0))   # never outside the window
    assert x + size[0] <= 3440 and y + size[1] <= 1440


def test_the_card_is_never_wider_than_its_bar():
    o = dict(config.DEFAULTS["overlay"], inputs_scale=2.0)
    h = layout.inputs_height(o, (0, 0, 3440, 1440), 17, overlay_render.INPUT_RATIO)
    assert overlay_render.input_size(h)[0] <= 440 - 2 * 17
    own = layout.inputs_height(dict(o, inputs_pos="custom"), (0, 0, 3440, 1440), 17, overlay_render.INPUT_RATIO)
    assert own == int(1440 * layout.INPUT_BASE * 2.0)                    # an own place keeps its size


def test_the_detection_blacks_out_the_input_card():
    from fogscout.worker import DetectionWorker
    w = DetectionWorker.__new__(DetectionWorker)
    w.overlay_rect = w.hud_rect = w.media_rect = w.today_rect = w.info_rect = w.toast_rect = None
    w.guide_rects = ()
    assert not w._own_windows()
    w.inputs_rect = (10, 20, 30, 40)
    assert w._own_windows()
    img = np.full((100, 100, 3), 200, np.uint8)
    w._mask_screen(img, True, 0, 0)
    assert img[20:60, 10:40].max() == 0 and img[61:, :].min() == 200


def test_the_preview_shows_the_card_where_the_game_does():
    from fogscout import preview
    o = dict(config.DEFAULTS["overlay"], show_inputs=True)
    info = {"timer": "", "server": "", "ping": None, "record": "", "memo": (), "name": "", "realm": ""}
    out, _rect = preview.layers(3440, 1440, o, "", [], None, None, "", info, 0.36, inputs="gamepad")
    layers = {n: (pic, x, y) for n, pic, x, y in out}
    pic, x, y = layers["inputs"]
    game = (0, 0, 3440, 1440)
    margin = int(1440 * o["margin"])
    h = layout.inputs_height(o, game, margin, overlay_render.INPUT_RATIO)
    assert pic.size == overlay_render.input_size(h)
    assert (x, y) == layout.inputs_xy("bottom_right", game, pic.size, margin, None, layout.bar_bands(o, game, margin))


def test_inputs_settings_are_part_of_a_layout():
    from fogscout import layoutmem
    assert {"inputs_pos", "inputs_xy", "inputs_scale"} <= set(layoutmem.OVERLAY_KEYS)
    assert config.DEFAULTS["overlay"]["show_inputs"] is False             # off until switched on
