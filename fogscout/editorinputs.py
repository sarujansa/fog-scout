"""1.39.1 (user: input display "Overlay + Editor"): the big clip editor's side of the input card – mixed into
qt_editor.EditorWindow.

* the inputs of a recording are its companion file "<video>.inputs.json" (written by the recorder, read with
  inputs.load – only our own format), per montage source;
* the timeline shows how busy the keys were as a strip at the foot of A1 (inputtrack.density);
* the inspector's section "Eingaben" switches the card on for the export and sets device, corner, size, dark area
  (inputtrack.InputSpec – part of the edit: undo, project format 7);
* the preview draws the card at the playhead, the export burns it in (clipedit, output time).

Nothing is sent anywhere; the file is only read."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QSlider, QWidget

from . import inputs, inputtrack
from .i18n import N_, _
from .qt_common import guard_wheel

CORNER_LABELS = {"bottom_left": N_("unten links"), "bottom_right": N_("unten rechts"), "top_left": N_("oben links"),
                 "top_right": N_("oben rechts")}
LAYOUT_LABELS = {"auto": N_("Automatisch (zuletzt benutztes Gerät)"), "keyboard": N_("Tastatur und Maus"),
                 "gamepad": N_("Gamepad")}


def companion(path: str) -> str:
    """The input file next to a recording."""
    return str(path) + inputs.INPUTS_SUFFIX


def read_inputs(path: str) -> list:
    """The recording's input changes, [] without a (valid) companion file."""
    p = companion(path)
    return inputs.load(p) if path and os.path.isfile(p) else []


