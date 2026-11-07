"""The overlay card "Eingaben" (1.39, user: "In vielen Twitch-Streams sehe ich Controller-Eingaben sichtbar"): the
keys, mouse buttons or gamepad controls held right now, as a card in the game – like the input displays streamers
use. Reading is inputs.Reader (only a fixed list of keys, only while a round runs and DBD is in front, see the hard
rule there); drawing is overlay_render.input_card; the place comes from layout.inputs_xy (shared with the preview).

Mixin of App (app.py) – the methods use App's attributes. Imports no other mixin (tests/test_mixins.py).
"""
from __future__ import annotations

import logging

from . import inputs, layout
from .appconst import INPUT_LAYOUTS, INPUT_SPOTS
from .capture import IS_WIN
from .i18n import _
from .overlay_render import INPUT_RATIO

log = logging.getLogger("fogscout")

INPUT_TICK_MS = 33             # the card follows the keys this often while a round runs (the overlay ticks 4×/s)


class InputsCard:
    def _inputs_init(self):
        self.inputs = inputs.Reader()
        self._inputs_choice = inputs.DeviceChoice()
        self._inputs_job = None             # the fast tick while a round runs
        self._inputs_seen = -1              # Reader.changes drawn last
        self._inputs_drawn = None           # (height, sample) of the picture on display
        self.inputs_win = None
        if IS_WIN:
            try:
                from .overlay_win32 import HudWindow
                self.inputs_win = HudWindow("Fog Scout Eingaben")
            except Exception as e:
                log.warning("Eingaben-Fenster nicht verfügbar: %s", e)
        if self.inputs_win is not None:
            self.inputs_win.on_moved = lambda x, y: self.events.put(("call", self._inputs_dragged, (x, y)))
            self.inputs_win.edit_label = _("EINGABEN")

    # ---- what may be read, what is shown
    def _inputs_round(self) -> bool:
        """A round runs in DBD's window – the only time the keys are looked at."""
        g = self.game
        return self._hist is not None and g is not None and not getattr(g, "minimized", False)

    def _inputs_allow(self) -> None:
        """Hand the reader DBD's window while the card is on and a round runs, else nothing (it stops looking)."""
        reader = getattr(self, "inputs", None)
        if reader is None:
            return
        on = bool(self.settings["overlay"].get("show_inputs", False))
        reader.allow(self.game.hwnd if on and self._inputs_round() else None)

    def _inputs_mode(self):
        """"live" (a round: the real keys), "sample" (moving the elements or "Overlay testen": made-up keys to see
        and drag), or None (hidden)."""
        o = self.settings["overlay"]
        if self.inputs_win is None or not o.get("show_inputs", False):
            return None
        if self.overlay.editing or getattr(self, "_forced", False):
            return "sample"
        if self._inputs_round() and not self.menu_paused and not self.hidden_after_match:
            return "live"
        return None

    # ---- placing (every overlay tick) and drawing (on every change of the keys)
    def _inputs_hide(self, stop_reading: bool = False) -> None:
        """Hide the card; ``stop_reading`` (the overlay is switched off): the keys are not looked at either."""
        if stop_reading and getattr(self, "inputs", None) is not None:
            self.inputs.allow(None)
        if self.inputs_win is not None:
            self.inputs_win.hide()
        self.worker.inputs_rect = None
        self._inputs_drawn = None
        if self._inputs_job is not None:
            self.root.after_cancel(self._inputs_job)
            self._inputs_job = None

    def _inputs_place(self) -> None:
        """Called by the overlay tick before the elements are moved apart (_el_resolve); with the overlay switched
        off the tick calls _inputs_hide(stop_reading=True) instead."""
        self._inputs_allow()
        win = self.inputs_win
        if win is None:
            return
        o = self.settings["overlay"]
        win.set_editing(bool(o.get("show_inputs", False)) and self.overlay.editing)
        mode = self._inputs_mode()
        gx, gy, gw, gh = game = self._game_rect()
        if mode is None or gh <= 0:
            self._inputs_hide()
            return
        margin = int(gh * o["margin"])
        spot = o.get("inputs_pos", "bottom_right")
        height = layout.inputs_height(o, game, margin, INPUT_RATIO)
        self._inputs_draw(height, mode == "sample")
        win.opacity = o.get("inputs_opacity", o["opacity"])
        x, y = layout.inputs_xy(spot, game, win.size, margin, o.get("inputs_xy"), self._bands(gx, gy, gw, gh))
        self.worker.inputs_rect = self._el_show("inputs", win, x, y, win.size)
        if mode == "live" and self._inputs_job is None:
            self._inputs_job = self.root.after(INPUT_TICK_MS, self._inputs_tick)

    def _inputs_draw(self, height: int, sample: bool) -> None:
        from .overlay_render import add_border, input_card
        o = self.settings["overlay"]
        win = self.inputs_win
        reader = self.inputs
        st = inputs.SAMPLE if sample else reader.state
        self._inputs_seen = reader.changes
        lay = self._inputs_choice.layout(o.get("inputs_layout", "auto"), st)
        accent = self._skin_accent()
        backdrop = bool(o.get("inputs_backdrop", True))
        key = (inputs.draw_key(st, lay), height, accent, backdrop, win.editing)
        if key != getattr(win, "_key", None):
            pic = input_card(st, lay, height, accent, backdrop)
            if win.editing:
                pic = add_border(pic, win.edit_label)
            win.set_picture(pic, key)
        self._inputs_drawn = (height, sample)

    def _inputs_tick(self) -> None:
        """Between the overlay ticks: the card follows the keys (drawn again only when they changed)."""
        self._inputs_job = None
        win, drawn = self.inputs_win, self._inputs_drawn
        if win is None or drawn is None or not win.shown or self._inputs_mode() != "live":
            return
        try:
            if self.inputs.changes != self._inputs_seen:
                self._inputs_draw(drawn[0], False)
                box = self.worker.inputs_rect
                if box:
                    win.show_at(box[0], box[1])
        except Exception as e:                       # a drawing error must not stop the overlay's ticks
            log.warning("Eingaben-Karte: %s", type(e).__name__)
            return
        self._inputs_job = self.root.after(INPUT_TICK_MS, self._inputs_tick)

    # ---- settings and dragging
    def _inputs_dragged(self, x, y) -> None:
        """The card dropped somewhere in the game (edit mode): its own place from now on."""
        self._layout_mark()
        gx, gy, gw, gh = self._game_rect()
        self._inputs_own_place(*layout.media_own(gw, gh, self.inputs_win.size, x - gx, y - gy))

    def _inputs_own_place(self, fx, fy) -> None:
        """Dragged in the preview or the game: its own place (its centre, share of the window)."""
        o = self.settings["overlay"]
        o["inputs_xy"], o["inputs_pos"] = [fx, fy], "custom"
        if hasattr(self, "inputs_pos_var"):
            self.inputs_pos_var.set(_(dict(INPUT_SPOTS)["custom"]))
        self._save_soon()
        self._tick_overlay(reschedule=False)

    def _inputs_on_changed(self) -> None:
        """The box "Eingaben im Spiel zeigen". The first time it is switched on, a note says what is read."""
        on = bool(self.inputs_on_var.get())
        self.settings["overlay"]["show_inputs"] = on
        if on and not self.settings.get("inputs_told", False):
            self.settings.set("inputs_told", True)
            self._inform(_("Eingaben im Spiel"), INPUTS_NOTE())
        self._save_soon()
        self._tick_overlay(reschedule=False)

    def _inputs_layout_changed(self) -> None:
        key = dict((_(label), k) for k, label in INPUT_LAYOUTS).get(self.inputs_layout_var.get(), "auto")
        self.settings["overlay"]["inputs_layout"] = key
        self._save_soon()
        self._tick_overlay(reschedule=False)

    def _inputs_spot_changed(self) -> None:
        self._layout_mark()
        key = dict((_(label), k) for k, label in INPUT_SPOTS).get(self.inputs_pos_var.get(), "bottom_right")
        self.settings["overlay"]["inputs_pos"] = key
        self._save_soon()
        self._tick_overlay(reschedule=False)

    def _inputs_backdrop_changed(self) -> None:
        self.settings["overlay"]["inputs_backdrop"] = bool(self.inputs_backdrop_var.get())
        self._save_soon()
        self._tick_overlay(reschedule=False)

    # ---- 1.39.1: the round's inputs next to its recording
    def _inputs_record_on(self) -> bool:
        return bool(self.settings["overlay"].get("show_inputs", False)) and bool(self.settings.get("inputs_record",
                                                                                                   True))

    def _inputs_round_start(self) -> None:
        reader = getattr(self, "inputs", None)
        if reader is not None:
            reader.take_log()                         # what came before the banner is not this round's

    def _inputs_round_end(self) -> None:
        """The changes of the round to the recorder (it keeps them in seconds of the file) – only with the box
        "Eingaben mit der Aufnahme speichern"; otherwise they are dropped. Never logged."""
        reader = getattr(self, "inputs", None)
        if reader is None:
            return
        events = reader.take_log()
        if events and self._inputs_record_on():
            self.recorder.inputs(events)

    def _inputs_record_changed(self) -> None:
        self.settings.set("inputs_record", bool(self.inputs_record_var.get()))
        self._save_soon()

    def _inputs_quit(self) -> None:
        reader = getattr(self, "inputs", None)
        if reader is not None:
            reader.stop()


def INPUTS_NOTE() -> str:          # noqa: N802 – a text, translated when asked for
    return _("Fog Scout zeigt nur, welche dieser Tasten gerade gedrückt sind: W, A, S, D, Q, E, R, Leertaste, "
             "Shift, Strg, die Maustasten und ein Gamepad (Knöpfe, Trigger, Sticks). Gelesen wird nur während einer "
             "Runde und nur, solange DBD das aktive Fenster ist – Tippen in anderen Programmen sieht Fog Scout nie. "
             "Nichts davon wird geloggt oder gesendet, und nichts geht an das Spiel; mit „Eingaben mit der Aufnahme "
             "speichern“ liegen die Tasten einer Runde als Datei neben ihrer OBS-Aufnahme (für den Clip-Editor). "
             "Eine offizielle "
             "Freigabe von Behaviour gibt es für solche Anzeigen nicht; sie geben keinen Spielvorteil.")
