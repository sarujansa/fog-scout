"""The clip editor window (1.16, user: "ein durchdachtes, hochwertiges und zeitgemässes Redesign der gesamten
Videoeditor-Oberfläche" – after DaVinci Resolve and CapCut, in Fog Scout's own colours): a compact top bar
(project name, save, undo/redo, export), the media library on the left, the viewer with its transport in the
middle, the inspector on the right (only the properties of what is picked) and the timeline with a video and an
audio track at the bottom – all in two splitters the user can move or fold away.

What it edits is ClipBase's machinery (qt_clip): the recording, its threads, playback and saving; the clips of the
timeline are sequence.py (pure), the undo history sequence.History, projects project.py. Nothing here touches the
game – only the recording files the user picked."""
from __future__ import annotations

import os
import threading
from dataclasses import replace

from PySide6.QtCore import QEvent, QSize, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QButtonGroup, QCheckBox, QFrame, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QListWidget, QProgressBar, QPushButton, QScrollArea, QScrollBar, QSizePolicy, QSlider, QSplitter,
                               QToolButton, QVBoxLayout, QWidget)

from . import annotate, clipedit, imageedit, medialib, obsrec, project, qt_icons, qt_theme, sequence
from .i18n import N_, _
from .editorproject import ProjectMixin
from .qt_clip import (CENSOR_LABELS, CONTENT_LABEL, CROP_LABELS, DRAW_TOOLS, MARK_AFTER_S, MARK_BEFORE_S, SHOW_FOR,
                      SIZE_LABELS, SPEED_LABELS, STEP_BIG, STEP_SMALL, ClipBase, PreviewView)
from .qt_common import guard_wheel
from .qt_layouts import FlowRow
from .qt_library import MediaLibrary
from .qt_timeline import SequenceTimeline

LIB_W, INSP_W = 270, 330            # px: the side panels at first
TL_H = 215                          # px: the timeline panel at first
MIN_W, MIN_H = 1024, 640
TOOL_ICONS = {"arrow": "arrow", "line": "line", "rect": "rect", "ellipse": "ellipse", "free": "free", "text": "text"}
MODES = ("select", "crop", "draw", "censor")
MODE_LABELS = {"select": N_("Auswahl"), "crop": N_("Ausschnitt"), "draw": N_("Zeichnen"), "censor": N_("Zensieren")}
MODE_TIPS = {"select": N_("Clips auf der Zeitleiste wählen, verschieben und trimmen (V)."),
             "crop": N_("Bildausschnitt – den Rahmen in der Vorschau ziehen (C)."),
             "draw": N_("Pfeile, Rahmen, Freihand und Text ins Bild zeichnen (D)."),
             "censor": N_("Bereiche unkenntlich machen – Namen, Chat, Freundesliste (X).")}
KEY_HINT = N_("? alle Tastenkürzel · Leertaste Abspielen · ←/→ 1 s · Shift 5 s · Strg oder ,/. 1 Bild · I/O Clip beginnt/endet hier · S Teilen · "
              "Entf Löschen · Strg+Z/Y Rückgängig/Wiederholen · F Vollbild · Strg+S Projekt · Strg+E Export")
LAYOUT_SAVE_MS = 600
_SH, _CT = Qt.ShiftModifier, Qt.ControlModifier
# 1.17.1: the key help (?) – (group, rows): (keys as shown, what they do, checks). A check is (Qt key, modifiers,
# target) for keyPressEvent or (key sequence, target) for a QShortcut; target = a method of the window, "tl:<name>"
# of the timeline, "mode:<tool>" or "help". tests/test_editor.py presses every check and expects the target to run –
# a key listed here works, the help is made from this table only.
SHORTCUTS = (
    (N_("Wiedergabe"), (
        (N_("Leertaste"), N_("Abspielen / Anhalten"), ((Qt.Key_Space, 0, "toggle_play"),)),
        ("← / →", N_("1 Sekunde zurück / vor"), ((Qt.Key_Left, 0, "step"), (Qt.Key_Right, 0, "step"))),
        (N_("Shift+← / →"), N_("5 Sekunden zurück / vor"), ((Qt.Key_Left, _SH, "step"), (Qt.Key_Right, _SH, "step"))),
        (N_("Strg+← / →  ·  , / ."), N_("1 Bild zurück / vor"),
         ((Qt.Key_Left, _CT, "step_frame"), (Qt.Key_Right, _CT, "step_frame"), (Qt.Key_Comma, 0, "step_frame"),
          (Qt.Key_Period, 0, "step_frame"))),
        (N_("Pos1 / Ende"), N_("Zum Anfang / zum Schluss"), ((Qt.Key_Home, 0, "goto"), (Qt.Key_End, 0, "goto"))),
        ("M", N_("Zur nächsten Marke"), ((Qt.Key_M, 0, "next_mark"),)),
        ("F", N_("Vollbild an / aus"), ((Qt.Key_F, 0, "toggle_fullscreen"),)))),
    (N_("Zeitleiste"), (
        ("I / O", N_("Clip beginnt / endet am Abspielkopf"), ((Qt.Key_I, 0, "set_start"), (Qt.Key_O, 0, "set_end"))),
        (N_("S oder Strg+B"), N_("Clip am Abspielkopf teilen"),
         ((Qt.Key_S, 0, "split_at_playhead"), ("Ctrl+B", "split_at_playhead"))),
        (N_("Entf"), N_("Markierten Clip löschen"), ((Qt.Key_Delete, 0, "delete_selected"),)),
        ("P", N_("Standbild am Abspielkopf einfügen"), ((Qt.Key_P, 0, "insert_hold"),)),
        ("+ / −", N_("Hinein- / herauszoomen"), ((Qt.Key_Plus, 0, "tl:zoom_in"), (Qt.Key_Minus, 0, "tl:zoom_out"))),
        (N_("Strg+0"), N_("Ganze Zeitleiste zeigen"), (("Ctrl+0", "tl:zoom_fit"),)))),
    (N_("Werkzeuge"), (
        ("V", N_("Auswählen"), ((Qt.Key_V, 0, "mode:select"),)),
        ("C", N_("Bildausschnitt"), ((Qt.Key_C, 0, "mode:crop"),)),
        ("D", N_("Zeichnen"), ((Qt.Key_D, 0, "mode:draw"),)),
        ("X", N_("Zensieren"), ((Qt.Key_X, 0, "mode:censor"),)),
        ("Esc", N_("Abbrechen, Werkzeug oder Auswahl aufheben – schliesst nie"),
         ((Qt.Key_Escape, 0, "mode:select"),)))),
    (N_("Projekt"), (
        (N_("Strg+Z / Strg+Y"), N_("Rückgängig / Wiederholen"), (("Ctrl+Z", "undo"), ("Ctrl+Y", "redo"))),
        (N_("Strg+S"), N_("Projekt speichern"), (("Ctrl+S", "save_project"),)),
        (N_("Strg+E"), N_("Exportieren"), (("Ctrl+E", "save"),)),
        (N_("Strg+W"), N_("Editor schliessen"), (("Ctrl+W", "close"),)),
        ("?", N_("Diese Übersicht ein / aus"), ((Qt.Key_Question, 0, "help"),)))),
)


# 1.18.1: keys that change the cut – ignored while the recording is checked against a saved project
EDIT_KEYS = frozenset((Qt.Key_I, Qt.Key_O, Qt.Key_S, Qt.Key_Delete, Qt.Key_Backspace, Qt.Key_C, Qt.Key_D, Qt.Key_X,
                       Qt.Key_P))


class KeyHelp(QFrame):
    """1.17.1: the editor's key help – a compact panel over the window (no dialog), made from SHORTCUTS only; ?,
    Esc or its × close it."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("keyhelp")
        self.setAttribute(Qt.WA_StyledBackground, True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 12, 12, 16)
        outer.setSpacing(8)
        top = QHBoxLayout()
        title = QLabel(_("Tastenkürzel"))
        title.setObjectName("keyhelptitle")
        top.addWidget(title)
        top.addStretch()
        close = QToolButton()
        close.setObjectName("quietbtn")
        close.setText("×")
        close.setToolTip(_("Schliessen (? oder Esc)"))
        close.clicked.connect(self.hide)
        top.addWidget(close)
        outer.addLayout(top)
        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        grid.setVerticalSpacing(14)
        for n, (group, rows) in enumerate(SHORTCUTS):
            box = QGridLayout()                           # keys and texts in two aligned columns per group
            box.setHorizontalSpacing(10)
            box.setVerticalSpacing(4)
            head = QLabel(_(group).upper())
            head.setObjectName("keyhelphead")
            box.addWidget(head, 0, 0, 1, 2)
            for i, (keys, what, _checks) in enumerate(rows, start=1):
                k = QLabel(_(keys))
                k.setObjectName("kbd")
                box.addWidget(k, i, 0, Qt.AlignLeft | Qt.AlignVCenter)
                box.addWidget(QLabel(_(what)), i, 1)
            box.setColumnStretch(1, 1)
            box.setRowStretch(len(rows) + 1, 1)
            grid.addLayout(box, n // 2, n % 2)
        outer.addLayout(grid)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.place()
            self.show()
            self.raise_()
        else:
            self.hide()

    def place(self):
        p = self.parentWidget()
        self.adjustSize()
        w, h = min(self.sizeHint().width(), p.width() - 40), min(self.sizeHint().height(), p.height() - 40)
        self.setGeometry((p.width() - w) // 2, (p.height() - h) // 2, w, h)


def editor_qss(c: dict, zoom: float = 1.0) -> str:
    """The editor's own style on top of the window's sheet: flat panels, tool buttons, the viewer's transport."""
    def px(size):
        return f"{max(8, round(size * zoom))}px"
    return f"""
QWidget#editor {{ background: {c['bg']}; }}
QFrame#topbar {{ background: {c['panel']}; border-bottom: 1px solid {c['border']}; }}
QFrame#panel {{ background: {c['panel']}; border: none; }}
QFrame#panel QScrollArea, QFrame#panel QScrollArea > QWidget > QWidget {{ background: {c['panel']}; }}
QFrame#viewer {{ background: {c['bg']}; border: none; }}
QFrame#statusbar {{ background: {c['panel']}; border-top: 1px solid {c['border']}; }}
QFrame#tlbar {{ background: {c['panel']}; border-bottom: 1px solid {c['border']}; }}
QLabel[class="section"] {{ color: {c['dim']}; font-size: {px(11)}; font-weight: 700; letter-spacing: 1px; }}
QLabel[class="title"] {{ color: {c['head']}; font-size: {px(13)}; font-weight: 700; }}
QLabel[class="brand"] {{ color: {c['dim']}; font-size: {px(12)}; font-weight: 600; }}
QLabel[class="time"] {{ color: {c['head']}; font-size: {px(13)}; font-weight: 600; }}
QLabel[class="label"] {{ color: {c['dim']}; }}
QLineEdit#projectname {{ background: transparent; border: 1px solid transparent; border-radius: 6px; padding: 4px 8px;
    font-size: {px(13)}; font-weight: 600; color: {c['head']}; }}
QLineEdit#projectname:hover {{ border-color: {c['border']}; background: {c['field']}; }}
QLineEdit#projectname:focus {{ border-color: {c['accent']}; background: {c['field']}; }}
QLineEdit#search {{ background: {c['field']}; border: 1px solid {c['border']}; border-radius: 6px; padding: 4px 8px; }}
QToolButton#toolbtn {{ background: transparent; border: 1px solid transparent; border-radius: 6px; padding: 3px; }}
QToolButton#toolbtn:hover {{ background: {c['hover']}; }}
QToolButton#toolbtn:pressed {{ background: {c['press']}; }}
QToolButton#toolbtn:checked {{ background: {c['accent']}; border-color: {c['accent']}; }}
QToolButton#toolbtn:disabled {{ background: transparent; }}
QToolButton#toolbtn::menu-indicator {{ image: none; }}
QToolButton#quietbtn {{ background: transparent; border: 1px solid transparent; border-radius: 6px; padding: 3px; }}
QToolButton#quietbtn:hover {{ background: {c['hover']}; }}
QToolButton#quietbtn:checked {{ background: {c['field']}; border-color: {c['border']}; }}
QToolButton#playbtn {{ background: {c['accent']}; border: 1px solid {c['accent']}; border-radius: 18px; padding: 0; }}
QToolButton#playbtn:hover {{ background: {c['accent_hover']}; }}
QToolButton#playbtn:disabled {{ background: {c['btn_dis']}; border-color: {c['border']}; }}
QSplitter::handle {{ background: {c['border']}; }}
QSplitter::handle:horizontal {{ width: 1px; }}
QSplitter::handle:vertical {{ height: 1px; }}
QSplitter::handle:hover {{ background: {c['accent']}; }}
QFrame#noticebar {{ background: {c['field']}; border: none; border-bottom: 1px solid {c['border']};
    border-left: 3px solid {c['accent']}; }}
QFrame#noticebar QLabel {{ color: {c['head']}; }}
QLabel#savestatus {{ color: {c['dim']}; padding: 0 4px; }}
QFrame#keyhelp {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 10px; }}
QLabel#keyhelptitle {{ font-weight: 700; color: {c['head']}; }}
QLabel#keyhelphead {{ font-size: {px(11)}; font-weight: 700; color: {c['dim']}; letter-spacing: 1px; padding-bottom: 2px; }}
QLabel#kbd {{ background: {c['field']}; border: 1px solid {c['border']}; border-radius: 4px; padding: 1px 6px;
    color: {c['head']}; }}
QFrame#inspector QPushButton, QFrame#panel QPushButton {{ padding: 4px 10px; }}
QFrame#inspector QComboBox {{ padding: 3px 26px 3px 8px; }}
QFrame#inspector QLineEdit {{ padding: 4px 8px; }}
QSlider::groove:horizontal {{ height: 4px; background: {c['border']}; border-radius: 2px; }}
QSlider::sub-page:horizontal {{ background: {c['accent']}; border-radius: 2px; }}
QSlider::handle:horizontal {{ width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; background: {c['head']};
    border: 1px solid {c['border']}; }}
QSlider::handle:horizontal:hover {{ background: {c['accent']}; }}
QSlider:disabled::sub-page:horizontal {{ background: {c['border']}; }}
QListView#media {{ background: transparent; border: none; outline: 0; }}
QListWidget#marks {{ background: {c['field']}; border: 1px solid {c['border']}; border-radius: 6px; padding: 2px; outline: 0; }}
QListWidget#marks::item {{ padding: 4px 6px; border-radius: 4px; }}
QListWidget#marks::item:selected {{ background: {c['select']}; color: #ffffff; }}
QListWidget#marks::item:hover:!selected {{ background: {c['hover']}; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {c['hover']}; border-radius: 4px; min-width: 30px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QProgressBar#busy {{ max-height: 4px; min-height: 4px; }}
QFrame#section {{ background: transparent; border: none; border-bottom: 1px solid {c['border']}; }}
QFrame#section:last {{ border-bottom: none; }}
QPushButton[class="swatch"] {{ border: 2px solid {c['border']}; border-radius: 11px; padding: 0; }}
QPushButton[class="swatch"]:checked {{ border: 2px solid {c['head']}; }}
"""


