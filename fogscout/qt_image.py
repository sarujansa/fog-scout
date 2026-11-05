"""The screenshot editor window (1.12, user: "ein gutes Bearbeitungstool für Videos und Screenshots die ich mit F12
mache" – crop & rotate, draw & text, censor & colour, share). The picture comes from Steam's screenshot folder
(steamshots, read only) or Fog Scout's own stills; the edit lives in an imageedit.ImageEdit and is applied to the
untouched original, saved as a new file in Fog Scout's folder (never over the source). Undo/redo per step, copy to
the clipboard for Discord.

The canvas is the clip editor's PreviewView: it draws the censor boxes, the drawings and the crop box over the
turned and colour-adjusted picture exactly as imageedit.render will."""
from __future__ import annotations

import logging
import os
import threading

from PIL import Image
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication, QImage, QKeySequence, QShortcut
from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QTabWidget,
                               QVBoxLayout, QWidget)

from . import annotate, askclaude, hudnames, imageclaude, imageedit, launch, qt_theme
from .i18n import N_, _
from .qt_clip import DRAW_TOOLS, SIZE_LABELS, PreviewView
from .qt_common import Bridge, PlainLabel, guard_wheel
from .qt_layouts import FlowRow

CENSOR_LABELS = {"pixel": N_("Verpixelt"), "blur": N_("Verwischt"), "black": N_("Schwarz")}
CROP_LABELS = {"none": N_("Kein Ausschnitt"), "free": N_("Frei"), "16:9": "16:9", "9:16": N_("9:16 (Hochformat)"),
               "1:1": "1:1", "4:3": "4:3", "4:5": "4:5"}
ADJUSTS = (("brightness", N_("Helligkeit")), ("contrast", N_("Kontrast")), ("saturation", N_("Sättigung")))
UNDO_KEPT = 60                     # steps that can be undone
ADJUST_DELAY_MS = 120              # a slider redraws the picture this long after it stopped
PREVIEW_MAX = 1920                 # the canvas shows a copy at most this long (px) – saving uses the original
SAVE_POLL_MS = 50                  # how often the window looks whether the saving thread is done
CLAUDE_POLL_MS = 50                # 1.38.3: how often the window looks for Claude's answer while one is due
RATIO_SAME = 0.005                 # a crop whose pixel aspect is this close to an offered ratio counts as it

# Running saves: window -> the file it writes. Holds a window closed meanwhile until its save is picked up (the App
# drops closed windows; the result still reaches on_saved), and keeps a second editor of the same picture from
# picking the same free name before the first copy exists (code review 35/48). Only the window thread touches it.
_SAVING = {}


def qimage(img: Image.Image) -> QImage:
    img = img.convert("RGB")
    w, h = img.size
    return QImage(img.tobytes(), w, h, w * 3, QImage.Format_RGB888).copy()


class _ClaudeBridge(Bridge):
    """1.35: Claude's answer from the asking thread into the window's thread. 1.38.3: was a QObject with a signal –
    the thread (up to a minute for a picture) emitted on it after the window had been closed and freed; now a plain
    queue the window's own timer drains (qt_common.Bridge, as the clip editor since 1.8.66)."""
    NAMES = ("answer",)
    LABEL = "Bild-Editor"


