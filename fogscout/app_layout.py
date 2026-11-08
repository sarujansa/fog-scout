"""Overlay layout, part of App (1.65): undo of place/size changes, one layout per DBD window size, arrow keys in
the preview. Pure logic in layoutmem.py."""
from __future__ import annotations

import copy
import time

from . import layout, layoutmem
from .appconst import SELECTABLE
from .config import HUD_SHOWN
from .i18n import N_, _

CAP_FIT = 0.97             # 1.8.24: shown below 97 % of the asked size = the bar holds the element back
SIZE_SETTLE = 2.0          # s a new window size must stay before its layout is loaded (no switch while resizing)


# 1.44.1: right click on an element in edit mode puts it back – the overlay keys of its usual place (config.DEFAULTS)
RESET_KEYS = {"map": ("anchor",), "today": ("today_pos", "today_xy"), "music": ("media_pos", "media_xy"),
              "text": ("info_pos", "info_xy"), "inputs": ("inputs_pos", "inputs_xy")}
RESET_NAMES = {"map": N_("Karte"), "hud": N_("Systemwerte"), "today": N_("Heute"), "music": N_("Musik"),
               "text": N_("Infos"), "inputs": N_("Eingaben")}
# 1.46: the overlay editor – the map's corners of the quick places are its preset anchors (they follow the bar)
MAP_CORNERS = {(0, 0): "top-left", (2, 0): "top-right", (0, 2): "bottom-left", (2, 2): "bottom-right"}
CELL_TOL = 0.006             # share of the game height: an element this close to a quick place is "there"
LOCKED_TOO = ("place", "resize", "nudge")       # preview acts a locked element ignores