class Section(QFrame):
    """One block of the inspector: a small heading and a body; ``show_if`` hides the whole block."""

    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("section")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 14)
        lay.setSpacing(8)
        self.head = QLabel(title.upper())
        self.head.setProperty("class", "section")
        lay.addWidget(self.head)
        self.body = QVBoxLayout()
        self.body.setSpacing(8)
        lay.addLayout(self.body)

    def row(self, label: str, widget=None, stretch=True):
        """A form row: dim label left, the widget right."""
        r = QHBoxLayout()
        r.setSpacing(8)
        lab = QLabel(label)
        lab.setProperty("class", "label")
        lab.setMinimumWidth(78)
        r.addWidget(lab)
        if widget is not None:
            r.addWidget(widget, 1 if stretch else 0)
        if not stretch:
            r.addStretch()
        self.body.addLayout(r)
        return r


class EditorWindow(ProjectMixin, ClipBase):
    """The full editor – see the module's docstring. ``media`` = the App's list of MediaItems for the library
    (callable), ``on_open(item, window)`` = the App opens another recording (a new window; ``window`` = this one, to
    be replaced when nothing was edited here), ``cache_dir`` = where the library's pictures are kept,
    ``layout`` = the splitter sizes remembered (setting editor_layout). 1.18.1: ``registry`` (projectsave; tests),
    ``autosave`` (setting editor_autosave), ``round_t`` (start of the round – part of the recording's identity)."""

    def __init__(self, path: str, marks: list, clips_dir: str, mode: str = "copy", sound: bool = True, media=None,
                 on_open=None, cache_dir: str | None = None, layout: dict | None = None, registry=None,
                 autosave: bool = True, round_t=None, **kw):
        self._project_init(registry, autosave, round_t)
        self.media, self.on_open, self.cache_dir = media, on_open, cache_dir
        self._layout = dict(layout or {})
        self.parts = []
        self.pos = 0.0
        self.mode = "select"
        self.history = None
        self._content_crop_auto = False
        self._crop_chosen = False
        self._commit_key = None
        self._fullscreen = None             # what to restore when leaving the full screen
        self._layout_timer = None
        self._applying = False
        self._zoom_edit = None              # 1.19: (clip index, 0 start / 1 end) while the zoom frame is edited
        self._short = None                  # 1.20: shorts.ShortSpec of this cut (layout, title, subtitles)
        self._short_view = False            # 1.20: the preview shows the composed short
        self._crop_saved = (None, None, False)
        super().__init__(path, marks, clips_dir, mode, sound, flags=Qt.Window, **kw)
        self.resize(1480, 900)
        self.setMinimumSize(MIN_W, MIN_H)
        self.setObjectName("editor")
        self.setAttribute(Qt.WA_DeleteOnClose)          # 1.16.1: the Qt side goes with the window (App prunes its list)
        self.setFocus()                                 # 1.18: the keys belong to the window, not to the first text field

    # ---- set-up
    def _ready(self, ok: bool):
        self.timeline.set_duration(self.info.duration, self.info.fps)
        self.timeline.set_marks(self.marks)
        if not ok:
            for w in (self.play_btn, self.split_btn, self.delete_btn, self.project_btn):
                w.setEnabled(False)
            self.history = sequence.History(sequence.EditState([]))
            self._refresh_undo()
            self._pstate = "unbound"                     # 1.18.1: an unreadable file has no project
            self._status_tick()
            return
        first = self.marks[0] if self.marks else None
        if first is not None:                            # a mark: the clip starts 20 s before it, ends 10 s after
            self.parts = [clipedit.Part(max(0.0, first - MARK_BEFORE_S), min(self.info.duration, first + MARK_AFTER_S))]
        else:
            self.parts = [clipedit.Part(0.0, self.info.duration)]
        self.history = sequence.History(self._state())
        self.timeline.set_parts(self.parts)
        self._refresh()
        self.goto(0.0)
        self._project_begin()                            # 1.18.1: the project is looked up in a thread

    def _build(self, mode, sound):
        c = self.colours = qt_theme.colours(self.dark)
        self.setStyleSheet((self.styleSheet() or "") + editor_qss(c))
        self.ratio = self.devicePixelRatioF() if hasattr(self, "devicePixelRatioF") else 1.0
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.topbar = self._build_topbar(c)
        outer.addWidget(self.topbar)
        top = self.topbar.layout()
        self._project_widgets(top, top.indexOf(self.name_edit) + 1)      # 1.18.1: save status and the notice bar
        outer.addWidget(self.notice)
        self.vsplit = QSplitter(Qt.Vertical)
        self.vsplit.setChildrenCollapsible(False)
        self.hsplit = QSplitter(Qt.Horizontal)
        self.hsplit.setChildrenCollapsible(False)
        self.library = MediaLibrary(self.dark, self.cache_dir, self.ffmpeg, self.ratio)
        self.library.setMinimumWidth(200)
        self.library.opened.connect(self._open_media)
        self.library.shown.connect(lambda it: self._show_file(it.path))
        self.hsplit.addWidget(self.library)
        self.hsplit.addWidget(self._build_viewer(c))
        self.inspector = self._build_inspector(c, mode)
        self.hsplit.addWidget(self.inspector)
        self.hsplit.setStretchFactor(0, 0)
        self.hsplit.setStretchFactor(1, 1)
        self.hsplit.setStretchFactor(2, 0)
        self.vsplit.addWidget(self.hsplit)
        self.vsplit.addWidget(self._build_timeline(c))
        self.vsplit.setStretchFactor(0, 1)
        self.vsplit.setStretchFactor(1, 0)
        outer.addWidget(self.vsplit, 1)
        outer.addWidget(self._build_statusbar(c))
        self._shortcuts()
        sizes = self._layout.get("h") or [LIB_W, 900, INSP_W]
        vsizes = self._layout.get("v") or [640, TL_H]
        self.hsplit.setSizes([int(v) for v in sizes][:3])
        self.vsplit.setSizes([int(v) for v in vsizes][:2])
        self.lib_btn.setChecked(self._layout.get("lib", True))
        self.insp_btn.setChecked(self._layout.get("insp", True))
        self._toggle_panel(self.library, self.lib_btn.isChecked())
        self._toggle_panel(self.inspector, self.insp_btn.isChecked())
        for sp in (self.hsplit, self.vsplit):
            sp.splitterMoved.connect(self._layout_changed)
        self._set_mode("select")
        self._mode_changed(self.mode_box.currentIndex(), save=False)
        self.gif_box.currentIndexChanged.connect(lambda _i: self._changed())
        self._fill_library()

    def _tool(self, name, tip, slot=None, checkable=False, size=18, quiet=False):
        """A flat icon button; ``quiet`` = a toggle whose "on" is a tinted icon, not a filled button (the panel
        switches, mute)."""
        c = self.colours
        b = QToolButton()
        b.setObjectName("quietbtn" if quiet else "toolbtn")
        b.setIcon(qt_icons.icon(name, c["fg"], c["head"], c["fg_dis"], c["accent"] if quiet else c["on_accent"],
                                size=size, ratio=self.ratio))
        b.setIconSize(QSize(size, size))
        b.setToolTip(tip)
        b.setAutoRaise(True)
        b.setFocusPolicy(Qt.NoFocus)
        b.setCheckable(checkable)
        if slot is not None:
            b.clicked.connect(slot)
        return b

    def _build_topbar(self, c):
        bar = QFrame()
        bar.setObjectName("topbar")
        bar.setFixedHeight(46)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(6)
        logo = QLabel()
        logo.setPixmap(qt_icons.pixmap("compass", c["accent"], 20, self.ratio))
        logo.setFixedSize(22, 22)
        lay.addWidget(logo)
        brand = QLabel(_("Fog Scout · Editor"))
        brand.setProperty("class", "brand")
        lay.addWidget(brand)
        lay.addSpacing(10)
        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("projectname")
        self.name_edit.setToolTip(_("Name des Projekts – auch der Name des exportierten Clips."))
        self.name_edit.setMinimumWidth(220)
        self.name_edit.setMaximumWidth(460)
        self.name_edit.setClearButtonEnabled(False)
        self.name_edit.returnPressed.connect(self.setFocus)
        lay.addWidget(self.name_edit, 1)
        self.project_btn = self._tool("save", _("Projekt speichern (Strg+S) – Schnitt, Ausschnitt, Zeichnungen, Zensur "
                                                "und Export-Einstellungen dieser Aufnahme, zum späteren Weiterarbeiten."),
                                      self.save_project)
        lay.addWidget(self.project_btn)
        self.undo_btn = self._tool("undo", _("Rückgängig (Strg+Z)."), self.undo)
        self.redo_btn = self._tool("redo", _("Wiederholen (Strg+Y)."), self.redo)
        lay.addWidget(self.undo_btn)
        lay.addWidget(self.redo_btn)
        lay.addStretch(2)
        self.busy = QProgressBar()
        self.busy.setObjectName("busy")
        self.busy.setRange(0, 0)
        self.busy.setTextVisible(False)
        self.busy.setFixedWidth(90)
        self.busy.setVisible(False)
        lay.addWidget(self.busy)
        self.lib_btn = self._tool("panel_left", _("Bibliothek ein-/ausblenden."), checkable=True, quiet=True)
        self.lib_btn.toggled.connect(lambda on: self._toggle_panel(self.library, on))
        self.insp_btn = self._tool("panel_right", _("Inspector ein-/ausblenden."), checkable=True, quiet=True)
        self.insp_btn.toggled.connect(lambda on: self._toggle_panel(self.inspector, on))
        self.tl_btn = self._tool("panel_bottom", _("Zeitleiste ein-/ausblenden."), checkable=True, quiet=True)
        self.tl_btn.setChecked(True)
        self.tl_btn.toggled.connect(lambda on: self._toggle_panel(self.tl_panel, on))
        for b in (self.lib_btn, self.insp_btn, self.tl_btn):
            lay.addWidget(b)
        lay.addSpacing(8)
        self.save_btn = QPushButton(_("Exportieren"))
        self.save_btn.setObjectName("primary")
        self.save_btn.setIcon(qt_icons.icon("export", c["on_accent"], size=16, ratio=self.ratio))
        self.save_btn.setToolTip(_("Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen "
                                   "(Strg+E) – Format und Kodierung im Inspector unter Export."))
        self.save_btn.setFocusPolicy(Qt.NoFocus)
        self.save_btn.clicked.connect(self.save)
        lay.addWidget(self.save_btn)
        return bar

    def _build_viewer(self, c):
        box = QFrame()
        box.setObjectName("viewer")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        rail = QFrame()
        rail.setObjectName("panel")
        rail.setFixedWidth(44)
        rl = QVBoxLayout(rail)
        rl.setContentsMargins(6, 10, 6, 10)
        rl.setSpacing(4)
        self.mode_group = QButtonGroup(self)
        self.mode_btns = {}
        for key, icon in (("select", "pointer"), ("crop", "crop"), ("draw", "pen"), ("censor", "censor")):
            b = self._tool(icon, _(MODE_TIPS[key]), checkable=True)
            b.setFixedSize(32, 32)
            b.toggled.connect(lambda on, k=key: on and self._set_mode(k))
            self.mode_group.addButton(b)
            self.mode_btns[key] = b
            rl.addWidget(b)
        rl.addStretch()
        self.still_btn = self._tool("camera", _("Standbild am Abspielkopf als PNG neben den Clips speichern."),
                                    lambda: self.save_still(self._src_pos()))
        self.still_btn.setFixedSize(32, 32)
        rl.addWidget(self.still_btn)
        row.addWidget(rail)
        self.preview = PreviewView(self.dark)
        self.preview.plain = True
        self.preview.setMinimumSize(320, 180)
        self.preview.boxes_changed.connect(self._boxes_changed)
        self.preview.boxes_changed.connect(lambda: self._commit())
        self.preview.crop_changed.connect(self._crop_moved)
        self.preview.shapes_changed.connect(self._shapes_changed)
        self.preview.shape_picked.connect(self._draw_picked)
        self.preview.new_times = self._times_from_here
        row.addWidget(self.preview, 1)
        lay.addLayout(row, 1)
        lay.addWidget(self._build_transport(c))
        return box

    def _build_transport(self, c):
        bar = QFrame()
        bar.setObjectName("panel")
        bar.setFixedHeight(52)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(4)
        self.pos_label = QLabel("0:00.0 / 0:00.0")
        self.pos_label.setProperty("class", "time")
        self.pos_label.setMinimumWidth(130)
        lay.addWidget(self.pos_label)
        lay.addStretch(1)
        self.b_start = self._tool("to_start", _("Zum Anfang (Pos1)."), lambda: self.goto(0.0))
        self.b_back5 = self._tool("rewind", _("5 Sekunden zurück (Shift+←)."), lambda: self.step(-STEP_BIG))
        self.b_back1 = self._tool("frame_prev", _("Ein Bild zurück (Strg+←); ← eine Sekunde."), lambda: self.step_frame(-1))
        self.play_btn = QToolButton()
        self.play_btn.setObjectName("playbtn")
        self.play_btn.setFixedSize(36, 36)
        self.play_btn.setIconSize(QSize(20, 20))
        self.play_btn.setFocusPolicy(Qt.NoFocus)
        self.play_btn.setToolTip(_("Abspielen / Pause (Leertaste)"))
        self.play_btn.clicked.connect(self.toggle_play)
        self._play_icons = (qt_icons.icon("play", c["on_accent"], size=20, ratio=self.ratio),
                            qt_icons.icon("pause", c["on_accent"], size=20, ratio=self.ratio))
        self.play_btn.setIcon(self._play_icons[0])
        self.b_fwd1 = self._tool("frame_next", _("Ein Bild vor (Strg+→); → eine Sekunde."), lambda: self.step_frame(1))
        self.b_fwd5 = self._tool("forward", _("5 Sekunden vor (Shift+→)."), lambda: self.step(STEP_BIG))
        self.b_end = self._tool("to_end", _("Zum Ende (Ende)."), lambda: self.goto(self.timeline.total()))
        for b in (self.b_start, self.b_back5, self.b_back1):
            lay.addWidget(b)
        lay.addSpacing(4)
        lay.addWidget(self.play_btn)
        lay.addSpacing(4)
        for b in (self.b_fwd1, self.b_fwd5, self.b_end):
            lay.addWidget(b)
        lay.addSpacing(14)
        self.in_btn = self._tool("mark_in", _("Der Clip unter dem Abspielkopf beginnt hier (Taste I)."), self.set_start)
        self.out_btn = self._tool("mark_out", _("Der Clip unter dem Abspielkopf endet hier (Taste O)."), self.set_end)
        self.watch_btn = self._tool("clip", _("Spielt den ganzen Schnitt von vorn ab und springt danach zurück."),
                                    self.watch_clip)
        for b in (self.in_btn, self.out_btn, self.watch_btn):
            lay.addWidget(b)
        lay.addStretch(1)
        self.mute_btn = self._tool("volume", _("Ton der Vorschau an/aus (Windows)."), checkable=True, quiet=True)
        self._vol_icons = (qt_icons.icon("volume", c["fg"], c["head"], c["fg_dis"], c["fg"], ratio=self.ratio),
                           qt_icons.icon("mute", c["dim"], c["head"], c["fg_dis"], c["dim"], ratio=self.ratio))
        self.mute_btn.setChecked(not self.sound_box.isChecked())
        self.mute_btn.setIcon(self._vol_icons[1 if self.mute_btn.isChecked() else 0])
        self.mute_btn.toggled.connect(self._mute_toggled)
        self.sound_box.toggled.connect(lambda on: self.mute_btn.setChecked(not on))
        lay.addWidget(self.mute_btn)
        self.volume = guard_wheel(QSlider(Qt.Horizontal))
        self.volume.setRange(0, 100)
        self.volume.setValue(100)
        self.volume.setFixedWidth(90)
        self.volume.setFocusPolicy(Qt.NoFocus)
        self.volume.setToolTip(_("Lautstärke der Vorschau (nicht des Clips)."))
        self.volume.valueChanged.connect(self._volume_changed)
        lay.addWidget(self.volume)
        lay.addSpacing(8)
        self.fs_btn = self._tool("fullscreen", _("Vollbild – nur die Vorschau (F, Esc beendet)."), self.toggle_fullscreen)
        lay.addWidget(self.fs_btn)
        return bar

    def _build_inspector(self, c, mode):
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setMinimumWidth(260)
        pl = QVBoxLayout(panel)
        pl.setContentsMargins(0, 0, 0, 0)
        pl.setSpacing(0)
        head = QFrame()
        head.setObjectName("tlbar")
        hl = QHBoxLayout(head)
        hl.setContentsMargins(14, 0, 10, 0)
        head.setFixedHeight(34)
        self.insp_title = QLabel(_("Inspector"))
        self.insp_title.setProperty("class", "section")
        hl.addWidget(self.insp_title)
        hl.addStretch()
        pl.addWidget(head)
        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setFrameShape(QFrame.NoFrame)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        body = QFrame()
        body.setObjectName("inspector")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(0)
        self.sections = {}
        for key, title, build in (("clip", _("Clip"), self._section_clip), ("fx", _("Effekte"), self._section_fx),
                                  ("marks", _("Marken (F8)"), self._section_marks),
                                  ("draw", _("Zeichnen"), self._section_draw), ("censor", _("Zensieren"), self._section_censor),
                                  ("picture", _("Bild"), self._section_picture), ("sound", _("Ton"), self._section_sound),
                                  ("export", _("Export"), self._section_export),
                                  ("short", _("Short (9:16)"), self._section_short)):
            sec = Section(title)
            build(sec, mode)
            self.sections[key] = sec
            bl.addWidget(sec)
        bl.addStretch()
        area.setWidget(body)
        pl.addWidget(area, 1)
        from PySide6.QtWidgets import QComboBox
        for box in body.findChildren(QComboBox):               # a long entry never widens the panel: it elides
            box.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            box.setMinimumContentsLength(9)
        return panel

    def _section_clip(self, sec, mode):
        self.clip_title = QLabel("")
        self.clip_title.setProperty("class", "title")
        sec.body.addWidget(self.clip_title)
        self.clip_facts = QLabel("")
        self.clip_facts.setProperty("class", "dim")
        self.clip_facts.setWordWrap(True)
        sec.body.addWidget(self.clip_facts)
        self.speed_box = self._combo(None, [(v, _(SPEED_LABELS[v]) if v == 1.0 else SPEED_LABELS[v])
                                            for v in clipedit.SPEEDS], 1.0,
                                     _("Zeitlupe oder Zeitraffer für den markierten Clip. Der Ton läuft mit."),
                                     self._speed_picked)
        sec.row(_("Tempo"), self.speed_box, stretch=False)
        row = FlowRow(spacing=6)
        self.split_btn = self._btn(row, _("Teilen"), self.split_at_playhead,
                                   _("Teilt den Clip unter dem Abspielkopf in zwei (Taste S)."))
        self.delete_btn = self._btn(row, _("Löschen"), self.delete_selected,
                                    _("Entfernt den markierten Clip von der Zeitleiste (Entf) – die Aufnahme bleibt."))
        self.delete_btn.setObjectName("danger")
        sec.body.addLayout(row)

    # ---- 1.19: effects of the marked clip
    FX_SLIDERS = (("brightness", N_("Helligkeit"), -50, 50, 0), ("contrast", N_("Kontrast"), 50, 200, 100),
                  ("saturation", N_("Sättigung"), 0, 200, 100))

    def _section_fx(self, sec, mode):
        self.fx_sliders, self.fx_values = {}, {}
        tips = {"brightness": _("Heller oder dunkler – nur dieser Clip."),
                "contrast": _("Mehr oder weniger Kontrast – nur dieser Clip."),
                "saturation": _("Kräftigere oder blassere Farben, ganz links schwarz-weiss – nur dieser Clip.")}
        for key, label, lo, hi, zero in self.FX_SLIDERS:
            sl = guard_wheel(QSlider(Qt.Horizontal))
            sl.setRange(lo, hi)
            sl.setValue(zero)
            sl.setToolTip(tips[key])
            sl.setFocusPolicy(Qt.NoFocus)
            val = QLabel("")
            val.setProperty("class", "dim")
            val.setMinimumWidth(38)
            box = QHBoxLayout()
            box.setSpacing(6)
            box.addWidget(sl, 1)
            box.addWidget(val)
            holder = QWidget()
            holder.setLayout(box)
            box.setContentsMargins(0, 0, 0, 0)
            sec.row(_(label), holder)
            sl.valueChanged.connect(self._color_changed)
            self.fx_sliders[key], self.fx_values[key] = sl, val
        row = FlowRow(spacing=6)
        self.fx_reset_btn = self._btn(row, _("Farbe zurücksetzen"), self._color_reset,
                                      _("Helligkeit, Kontrast und Sättigung dieses Clips wieder wie aufgenommen."))
        self.fx_all_btn = self._btn(row, _("Auf alle Clips"), self._color_to_all,
                                    _("Übernimmt Helligkeit, Kontrast und Sättigung dieses Clips für alle Clips auf der "
                                      "Zeitleiste (ein Schritt, Strg+Z macht ihn rückgängig)."))
        sec.body.addLayout(row)
        zl = QLabel(_("Zoom"))
        zl.setProperty("class", "label")
        sec.body.addWidget(zl)
        row = FlowRow(spacing=6)
        self.zoom_btns = {}
        for which, text, tip in ((0, _("Start-Ausschnitt"), _("Den Ausschnitt am Anfang des Clips in der Vorschau "
                                                              "ziehen – dazwischen fährt die Kamera gleichmässig.")),
                                 (1, _("End-Ausschnitt"), _("Den Ausschnitt am Ende des Clips in der Vorschau ziehen."))):
            b = self._btn(row, text, lambda _c=False, w=which: self._zoom_tool(w), tip)
            b.setCheckable(True)
            b.setProperty("class", "seg")
            self.zoom_btns[which] = b
        self.zoom_clear_btn = self._btn(row, _("Zoom entfernen"), self._zoom_clear,
                                        _("Der Clip zeigt wieder das ganze Bild."))
        sec.body.addLayout(row)
        self.zoom_still = QCheckBox(_("Ohne Bewegung"))
        self.zoom_still.setToolTip(_("Ein fester Ausschnitt: Start und Ende gleich – der End-Ausschnitt folgt dem Start."))
        self.zoom_still.toggled.connect(self._zoom_still_toggled)
        sec.body.addWidget(self.zoom_still)
        self.reverse_box = QCheckBox(_("Rückwärts"))
        self.reverse_box.toggled.connect(self._reverse_toggled)
        sec.body.addWidget(self.reverse_box)
        self.reverse_hint = QLabel("")
        self.reverse_hint.setProperty("class", "dim")
        self.reverse_hint.setWordWrap(True)
        sec.body.addWidget(self.reverse_hint)
        holds = [(v, f"{v:g} s") for v in clipedit.HOLDS]
        self.hold_box = self._combo(None, holds, 2.0, _("Wie lange ein Standbild steht – für ein neues, oder für das "
                                                        "markierte Standbild."), self._hold_picked)
        sec.row(_("Standbild"), self.hold_box, stretch=False)
        row = FlowRow(spacing=6)
        self.hold_btn = self._btn(row, _("Standbild einfügen"), self.insert_hold,
                                  _("Hält das Bild am Abspielkopf so lange an wie eingestellt (Taste P) – ohne Ton."))
        sec.body.addLayout(row)

    def _fx_part(self):
        """(index, clip) of the marked clip, else (None, None)."""
        i = self.timeline.selection
        if i is None or not 0 <= i < len(self.parts):
            return None, None
        return i, self.parts[i]

    def _fx_show(self):
        """The section shows the marked clip's effects (without firing their handlers)."""
        i, p = self._fx_part()
        color = (p.color if p is not None and p.color else clipedit.COLOR_NONE)
        for (key, _label, _lo, _hi, _zero), v in zip(self.FX_SLIDERS, color):
            sl = self.fx_sliders[key]
            sl.blockSignals(True)
            sl.setValue(int(round(v * 100)))
            sl.blockSignals(False)
            self.fx_values[key].setText(f"{int(round(v * 100)):+d}" if key == "brightness" else f"{int(round(v * 100))} %")
        if p is None:
            return
        still = p.hold > 0
        for w in (*self.fx_sliders.values(), self.fx_reset_btn, self.fx_all_btn):
            w.setEnabled(True)
        self.fx_reset_btn.setEnabled(bool(p.color))
        for b in (*self.zoom_btns.values(), self.zoom_still):
            b.setEnabled(True)
        self.zoom_clear_btn.setEnabled(bool(p.zoom))
        self.zoom_still.blockSignals(True)
        self.zoom_still.setChecked(bool(p.zoom) and p.zoom[0] == p.zoom[1])
        self.zoom_still.blockSignals(False)
        limit = clipedit.reverse_max_s(self.info)
        too_long = (p.end - p.start) > limit + 1e-6
        self.reverse_box.blockSignals(True)
        self.reverse_box.setChecked(p.reverse)
        self.reverse_box.blockSignals(False)
        self.reverse_box.setEnabled(not still and (p.reverse or not too_long))
        self.reverse_box.setToolTip(_("Spielt den Clip rückwärts ab, auch den Ton. Bei dieser Aufnahme höchstens "
                                      "{n} s je Clip (sonst braucht ffmpeg zu viel Arbeitsspeicher).", n=f"{limit:g}"))
        self.reverse_hint.setText(_("Rückwärts geht bis {n} s je Clip – diesen Clip vorher teilen.", n=f"{limit:g}")
                                  if too_long and not still and not p.reverse else "")
        self.reverse_hint.setVisible(bool(self.reverse_hint.text()))
        self.hold_box.blockSignals(True)
        if still:
            idx = self.hold_box.findData(p.hold)
            if idx < 0:
                self.hold_box.addItem(f"{p.hold:g} s", p.hold)
                idx = self.hold_box.count() - 1
            self.hold_box.setCurrentIndex(idx)
        self.hold_box.blockSignals(False)
        self.hold_btn.setEnabled(bool(self.parts))

    def _fx_set(self, i, key, **fields):
        """Change clip ``i`` and commit (``key`` merges a slider's drag into one undo step)."""
        self.parts = sequence.with_effects(self.parts, i, **fields)
        self.timeline.set_parts(self.parts)
        self._commit(key)
        self.goto(self.pos)

    def _color_changed(self, _v=None):
        i, p = self._fx_part()
        if p is None:
            return
        vals = [self.fx_sliders[k].value() / 100 for k, *_r in self.FX_SLIDERS]
        self._fx_set(i, ("color", i), color=clipedit.clean_color(vals))

    def _color_reset(self):
        i, p = self._fx_part()
        if p is not None and p.color:
            self._fx_set(i, None, color=None)

    def _color_to_all(self):
        _i, p = self._fx_part()
        if p is None:
            return
        self.parts = [replace(q, color=p.color) for q in self.parts]
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(self.pos)
        self.status.setText(_("Farbe auf alle {n} Clips übernommen.", n=len(self.parts)))

    def _reverse_toggled(self, on):
        i, p = self._fx_part()
        if p is None or p.hold > 0:
            return
        if on and (p.end - p.start) > clipedit.reverse_max_s(self.info) + 1e-6:
            self._fx_show()
            return
        self._fx_set(i, None, reverse=bool(on))

    def _hold_picked(self, _i=None):
        i, p = self._fx_part()
        if p is not None and p.hold > 0:
            self.parts = sequence.set_hold(self.parts, i, float(self.hold_box.currentData() or 2.0))
            self.timeline.set_parts(self.parts)
            self._commit()
            self._refresh()

    def insert_hold(self):
        """1.19 (P): a still of the picture at the playhead, as long as the box says."""
        if not self.parts:
            return
        seconds = float(self.hold_box.currentData() or 2.0)
        parts, j = sequence.insert_hold(self.parts, self.pos, seconds)
        if j is None:
            return
        self.parts = parts
        self.timeline.set_parts(self.parts)
        self.timeline.select(j)
        self._commit()
        self.goto(sequence.starts(self.parts)[j])
        self.status.setText(_("Standbild eingefügt: {n} s ohne Ton.", n=f"{seconds:g}"))

    def _fx_clear(self, i):
        if 0 <= i < len(self.parts) and clipedit.has_effects(self.parts[i]):
            self._zoom_leave()
            self._fx_set(i, None, color=None, zoom=None, reverse=False)

    # ---- 1.19: the zoom tool (the crop frame of the preview, borrowed for the clip's start/end box)
    def _zoom_tool(self, which):
        i, p = self._fx_part()
        if p is None:
            return
        if self._zoom_edit == (i, which):
            self._zoom_leave()
            return
        self._zoom_leave()
        if self._short_view:                                  # 1.20: the frame belongs on the recording's picture
            self.short_view_box.setChecked(False)
        if self.mode != "select":
            self.mode_btns["select"].setChecked(True)
        pv = self.preview
        self._crop_saved = (pv.crop, pv.crop_ratio, pv.zoom_crop)
        self._zoom_edit = (i, which)
        for k, b in self.zoom_btns.items():
            b.setChecked(k == which)
        box = p.zoom[which] if p.zoom else (0.0, 0.0, 1.0, 1.0)
        pv.set_zoom_crop(False)
        pv.set_crop(box, (self.info.width or 16) / max(1, self.info.height or 9))
        pv.set_crop_edit(True)
        st = sequence.starts(self.parts)
        self.goto(st[i] if which == 0 else max(st[i], st[i + 1] - 0.05))
        self.status.setText(_("Zoom: Ausschnitt in der Vorschau ziehen oder an den Ecken grösser/kleiner ziehen – "
                              "Esc beendet."))

    def _zoom_leave(self) -> bool:
        """End the zoom tool: the preview's crop frame is the clip crop again. False when it was not on."""
        if getattr(self, "_zoom_edit", None) is None:
            return False
        self._zoom_edit = None
        crop, ratio, zc = self._crop_saved
        pv = self.preview
        pv.set_crop_edit(False)
        pv.set_crop(crop, ratio)
        pv.set_zoom_crop(zc)
        for b in self.zoom_btns.values():
            b.setChecked(False)
        if self.status.text().startswith(_("Zoom")):
            self.status.setText("")
        if not self._closed:
            self.goto(self.pos)
        return True

    def _zoom_moved(self):
        """The zoom frame was drawn or moved: the clip's start/end box (both with "Ohne Bewegung")."""
        i, which = self._zoom_edit
        if not 0 <= i < len(self.parts):
            self._zoom_leave()
            return
        p = self.parts[i]
        box = clipedit.clean_box(self.preview.crop)
        full = (0.0, 0.0, 1.0, 1.0)
        z = list(p.zoom) if p.zoom else [full, full]
        z[which] = box
        if self.zoom_still.isChecked():
            z = [box, box]
        self.parts = sequence.with_effects(self.parts, i, zoom=clipedit.clean_zoom(z))
        self.timeline.set_parts(self.parts)
        self._commit(("zoom", i, which))
        self._fx_show()

    def _zoom_still_toggled(self, on):
        i, p = self._fx_part()
        if p is None or not p.zoom:
            return
        if on:
            self._fx_set(i, None, zoom=clipedit.clean_zoom((p.zoom[0], p.zoom[0])))

    def _zoom_clear(self):
        i, p = self._fx_part()
        if p is not None and p.zoom:
            self._zoom_leave()
            self._fx_set(i, None, zoom=None)

    # ---- 1.20: the vertical short (export format "Short / TikTok")
    def _section_short(self, sec, mode):
        from . import shorts
        self.short_layout = self._combo(None, [("blur", _("Unscharfer Hintergrund")), ("crop", _("Zuschnitt 9:16"))],
                                        "blur", _("Unscharfer Hintergrund: das ganze Spielbild in der Mitte, oben und "
                                                  "unten dasselbe Bild unscharf. Zuschnitt: die Mitte (oder der "
                                                  "9:16-Ausschnitt unter Bild) füllt das Hochformat."),
                                        self._short_layout_picked)
        sec.row(_("Vorlage"), self.short_layout)
        self.short_view_box = QCheckBox(_("Als Short anzeigen"))
        self.short_view_box.setToolTip(_("Die Vorschau zeigt das fertige Hochformat mit Titel und Untertiteln – "
                                         "Zeichnungen und Zensur sind im Export drin, hier nicht zu sehen."))
        self.short_view_box.toggled.connect(self._short_view_toggled)
        sec.body.addWidget(self.short_view_box)
        self.short_title = QLineEdit()
        self.short_title.setPlaceholderText(_("Titel oben (leer = keiner)"))
        self.short_title.setMaxLength(shorts.MAX_TEXT)
        self.short_title.textEdited.connect(self._short_title_edited)
        self.short_title.returnPressed.connect(self.setFocus)
        sec.row(_("Titel"), self.short_title)
        self.short_size = self._combo(None, [(0, _("klein")), (1, _("mittel")), (2, _("gross"))], 1,
                                      _("Schriftgrösse des Titels."), self._short_size_picked)
        sec.row(_("Grösse"), self.short_size, stretch=False)
        lbl = QLabel(_("Untertitel"))
        lbl.setProperty("class", "label")
        sec.body.addWidget(lbl)
        self.sub_text = QLineEdit()
        self.sub_text.setPlaceholderText(_("Text eingeben, dann „Untertitel am Abspielkopf“"))
        self.sub_text.setMaxLength(shorts.MAX_TEXT)
        self.sub_text.returnPressed.connect(self._sub_add)
        sec.body.addWidget(self.sub_text)
        row = FlowRow(spacing=6)
        self.sub_add_btn = self._btn(row, _("Untertitel am Abspielkopf"), self._sub_add,
                                     _("Der Text erscheint ab dem Abspielkopf {n} s lang unten im Short.",
                                       n=f"{shorts.SUB_DEFAULT_S:g}"))
        sec.body.addLayout(row)
        self.sub_list = QListWidget()
        self.sub_list.setObjectName("marks")
        self.sub_list.setMaximumHeight(130)
        self.sub_list.setFocusPolicy(Qt.NoFocus)
        self.sub_list.itemClicked.connect(self._sub_picked)
        sec.body.addWidget(self.sub_list)
        row = FlowRow(spacing=6)
        self.sub_start_btn = self._btn(row, _("Beginnt hier"), lambda: self._sub_edge(0),
                                       _("Der markierte Untertitel beginnt am Abspielkopf."))
        self.sub_end_btn = self._btn(row, _("Endet hier"), lambda: self._sub_edge(1),
                                     _("Der markierte Untertitel endet am Abspielkopf."))
        self.sub_del_btn = self._btn(row, _("Entfernen"), self._sub_remove, _("Entfernt den markierten Untertitel."))
        sec.body.addLayout(row)

    def _mode_changed(self, _i, save=True):
        super()._mode_changed(_i, save)
        if getattr(self, "sections", None) is None:
            return
        if self.mode_box.currentData() != "shorts" and self._short_view:
            self.short_view_box.setChecked(False)
        self._inspector_refresh()

    def _short_spec(self):
        from . import shorts
        return self._short.copy() if self._short is not None else shorts.ShortSpec()

    def _short_set(self, spec, key=None):
        """The short changed: one undo step (``key`` merges typing), the preview and the timeline follow."""
        self._short = None if spec.empty() else spec
        self._commit(key)
        self._short_show()
        if self._short_view:
            self.goto(self.pos)

    def _short_show(self):
        """The section shows the short (without firing its handlers)."""
        spec = self._short_spec()
        for box, value in ((self.short_layout, spec.layout), (self.short_size, spec.title_size)):
            box.blockSignals(True)
            box.setCurrentIndex(max(0, box.findData(value)))
            box.blockSignals(False)
        if self.short_title.text() != spec.title and not self.short_title.hasFocus():
            self.short_title.setText(spec.title)
        row = self.sub_list.currentRow()
        self.sub_list.blockSignals(True)
        self.sub_list.clear()
        for sub in spec.subs:
            self.sub_list.addItem(f"{clipedit.fmt_pos(sub.t0)}–{clipedit.fmt_pos(sub.t1)}  {sub.text}")
        if 0 <= row < self.sub_list.count():
            self.sub_list.setCurrentRow(row)
        self.sub_list.blockSignals(False)
        has = self.sub_list.currentRow() >= 0
        for b in (self.sub_start_btn, self.sub_end_btn, self.sub_del_btn):
            b.setEnabled(has)
        self.timeline.set_subs([(s.t0, s.t1) for s in spec.subs])

    def _short_layout_picked(self, _i=None):
        spec = self._short_spec()
        spec.layout = self.short_layout.currentData() or "blur"
        self._short_set(spec)

    def _short_size_picked(self, _i=None):
        spec = self._short_spec()
        spec.title_size = int(self.short_size.currentData() or 0)
        self._short_set(spec)

    def _short_title_edited(self, text):
        from . import shorts
        spec = self._short_spec()
        spec.title = shorts.clean_text(text)
        self._short_set(spec, key="short_title")

    def _sub_add(self):
        from . import shorts
        text = shorts.clean_text(self.sub_text.text())
        if not text or not self.parts:
            self.status.setText(_("Erst den Text des Untertitels eingeben."))
            return
        spec = self._short_spec()
        t0 = round(self.pos, 2)
        t1 = round(min(self.timeline.total(), t0 + shorts.SUB_DEFAULT_S), 2)
        if t1 - t0 < 0.1:
            t0 = max(0.0, t1 - shorts.SUB_DEFAULT_S)
        spec.subs.append(shorts.Sub(t0, t1, text))
        spec.subs.sort(key=lambda s: s.t0)
        self.sub_text.clear()
        self._short_set(spec)
        self.sub_list.setCurrentRow(next(i for i, s in enumerate(spec.subs) if s.t0 == t0 and s.text == text))
        self._short_show()

    def _sub_picked(self, _item=None):
        spec = self._short_spec()
        i = self.sub_list.currentRow()
        if 0 <= i < len(spec.subs):
            self.goto(spec.subs[i].t0)
        self._short_show()

    def _sub_edge(self, which):
        spec = self._short_spec()
        i = self.sub_list.currentRow()
        if not 0 <= i < len(spec.subs):
            return
        s = spec.subs[i]
        if which == 0:
            s.t0 = round(min(self.pos, s.t1 - 0.1), 2)
        else:
            s.t1 = round(max(self.pos, s.t0 + 0.1), 2)
        self._short_set(spec)

    def _sub_remove(self):
        spec = self._short_spec()
        i = self.sub_list.currentRow()
        if 0 <= i < len(spec.subs):
            del spec.subs[i]
            self._short_set(spec)

    def _short_view_toggled(self, on):
        if on and self.mode != "select":
            self.mode_btns["select"].setChecked(True)
        if on:
            self._zoom_leave()
        self._short_view = bool(on)
        self.preview.overlays = not on
        self.goto(self.pos)

    def _short_canvas(self) -> tuple:
        _w, h = clipedit.scaled(self.info, clipedit.PREVIEW_H)
        return h * 9 // 16 // 2 * 2, h // 2 * 2

    def _play_size(self):
        return self._short_canvas() if self._short_view else None

    def _short_vf(self) -> list:
        """1.20: the clip crop and the short's canvas on the preview picture (only while it shows the short)."""
        if not self._short_view:
            return []
        from . import shorts
        cw, ch = self._short_canvas()
        out = []
        crop = self.edit_plan().crop
        if crop:
            x, y, w_, h_ = crop
            out.append(f"crop=iw*{w_:.5f}:ih*{h_:.5f}:iw*{x:.5f}:ih*{y:.5f}")
        spec = self._short_spec()
        out.append(shorts.canvas_filters(spec.layout, cw, ch, label="p"))
        return out

    def _play_vf(self, part, t0, still: bool = False) -> list:
        return super()._play_vf(part, t0, still) + self._short_vf()

    def _paint(self, img):
        if self._short_view and self._short is not None:          # the title and subtitles at the playhead
            from . import shorts
            img = shorts.paste_texts(img, self._short, self.pos)
        super()._paint(img)

    def _section_marks(self, sec, mode):
        self.mark_list = QListWidget()
        self.mark_list.setObjectName("marks")
        self.mark_list.setMaximumHeight(120)
        self.mark_list.setFocusPolicy(Qt.NoFocus)           # the window keeps the keys (arrows seek, M = next mark)
        for m in self.marks:
            self.mark_list.addItem(f"⚑  {clipedit.fmt_pos(m)}")
        self.mark_list.itemClicked.connect(lambda _it: self.goto_src(self._picked_mark()))
        self.mark_list.itemDoubleClicked.connect(lambda _it: self.clip_around_mark())
        sec.body.addWidget(self.mark_list)
        row = FlowRow(spacing=6)
        self.around_btn = self._btn(row, _("Clip um Marke"), self.clip_around_mark,
                                    _("Der Clip beginnt {before} s vor der markierten Marke (ohne Auswahl: der "
                                      "nächsten am Abspielkopf) und endet {after} s danach.",
                                      before=f"{MARK_BEFORE_S:g}", after=f"{MARK_AFTER_S:g}"))
        self.around_btn.setEnabled(bool(self.marks))
        self.mark_btn = self._btn(row, _("Zur Marke ▸"), self.next_mark, _("Springt zur nächsten F8-Marke (Taste M)."))
        self.mark_btn.setEnabled(bool(self.marks))
        sec.body.addLayout(row)

    def _section_picture(self, sec, mode):
        self.crop_box = self._combo(None, [(k, _(v) if k in ("none", "free", "9:16") else v)
                                           for k, v in CROP_LABELS.items()], "none",
                                    _("Schneidet einen Bereich aus dem Bild – 9:16 für YouTube Shorts und TikTok, 1:1 "
                                      "für Instagram. Den Rahmen in der Vorschau verschieben und an den Ecken ziehen."),
                                    self._crop_picked)
        sec.row(_("Ausschnitt"), self.crop_box)
        row = FlowRow(spacing=6)
        self.crop_btn = self._btn(row, _("Rahmen bearbeiten"), self._crop_tool,
                                  _("Rahmen in der Vorschau verschieben oder an den Ecken grösser/kleiner ziehen. "
                                    "Nochmal drücken beendet das Werkzeug."))
        self.crop_btn.setCheckable(True)
        self.crop_btn.setProperty("class", "seg")
        sec.body.addLayout(row)
        self.content_hint = QLabel(_("Die Aufnahme hat schwarze Ränder: „Ohne schwarze Ränder“ speichert nur das "
                                     "Spielbild, „Kein Ausschnitt“ das ganze Bild."))
        self.content_hint.setProperty("class", "dim")
        self.content_hint.setWordWrap(True)
        self.content_hint.setVisible(False)              # 1.12.6: once black borders were found
        sec.body.addWidget(self.content_hint)
        fades = [(v, _("aus") if v == 0 else f"{v:g} s") for v in clipedit.FADES]
        self.fade_in_box = self._combo(None, fades, 0.0, _("Der Clip beginnt aus Schwarz und mit leisem Ton."),
                                       lambda _i: self._commit())
        self.fade_out_box = self._combo(None, fades, 0.0, _("Der Clip endet in Schwarz, der Ton wird leiser."),
                                        lambda _i: self._commit())
        sec.row(_("Einblenden"), self.fade_in_box, stretch=False)
        sec.row(_("Ausblenden"), self.fade_out_box, stretch=False)

    def _section_draw(self, sec, mode):
        tr = FlowRow(spacing=4)
        self.draw_btns = {}
        for kind, label in DRAW_TOOLS:
            b = self._tool(TOOL_ICONS[kind], _(label) + " – " + _("Im Bild ziehen (Text: klicken). Eine Zeichnung "
                                                                   "anklicken markiert sie, ziehen verschiebt sie, Entf "
                                                                   "löscht sie."), checkable=True)
            b.setFixedSize(32, 32)
            b.toggled.connect(lambda on, k=kind: self._draw_tool(k, on))
            self.draw_btns[kind] = b
            tr.addWidget(b)
        sec.body.addLayout(tr)
        pr = FlowRow(spacing=6)
        self.colour_btns = {}
        for colour in annotate.COLOURS:
            b = QPushButton("")
            b.setProperty("class", "swatch")
            b.setFixedSize(22, 22)
            b.setFocusPolicy(Qt.NoFocus)
            b.setCheckable(True)
            b.setToolTip(_("Farbe"))
            b.setStyleSheet(f"QPushButton {{ background: {colour}; }}")
            b.clicked.connect(lambda _c=False, col=colour: self._draw_colour(col))
            pr.addWidget(b)
            self.colour_btns[colour] = b
        self.colour_btns[annotate.COLOURS[0]].setChecked(True)
        sec.body.addLayout(pr)
        self.draw_size_box = self._combo(None, list(enumerate(_(x) for x in SIZE_LABELS)), 1,
                                         _("Strichstärke bzw. Textgrösse."), self._draw_size)
        sec.row(_("Stärke"), self.draw_size_box, stretch=False)
        self.draw_when_box = self._combo(None, [(v, _(lbl)) for v, lbl in SHOW_FOR], 3.0,
                                         _("Wie lange die Zeichnung im Clip zu sehen ist – ab der Stelle des "
                                           "Abspielkopfs. Gilt für neue und für die markierte Zeichnung."),
                                         self._draw_when)
        sec.row(_("Sichtbar"), self.draw_when_box, stretch=False)
        self.draw_text = QLineEdit()
        self.draw_text.setPlaceholderText(_("Text für das Text-Werkzeug"))
        self.draw_text.textEdited.connect(self._draw_text_edited)
        self.draw_text.returnPressed.connect(self.setFocus)
        sec.body.addWidget(self.draw_text)
        xr = FlowRow(spacing=6)
        self.draw_del_btn = self._btn(xr, _("Zeichnung entfernen"), self._draw_remove,
                                      _("Entfernt die markierte Zeichnung (Entf)."))
        self.draw_clear_btn = self._btn(xr, _("Alle Zeichnungen entfernen"), self._draw_clear, "")
        sec.body.addLayout(xr)

    def _section_censor(self, sec, mode):
        self.censor_box = QCheckBox(_("Beim Speichern anwenden"))
        self.censor_box.setChecked(self._censor_on)
        self.censor_box.setFocusPolicy(Qt.NoFocus)
        self.censor_box.setToolTip(_("Die Kästen werden im gespeicherten Clip unkenntlich gemacht (dafür wird das "
                                     "Bild neu kodiert, auch im Format „Schnell“)."))
        self.censor_box.toggled.connect(self._censor_toggled)
        sec.body.addWidget(self.censor_box)
        self.style_box = self._choice()
        for key in clipedit.CENSOR_STYLES:
            self.style_box.addItem(_(CENSOR_LABELS[key]), key)
        self.style_box.setCurrentIndex(max(0, list(clipedit.CENSOR_STYLES).index(self._censor_style)
                                           if self._censor_style in clipedit.CENSOR_STYLES else 0))
        self.style_box.currentIndexChanged.connect(self._censor_style_changed)
        sec.row(_("Art"), self.style_box, stretch=False)
        zb = FlowRow(spacing=6)
        self.tool_btn = self._btn(zb, _("Kasten zeichnen"), self._tool_toggled,
                                  _("Im Bild einen Bereich aufziehen; Kästen lassen sich verschieben und an der "
                                    "Ecke rechts unten vergrössern. Nochmal drücken beendet das Werkzeug."))
        self.tool_btn.setCheckable(True)
        self.tool_btn.setProperty("class", "seg")
        self.names_btn = self._btn(zb, _("Namen links unten"), self._add_names_box,
                                   _("Setzt einen Kasten dorthin, wo DBD die Namen der Survivor zeigt (links unten "
                                     "im Spielbild) – bei Bedarf verschieben."))
        self.remove_btn = self._btn(zb, _("Kasten entfernen"), self._remove_box,
                                    _("Entfernt den markierten Kasten (Taste Entf)."))
        self.clear_btn = self._btn(zb, _("Alle entfernen"), self._clear_boxes, "")
        sec.body.addLayout(zb)
        self.censor_hint = QLabel("")
        self.censor_hint.setProperty("class", "dim")
        self.censor_hint.setWordWrap(True)
        sec.body.addWidget(self.censor_hint)

    def _section_sound(self, sec, mode):
        sec.body.addLayout(self._mix_row(stacked=True))
        self.mix_label.setVisible(False)                     # the section has the heading

    def _section_export(self, sec, mode):
        self._mode_boxes(mode)
        fmt = FlowRow(spacing=6)
        fmt.addWidget(self.mode_box)
        fmt.addWidget(self.target_box)
        fmt.addWidget(self.gif_box)
        sec.row(_("Format"))
        sec.body.addLayout(fmt)
        enc = self._encoding_row()
        self.enc_label.setVisible(False)
        self.enc_widgets = self.enc_widgets[1:]                 # the section row names it; _mode_changed leaves it hidden
        sec.row(_("Kodierung"))
        sec.body.addLayout(enc)
        self.size_label = QLabel("")
        self.size_label.setProperty("class", "dim")
        self.size_label.setWordWrap(True)
        sec.body.addWidget(self.size_label)
        row = FlowRow(spacing=6)
        self.export_btn = self._btn(row, _("Exportieren"), self.save,
                                    _("Schreibt den Schnitt als Clip in den Ordner „Clips“ neben den Aufnahmen "
                                      "(Strg+E) – Format und Kodierung im Inspector unter Export."))
        self.show_btn = self._btn(row, _("Im Explorer zeigen"), self._show_saved,
                                  _("Zeigt den zuletzt gespeicherten Clip im Explorer."))
        self.show_btn.setEnabled(False)
        self.open_btn = self._btn(row, _("Clips-Ordner öffnen"), self._open_clips, _("Öffnet den Ordner „Clips“ im Explorer."))
        sec.body.addLayout(row)

    def _build_timeline(self, c):
        self.tl_panel = QFrame()
        self.tl_panel.setObjectName("panel")
        self.tl_panel.setMinimumHeight(150)
        lay = QVBoxLayout(self.tl_panel)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        bar = QFrame()
        bar.setObjectName("tlbar")
        bar.setFixedHeight(34)
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(10, 0, 10, 0)
        bl.setSpacing(2)
        title = QLabel(_("Zeitleiste"))
        title.setProperty("class", "section")
        bl.addWidget(title)
        bl.addSpacing(12)
        self.tl_split_btn = self._tool("split", _("Teilt den Clip unter dem Abspielkopf in zwei (Taste S)."),
                                       self.split_at_playhead)
        self.tl_delete_btn = self._tool("trash", _("Entfernt den markierten Clip von der Zeitleiste (Entf) – die "
                                                   "Aufnahme bleibt."), self.delete_selected)
        bl.addWidget(self.tl_split_btn)
        bl.addWidget(self.tl_delete_btn)
        bl.addSpacing(8)
        self.seq_label = QLabel("")
        self.seq_label.setProperty("class", "dim")
        bl.addWidget(self.seq_label)
        bl.addStretch()
        self.zoom_out_btn = self._tool("zoom_out", _("Zeitleiste herauszoomen (−, Strg+Mausrad)."), lambda: self.timeline.zoom_out())
        self.zoom_in_btn = self._tool("zoom_in", _("Zeitleiste hineinzoomen (+, Strg+Mausrad)."), lambda: self.timeline.zoom_in())
        self.zoom_fit_btn = self._tool("zoom_fit", _("Den ganzen Schnitt einpassen (Strg+0)."), lambda: self.timeline.zoom_fit())
        for b in (self.zoom_out_btn, self.zoom_in_btn, self.zoom_fit_btn):
            bl.addWidget(b)
        lay.addWidget(bar)
        self.timeline = SequenceTimeline(self.dark)
        self.timeline.seek.connect(self.goto)
        self.timeline.scrubbed.connect(self._scrub_edge)
        self.timeline.selected.connect(self._clip_selected)
        self.timeline.edited.connect(self._timeline_edited)
        self.timeline.picked.connect(self._timeline_pick)
        self.timeline.dropped.connect(self._dropped)
        self.timeline.viewed.connect(self._sync_scroll)
        lay.addWidget(self.timeline)
        self.tl_scroll = QScrollBar(Qt.Horizontal)
        self.tl_scroll.setFocusPolicy(Qt.NoFocus)
        self.tl_scroll.valueChanged.connect(lambda v: self.timeline.set_offset(v / 1000.0))
        lay.addWidget(self.tl_scroll)
        return self.tl_panel

    def _build_statusbar(self, c):
        bar = QFrame()
        bar.setObjectName("statusbar")
        bar.setFixedHeight(26)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(12)
        self.status = QLabel("")
        self.status.setProperty("class", "dim")
        lay.addWidget(self.status, 1)
        self.hint = QLabel("")
        self.hint.setProperty("class", "dim")
        self.hint.setToolTip(_(KEY_HINT))
        self.hint.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.hint.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        lay.addWidget(self.hint, 2)
        return bar

    def _hint_fit(self):
        """The key hint as much as the status bar's room allows, cut with an ellipsis at its end."""
        if getattr(self, "hint", None) is None:
            return
        fm = self.hint.fontMetrics()
        self.hint.setText(fm.elidedText(_(KEY_HINT), Qt.ElideRight, max(40, self.hint.width() - 4)))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        QTimer.singleShot(0, self._hint_fit)
        if getattr(self, "key_help", None) is not None and not self.key_help.isHidden():
            self.key_help.place()

    def _shortcuts(self):
        def editing(fn):                                 # 1.18.1: nothing is edited while the recording is checked
            return lambda: None if self._edit_locked() else fn()
        for std, extra, slot in ((QKeySequence.Undo, (), editing(self.undo)),
                                 (QKeySequence.Redo, ("Ctrl+Y",), editing(self.redo)),
                                 (QKeySequence.Save, (), self.save_project), (None, ("Ctrl+E",), self.save),
                                 (None, ("Ctrl+0",), lambda: self.timeline.zoom_fit()),
                                 (None, ("Ctrl+B",), editing(self.split_at_playhead)),
                                 (None, ("Ctrl+W",), self.close)):             # 1.18: Esc no longer closes
            keys = list(QKeySequence.keyBindings(std)) if std is not None else []
            keys += [QKeySequence(k) for k in extra if QKeySequence(k) not in keys]
            sc = QShortcut(self)
            sc.setKeys(keys)
            sc.activated.connect(slot)

    # ---- panels and layout
    def _toggle_panel(self, panel, on: bool):
        panel.setVisible(bool(on))
        self._layout_changed()

    def _layout_changed(self, *_a):
        if self._layout_timer is None:
            self._layout_timer = QTimer(self)
            self._layout_timer.setSingleShot(True)
            self._layout_timer.setInterval(LAYOUT_SAVE_MS)
            self._layout_timer.timeout.connect(self._layout_save)
        self._layout_timer.start()

    def _layout_save(self):
        if self._fullscreen is not None or self._closed:
            return
        data = {"h": self.hsplit.sizes(), "v": self.vsplit.sizes(), "lib": self.lib_btn.isChecked(),
                "insp": self.insp_btn.isChecked()}
        if all(v > 0 for v in data["v"]) and data != self._layout:
            self._layout = data
            self._setting("editor_layout", data)

    def toggle_fullscreen(self):
        """Only the viewer: the panels fold away and the window fills the screen (F / Esc back)."""
        if self._fullscreen is None:
            self._fullscreen = (self.topbar.isVisible(), self.library.isVisible(), self.inspector.isVisible(),
                                self.tl_panel.isVisible(), self.isMaximized())
            for w in (self.topbar, self.library, self.inspector, self.tl_panel):
                w.setVisible(False)
            self.showFullScreen()
            self.fs_btn.setIcon(qt_icons.icon("fullscreen_exit", self.colours["fg"], self.colours["head"], ratio=self.ratio))
        else:
            top, lib, insp, tl, maxed = self._fullscreen
            self._fullscreen = None
            self.showMaximized() if maxed else self.showNormal()
            self.topbar.setVisible(top)
            self.library.setVisible(lib)
            self.inspector.setVisible(insp)
            self.tl_panel.setVisible(tl)
            self.fs_btn.setIcon(qt_icons.icon("fullscreen", self.colours["fg"], self.colours["head"], ratio=self.ratio))

    def _sync_scroll(self):
        tl = self.timeline
        self.tl_scroll.blockSignals(True)
        self.tl_scroll.setRange(0, int(tl.max_offset() * 1000))
        self.tl_scroll.setPageStep(int(tl._track_width() / tl.scale * 1000))
        self.tl_scroll.setValue(int(tl.offset * 1000))
        self.tl_scroll.blockSignals(False)

    # ---- the library
    def _fill_library(self):
        items = []
        if callable(self.media):
            try:
                items = list(self.media() or [])
            except Exception:                           # the list is a convenience: never breaks the editor
                items = []
        # 1.18.1: the project files' heads (format 1 and 2, cached by mtime and size) say which rows have one
        names = {e.source.get("file") for e in project.scan(os.path.join(self.clips_dir, project.PROJECT_DIR)) if e.ok}
        for it in items:
            it.project = os.path.basename(it.path) in names
        self.library.set_items(items, current=self.path)

    def _open_media(self, item):
        """A library row (double click, drop on the timeline): the App opens it – in place of this window when
        nothing was cut here yet, else in a window of its own so the cut stays."""
        if item is None:
            return
        if item.key == os.path.normcase(os.path.abspath(self.path)):
            self.status.setText(_("Diese Aufnahme ist schon auf der Zeitleiste."))
            return
        if self.on_open is None:
            self.status.setText(_("Öffnen aus der Bibliothek ist hier nicht verfügbar."))
            return
        pristine = self.history is None or not self.history.can_undo()
        self.on_open(item, self if pristine else None)

    def _dropped(self, path):
        item = self.library.item_for(path)
        if item is None and os.path.isfile(path) and medialib.is_video(path):
            item = self.library.add_files([path])
        if item is None:
            self.status.setText(_("Keine Videodatei: {file}", file=os.path.basename(path)))
            return
        self._open_media(item)

    def _show_file(self, path):
        import subprocess
        if os.name == "nt" and os.path.exists(path):
            subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])   # noqa: S603,S607
        else:
            self.status.setText(path)

    def event(self, e):
        if e.type() == QEvent.WindowActivate and getattr(self, "library", None) is not None and self._pumping_ok():
            self._fill_library()
        elif e.type() == QEvent.WindowDeactivate and not self._closed:
            self._submit(view_event=True)                # 1.18.1: focus away – the state with its view
        return super().event(e)

    def _pumping_ok(self) -> bool:
        if self._closed or self.history is None:
            return False
        import time
        now = time.monotonic()
        if now - getattr(self, "_lib_filled", 0.0) < 5.0:         # at most every few seconds
            return False
        self._lib_filled = now
        return True

    def _extra_threads(self):
        self.bridge.wave.connect(lambda bins: self.timeline.set_wave(bins, clipedit.WAVE_PER_S))
        if self.info.audio_tracks > 0:
            path, duration, ffmpeg, b, cancel = self.path, self.info.duration, self.ffmpeg, self.bridge, self._cancel

            def wave():                         # 1.16.2: ends with the window (cancel), emits nothing after it
                bins = clipedit.waveform(path, duration, ffmpeg, cancel=cancel)
                if not cancel.is_set():
                    b.wave.emit(bins)
            threading.Thread(target=wave, name="clip-wave", daemon=True).start()

    def _drain(self):
        super()._drain()
        if not self._closed and getattr(self, "library", None) is not None:
            self.library.pump()

    # ---- the state, undo and redo
    def _state(self) -> sequence.EditState:
        crop = self.preview.crop if self._zoom_edit is None else self._crop_saved[0]   # 1.19: the zoom tool borrows it
        return sequence.EditState([replace(p) for p in self.parts],
                                  tuple(crop) if crop and self.crop_box.currentData() != "none" else None,
                                  str(self.crop_box.currentData() or "none"),
                                  [replace(s, pts=list(s.pts)) for s in self.preview.shapes],
                                  float(self.fade_in_box.currentData() or 0), float(self.fade_out_box.currentData() or 0),
                                  [list(b) for b in self.preview.boxes], self._censor_on, self._censor_style,
                                  self._short.copy() if self._short is not None else None)

    def _apply(self, state: sequence.EditState):
        """Show ``state`` (undo/redo, a loaded project) without writing history."""
        self._zoom_leave()
        self._short = state.short.copy() if getattr(state, "short", None) is not None else None
        self._applying = True
        try:
            self.parts = [replace(p) for p in state.parts]
            self.timeline.set_parts(self.parts)
            key = state.crop_key if state.crop else "none"
            if key == "content" and self.crop_box.findData("content") < 0:
                key = "free"
            self.crop_box.blockSignals(True)
            self.crop_box.setCurrentIndex(max(0, self.crop_box.findData(key)))
            self.crop_box.blockSignals(False)
            ratio = dict(clipedit.ASPECTS).get(key)
            self.preview.set_zoom_crop(key == "content")
            self.preview.set_crop(state.crop, ratio)
            if key == "none":
                self.crop_btn.setChecked(False)
                self.preview.set_crop_edit(False)
            self.preview.set_shapes([replace(s, pts=list(s.pts)) for s in state.shapes])
            for box, value in ((self.fade_in_box, state.fade_in), (self.fade_out_box, state.fade_out)):
                box.blockSignals(True)
                box.setCurrentIndex(max(0, box.findData(value)))
                box.blockSignals(False)
            self.preview.set_boxes(state.boxes)
            self._censor_on, self._censor_style = bool(state.censor_on), state.censor_style
            self.censor_box.blockSignals(True)
            self.censor_box.setChecked(self._censor_on)
            self.censor_box.blockSignals(False)
            self.style_box.blockSignals(True)
            self.style_box.setCurrentIndex(max(0, self.style_box.findData(self._censor_style)))
            self.style_box.blockSignals(False)
            self.preview.set_look(self._censor_on, self._censor_style)
        finally:
            self._applying = False
        self.pos = min(self.pos, self.timeline.total())
        self.goto(self.pos)
        self._refresh()

    def _commit(self, key=None):
        """After a change: into the history, the window follows."""
        if self._applying or self.history is None:
            return
        if self.history.push(self._state(), key):
            self._refresh_undo()
            self._changed()
        self._refresh()

    def _refresh_undo(self):
        if self.history is None:
            return
        self.undo_btn.setEnabled(self.history.can_undo())
        self.redo_btn.setEnabled(self.history.can_redo())

    def undo(self):
        if self.history is not None and self.history.can_undo():
            self._apply(self.history.undo())
            self._refresh_undo()
            self._changed()
            self.status.setText(_("Rückgängig."))

    def redo(self):
        if self.history is not None and self.history.can_redo():
            self._apply(self.history.redo())
            self._refresh_undo()
            self._changed()
            self.status.setText(_("Wiederholt."))

    def _refresh(self):
        """Labels and sections after any change."""
        if self.history is None and not self.info.ok:
            return
        self._show_pos()
        self._show_size()
        self._inspector_refresh()
        total = self.timeline.total()
        n = len(self.parts)
        self.seq_label.setText(_("{n} Clip(s) · {length} s", n=n, length=f"{total:.1f}") if n else _("Keine Clips auf der Zeitleiste."))
        if not self.name_edit.isModified() or not self.name_edit.text():
            self.name_edit.setText(self._default_name())
            self.name_edit.setCursorPosition(0)
            self.name_edit.setModified(False)
        self._censor_hint()

    def _inspector_refresh(self):
        sel = self.timeline.selection
        secs = self.sections
        secs["clip"].setVisible(sel is not None)
        secs["fx"].setVisible(sel is not None)
        secs["short"].setVisible(self.mode_box.currentData() == "shorts")     # 1.20
        if secs["short"].isVisibleTo(self):
            self._short_show()
        secs["marks"].setVisible(bool(self.marks))
        secs["draw"].setVisible(self.mode == "draw")
        secs["censor"].setVisible(self.mode == "censor")
        if sel is not None and sel < len(self.parts):
            p = self.parts[sel]
            st = sequence.starts(self.parts)
            self.clip_title.setText(_("Clip {n} von {total}", n=sel + 1, total=len(self.parts)))
            self.clip_facts.setText(_("Aufnahme {start} – {end} · auf der Zeitleiste ab {at} · {length} s",
                                      start=clipedit.fmt_pos(p.start), end=clipedit.fmt_pos(p.end),
                                      at=clipedit.fmt_pos(st[sel]), length=f"{sequence.length(p):.1f}"))
            self._select_speed(p.speed)
            self.speed_box.setEnabled(p.hold <= 0)              # 1.19: a still has no tempo
            if p.hold > 0:
                self.clip_title.setText(_("Standbild – Clip {n} von {total}", n=sel + 1, total=len(self.parts)))
                self.clip_facts.setText(_("Bild bei {at} der Aufnahme · {length} s ohne Ton",
                                          at=clipedit.fmt_pos(p.start), length=f"{p.hold:g}"))
            self._fx_show()
        self.insp_title.setText({"select": _("Inspector"), "crop": _("Ausschnitt"), "draw": _("Zeichnen"),
                                 "censor": _("Zensieren")}[self.mode])
        self.delete_btn.setEnabled(sel is not None)
        self.tl_delete_btn.setEnabled(sel is not None)
        self.split_btn.setEnabled(bool(self.parts))
        self.tl_split_btn.setEnabled(bool(self.parts))
        self.save_btn.setEnabled(bool(self.parts) and self.info.ok and not self._exporting())
        self.export_btn.setEnabled(self.save_btn.isEnabled())

    def _exporting(self) -> bool:
        from .qt_clip import _SAVES
        return any(job.win is self and not job.out.lower().endswith(".png") for job in _SAVES)

    # ---- modes (the tool rail)
    def _set_mode(self, mode: str):
        if mode not in MODES:
            return
        if mode != "select":
            self._zoom_leave()
            if self._short_view:                              # 1.20: tools work on the recording's picture
                self.short_view_box.setChecked(False)
        self.mode = mode
        btn = self.mode_btns[mode]
        if not btn.isChecked():
            btn.setChecked(True)
        if mode != "crop" and self.crop_btn.isChecked():
            self.crop_btn.setChecked(False)
            self.preview.set_crop_edit(False)
        if mode != "draw":
            for b in self.draw_btns.values():
                if b.isChecked():
                    b.setChecked(False)
            self.preview.set_shape_tool(None)
        if mode != "censor" and self.tool_btn.isChecked():
            self.tool_btn.setChecked(False)
            self.preview.set_editing(False)
        if mode == "crop" and not self.crop_btn.isChecked():
            self.crop_btn.setChecked(True)
            self._crop_tool()
        elif mode == "draw" and not any(b.isChecked() for b in self.draw_btns.values()):
            self.draw_btns[getattr(self, "_last_draw", "arrow")].setChecked(True)
        elif mode == "censor" and not self.tool_btn.isChecked():
            self.tool_btn.setChecked(True)
            self._tool_toggled()
        self._inspector_refresh()

    # ---- the playhead (output time)
    def _src_pos(self) -> float:
        return sequence.source_at(self.parts, self.pos)[1]

    def goto(self, t: float):
        """The playhead to output second ``t``: stops a playback, asks for the picture of that moment."""
        if self.playing:
            self._stop_player()
        total = self.timeline.total()
        self.pos = min(max(0.0, float(t)), total)
        self.timeline.set_playhead(self.pos)
        self.timeline.ensure_visible(self.pos)
        i, src = sequence.source_at(self.parts, self.pos)
        self.preview.set_now(src)
        self._show_pos()
        self._scrub(src, vf=self._effects_vf(i, src))

    def _effects_vf(self, i, src) -> list:
        """1.19: the effects of clip ``i`` on the still at ``src`` – the zoom tool shows the whole picture (its boxes
        are drawn over it)."""
        if i is None or not 0 <= i < len(self.parts):
            return []
        p = self.parts[i]
        if self._zoom_edit is not None:
            p = replace(p, zoom=None)
        w, h = clipedit.scaled(self.info, clipedit.PREVIEW_H)
        return clipedit.preview_filters(p, w, h, t0=src, still=True) + self._short_vf()

    def goto_src(self, src):
        """The playhead to the output moment at which source second ``src`` plays (the nearest one when the
        moment is used more than once); a moment outside every clip only shows its picture."""
        if src is None:
            return
        where = sequence.occurrences(self.parts, src)
        if where:
            self.goto(min(where, key=lambda t: abs(t - self.pos)))
        else:
            self.status.setText(_("{at} liegt in keinem Clip der Zeitleiste.", at=clipedit.fmt_pos(src)))
            self.preview.set_now(src)
            self._scrub(src)

    def _scrub_edge(self, src):
        """A trimmed edge: show that picture (the playhead stays)."""
        self.preview.set_now(src)
        self._scrub(src, quick=True)

    def _apply_take_over(self, start: float, end: float, pos: float):
        """1.8.8: the compact editor hands over its range and position (source seconds). 1.18.1: called by
        ProjectMixin.take_over – once the project is known and the user agreed to replace its clips (F1)."""
        if not self.info.ok:
            return
        self.parts = [clipedit.Part(max(0.0, start), min(self.info.duration, max(start + 0.1, end)))]
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto_src(min(max(start, pos), end))

    def step(self, seconds: float):
        self.goto(self.pos + seconds)

    def step_frame(self, n: int):
        self.goto(self.pos + n / max(1.0, self.info.fps))

    def _show_pos(self):
        self.pos_label.setText(f"{clipedit.fmt_pos(self.pos)} / {clipedit.fmt_pos(self.timeline.total())}")

    def _segments(self) -> list:
        i, src = sequence.source_at(self.parts, self.pos)
        if i is None:
            return []
        st = sequence.starts(self.parts)
        if i == len(self.parts) - 1 and self.pos >= st[-1] - 0.05:       # at the very end: from the start
            self.pos = 0.0
            i = 0
        segs = [self._segment(i, st[i], self.pos)]
        segs += [self._segment(k, st[k], st[k]) for k in range(i + 1, len(self.parts))]
        return segs

    def _segment(self, i, start_out, at):
        """1.19: the playback stretch of clip ``i`` from output time ``at`` on – (source from, source to, tempo,
        output time at its start, the clip[, seconds a still has left])."""
        p = self.parts[i]
        if p.hold > 0:
            return (p.start, p.start, 1.0, at, p, max(0.0, p.hold - (at - start_out)))
        _k, src = sequence.source_at(self.parts, at) if at > start_out else (i, p.end if p.reverse else p.start)
        if p.reverse:                                   # backwards: the source up to here, played from its end
            return (p.start, src, p.speed, at, p)
        return (src, p.end, p.speed, at, p)

    def _played_at(self, t):
        if self._seg is None:
            return
        start, _end, speed, out0 = self._seg[:4]
        self.pos = out0 + max(0.0, t - start) / max(0.01, speed)
        self.timeline.set_playhead(self.pos)
        self.timeline.ensure_visible(self.pos)

    def _after_playing(self, back):
        self.goto(back if back is not None else self.pos)

    def _show_playing(self, on: bool):
        self.play_btn.setIcon(self._play_icons[1 if on else 0])
        self.play_btn.setToolTip(_("Pause (Leertaste)") if on else _("Abspielen / Pause (Leertaste)"))

    def watch_clip(self):
        """Play the whole cut from its start, then back to the start."""
        self.goto(0.0)
        self._play_to = 0.0
        self.toggle_play()

    def _mute_toggled(self, muted):
        self.mute_btn.setIcon(self._vol_icons[1 if muted else 0])
        if self.sound_box.isChecked() == muted:
            self.sound_box.setChecked(not muted)
        if self.playing:
            self._restart_playing()

    def _volume_changed(self, v):
        self._volume = max(0.0, min(1.0, v / 100.0))
        if self.playing and self._sound_wanted():
            self._restart_playing()

    def _restart_playing(self):
        back = self._play_to
        self._stop_player()
        self._play_to = back
        self.toggle_play()

    # ---- editing the sequence
    def _clip_at_playhead(self):
        return sequence.source_at(self.parts, self.pos)

    def split_at_playhead(self):
        new, j = sequence.split(self.parts, self.pos)
        if j is None:
            self.status.setText(_("Hier lässt sich nichts teilen – der Abspielkopf steht auf einer Clip-Grenze."))
            return
        self.parts = new
        self.timeline.set_parts(self.parts)
        self.timeline.select(j)
        self._commit()
        self.status.setText(_("Clip geteilt – jetzt {n} Clips.", n=len(self.parts)))

    def delete_selected(self):
        i = self.timeline.selection
        if i is None:
            return
        self.parts = sequence.remove(self.parts, i)
        self.timeline.selection = None
        self.timeline.set_parts(self.parts)
        self.timeline.selected.emit(None)
        self._commit()
        self.goto(min(self.pos, self.timeline.total()))
        self.status.setText(_("Clip entfernt – die Aufnahme bleibt, wie sie ist."))

    def set_start(self):
        """I: the clip under the playhead begins here (the earlier part of it goes)."""
        i, src = self._clip_at_playhead()
        if i is None:
            return
        self.parts = sequence.trim(self.parts, i, "start", src, self.info.duration)
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(sequence.starts(self.parts)[i])

    def set_end(self):
        i, src = self._clip_at_playhead()
        if i is None:
            return
        self.parts = sequence.trim(self.parts, i, "end", src, self.info.duration)
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(sequence.starts(self.parts)[i + 1])

    def _speed_picked(self, _i):
        i = self.timeline.selection
        if i is None or self._applying:
            return
        speed = float(self.speed_box.currentData() or 1.0)
        if abs(self.parts[i].speed - speed) < 1e-6:
            return
        self.parts = sequence.with_speed(self.parts, i, speed)
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(self.pos)

    def _select_speed(self, speed):
        i = self.speed_box.findData(speed)
        if i >= 0 and i != self.speed_box.currentIndex():
            self.speed_box.blockSignals(True)
            self.speed_box.setCurrentIndex(i)
            self.speed_box.blockSignals(False)

    def _timeline_edited(self, what, new_parts):
        self.parts = list(new_parts)
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(self.pos)

    def _clip_selected(self, i):
        if self._zoom_edit is not None and self._zoom_edit[0] != i:
            self._zoom_leave()                          # 1.19: the zoom frame belongs to the clip it was opened on
        self._inspector_refresh()

    def _timeline_pick(self, ident, t, i):
        if ident == "seek":
            self.goto(t)
        elif ident == "split":
            self.goto(t)
            self.split_at_playhead()
        elif ident == "delete" and i is not None:
            self.timeline.select(i)
            self.delete_selected()
        elif ident in ("start", "end") and i is not None:
            self.goto(t)
            self.set_start() if ident == "start" else self.set_end()
        elif ident == "speed" and i is not None:
            self.timeline.select(i)
            self.parts = sequence.with_speed(self.parts, i, float(t))
            self.timeline.set_parts(self.parts)
            self._commit()
        elif ident == "still":
            self.save_still(sequence.source_at(self.parts, t)[1])
        elif ident == "hold":                                    # 1.19
            self.goto(t)
            self.insert_hold()
        elif ident == "fx_clear" and i is not None:
            self._fx_clear(i)

    # ---- marks
    def _picked_mark(self):
        if not self.marks:
            return None
        row = self.mark_list.currentRow()
        if 0 <= row < len(self.marks):
            return self.marks[row]
        src = self._src_pos()
        return min(self.marks, key=lambda m: abs(m - src))

    def next_mark(self):
        src = self._src_pos()
        later = [m for m in self.marks if m > src + 0.05]
        if later or self.marks:
            self.goto_src(later[0] if later else self.marks[0])

    def clip_around_mark(self):
        m = self._picked_mark()
        if m is None:
            return
        self.parts = [clipedit.Part(max(0.0, m - MARK_BEFORE_S), min(self.info.duration, m + MARK_AFTER_S))]
        self.timeline.set_parts(self.parts)
        self._commit()
        self.goto(0.0)

    # ---- the plan
    def edit_plan(self) -> clipedit.Edit:
        """What will be saved: the clips in play order, crop, drawings (copies), fades."""
        frame = self.preview.crop if self._zoom_edit is None else self._crop_saved[0]   # 1.19: the zoom tool borrows it
        crop = frame if self.crop_box.currentData() != "none" else None
        shapes = [replace(s, pts=list(s.pts)) for s in self.preview.shapes if s.kind != "text" or s.text.strip()]
        return clipedit.Edit([replace(p) for p in self.parts], crop, shapes,
                             float(self.fade_in_box.currentData() or 0), float(self.fade_out_box.currentData() or 0),
                             self._short.copy() if self._short is not None else None)

    def _saving(self, on: bool):
        self.busy.setVisible(on)
        self.save_btn.setEnabled(not on and bool(self.parts))
        self.export_btn.setEnabled(self.save_btn.isEnabled())

    # ---- picture: crop (1.12) and black borders (1.12.6)
    def _content_found(self, box):
        """The recording has black borders around the game: the strip shows the game part, the crop „Ohne schwarze
        Ränder“ is offered and picked while no crop was chosen by hand."""
        super()._content_found(box)
        if self.crop_box.findData("content") < 0:
            self.crop_box.insertItem(1, _(CONTENT_LABEL), "content")
        self.content_hint.setVisible(True)
        if self.crop_box.currentData() == "none" and not self._crop_chosen:
            self._content_crop_auto = True
            try:
                self.crop_box.setCurrentIndex(self.crop_box.findData("content"))
            finally:
                self._content_crop_auto = False

    def _crop_picked(self, _i):
        key = self.crop_box.currentData()
        ratio = dict(clipedit.ASPECTS).get(key)
        if not self._content_crop_auto and not self._applying:
            self._crop_chosen = True
        self.preview.set_zoom_crop(key == "content")
        if key == "none":
            self.preview.set_crop(None)
            self.crop_btn.setChecked(False)
            self.preview.set_crop_edit(False)
        elif key == "content":
            self.crop_btn.setChecked(False)
            self.preview.set_crop_edit(False)
            self.preview.set_crop(self._content or (0.0, 0.0, 1.0, 1.0), None)
        else:
            base = self.preview.crop or (0.0, 0.0, 1.0, 1.0)
            box = imageedit.aspect_box(base if key == "free" else (0.0, 0.0, 1.0, 1.0), ratio,
                                       (self.info.width or 16, self.info.height or 9))
            self.preview.set_crop(box, ratio)
            self.crop_btn.setChecked(True)
            self.preview.set_crop_edit(True)
            if self.mode != "crop":
                self.mode_btns["crop"].setChecked(True)
        if self._content_crop_auto and self.history is not None and not self.history.can_undo():
            self.history = sequence.History(self._state())      # found borders are the starting point, no step
            self._baseline_moved()                              # 1.18.1: … and no change worth a project file
            self._refresh()
        else:
            self._commit()

    def _crop_tool(self):
        on = self.crop_btn.isChecked()
        if on and self.crop_box.currentData() == "none":
            self.crop_box.setCurrentIndex(self.crop_box.findData("free"))      # draws a full box, tool on
            return
        self.preview.set_crop_edit(on)
        if on and self.mode != "crop":
            self.mode_btns["crop"].setChecked(True)

    def _crop_moved(self):
        """The crop frame was drawn or moved by hand: „Ohne schwarze Ränder“ becomes „Frei“."""
        if self._zoom_edit is not None:                  # 1.19: the frame is the clip's zoom box just now
            self._zoom_moved()
            return
        if self.crop_box.currentData() == "content":
            self.crop_box.blockSignals(True)
            self.crop_box.setCurrentIndex(self.crop_box.findData("free"))
            self.crop_box.blockSignals(False)
            self._crop_chosen = True
            self.preview.set_zoom_crop(False)
        self._commit()

    # ---- drawings (1.12)
    def _draw_tool(self, kind, on):
        if on:
            self._last_draw = kind
            for k, b in self.draw_btns.items():
                if k != kind and b.isChecked():
                    b.setChecked(False)
            self.preview.set_shape_tool(kind)
            self.preview.pen["text"] = self.draw_text.text()
            if self.mode != "draw":
                self.mode_btns["draw"].setChecked(True)
        elif not any(b.isChecked() for b in self.draw_btns.values()):
            self.preview.set_shape_tool(None)

    def _draw_colour(self, colour):
        for c, b in self.colour_btns.items():
            b.setChecked(c == colour)
        self.preview.pen["colour"] = colour
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.colour = colour
            self.preview.replace_selected_shape(sel)

    def _draw_size(self, _i):
        i = int(self.draw_size_box.currentData() or 0)
        self.preview.pen["size"] = annotate.SIZES[i]
        self.preview.pen["text_size"] = annotate.TEXT_SIZES[i]
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.size = annotate.TEXT_SIZES[i] if sel.kind == "text" else annotate.SIZES[i]
            self.preview.replace_selected_shape(sel)

    def _times_from_here(self):
        dur = self.draw_when_box.currentData()
        t = self._src_pos()
        return (None, None) if dur is None else (t, min(self.info.duration or t + dur, t + float(dur)))

    def _draw_when(self, _i):
        sel = self.preview.selected_shape()
        if sel is not None:
            sel.t0, sel.t1 = self._times_from_here()
            self.preview.replace_selected_shape(sel)

    def _draw_text_edited(self, text):
        self.preview.pen["text"] = text
        sel = self.preview.selected_shape()
        if sel is not None and sel.kind == "text":
            sel.text = text or " "
            self._commit_key = ("text", self.preview.shape_sel)
            self.preview.replace_selected_shape(sel)

    def _draw_picked(self, i):
        sel = self.preview.selected_shape()
        if sel is not None and sel.kind == "text":
            self.draw_text.setText(sel.text)

    def _draw_remove(self):
        self.preview.remove_selected_shape()

    def _draw_clear(self):
        if self.preview.shapes:
            self.preview.set_shapes([])
            self.preview.shapes_changed.emit()

    def _shapes_changed(self):
        key, self._commit_key = self._commit_key, None
        self._commit(key)

    # ---- censoring (1.7.2)
    def _censor_toggled(self, on):
        self._censor_on = bool(on)
        self.preview.set_look(self._censor_on, self._censor_style)
        self._setting("clip_censor_on", self._censor_on)
        self._commit()

    def _censor_style_changed(self, _i):
        self._censor_style = self.style_box.currentData() or "pixel"
        self.preview.set_look(self._censor_on, self._censor_style)
        self._setting("clip_censor_style", self._censor_style)
        self._commit()

    def _tool_toggled(self):
        on = self.tool_btn.isChecked()
        self.preview.set_editing(on)
        if on and self.mode != "censor":
            self.mode_btns["censor"].setChecked(True)
        self._censor_hint()

    def _add_names_box(self):
        self.preview.add_box(clipedit.names_box(self.info.width, self.info.height))
        if not self.censor_box.isChecked():
            self.censor_box.setChecked(True)

    def _remove_box(self):
        if not self.preview.remove_selected() and self.preview.boxes:
            self.preview.selected = len(self.preview.boxes) - 1
            self.preview.remove_selected()

    def _clear_boxes(self):
        self.preview.clear_boxes()

    def _censor_hint(self):
        n = len(self.preview.boxes)
        if not n:
            text = _("Noch kein Kasten. „Namen links unten“ setzt einen auf die Survivor-Namen, „Kasten zeichnen“ "
                     "lässt dich einen aufziehen.")
        elif self.preview.editing:
            text = _("{n} Kasten/Kästen – ziehen = verschieben, Ecke rechts unten = Grösse, Klick = markieren.", n=n)
        else:
            text = _("{n} Kasten/Kästen gemerkt – sie gelten auch für den nächsten Clip.", n=n)
        self.censor_hint.setText(text)
        self.remove_btn.setEnabled(n > 0)
        self.clear_btn.setEnabled(n > 0)

    # ---- projects (1.16)
    def _project_extra(self) -> dict:
        name = self.name_edit.text() if self.name_edit.isModified() else ""     # 1.18.1: the derived name is no work
        return {"name": name, "mode": self.mode_box.currentData(), "target_mb": self._target_mb,
                "gif_h": int(self.gif_box.currentData() or clipedit.DEFAULT_GIF_H),
                "encoding": {"codec": self._encoding.codec, "quality": self._encoding.quality,
                             "height": int(self._encoding.height), "hw": self._encoding.hw},
                "mix_on": dict(self._mix_on), "mix_vol": dict(self._mix_vol)}

    def _apply_project_extra(self, extra: dict):
        name = str(extra.get("name") or "")
        if name:
            self.name_edit.setText(name)
            self.name_edit.setModified(True)
        mode = extra.get("mode")
        if mode in clipedit.MODES:
            self.mode_box.setCurrentIndex(self.mode_box.findData(mode))
        if extra.get("target_mb") in clipedit.TARGETS_MB:
            self.target_box.setCurrentIndex(self.target_box.findData(int(extra["target_mb"])))
        if extra.get("gif_h") in clipedit.GIF_HEIGHTS:
            self.gif_box.setCurrentIndex(self.gif_box.findData(int(extra["gif_h"])))
        enc = extra.get("encoding") if isinstance(extra.get("encoding"), dict) else None
        if enc:
            from . import encoders
            try:
                self._encoding = encoders.Encoding(str(enc.get("codec") or "h264"), str(enc.get("quality") or "balanced"),
                                                   int(enc.get("height") or 0), str(enc.get("hw") if enc.get("hw") is not None else "auto"))
                self._encoding_fill()
            except (TypeError, ValueError):
                pass
        for key, store in (("mix_on", self._mix_on), ("mix_vol", self._mix_vol)):
            val = extra.get(key)
            if isinstance(val, dict):
                for k in obsrec.SOURCES:
                    if k in val:
                        store[k] = bool(val[k]) if key == "mix_on" else int(val[k] or 0)
        self._mix_fill()

    # ---- keys and closing
    def toggle_help(self):
        """1.17.1: ? – the key help over the window (KeyHelp, made from SHORTCUTS)."""
        if getattr(self, "key_help", None) is None:
            self.key_help = KeyHelp(self)
        self.key_help.toggle()

    def keyPressEvent(self, e):
        k, mods = e.key(), e.modifiers()
        big, frame = bool(mods & Qt.ShiftModifier), bool(mods & Qt.ControlModifier)
        help_on = getattr(self, "key_help", None) is not None and not self.key_help.isHidden()
        if k in EDIT_KEYS and self._edit_locked():
            e.accept()                                     # 1.18.1: the recording is checked (editorproject)
        elif k == Qt.Key_Question or e.text() == "?":
            self.toggle_help()
        elif k == Qt.Key_Escape and help_on:
            self.key_help.hide()
        elif k == Qt.Key_Space:
            self.toggle_play()
        elif k == Qt.Key_Left:
            self.step_frame(-1) if frame else self.step(-(STEP_BIG if big else STEP_SMALL))
        elif k == Qt.Key_Right:
            self.step_frame(1) if frame else self.step(STEP_BIG if big else STEP_SMALL)
        elif k in (Qt.Key_Comma, Qt.Key_Period):          # 1.17: one frame back / on, as in most players
            self.step_frame(-1 if k == Qt.Key_Comma else 1)
        elif k == Qt.Key_I:
            self.set_start()
        elif k == Qt.Key_O:
            self.set_end()
        elif k == Qt.Key_M:
            self.next_mark()
        elif k == Qt.Key_S and not frame:
            self.split_at_playhead()
        elif k == Qt.Key_P and not frame:                         # 1.19: a still at the playhead
            self.insert_hold()
        elif k == Qt.Key_Home:
            self.goto(0.0)
        elif k == Qt.Key_End:
            self.goto(self.timeline.total())
        elif k == Qt.Key_F:
            self.toggle_fullscreen()
        elif k == Qt.Key_V:
            self.mode_btns["select"].setChecked(True)
        elif k == Qt.Key_C and not frame:
            self.mode_btns["crop"].setChecked(True)
        elif k == Qt.Key_D:
            self.mode_btns["draw"].setChecked(True)
        elif k == Qt.Key_X:
            self.mode_btns["censor"].setChecked(True)
        elif k in (Qt.Key_Plus, Qt.Key_Equal):
            self.timeline.zoom_in()
        elif k in (Qt.Key_Minus, Qt.Key_Underscore):
            self.timeline.zoom_out()
        elif k in (Qt.Key_Delete, Qt.Key_Backspace):
            if self.preview.shape_tool and self.preview.selected_shape():
                self.preview.remove_selected_shape()                # 1.12: a drawing
            elif self.preview.editing and self.preview.selected is not None:
                self.preview.remove_selected()
            else:
                self.delete_selected()
        elif k == Qt.Key_Escape:
            self._escape()
        else:
            super().keyPressEvent(e)

    def _escape(self):
        """1.18 (user: „Esc darf den Editor nie schliessen“): one step per press – the focus leaves a text field, else
        a drag under way is cancelled (nothing of it stays, no undo step), else the tool goes back to select, else the
        selection goes, else the full screen ends. Nothing closes the window but × and Strg+W."""
        fw = QApplication.focusWidget()
        if isinstance(fw, (QLineEdit, QAbstractSpinBox)) and self.isAncestorOf(fw):
            fw.clearFocus()
            self.setFocus()
            return
        if self.preview.cancel_gesture():
            self.status.setText(_("Abgebrochen."))
            return
        if self.timeline.cancel_gesture():
            self.goto(self.pos)                                  # a trim showed its edge: back to the playhead
            self.status.setText(_("Abgebrochen."))
            return
        if self._zoom_leave():                                   # 1.19: the zoom frame counts as a tool
            return
        if self.mode != "select":
            self.mode_btns["select"].setChecked(True)
            return
        if self._clear_selection():
            return
        if self._fullscreen is not None:
            self.toggle_fullscreen()
            return
        if not getattr(self, "_esc_hinted", False):
            self._esc_hinted = True
            self.status.setText(_("Esc schliesst den Editor nicht – schliessen mit × oder Strg+W."))

    def _clear_selection(self) -> bool:
        """1.18: the marked clip, drawing, censor box and mark are unmarked; False when nothing was marked."""
        done = False
        if self.timeline.selection is not None:
            self.timeline.select(None)
            done = True
        pv = self.preview
        if pv.selected is not None:
            pv.selected = None
            pv.update()
            done = True
        if pv.shape_sel is not None:
            pv.shape_sel = None
            pv.update()
            pv.shape_picked.emit(-1)
            done = True
        if self.mark_list.currentRow() >= 0 or self.mark_list.selectedItems():
            self.mark_list.clearSelection()
            self.mark_list.setCurrentRow(-1)
            done = True
        return done

    def closeEvent(self, e):
        if not self._project_close_ok():                 # 1.18.1: the notice bar asks first (never a modal dialog)
            e.ignore()
            return
        self._project_release()
        self._layout_save()
        lib = getattr(self, "library", None)
        if lib is not None:
            lib.loader.stop()
            lib.model.thumbs.clear()
            lib.model.set_items([])
        super().closeEvent(e)