class ImageWindow(QWidget):
    """One editor per picture. ``out_dir`` = where edited copies go, ``on_saved(path)``/``log(text, kind)`` from
    the App."""

    def __init__(self, path: str, out_dir: str, on_saved=None, log=None, dark=True, qss: str = "", parent=None):
        super().__init__(parent, Qt.Window)
        self.path, self.out_dir = path, out_dir
        self.on_saved, self.log = on_saved, (log or (lambda text, kind="System": None))
        self.dark = dark
        self.setObjectName("page")
        self.setWindowTitle(_("Bild bearbeiten – {name}", name=os.path.basename(path)))
        if qss:
            self.setStyleSheet(qss)
        try:
            with Image.open(path) as im:
                self.original = imageedit.converted(im, "RGB")   # 16-bit grey scaled, not clipped
        except (OSError, ValueError, Image.DecompressionBombError) as e:   # the last: > 2× MAX_IMAGE_PIXELS
            self.original = None
            self.error = str(e)
        else:
            self.error = ""
        self.preview = self._preview_copy(self.original)
        self.edit = imageedit.ImageEdit()
        self.undo_stack, self.redo_stack = [], []
        self._step = None                  # what the last undo step was for while it may go on: "slider", ("text", i)
        self._next_step = None             # what the canvas change under way continues (typing into a text)
        self._crop_pick = None             # the aspect the user last picked other than "none" (free or a ratio)
        self.last_out = None
        self._adjust_timer = QTimer(self)
        self._adjust_timer.setSingleShot(True)
        self._adjust_timer.setInterval(ADJUST_DELAY_MS)
        self._adjust_timer.timeout.connect(self._adjust_apply)
        self._saver, self._save_done = None, {}
        self._save_timer = QTimer(self)
        self._save_timer.setInterval(SAVE_POLL_MS)
        self._save_timer.timeout.connect(self._save_poll)
        self.claude_key = lambda: ""       # 1.35: set by the App – the key while „Bilder an Claude“ is on, else ""
        self._claude_seq, self._claude_base, self._claude_result, self._claude_busy = 0, None, None, False
        self._claude_bridge = _ClaudeBridge()
        self._claude_bridge.answer.connect(self._claude_answer)
        self._claude_pump = QTimer(self)                   # runs only while an answer is due; dies with the window
        self._claude_pump.setInterval(CLAUDE_POLL_MS)
        self._claude_pump.timeout.connect(self._claude_drain)
        self._closed = False
        self._build()
        self.resize(1280, 860)
        self.setMinimumSize(900, 620)
        self.setFocusPolicy(Qt.StrongFocus)     # a click on the picture takes the keys back from a text field
        if self.original is None:
            self.status.setText(_("Bild nicht lesbar: {error}", error=self.error))
            for b in (self.save_btn, self.copy_btn, self.tools):
                b.setEnabled(False)
            return
        self._refresh(frame=True)

    # ---- building
    def _btn(self, row, text, slot, tip="", check=False):
        b = QPushButton(text)
        b.setFocusPolicy(Qt.NoFocus)
        b.clicked.connect(slot)
        if tip:
            b.setToolTip(tip)
        if check:
            b.setCheckable(True)
            b.setProperty("class", "seg")
        row.addWidget(b)
        return b

    def _combo(self, row, items, current, tip, slot, chosen=False):
        """``chosen``: ``slot`` on every pick of the user, also of the entry already shown (``activated``)."""
        box = guard_wheel(QComboBox())
        for data, label in items:
            box.addItem(label, data)
        box.setCurrentIndex(next((i for i, (d, _l) in enumerate(items) if d == current), 0))
        box.setToolTip(tip)
        (box.activated if chosen else box.currentIndexChanged).connect(slot)
        row.addWidget(box)
        return box

    @staticmethod
    def _page():
        page = QFrame()
        page.setProperty("class", "card")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(*qt_theme.PAD_CARD)
        lay.setSpacing(8)
        return page, lay

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(12)
        left = QVBoxLayout()
        self.canvas = PreviewView(self.dark)
        self.canvas.setMinimumSize(560, 315)
        self.canvas.set_look(True, "pixel")
        self.canvas.boxes_changed.connect(self._canvas_changed)
        self.canvas.crop_changed.connect(self._canvas_changed)
        self.canvas.shapes_changed.connect(self._canvas_changed)
        self.canvas.shape_picked.connect(self._shape_picked)
        left.addWidget(self.canvas, 1)
        self.size_label = QLabel("")
        self.size_label.setProperty("class", "dim")
        left.addWidget(self.size_label)
        lay.addLayout(left, 1)

        side = QVBoxLayout()
        side.setSpacing(10)
        self.tools = QTabWidget()
        self.tools.addTab(self._crop_page(), _("Zuschneiden"))
        self.tools.addTab(self._draw_page(), _("Zeichnen"))
        self.tools.addTab(self._censor_page(), _("Zensieren"))
        self.tools.addTab(self._colour_page(), _("Farbe"))
        self.tools.addTab(self._claude_page(), _("Claude"))
        self.tools.currentChanged.connect(self._tab_changed)
        side.addWidget(self.tools)
        side.addStretch()
        ur = QHBoxLayout()
        self.undo_btn = self._btn(ur, _("↶ Rückgängig"), self.undo, _("Letzten Schritt zurücknehmen (Strg+Z)."))
        self.redo_btn = self._btn(ur, _("↷ Wiederholen"), self.redo, _("Zurückgenommenen Schritt wiederholen (Strg+Y)."))
        self.reset_btn = self._btn(ur, _("Alles zurücksetzen"), self.reset_all,
                                   _("Verwirft alle Änderungen – das Original bleibt ohnehin unverändert."))
        ur.addStretch()
        side.addLayout(ur)
        out, ol = self._page()
        head = QLabel(_("Speichern").upper())
        head.setProperty("class", "sub")
        ol.addWidget(head)
        nr = QHBoxLayout()
        self.name_edit = QLineEdit(os.path.splitext(imageedit.out_name(self.path))[0])
        nr.addWidget(self.name_edit, 1)
        self.fmt_box = self._combo(nr, [("png", "PNG"), ("jpg", "JPG")], "png",
                                   _("PNG: verlustfrei · JPG: kleinere Datei."), lambda _i: None)
        ol.addLayout(nr)
        sr = FlowRow(spacing=6)
        self.save_btn = self._btn(sr, _("Bild speichern"), self.save,
                                  _("Speichert eine bearbeitete Kopie in Fog Scouts Ordner – das Original (z. B. im "
                                    "Screenshot-Ordner von Steam) bleibt unverändert (Strg+S)."))
        self.save_btn.setObjectName("primary")
        self.copy_btn = self._btn(sr, _("In Zwischenablage"), self.copy,
                                  _("Kopiert das bearbeitete Bild – in Discord mit Strg+V einfügen (Strg+C)."))
        self.show_btn = self._btn(sr, _("Im Explorer zeigen"), self._show_saved,
                                  _("Zeigt das zuletzt gespeicherte Bild im Explorer."))
        self.show_btn.setEnabled(False)
        ol.addLayout(sr)
        self.status = QLabel("")
        self.status.setProperty("class", "dim")
        self.status.setWordWrap(True)
        ol.addWidget(self.status)
        side.addWidget(out)
        hint = QLabel(_("Strg+Z rückgängig · Strg+Y wiederholen · Strg+C kopieren · Strg+S speichern · Entf "
                        "Markiertes löschen · Esc schliessen"))
        hint.setProperty("class", "dim")
        hint.setWordWrap(True)
        side.addWidget(hint)
        wrap = QWidget()
        wrap.setLayout(side)
        wrap.setFixedWidth(430)
        lay.addWidget(wrap)
        for std, extra, slot in ((QKeySequence.Undo, (), self.undo), (QKeySequence.Redo, ("Ctrl+Y",), self.redo),
                                 (QKeySequence.Copy, (), self.copy), (QKeySequence.Save, (), self.save)):
            # every key of the platform plus Ctrl+Y, each once: two shortcuts on one key are ambiguous to Qt and
            # neither fires (QKeySequence.Redo is Ctrl+Y on Windows – Ctrl+Y did nothing, code review 12)
            keys = QKeySequence.keyBindings(std)
            keys += [QKeySequence(k) for k in extra if QKeySequence(k) not in keys]
            sc = QShortcut(self)
            sc.setKeys(keys)
            sc.activated.connect(slot)
        self._show_buttons()

    def _crop_page(self):
        page, pl = self._page()
        r = QHBoxLayout()
        r.addWidget(QLabel(_("Ausschnitt")))
        self.crop_box = self._combo(r, [(k, _(v) if k in ("none", "free", "9:16") else v)
                                        for k, v in CROP_LABELS.items()], "none",
                                    _("Seitenverhältnis des Ausschnitts; den Rahmen im Bild verschieben und an den "
                                      "Ecken ziehen."), self._crop_picked)
        r.addStretch()
        pl.addLayout(r)
        r = QHBoxLayout()
        self.crop_btn = self._btn(r, _("Rahmen bearbeiten"), self._crop_tool,
                                  _("Rahmen im Bild ziehen, verschieben, an den Ecken ändern."), check=True)
        r.addStretch()
        pl.addLayout(r)
        # slots are bound methods, never lambdas or partials holding self: PySide keeps those as long as the button,
        # the button lives as long as the window – a cycle through C++ the GC cannot see, so a closed editor kept
        # its full-size picture until Fog Scout quit (code review 11). Bound methods are held weakly.
        r = QHBoxLayout()
        self._btn(r, _("⟲ Links drehen"), self._turn_left, _("Um 90° gegen den Uhrzeigersinn drehen."))
        self._btn(r, _("⟳ Rechts drehen"), self._turn_right, _("Um 90° im Uhrzeigersinn drehen."))
        r.addStretch()
        pl.addLayout(r)
        r = QHBoxLayout()
        self._btn(r, _("⇆ Spiegeln"), self._mirror, _("Links und rechts tauschen."))
        self._btn(r, _("⇅ Kippen"), self._tip_over, _("Oben und unten tauschen."))
        r.addStretch()
        pl.addLayout(r)
        return page

    def _draw_page(self):
        page, pl = self._page()
        r = FlowRow(spacing=6)                    # six tools: they wrap in the narrow side column
        self.draw_btns = {}
        for kind, label in DRAW_TOOLS:
            self.draw_btns[kind] = self._btn(r, _(label), self._draw_tool_clicked,
                                             _("Im Bild ziehen (Text: klicken). Eine Zeichnung anklicken markiert "
                                               "sie, ziehen verschiebt sie, Entf löscht sie."), check=True)
        pl.addLayout(r)
        r = QHBoxLayout()
        self.colour_btns = {}
        for colour in annotate.COLOURS:
            b = QPushButton("")
            b.setFixedSize(24, 24)
            b.setFocusPolicy(Qt.NoFocus)
            b.setCheckable(True)
            b.setToolTip(_("Farbe"))
            c = qt_theme.colours(qt_theme.current_dark())             # 1.22.3: the ring was white on white
            b.setStyleSheet(f"QPushButton {{ background: {colour}; border: 2px solid {c['border']}; border-radius: 4px; }}"
                            f"QPushButton:checked {{ border: 2px solid {c['head']}; }}")
            b.clicked.connect(self._colour_clicked)
            r.addWidget(b)
            self.colour_btns[colour] = b
        self.colour_btns[annotate.COLOURS[0]].setChecked(True)
        self.draw_size_box = self._combo(r, list(enumerate(_(x) for x in SIZE_LABELS)), 1,
                                         _("Strichstärke bzw. Textgrösse."), self._draw_size, chosen=True)
        r.addStretch()
        pl.addLayout(r)
        r = QHBoxLayout()
        self.draw_text = QLineEdit()
        self.draw_text.setPlaceholderText(_("Text für das Text-Werkzeug"))
        self.draw_text.textEdited.connect(self._draw_text_edited)
        self.draw_text.editingFinished.connect(self._typing_done)
        self.draw_text.returnPressed.connect(self.setFocus)     # Enter: done typing, the keys go to the editor
        r.addWidget(self.draw_text, 1)
        pl.addLayout(r)
        r = QHBoxLayout()
        self._btn(r, _("Zeichnung entfernen"), self._draw_remove, _("Entfernt die markierte Zeichnung (Entf)."))
        self._btn(r, _("Alle Zeichnungen entfernen"), self._draw_clear, "")
        r.addStretch()
        pl.addLayout(r)
        return page

    def _censor_page(self):
        page, pl = self._page()
        r = QHBoxLayout()
        self.censor_tool = self._btn(r, _("Kasten zeichnen"), self._censor_toggle,
                                     _("Im Bild einen Bereich aufziehen, der unkenntlich wird – Namen, Chat, "
                                       "Freundesliste. Kästen lassen sich verschieben und an der Ecke rechts unten "
                                       "vergrössern."), check=True)
        self.censor_style = self._combo(r, [(k, _(v)) for k, v in CENSOR_LABELS.items()], "pixel",
                                        _("Wie der Bereich unkenntlich wird."), self._censor_style_changed)
        r.addStretch()
        pl.addLayout(r)
        r = FlowRow(spacing=6)                    # 1.38: the HUD's name places (hudnames), no Claude
        self._btn(r, _("Namen links unten"), self._names_match,
                  _("Setzt einen Kasten dorthin, wo DBD im Match die Namen der Survivor zeigt (links unten im "
                    "Spielbild) – bei Bedarf verschieben."))
        self._btn(r, _("Namen beim Zuschauen"), self._names_spectate,
                  _("Setzt Kästen auf die Namen, wie DBD sie beim Zuschauen zeigt: die Liste links weiter oben und "
                    "den Namen oben in der Mitte – bei Bedarf verschieben."))
        pl.addLayout(r)
        r = QHBoxLayout()
        self._btn(r, _("Kasten entfernen"), self._censor_remove, _("Entfernt den markierten Kasten (Entf)."))
        self._btn(r, _("Alle entfernen"), self._censor_clear, "")
        r.addStretch()
        pl.addLayout(r)
        pl.addStretch()                           # 1.38: spare height below the rows, not between them
        return page

    def _colour_page(self):
        page, pl = self._page()
        self.sliders = {}
        for key, label in ADJUSTS:
            r = QHBoxLayout()
            name = QLabel(_(label))
            name.setMinimumWidth(90)
            r.addWidget(name)
            sl = guard_wheel(QSlider(Qt.Horizontal))
            sl.setRange(int(imageedit.ADJUST_RANGE[0] * 100), int(imageedit.ADJUST_RANGE[1] * 100))
            sl.setValue(100)
            sl.setToolTip(_("100 % = unverändert."))
            val = QLabel("100 %")
            val.setMinimumWidth(48)
            sl.valueChanged.connect(self._slider_moved)
            r.addWidget(sl, 1)
            r.addWidget(val)
            pl.addLayout(r)
            self.sliders[key] = (sl, val)
        r = QHBoxLayout()
        self._btn(r, _("Farbe zurücksetzen"), self._colour_reset, _("Helligkeit, Kontrast und Sättigung auf 100 %."))
        r.addStretch()
        pl.addLayout(r)
        return page

    def _claude_page(self):
        """1.35: „Mit Claude bearbeiten“ – the wish and the picture go to Claude only on „Vorschlagen“."""
        page, pl = self._page()
        self.cl_field = QLineEdit()
        self.cl_field.setPlaceholderText(_("z. B. Spielernamen verpixeln, auf 16:9 zuschneiden, etwas heller"))
        self.cl_field.setMaxLength(imageclaude.MAX_REQUEST)
        self.cl_field.returnPressed.connect(self.claude_ask)
        pl.addWidget(self.cl_field)
        r = QHBoxLayout()
        self.cl_ask_btn = self._btn(r, _("Vorschlagen"), self.claude_ask,
                                    _("Schickt deine Bitte und das Bild, wie es hier zu sehen ist (bereits zensierte "
                                      "Bereiche bleiben zensiert), an Claude; nichts wird geändert, bevor du "
                                      "übernimmst."))
        r.addStretch()
        pl.addLayout(r)
        self.cl_status = PlainLabel("", "dim")
        pl.addWidget(self.cl_status)
        self.cl_list = PlainLabel("")
        self.cl_list.hide()
        pl.addWidget(self.cl_list)
        r = QHBoxLayout()
        self.cl_take_btn = self._btn(r, _("Übernehmen"), self.claude_take,
                                     _("Führt die vorgeschlagenen Schritte aus – ein Schritt zum Rückgängigmachen "
                                       "(Strg+Z)."))
        self.cl_take_btn.setObjectName("primary")
        self.cl_drop_btn = self._btn(r, _("Verwerfen"), self.claude_drop,
                                     _("Vergisst den Vorschlag; das Bild bleibt, wie es ist."))
        r.addStretch()
        pl.addLayout(r)
        hint = PlainLabel(_("Das Bild kann Spielernamen zeigen – es geht nur auf Klick an Claude "
                            "(api.anthropic.com), verkleinert und nur im Speicher."), "dim")
        pl.addWidget(hint)
        self._claude_buttons(False)
        return page

    def _claude_buttons(self, shown: bool):
        for b in (self.cl_take_btn, self.cl_drop_btn):
            b.setVisible(shown)

    def _claude_refresh(self):
        """Field and button follow the permission (the App may switch it while the window is open)."""
        on = bool(self.claude_key()) and self.original is not None
        self.cl_field.setEnabled(on)
        self.cl_ask_btn.setEnabled(on and not self._claude_busy)
        if not on and self._claude_result is None and not self._claude_busy:
            self.cl_status.setText(_("Aus – in Einstellungen → Verbindungen → Claude „Bilder im Bild-Editor an "
                                     "Claude schicken“ einschalten und einen API-Key eintragen."))
            self._claude_off_shown = True
        elif on and getattr(self, "_claude_off_shown", False):
            self._claude_off_shown = False
            self.cl_status.setText("")

    def claude_ask(self):
        if self._claude_busy or self.original is None:
            return
        key = self.claude_key()
        wish = self.cl_field.text().strip()
        if not key or not wish:
            self._claude_refresh()
            return
        try:
            block = askclaude.image_block(imageclaude.picture(self.original, self.edit))
        except (ValueError, OSError):
            self.cl_status.setText(_("Das Bild lässt sich nicht für Claude verkleinern."))
            return
        self._claude_seq += 1
        seq, base, size = self._claude_seq, self.edit.copy(), self._turned_size()
        self._claude_base, self._claude_result, self._claude_busy = base, None, True
        self.cl_ask_btn.setEnabled(False)
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Claude denkt nach …"))
        emit, text = self._claude_bridge.answer.emit, imageclaude.content(wish)

        def work():
            try:
                emit((seq, base, size, askclaude.request(key, imageclaude.SYSTEM, text, imageclaude.SCHEMA,
                                                         images=[block]), None))
            except askclaude.AskError as e:
                emit((seq, base, size, None, e.kind))
            except Exception as e:                       # only the kind – never the wish, the picture or the key
                logging.getLogger(__name__).warning("Claude im Bild-Editor: unerwarteter Fehler %s",
                                                    e.__class__.__name__)
                emit((seq, base, size, None, "bad"))
        threading.Thread(target=work, name="claude-image", daemon=True).start()
        self._claude_pump.start()

    def _claude_drain(self):
        if self._closed:
            self._claude_pump.stop()
            self._claude_bridge.clear()
            return
        self._claude_bridge.drain()
        if not self._claude_busy and not self._claude_bridge.pending():
            self._claude_pump.stop()

    def _claude_answer(self, item):
        seq, base, size, data, error = item
        if self._closed or seq != self._claude_seq:
            return
        self._claude_busy = False
        try:
            self._claude_show(base, size, data, error)
        except Exception:                                # never left on „Claude denkt nach …“
            self._claude_result = None
            self._claude_buttons(False)
            self.cl_status.setText(askclaude.error_text("bad"))
        finally:
            self._claude_refresh()

    def _claude_show(self, base, size, data, error):
        if error is not None:
            self.cl_status.setText(askclaude.error_text(error))
            return
        if self.edit != base:
            self.cl_status.setText(_("Das Bild hat sich inzwischen geändert – bitte neu vorschlagen."))
            return
        try:
            new, done, skipped = imageclaude.apply(base, data.get("ops"), size)
        except ValueError:
            self.cl_list.hide()
            self.cl_status.setText(askclaude.error_text("bad"))
            return
        summary = " ".join(str(data.get("summary") or "").split())[:300]
        lines = ["• " + _(w, **kw) for _op, (w, kw) in done]
        lines += ["– " + _("übersprungen: {why}", why=_(w, **kw)) for _op, (w, kw) in skipped]
        self.cl_list.setText("\n".join(lines))
        self.cl_list.setVisible(bool(lines))
        if not done or new == base:
            self.cl_status.setText(summary or _("Claude hat keinen passenden Schritt gefunden."))
            return
        self._claude_result = new
        self.cl_status.setText(summary)
        self._claude_buttons(True)

    def claude_take(self):
        new, base = self._claude_result, self._claude_base
        if new is None:
            return
        if self.edit != base:
            self.claude_drop()
            self.cl_status.setText(_("Das Bild hat sich inzwischen geändert – bitte neu vorschlagen."))
            return
        self._snapshot()                                 # one step back with Ctrl+Z
        self.edit = new.copy()
        self._step = None
        self._sync_crop_box()
        self._refresh(frame=True)
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText(_("Übernommen – Strg+Z macht es rückgängig."))

    def claude_drop(self):
        self._claude_result = None
        self._claude_buttons(False)
        self.cl_list.hide()
        self.cl_status.setText("")

    # ---- state
    def _snapshot(self, step=None):
        """Before a change: the edit as it was, for undo. ``step``: what the change was, while more of the same
        (moving a slider on, typing on into the same text) belongs to this one undo step."""
        self.undo_stack.append(self.edit.copy())
        del self.undo_stack[:-UNDO_KEPT]
        self.redo_stack.clear()
        self._step = step
        self._show_buttons()

    def _show_buttons(self):
        self.undo_btn.setEnabled(bool(self.undo_stack))
        self.redo_btn.setEnabled(bool(self.redo_stack))
        self.reset_btn.setEnabled(self.edit.changed() or bool(self.undo_stack))

    def _canvas_changed(self):
        """The canvas changed boxes, crop or drawings – into the edit (one undo step)."""
        new = self.edit.copy()
        new.censor = [tuple(b) for b in self.canvas.boxes]
        new.crop = tuple(self.canvas.crop) if self.canvas.crop and self.crop_box.currentData() != "none" else None
        new.shapes = [annotate.Shape(s.kind, list(s.pts), s.colour, s.size, s.text) for s in self.canvas.shapes]
        if new != self.edit:
            if self._next_step is None or self._next_step != self._step:
                self._snapshot(self._next_step)
            self.edit = new
            self._show_size()
            self._show_buttons()

    def _refresh(self, frame=False):
        """Canvas from the edit: the turned, colour-adjusted picture (``frame``) and the boxes, drawings, crop."""
        if self.original is None:
            return
        if frame:
            pic = imageedit.adjust(imageedit.base(self.preview, self.edit), self.edit.brightness,
                                   self.edit.contrast, self.edit.saturation)
            self.canvas.source_size = self._turned_size()
            self.canvas.set_frame(qimage(pic))
        self.canvas.set_boxes([list(b) for b in self.edit.censor])
        self.canvas.set_look(True, self.edit.censor_style)
        i = self.censor_style.findData(self.edit.censor_style)      # undo/reset: the box says what is saved
        if i >= 0 and i != self.censor_style.currentIndex():
            self.censor_style.blockSignals(True)
            self.censor_style.setCurrentIndex(i)
            self.censor_style.blockSignals(False)
        self.canvas.set_shapes([annotate.Shape(s.kind, list(s.pts), s.colour, s.size, s.text)
                                for s in self.edit.shapes])
        ratio = dict(imageedit.ASPECTS).get(self.crop_box.currentData())
        self.canvas.set_crop(self.edit.crop, ratio)
        for key, (sl, val) in self.sliders.items():
            v = int(round(getattr(self.edit, key) * 100))
            if sl.value() != v:
                sl.blockSignals(True)
                sl.setValue(v)
                sl.blockSignals(False)
            val.setText(f"{v} %")
        self._show_size()
        self._show_buttons()

    @staticmethod
    def _preview_copy(img):
        """What the canvas turns and colours on every change: a 3440×1440 screenshot cost ~25 ms more per step
        than a copy at ``PREVIEW_MAX`` – the canvas is never that large anyway."""
        if img is None or max(img.size) <= PREVIEW_MAX:
            return img
        small = img.copy()
        small.thumbnail((PREVIEW_MAX, PREVIEW_MAX), Image.LANCZOS)
        return small

    def _turned_size(self) -> tuple:
        w, h = self.original.size
        return (h, w) if self.edit.rotate % 2 else (w, h)

    def _show_size(self):
        if self.original is None:
            return
        w, h = self._turned_size()
        if self.edit.crop:
            x0, y0, x1, y1 = imageedit.box_px(self.edit.crop, (w, h))
            w, h = x1 - x0, y1 - y0
        self.size_label.setText(_("{w} × {h} Pixel · Original bleibt unverändert", w=w, h=h))

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append(self.edit.copy())
        self.edit = self.undo_stack.pop()
        self._step = None                  # a slider moved or text typed next is a step of its own (code review 42)
        self._sync_crop_box()
        self._refresh(frame=True)

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append(self.edit.copy())
        self.edit = self.redo_stack.pop()
        self._step = None
        self._sync_crop_box()
        self._refresh(frame=True)

    def reset_all(self):
        if self.edit.changed():
            self._snapshot()
        self.edit = imageedit.ImageEdit()
        self._step = None
        self._sync_crop_box()
        self._refresh(frame=True)

    def _sync_crop_box(self):
        """The aspect choice follows an undo/redo/turn: none without a crop, else the ratio shown if the crop still
        has it, else the user's last pick – free fits any crop –, else the offered ratio the crop has (a quarter turn
        makes 16:9 9:16), else free. The canvas locks a corner drag to it, so a stale ratio made the crop jump (code
        review 34); a ratio the user never picked must not lock it either – a free crop of a 16:9 picture starts as
        exactly 16:9."""
        cur = self.crop_box.currentData()
        if self.edit.crop is None:
            key = "none"
        else:
            w, h = self._turned_size()
            aspect = (self.edit.crop[2] * w) / max(1e-9, self.edit.crop[3] * h)
            ratios = dict(imageedit.ASPECTS)
            shown = (cur,) if ratios.get(cur) else ()          # free/none shown may be this method's own fallback
            offered = tuple(k for k, ratio in imageedit.ASPECTS if ratio)
            key = next((k for k in shown + (self._crop_pick,) + offered if k in ratios
                        and (ratios[k] is None or abs(aspect / ratios[k] - 1.0) <= RATIO_SAME)), "free")
        if key != cur:
            self.crop_box.blockSignals(True)
            self.crop_box.setCurrentIndex(self.crop_box.findData(key))
            self.crop_box.blockSignals(False)

    # ---- tools
    def _tab_changed(self, _i):
        page = self.tools.currentIndex()
        if page != 0 and self.crop_btn.isChecked():
            self.crop_btn.setChecked(False)
            self.canvas.set_crop_edit(False)
        if page != 1:
            for b in self.draw_btns.values():
                b.setChecked(False)
            self.canvas.set_shape_tool(None)
            self._draw_unpick()
        if page != 2 and self.censor_tool.isChecked():
            self.censor_tool.setChecked(False)
            self.canvas.set_editing(False)
        if page == 4:                                    # 1.35: the App may switch Claude while the window is open
            self._claude_refresh()

    def _crop_picked(self, _i):
        if self.original is None:
            return
        key = self.crop_box.currentData()
        if key != "none":
            self._crop_pick = key
        if key == "none":
            if self.edit.crop is not None:
                self._snapshot()
                self.edit.crop = None
            self.crop_btn.setChecked(False)
            self.canvas.set_crop_edit(False)
        else:
            ratio = dict(imageedit.ASPECTS).get(key)
            box = imageedit.aspect_box(self.edit.crop if key == "free" and self.edit.crop else (0, 0, 1, 1), ratio,
                                       self._turned_size())
            self._snapshot()
            self.edit.crop = box
            self.crop_btn.setChecked(True)
            self.canvas.set_crop_edit(True)
        self._refresh()

    def _crop_tool(self):
        on = self.crop_btn.isChecked()
        if on and self.crop_box.currentData() == "none":
            self.crop_box.setCurrentIndex(self.crop_box.findData("free"))
            return
        self.canvas.set_crop_edit(on)

    def turn(self, quarters):
        if self.original is None:
            return
        self._snapshot()
        self.edit = imageedit.turned(self.edit, quarters, self._turned_size())
        self._sync_crop_box()
        self._refresh(frame=True)

    def flip(self, horizontal):
        if self.original is None:
            return
        self._snapshot()
        self.edit = imageedit.flipped(self.edit, horizontal, self._turned_size())
        self._refresh(frame=True)

    def _turn_left(self):
        self.turn(3)

    def _turn_right(self):
        self.turn(1)

    def _mirror(self):
        self.flip(True)

    def _tip_over(self):
        self.flip(False)

    def _draw_tool_clicked(self):
        kind = next((k for k, b in self.draw_btns.items() if b is self.sender()), None)
        if kind is not None:
            self._draw_tool(kind)

    def _draw_tool(self, kind):
        on = self.draw_btns[kind].isChecked()
        for k, b in self.draw_btns.items():
            if k != kind:
                b.setChecked(False)
        self.canvas.set_shape_tool(kind if on else None)
        self.canvas.pen["text"] = self.draw_text.text()
        if not on:
            self._draw_unpick()

    def _draw_unpick(self):
        """No draw tool on: no drawing stays picked. Its frame is only drawn while a tool is on – colour, size,
        text and 'Zeichnung entfernen' changed a drawing nobody could see was meant (code review 37)."""
        if self.canvas.shape_sel is not None:
            self.canvas.shape_sel = None
            self.canvas.update()

    def _colour_clicked(self):
        colour = next((c for c, b in self.colour_btns.items() if b is self.sender()), None)
        if colour is not None:
            self._draw_colour(colour)

    def _draw_colour(self, colour):
        for c, b in self.colour_btns.items():
            b.setChecked(c == colour)
        self.canvas.pen["colour"] = colour
        sel = self.canvas.selected_shape()
        if sel is not None:
            sel.colour = colour
            self.canvas.replace_selected_shape(sel)

    def _draw_size(self, _i):
        i = int(self.draw_size_box.currentData() or 0)
        self.canvas.pen["size"], self.canvas.pen["text_size"] = annotate.SIZES[i], annotate.TEXT_SIZES[i]
        sel = self.canvas.selected_shape()
        if sel is not None:
            sel.size = annotate.TEXT_SIZES[i] if sel.kind == "text" else annotate.SIZES[i]
            self.canvas.replace_selected_shape(sel)

    def _draw_text_edited(self, text):
        self.canvas.pen["text"] = text
        sel = self.canvas.selected_shape()
        if sel is not None and sel.kind == "text":
            sel.text = text or " "
            # typing on into the same text is one undo step, not one per key: a sentence pushed the crop and the
            # censor boxes out of the UNDO_KEPT steps (code review 36)
            self._next_step = ("text", self.canvas.shape_sel)
            try:
                self.canvas.replace_selected_shape(sel)
            finally:
                self._next_step = None

    def _typing_done(self):
        """Enter, leaving the field or picking a drawing: the next text typed is an undo step of its own."""
        if isinstance(self._step, tuple):
            self._step = None

    def _shape_picked(self, _i):
        self._typing_done()
        sel = self.canvas.selected_shape()
        if sel is not None and sel.kind == "text":
            self.draw_text.setText(sel.text)

    def _draw_remove(self):
        self.canvas.remove_selected_shape()

    def _draw_clear(self):
        if self.canvas.shapes:
            self.canvas.set_shapes([])
            self._canvas_changed()

    def _censor_toggle(self):
        self.canvas.set_editing(self.censor_tool.isChecked())

    def _censor_style_changed(self, _i):
        style = self.censor_style.currentData() or "pixel"
        if style != self.edit.censor_style:
            self._snapshot()
            self.edit.censor_style = style
        self.canvas.set_look(True, style)

    def _names_match(self):
        self._names("match")

    def _names_spectate(self):
        self._names("spectate")

    def _names(self, kind: str):
        """1.38: censor boxes on the HUD's name places of the picture as it came (hudnames), turned and mirrored
        like the picture – one undo step; boxes already there are not added twice."""
        if self.original is None:
            return
        w, h = self.original.size
        placed = imageedit.ImageEdit(censor=hudnames.boxes(kind, (w, h)))
        if self.edit.rotate:
            placed = imageedit.turned(placed, self.edit.rotate, (w, h))
        size = (h, w) if self.edit.rotate % 2 else (w, h)
        if self.edit.flip_h:
            placed = imageedit.flipped(placed, True, size)
        if self.edit.flip_v:
            placed = imageedit.flipped(placed, False, size)
        new = self.edit.copy()
        new.censor = [imageedit.clamp_box(b) for b in hudnames.add(self.edit.censor, placed.censor)]
        if new.censor == self.edit.censor:
            return
        self._snapshot()
        self.edit = new
        self._step = None
        self._refresh()

    def _censor_remove(self):
        if not self.canvas.remove_selected() and self.canvas.boxes:
            self.canvas.selected = len(self.canvas.boxes) - 1
            self.canvas.remove_selected()

    def _censor_clear(self):
        self.canvas.clear_boxes()

    def _slider_moved(self, v):
        key = next((k for k, (sl, _val) in self.sliders.items() if sl is self.sender()), None)
        if key is not None:
            self._slid(key, v, self.sliders[key][1])

    def _slid(self, key, v, label):
        label.setText(f"{v} %")
        if self._step != "slider" or not self._adjust_timer.isActive():
            self._snapshot("slider")               # one undo step per slider move, not per pixel
        setattr(self.edit, key, v / 100.0)
        self._adjust_timer.start()

    def _adjust_apply(self):
        self._refresh(frame=True)

    def _colour_reset(self):
        if (self.edit.brightness, self.edit.contrast, self.edit.saturation) != (1.0, 1.0, 1.0):
            self._snapshot()
            self.edit.brightness = self.edit.contrast = self.edit.saturation = 1.0
            self._refresh(frame=True)

    # ---- output
    def result(self) -> Image.Image | None:
        return None if self.original is None else imageedit.render(self.original, self.edit)

    def copy(self):
        img = self.result()
        if img is None:
            return
        QGuiApplication.clipboard().setImage(qimage(img))
        self.status.setText(_("In die Zwischenablage kopiert – in Discord mit Strg+V einfügen."))

    def save(self):
        """Render and write the copy in a thread (3440×1440 with drawings: ~1 s – the window stays usable); the
        thread only touches PIL and the file, the result is picked up by ``_save_poll`` in the window thread."""
        if self.original is None or self._saver is not None:
            return
        fmt = self.fmt_box.currentData() or "png"
        name = "".join(ch for ch in self.name_edit.text() if ch not in '<>:"/\\|?*').strip()[:150] or \
            os.path.splitext(imageedit.out_name(self.path))[0]
        try:
            os.makedirs(self.out_dir, exist_ok=True)
        except OSError as e:
            self._save_failed(e)
            return
        taken = {os.path.normcase(os.path.abspath(p)) for p in (*_SAVING.values(), self.path)}
        out = os.path.join(self.out_dir, f"{name}.{fmt}")
        n = 2
        while os.path.exists(out) or os.path.normcase(os.path.abspath(out)) in taken:
            out = os.path.join(self.out_dir, f"{name} ({n}).{fmt}")
            n += 1
        original, edit, done = self.original, self.edit.copy(), {}

        def work():
            try:
                done["out"] = imageedit.save(imageedit.render(original, edit), out, fmt)
            except (OSError, ValueError) as e:
                done["error"] = e
        self._save_done = done
        self._saver = threading.Thread(target=work, name="image-save", daemon=True)
        _SAVING[self] = out
        self.save_btn.setEnabled(False)
        self.status.setText(_("Speichert …"))
        self._saver.start()
        self._save_timer.start()

    def _save_poll(self):
        if self._saver is None or self._saver.is_alive():
            return
        self._save_timer.stop()
        self._saver = None
        _SAVING.pop(self, None)
        self.save_btn.setEnabled(True)
        done = self._save_done
        if "out" not in done:
            self._save_failed(done.get("error", ""))
            return
        out = done["out"]
        self.last_out = out
        self.show_btn.setEnabled(True)
        self.status.setText(_("Gespeichert: {file}", file=os.path.basename(out)))
        self.log(_("Bild gespeichert: {file}", file=out), "System")
        if self.on_saved:
            self.on_saved(out)

    def _save_failed(self, e):
        self.status.setText(_("Bild nicht gespeichert: {error}", error=e))
        self.log(_("Bild nicht gespeichert: {error}", error=e), "Fehler")

    def wait_saved(self, timeout: float = 30.0):
        """Tests: block until a running save is done and picked up."""
        if self._saver is not None:
            self._saver.join(timeout)
        self._save_poll()

    def _show_saved(self):
        if not self.last_out:
            return
        if os.name == "nt":
            launch.show_in_folder(self.last_out)
        else:
            self.status.setText(self.last_out)

    def closeEvent(self, e):
        """1.38.3: an answer still on its way is dropped – the thread only finds a plain queue, never the window."""
        self._closed = True
        self._claude_pump.stop()
        self._claude_bridge.clear()
        self._claude_bridge.handlers.clear()        # the thread keeps the bridge, not the window through its handler
        super().closeEvent(e)

    def keyPressEvent(self, e):
        k = e.key()
        if k in (Qt.Key_Delete, Qt.Key_Backspace):
            if self.canvas.shape_tool and self.canvas.selected_shape() is not None:
                self.canvas.remove_selected_shape()
            elif self.canvas.editing:
                self.canvas.remove_selected()
        elif k == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(e)