class LayoutMemory:
    def _layout_init(self):
        self._undo = layoutmem.UndoStack()
        self._layout_seen = (None, 0.0)          # (window size, since) – a new size must settle first

    # ---------------------------------------------------------------- undo
    def _layout_mark(self):
        """Before a change of place or size: remember the layout (one step per gesture)."""
        if getattr(self, "_layout_applying", False):
            return
        self._undo.mark(layoutmem.snapshot(self.settings.data), time.monotonic())
        self._undo_btn_state()

    def _el_reset(self, name):
        """1.44.1: one element back to its usual place (right click on it in edit mode, game or preview) – one undo
        step; the others stay where they are ("Zurücksetzen" only ever put the map back)."""
        from .config import DEFAULTS
        if name not in RESET_NAMES:
            return
        self._layout_mark()
        data = self.settings.data
        o = data.setdefault("overlay", {})
        if name == "hud":
            if data.get("sysinfo") == "custom":
                data["sysinfo"] = DEFAULTS["sysinfo"]
            data["sysinfo_pos"] = copy.deepcopy(DEFAULTS["sysinfo_pos"])
        else:
            for k in RESET_KEYS[name]:
                o[k] = copy.deepcopy(DEFAULTS["overlay"][k])
        self._drop_order = [n for n in getattr(self, "_drop_order", []) if n != name]
        getattr(self, "_el_shift", {}).pop(name, None)
        if name == "inputs" and hasattr(self, "inputs_pos_var"):
            from .appconst import INPUT_SPOTS
            self.inputs_pos_var.set(_(dict(INPUT_SPOTS).get(o["inputs_pos"], "")))
        self._layout_apply(layoutmem.snapshot(data))      # every control that shows it, saved, one tick
        self._log(_("{name} wieder an seinem üblichen Platz.", name=_(RESET_NAMES[name])), "Overlay")

    def undo_layout(self):
        """Button "Rückgängig" / Ctrl+Z on the overlay page: the layout before the last change."""
        snap = self._undo.undo(layoutmem.snapshot(self.settings.data))
        if snap is None:
            self._log(_("Nichts rückgängig zu machen."), "Overlay")
        else:
            self._layout_apply(snap)
            self._log(_("Position/Grösse rückgängig gemacht."), "Overlay")
        self._undo_btn_state()

    def _undo_btn_state(self):
        btn = getattr(self, "undo_btn", None)
        if btn is not None:
            btn.state(["!disabled"] if len(self._undo) else ["disabled"])

    def _layout_apply(self, snap):
        """A stored layout into the settings and every control that shows it."""
        from .appconst import BAR_ALIGNS, HUD_SIDES, MEDIA_SPOTS, TODAY_SPOTS
        self._layout_applying = True
        try:
            layoutmem.apply(self.settings.data, snap)
            o = self.settings["overlay"]
            self.anchor_var.set(self._anchor_text(o.get("anchor", "auto")))
            self._set_pos_sliders(o.get("pos_x", 0.0), o.get("pos_y", 0.0))
            self.size_var.set(o["height"] * 100)
            self.size_label.configure(text=f"{o['height'] * 100:.0f} %")
            self.media_size_var.set(round(o.get("media_scale", 1.0) * 100))
            self.media_pos_var.set(_(dict(MEDIA_SPOTS).get(o.get("media_pos", "bottom_right"), "")))
            self.today_pos_var.set(_(dict(TODAY_SPOTS).get(o.get("today_pos", "below"), "")))
            if hasattr(self, "keep_out_var"):                                # 1.8.25
                self.keep_out_var.set(bool(o.get("keep_out_on", True)))
            if hasattr(self, "same_width_var"):                              # 1.8.29
                self.same_width_var.set(bool(o.get("cards_same_width", True)))
            if hasattr(self, "info_pos_var"):                                # 1.8.24
                from .appconst import INFO_SPOTS
                self.info_pos_var.set(_(dict(INFO_SPOTS).get(o.get("info_pos", "below"), "")))
            self.bar_align_var.set(_(dict(BAR_ALIGNS).get(o.get("bar_align", "centre"), "")))
            self.gap_var.set(float(o.get("stack_gap", 8)))
            self.limits_var.set(bool(o.get("bar_limits_on", False)))         # 1.8.14
            self.limits_same_var.set(bool(o.get("bar_limits_same", False)))
            self.sysinfo_var.set(_(dict(HUD_SIDES).get(self.settings.get("sysinfo", "off"), "")))
            self._pos_hint()
            self._show_map_size()
            self._sel_sync()
        finally:
            self._layout_applying = False
        self._save_soon()
        self._tick_overlay(reschedule=False)

    # ---------------------------------------------------------------- per window size
    def _layout_size_key(self):
        g = self.game
        if g is None or g.minimized or g.width <= 100:
            return None
        return layoutmem.size_key(g.width, g.height)

    def _layout_size_tick(self):
        """4×/s: the layout of the DBD window size in use is kept in settings.layouts; a new size (settled for
        SIZE_SETTLE) loads its own layout, a size seen for the first time starts with the one in use."""
        if not hasattr(self, "anchor_var"):
            return
        q = getattr(self, "qt", None)                 # 1.16.1 (audit, 10–13 ms 4×/s): the slider's mark is for the
        if q is None or (q.current_key() == "overlay" and q.isVisible()):   # overlay page – computed only there
            self._size_cap_tick()
        scope = self._size_scope_text()
        if scope != self.size_scope_var.get():
            self.size_scope_var.set(scope)
            self._sel_sync()                      # another map on display: its own size on the slider
        text = self._layout_size_text()
        if text != self.per_size_text.get():
            self.per_size_text.set(text)
        if not self.settings.get("layout_per_size", True):
            return
        store = self.settings.data.setdefault("layouts", {})
        cur = self.settings.get("layout_key")
        key = self._layout_size_key()
        now = time.monotonic()
        if key != self._layout_seen[0]:
            self._layout_seen = (key, now)
        if key and key != cur and now - self._layout_seen[1] >= SIZE_SETTLE:
            if cur:
                store[cur] = layoutmem.snapshot(self.settings.data)
            self.settings.set("layout_key", key)
            if key in store and cur:
                self._layout_apply(store[key])
                self._undo.clear()
                self._undo_btn_state()
                self._log(_("DBD-Fenster {size}: Layout für diese Grösse geladen.", size=key.replace("x", "×")),
                          "Overlay")
            elif cur:
                self._log(_("DBD-Fenster {size}: neue Grösse – Layout wird ab jetzt dafür gemerkt.",
                            size=key.replace("x", "×")), "Overlay")
            store[key] = layoutmem.snapshot(self.settings.data)
            self._save_soon()
            return
        if cur:                                  # changes (also with DBD closed) belong to the size last used
            snap = layoutmem.snapshot(self.settings.data)
            if store.get(cur) != snap:
                store[cur] = snap

    def _per_size_changed(self):
        self.settings.set("layout_per_size", bool(self.per_size_var.get()))
        self._save_soon()

    def _layout_size_text(self):
        key = self.settings.get("layout_key")
        if not self.settings.get("layout_per_size", True) or not key:
            return ""
        n = len(self.settings.get("layouts") or {})
        return _("Aktuell: Layout für {size} · {n} Grössen gemerkt", size=key.replace("x", "×"), n=n)

    # ---------------------------------------------------------------- the bar limits the map
    def _size_cap_tick(self):
        """1.65.2 (user: "die Map wird nicht grösser"): in a black bar the map can only be as wide as the bar – on
        3440×1440 about 31 % of the height. Say so under the size slider when that is what holds it back.
        1.8.24 (user: "die Map mit der Scrollbar grösser – ändert sich nicht in der Vorschau, evtl. die anderen
        Elemente auch"): for every element, from the preview's own fitting (``fits``) – the slider marks the size
        from which on nothing grows (``_dbdms_cap``, the value reads "36 % → 31 %") and the hint says why."""
        if not hasattr(self, "size_cap_var"):
            return
        name = getattr(self, "_sel", "map")
        data = self._preview_data()
        fit = float(data.get("fits", {}).get(name, 1.0))
        lo, _hi, value = self._sel_range(name)
        cap = max(lo, value * fit) if fit < CAP_FIT else None
        if cap is not None and value - cap < 1:
            cap = None                            # rounding: not worth a mark
        text = ""
        if cap is not None:
            o = self.settings["overlay"]
            what = _(dict(SELECTABLE).get(name, "Karte"))
            text = _("{what} ist hier schon so gross wie möglich – ab {cap} % ändert der Regler nichts mehr "
                     "(der schwarze Balken ist voll).", what=what, cap=f"{cap:.0f}")
            if name in ("map", "text") and not o.get("grow_past_bar", False):
                text += " " + _("Grösser mit „Karte darf grösser als der Balken werden“ (ragt dann ins Spielbild).")
        scale = getattr(self, "sel_scale", None)
        if scale is not None and getattr(scale, "_dbdms_cap", None) != cap:
            scale._dbdms_cap = cap
        if text != self.size_cap_var.get():
            self.size_cap_var.set(text)

    # ---------------------------------------------------------------- arrow keys in the preview
    def _nudge(self, dx, dy):
        """Arrow keys on the preview (moving mode): the picked element by (dx, dy) screen pixels."""
        lay = {n: (x, y) for n, x, y, _w, _h in self._preview_data()["layers"]}.get(getattr(self, "_sel", "map"))
        if lay is None:
            return
        self._preview_pick_now(("place", self._sel, lay[0] + dx, lay[1] + dy))

    # ---------------------------------------------------------------- 1.46: the overlay editor
    def _locked_names(self) -> set:
        locked = self.settings["overlay"].get("locked") or []
        return {n for n in locked if n in RESET_NAMES} if isinstance(locked, list) else set()

    def _el_locked(self, name) -> bool:
        return name in self._locked_names()

    def _lock_toggle(self, name, on):
        """Lock / unlock one element (the editor's list, the right-click menu): a locked element is not dragged in
        the preview nor in the game (its window stays click-through while moving). Not part of a layout."""
        if name not in RESET_NAMES:
            return
        locked = self._locked_names()
        locked = (locked | {name}) if on else (locked - {name})
        self.settings["overlay"]["locked"] = sorted(locked)
        self.overlay.set_locked(bool(self.overlay.editing) and "map" in locked)
        self._log(_("{name} gesperrt – bleibt beim Anordnen, wo es ist.", name=_(RESET_NAMES[name])) if on else
                  _("{name} entsperrt.", name=_(RESET_NAMES[name])), "Overlay")
        self._save_soon()
        self._tick_overlay(reschedule=False)

    def _el_editable(self, name) -> bool:
        """The element's window can be grabbed now: moving mode on and the element not locked."""
        return bool(self.overlay.editing) and not self._el_locked(name)

    def _el_shown(self, name) -> bool:
        o = self.settings["overlay"]
        if name == "map":
            return bool(o.get("show_map", True))
        if name == "text":
            return layout.info_apart(o)
        if name == "hud":
            return self.settings.get("sysinfo", "off") in HUD_SHOWN
        return bool(o.get({"today": "show_today", "music": "show_media", "inputs": "show_inputs"}[name],
                          name != "inputs"))

    def _el_place_text(self, name) -> str:
        o = self.settings["overlay"]
        if name == "map" and o.get("anchor", "auto") not in ("auto", "custom"):
            return self._anchor_text(o["anchor"])
        own = layout.own_places(o, self.settings.get("sysinfo", "off"))
        return _("eigener Platz") if name in own or (name == "map" and o.get("anchor") == "custom") \
            else _("automatisch")

    def _elements_data(self) -> dict:
        """The editor's list: per element shown / its place / size / locked, the element picked, moving mode and
        the window size whose layout is edited."""
        o = self.settings["overlay"]
        own = layout.own_places(o, self.settings.get("sysinfo", "off"))
        locked = self._locked_names()
        rows = {}
        for name, _label in SELECTABLE:
            rows[name] = {"shown": self._el_shown(name), "own": name in own or (name == "map" and
                                                                                   o.get("anchor") == "custom"),
                          "place": self._el_place_text(name), "size": round(self._sel_range(name)[2]),
                          "locked": name in locked, "can_hide": name != "text"}
        key = self.settings.get("layout_key") if self.settings.get("layout_per_size", True) else ""
        return {"order": [n for n, _l in SELECTABLE], "rows": rows, "selected": getattr(self, "_sel", "map"),
                "editing": bool(self.overlay.editing), "layout": key or ""}

    def _elements_act(self, value):
        """A click in the editor's list: ("select", name) / ("general",) / ("show", name, on) / ("lock", name, on) /
        ("menu", name, x, y)."""
        what = value[0] if value else None
        if what == "select":
            self._select(value[1])
        elif what == "general":
            qt = getattr(self, "qt", None)
            if qt is not None and hasattr(qt, "open_tab"):
                qt.open_tab("overlay", "ov.pos")
        elif what == "show":
            self._el_show_switch(value[1], bool(value[2]))
        elif what == "lock":
            self._lock_toggle(value[1], bool(value[2]))
        elif what == "menu":
            self._preview_menu(value[1], (value[2], value[3]))

    def _el_show_switch(self, name, on):
        """The eye in the editor's list: the element's own switch (the same tick box / choice as in its tab)."""
        if name == "text" or on == self._el_shown(name):
            return
        if name == "map":
            self.show_map_var.set(on)
            self._overlay_flags_changed()
        elif name == "hud":
            from .appconst import HUD_SIDES
            side = (getattr(self, "_sysinfo_last", "") or "right") if on else "off"
            self.sysinfo_var.set(_(dict(HUD_SIDES)[side]))
            self._sysinfo_changed()
        elif name == "today":
            self.today_var.set(on)
            self._look_flags_changed()
        elif name == "music":
            self.media_var.set(on)
            self._look_flags_changed()
        elif name == "inputs":
            self.inputs_on_var.set(on)
            self._inputs_on_changed()

    def _cell_box(self, name, col, row):
        """(x, y) in game pixels of ``name`` at the quick place (col, row) – corners and edges keep the margin."""
        data = self._preview_data()
        size = {n: (w, h) for n, _x, _y, w, h in data["layers"]}.get(name)
        if size is None:
            return None
        gw, gh = data["screen"]
        m = int(gh * self.settings["overlay"]["margin"])
        w, h = size
        return (m, (gw - w) / 2, gw - m - w)[col], (m, (gh - h) / 2, gh - m - h)[row]

    def _anchors_data(self) -> dict:
        """The quick places of the element picked: which one it is at ("auto" = its usual place), enabled."""
        name = getattr(self, "_sel", "map")
        o = self.settings["overlay"]
        cell = None
        if name == "map" and o.get("anchor", "auto") != "custom":
            cell = "auto" if o.get("anchor", "auto") == "auto" else \
                next((c for c, a in MAP_CORNERS.items() if a == o["anchor"]), None)
        elif name != "map" and name not in layout.own_places(o, self.settings.get("sysinfo", "off")):
            cell = "auto"
        else:
            data = self._preview_data()
            at = {n: (x, y) for n, x, y, _w, _h in data["layers"]}.get(name)
            tol = max(2.0, data["screen"][1] * CELL_TOL)
            for c in range(3):
                for r in range(3):
                    box = self._cell_box(name, c, r) if at else None
                    if box and abs(box[0] - at[0]) <= tol and abs(box[1] - at[1]) <= tol:
                        cell = (c, r)
        return {"name": name, "cell": cell, "enabled": not self._el_locked(name)}

    def _anchor_cell(self, value):
        """A quick place clicked: ("cell", col, row) puts the element picked there as its own place (the map's
        corners: the preset anchors, they keep to the black bar); ("auto",) = back to its usual place. One undo
        step; a locked element does not move."""
        name = getattr(self, "_sel", "map")
        if self._el_locked(name) or not value:
            return
        if value[0] == "auto":
            self._el_reset(name)
            return
        _what, col, row = value
        if name == "map" and (col, row) in MAP_CORNERS:
            self._layout_mark()
            self.anchor_var.set(self._anchor_text(MAP_CORNERS[(col, row)]))
            self._anchor_changed()
            return
        box = self._cell_box(name, col, row)
        if box is not None:
            self._preview_pick_now(("place", name, box[0], box[1]))

    def _focus_mode_toggle(self):
        """"Fokus": the overlay editor's canvas takes the whole window – list and inspector away, the navigation
        narrow. Esc or the button again ends it (leaving the page too)."""
        self._editor_focus = not getattr(self, "_editor_focus", False)
        qt = getattr(self, "qt", None)
        if qt is not None and hasattr(qt, "set_focus_nav"):
            qt.set_focus_nav(self._editor_focus)
        if hasattr(self, "_qt_refresh"):
            self._qt_refresh(force=True)