class InputMixin:
    def _inputs_init(self, path):
        self._input_events = {0: read_inputs(path)}     # source → [(second of that recording, code)]
        self._input_spec = None                         # inputtrack.InputSpec once touched (None = never, not in the
        #                                                 project – an old cut keeps its content)

    def _input_has(self) -> bool:
        return any(self._input_events.values())

    def _input_source(self, s: int, path: str):
        """1.22/1.39.1: a montage source joins – its own input file."""
        self._input_events[s] = read_inputs(path)
        self._input_timeline(s)
        if getattr(self, "sections", None):
            self._inspector_refresh()

    def _input_timeline(self, s: int | None = None):
        for src, events in self._input_events.items():
            if s is not None and src != s:
                continue
            if events:
                length = max(events[-1][0] + 1.0, self.timeline.source_duration(src))
                self.timeline.set_inputs(src, inputtrack.density(events, length), inputtrack.DENSITY_PER_S)

    def _input_now(self) -> inputtrack.InputSpec:
        return self._input_spec.copy() if self._input_spec is not None else inputtrack.InputSpec()

    # ---- the inspector
    def _section_inputs(self, sec, mode):
        self.input_on_box = QCheckBox(_("Eingaben im Export zeigen"))
        self.input_on_box.setToolTip(_("Die Karte mit den gedrückten Tasten der Runde kommt ins fertige Video – an der "
                                       "gewählten Ecke, im Takt des Schnitts (Tempo und Rückwärts eingerechnet)."))
        self.input_on_box.toggled.connect(lambda on: self._input_set(on=bool(on)))
        sec.body.addWidget(self.input_on_box)
        self.input_layout_box = self._combo(None, [(k, _(v)) for k, v in LAYOUT_LABELS.items()], "auto",
                                            _("Welche Ansicht die Karte zeigt – automatisch das Gerät, das gerade "
                                              "benutzt wurde."), lambda _i: self._input_set(
                                                layout=self.input_layout_box.currentData()))
        sec.row(_("Gerät"), self.input_layout_box)
        self.input_corner_box = self._combo(None, [(k, _(v)) for k, v in CORNER_LABELS.items()], "bottom_right",
                                            _("Wo die Karte im Bild liegt."),
                                            lambda _i: self._input_set(corner=self.input_corner_box.currentData()))
        sec.row(_("Ecke"), self.input_corner_box)
        sl = guard_wheel(QSlider(Qt.Horizontal))
        sl.setRange(*inputtrack.SIZE_RANGE)
        sl.setValue(inputtrack.DEFAULT_SIZE)
        sl.setFocusPolicy(Qt.NoFocus)
        sl.setToolTip(_("Höhe der Karte im Verhältnis zur Bildhöhe."))
        val = QLabel(f"{inputtrack.DEFAULT_SIZE} %")
        val.setProperty("class", "dim")
        val.setMinimumWidth(42)
        sl.valueChanged.connect(lambda v: val.setText(f"{v} %"))
        sl.valueChanged.connect(lambda v: self._input_set(size=int(v)))
        box = QHBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(6)
        box.addWidget(sl, 1)
        box.addWidget(val)
        holder = QWidget()
        holder.setLayout(box)
        self.input_size_slider = sl
        sec.row(_("Grösse"), holder)
        self.input_backdrop_box = QCheckBox(_("Dunkle Fläche hinter den Tasten"))
        self.input_backdrop_box.setToolTip(_("Eine halb durchsichtige dunkle Fläche hinter der Karte."))
        self.input_backdrop_box.setChecked(True)
        self.input_backdrop_box.toggled.connect(lambda on: self._input_set(backdrop=bool(on)))
        sec.body.addWidget(self.input_backdrop_box)
        hint = QLabel(_("Aus der Datei neben der Aufnahme (Overlay › Eingaben › „Eingaben mit der Aufnahme "
                        "speichern“). Clips aus F8 haben keine."))
        hint.setWordWrap(True)
        hint.setProperty("class", "dim")
        sec.body.addWidget(hint)

    def _input_set(self, **change):
        if getattr(self, "_applying", False):
            return
        spec = self._input_now()
        for k, v in change.items():
            setattr(spec, k, v)
        if spec == self._input_spec:
            return
        self._input_spec = spec
        self._commit("inputs" if "size" in change else None)
        self.goto(self.pos)                                    # the preview shows it at once

    def _input_show(self):
        spec = self._input_now()
        for w, f in ((self.input_on_box, lambda: self.input_on_box.setChecked(spec.on)),
                     (self.input_layout_box, lambda: self.input_layout_box.setCurrentIndex(
                         max(0, self.input_layout_box.findData(spec.layout)))),
                     (self.input_corner_box, lambda: self.input_corner_box.setCurrentIndex(
                         max(0, self.input_corner_box.findData(spec.corner)))),
                     (self.input_size_slider, lambda: self.input_size_slider.setValue(spec.size)),
                     (self.input_backdrop_box, lambda: self.input_backdrop_box.setChecked(spec.backdrop))):
            w.blockSignals(True)
            f()
            w.blockSignals(False)

    # ---- state, export, preview
    def _input_state(self):
        return self._input_spec.copy() if self._input_spec is not None else None

    def _input_apply(self, spec):
        self._input_spec = spec.copy() if spec is not None else None
        if getattr(self, "input_on_box", None) is not None:
            self._input_show()

    def _input_burn(self):
        """What clipedit.export gets: (spec, {source: events}) when the card is on and there are inputs."""
        if self._input_spec is None or not self._input_spec.on or not self._input_has():
            return None
        return self._input_spec.copy(), {s: list(e) for s, e in self._input_events.items()}

    def _input_track(self):
        """(segments, layouts) of the cut in output time – the same the export burns in; kept per cut."""
        spec = self._input_now()
        key = (tuple(repr(p) for p in self.parts), spec.layout, tuple((s, len(e)) for s, e in self._input_events.items()))
        hit = getattr(self, "_input_cache", None)
        if hit is None or hit[0] != key:
            segs = inputtrack.segments(self.parts, self._input_events)
            hit = self._input_cache = (key, segs, inputtrack.layouts(segs, spec.layout))
        return hit[1], hit[2]

    def _input_paint(self, img):
        """The card on the preview picture at the playhead (the export's picture, scaled to the preview)."""
        spec = self._input_spec
        if spec is None or not spec.on or not self._input_has() or not self.parts:
            return img
        from .overlay_render import input_card
        segs, lays = self._input_track()
        k = next((j for j, (t0, t1, _c) in enumerate(segs) if t0 <= self.pos < t1), len(segs) - 1)
        if k < 0:
            return img
        x, y, h = inputtrack.card_box(spec, img.width, img.height)
        card = input_card(inputs.decode(segs[k][2]), lays[k], h, None, spec.backdrop)
        out = img.convert("RGBA")
        out.alpha_composite(card, (x, y))
        return out.convert("RGB")
