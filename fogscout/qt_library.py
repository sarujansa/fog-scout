"""The editor's media library (1.16): the rounds, clips and imported files as a list with a picture, a name and a
line of facts each, a search field, a sort box and "Importieren"; a row is dragged onto the timeline
(qt_timeline.MIME) or opened with a double click. The pictures come from one ffmpeg key-frame seek per file in a
thread (``ThumbLoader``, never a Qt object there – qt_clip 1.8.66), cached below ``cache/clipthumbs`` so the next
editor shows them at once. The list itself is medialib.py (pure)."""
from __future__ import annotations

import hashlib
import os
import queue
import threading

from PySide6.QtCore import QAbstractListModel, QMimeData, QModelIndex, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QListView, QMenu, QStyle, QStyledItemDelegate, QToolButton, QVBoxLayout)

from . import clipedit, medialib, qt_icons, qt_theme
from .i18n import _
from .qt_common import guard_wheel
from .qt_timeline import MIME

ROW_H = 54
THUMB_W, THUMB_H = 72, 40
THUMB_AT = 0.3                      # the picture from this share into the video (not the black first frame)
THUMB_MAX_S = 20.0                  # … but at most this many seconds in
CACHE_DIR = os.path.join("cache", "clipthumbs")
ITEM_ROLE = Qt.UserRole + 1
_MEM = {}                           # (path, size, mtime) -> PIL image, for the editors of one program run


def _cache_key(path: str) -> tuple:
    try:
        st = os.stat(path)
        return path, st.st_size, st.st_mtime_ns
    except OSError:
        return path, 0, 0


class ThumbLoader:
    """Pictures of videos in a thread: ``request(items)`` sets what to do (newest first), ``take()`` in the window
    thread gives (path, PIL image or None, seconds) – ``seconds`` probed for items that did not know their length."""

    def __init__(self, cache_dir: str | None, ffmpeg: str | None, ratio: float = 1.0):
        self.cache_dir, self.ffmpeg = cache_dir, ffmpeg
        self.box = (int(THUMB_W * ratio) * 2, int(THUMB_H * ratio) * 2)
        self._done: queue.Queue = queue.Queue()
        self._lock = threading.Condition()
        self._todo = []
        self._thread = None
        self._stop = False

    def request(self, items):
        with self._lock:
            self._todo = [(it.path, it.seconds) for it in items]
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._run, daemon=True, name="clip-library")
                self._thread.start()
            self._lock.notify()

    def take(self, limit: int = 8) -> list:
        out = []
        while len(out) < limit:
            try:
                out.append(self._done.get_nowait())
            except queue.Empty:
                break
        return out

    def stop(self):
        with self._lock:
            self._stop = True
            self._todo = []
            self._lock.notify()

    def _next(self):
        with self._lock:
            while not self._todo and not self._stop:
                if not self._lock.wait(20):
                    return None
            if self._stop or not self._todo:
                return None
            return self._todo.pop(0)

    def _file(self, key) -> str | None:
        if not self.cache_dir:
            return None
        name = hashlib.sha1(f"{key[0]}|{key[1]}|{key[2]}|{self.box}".encode("utf-8")).hexdigest()[:24] + ".jpg"
        return os.path.join(self.cache_dir, name)

    def _run(self):
        from PIL import Image
        while True:
            job = self._next()
            if job is None:
                with self._lock:
                    if self._stop or not self._todo:
                        self._thread = None
                        return
                continue
            path, seconds = job
            key = _cache_key(path)
            img = _MEM.get(key)
            if img is None:
                target = self._file(key)
                if target and os.path.isfile(target):
                    try:
                        with Image.open(target) as im:
                            img = im.convert("RGB")
                    except (OSError, ValueError):
                        img = None
            try:
                if img is None or seconds <= 0:
                    info = clipedit.probe(path, self.ffmpeg)
                    if info.ok:
                        seconds = seconds or info.duration
                        if img is None:
                            at = min(THUMB_MAX_S, info.duration * THUMB_AT)
                            img = clipedit.frame_at(path, at, self.box[1], info, self.ffmpeg, keyframe=True)
                            if img is not None:
                                img.thumbnail(self.box, Image.LANCZOS)
                                target = self._file(key)
                                if target:
                                    try:
                                        os.makedirs(self.cache_dir, exist_ok=True)
                                        img.save(target, quality=85)
                                    except OSError:
                                        pass
                if img is not None:
                    _MEM[key] = img
                    if len(_MEM) > 400:
                        _MEM.pop(next(iter(_MEM)))
            except Exception:                              # one broken file never ends the thread
                img = None
            self._done.put((path, img, seconds))


class MediaModel(QAbstractListModel):
    """The rows: medialib.MediaItem each; drags carry the item's path."""

    def __init__(self):
        super().__init__()
        self.items = []
        self.thumbs = {}                 # path -> QPixmap
        self.current = None              # path of the recording open in the editor

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self.items):
            return None
        it = self.items[index.row()]
        if role == Qt.DisplayRole:
            return it.name
        if role == ITEM_ROLE:
            return it
        if role == Qt.ToolTipRole:
            return f"{it.name}\n{medialib.facts(it)}\n{it.path}"
        return None

    def flags(self, index):
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return base | Qt.ItemIsDragEnabled if index.isValid() else base

    def mimeTypes(self):
        return [MIME, "text/plain"]

    def mimeData(self, indexes):
        mime = QMimeData()
        for idx in indexes:
            if idx.isValid():
                it = self.items[idx.row()]
                mime.setData(MIME, it.path.encode("utf-8"))
                mime.setText(it.path)
                break
        return mime

    def set_items(self, items):
        self.beginResetModel()
        self.items = list(items)
        self.endResetModel()

    def row_of(self, path: str) -> int:
        key = os.path.normcase(os.path.abspath(path))
        return next((i for i, it in enumerate(self.items) if it.key == key), -1)

    def set_thumb(self, path: str, pm: QPixmap, seconds: float = 0.0):
        self.thumbs[path] = pm
        row = self.row_of(path)
        if row >= 0:
            if seconds > 0 and self.items[row].seconds <= 0:
                self.items[row].seconds = seconds
            idx = self.index(row, 0)
            self.dataChanged.emit(idx, idx)


class MediaDelegate(QStyledItemDelegate):
    def __init__(self, model: MediaModel, dark: bool, parent=None):
        super().__init__(parent)
        self.model_, self.dark = model, dark
        self._film = {}

    def sizeHint(self, option, index):
        return QSize(220, ROW_H)

    def paint(self, p, option, index):
        c = qt_theme.colours(self.dark)
        it = index.data(ITEM_ROLE)
        if it is None:
            return
        r = QRectF(option.rect)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        selected = bool(option.state & QStyle.State_Selected)
        hover = bool(option.state & QStyle.State_MouseOver)
        if selected or hover:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(c["hover"] if not selected else c["press"]))
            p.drawRoundedRect(r.adjusted(4, 2, -4, -2), 6, 6)
        if selected:
            p.setBrush(QColor(c["accent"]))
            p.drawRoundedRect(QRectF(r.left() + 4, r.top() + 10, 3, r.height() - 20), 1.5, 1.5)
        # picture
        pr = QRectF(r.left() + 14, r.top() + (r.height() - THUMB_H) / 2, THUMB_W, THUMB_H)
        path = QPainterPath()
        path.addRoundedRect(pr, 4, 4)
        p.setClipPath(path)
        p.fillRect(pr, QColor("#0e0f11"))
        pm = self.model_.thumbs.get(it.path)
        if pm is not None and not pm.isNull():
            ratio = pm.devicePixelRatio() or 1.0
            w, h = pm.width() / ratio, pm.height() / ratio
            s = max(pr.width() / w, pr.height() / h)
            dw, dh = w * s, h * s
            p.drawPixmap(QRectF(pr.center().x() - dw / 2, pr.center().y() - dh / 2, dw, dh).toRect(), pm)
        else:
            icon = qt_icons.pixmap("film", c["dim"], 18, option.widget.devicePixelRatioF() if option.widget else 1.0)
            p.drawPixmap(int(pr.center().x() - 9), int(pr.center().y() - 9), icon)
        p.setClipping(False)
        # text
        x = pr.right() + 12
        wtext = r.right() - 12 - x
        font = QFont(option.font)
        font.setPixelSize(12)
        font.setWeight(QFont.DemiBold)
        p.setFont(font)
        fm = p.fontMetrics()
        name = it.name
        if it.key == (self.model_.current or ""):
            p.setPen(QColor(c["accent"]))
            p.setBrush(QColor(c["accent"]))
            p.drawEllipse(QRectF(x, r.top() + 15, 6, 6))
            x += 11
            wtext -= 11
        p.setPen(QColor(c["head"] if self.dark else c["fg"]))
        p.drawText(QRectF(x, r.top() + 8, wtext, 18), Qt.AlignLeft | Qt.AlignVCenter, fm.elidedText(name, Qt.ElideRight, int(wtext)))
        font.setPixelSize(11)
        font.setWeight(QFont.Normal)
        p.setFont(font)
        p.setPen(QColor(c["dim"]))
        facts = medialib.facts(it)
        if it.project:
            facts = _("Projekt") + " · " + facts
        p.drawText(QRectF(x, r.top() + 28, wtext, 16), Qt.AlignLeft | Qt.AlignVCenter,
                   p.fontMetrics().elidedText(facts, Qt.ElideRight, int(wtext)))
        p.restore()


class MediaLibrary(QFrame):
    """The panel: search, sort and import on top, the list below."""
    opened = Signal(object)              # a MediaItem the user wants on the timeline
    shown = Signal(object)               # … shown in Explorer
    refresh_wanted = Signal()            # the list should be read again (after an import, when shown)

    def __init__(self, dark: bool, cache_dir: str | None, ffmpeg: str | None, ratio: float = 1.0):
        super().__init__()
        self.dark = dark
        self.setObjectName("panel")
        self.items = []
        self.extra = []                  # imported files of this session
        self.model = MediaModel()
        self.loader = ThumbLoader(cache_dir, ffmpeg, ratio)
        self.ratio = ratio
        self._dialog = None
        self._menu = None
        c = qt_theme.colours(dark)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 8)
        lay.setSpacing(8)
        head = QHBoxLayout()
        head.setSpacing(6)
        title = QLabel(_("Bibliothek"))
        title.setProperty("class", "section")
        head.addWidget(title)
        head.addStretch()
        self.import_btn = QToolButton()
        self.import_btn.setObjectName("toolbtn")
        self.import_btn.setIcon(qt_icons.icon("import", c["fg"], c["head"], c["fg_dis"], c["on_accent"], ratio=ratio))
        self.import_btn.setToolTip(_("Videodatei importieren – sie erscheint in der Bibliothek und lässt sich wie "
                                     "eine Aufnahme öffnen."))
        self.import_btn.setAutoRaise(True)
        self.import_btn.setFocusPolicy(Qt.NoFocus)
        self.import_btn.clicked.connect(self.import_files)
        head.addWidget(self.import_btn)
        lay.addLayout(head)
        row = QHBoxLayout()
        row.setSpacing(6)
        self.search = QLineEdit()
        self.search.setObjectName("search")
        self.search.setPlaceholderText(_("Suchen …"))
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self._refill)
        row.addWidget(self.search, 1)
        self.sort_box = guard_wheel(QComboBox())
        self.sort_box.setObjectName("sort")
        self.sort_box.setFocusPolicy(Qt.NoFocus)
        for key, label in medialib.SORTS:
            self.sort_box.addItem(_(label), key)
        self.sort_box.setToolTip(_("Sortierung der Bibliothek."))
        self.sort_box.currentIndexChanged.connect(self._refill)
        row.addWidget(self.sort_box)
        lay.addLayout(row)
        self.view = QListView()
        self.view.setObjectName("media")
        self.view.setModel(self.model)
        self.view.setItemDelegate(MediaDelegate(self.model, dark, self.view))
        self.view.setUniformItemSizes(True)
        self.view.setDragEnabled(True)
        self.view.setDragDropMode(QAbstractItemView.DragOnly)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.view.setMouseTracking(True)
        self.view.setFrameShape(QFrame.NoFrame)
        self.view.setFocusPolicy(Qt.NoFocus)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self._menu_at)
        self.view.doubleClicked.connect(lambda idx: self._open(idx))
        lay.addWidget(self.view, 1)
        self.empty = QLabel(_("Keine Aufnahmen – OBS-Aufnahmen und Clips erscheinen hier, „Importieren“ holt eine "
                              "andere Videodatei."))
        self.empty.setProperty("class", "dim")
        self.empty.setWordWrap(True)
        self.empty.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.empty)
        self.count = QLabel("")
        self.count.setProperty("class", "dim")
        lay.addWidget(self.count)
        self._refill()

    # ---- data
    def set_items(self, items, current: str | None = None):
        self.items = list(items)
        if current is not None:
            self.model.current = os.path.normcase(os.path.abspath(current))
        self._refill()

    def set_current(self, path: str):
        self.model.current = os.path.normcase(os.path.abspath(path))
        self.view.viewport().update()

    def all_items(self) -> list:
        seen, out = set(), []
        for it in self.extra + self.items:
            if it.key not in seen:
                seen.add(it.key)
                out.append(it)
        return out

    def item_for(self, path: str):
        key = os.path.normcase(os.path.abspath(path))
        return next((it for it in self.all_items() if it.key == key), None)

    def _refill(self, *_a):
        shown = medialib.sort_items(medialib.filter_items(self.all_items(), self.search.text()),
                                    self.sort_box.currentData() or "new")
        self.model.set_items(shown)
        self.empty.setVisible(not shown and not self.search.text())
        self.view.setVisible(bool(shown) or bool(self.search.text()))
        self.count.setText(_("{n} Einträge", n=len(shown)) if len(shown) != 1 else _("1 Eintrag"))
        self.loader.request([it for it in shown if it.path not in self.model.thumbs])

    def pump(self):
        """Window thread: finished pictures into the model."""
        for path, img, seconds in self.loader.take():
            if img is None:
                pm = QPixmap()
            else:
                w, h = img.size
                data = img.convert("RGB").tobytes()
                pm = QPixmap.fromImage(QImage(data, w, h, w * 3, QImage.Format_RGB888).copy())
                pm.setDevicePixelRatio(self.ratio * 2)
            self.model.set_thumb(path, pm, seconds)
            it = self.item_for(path)
            if it is not None and seconds > 0 and it.seconds <= 0:
                it.seconds = seconds

    # ---- actions
    def _open(self, idx):
        it = idx.data(ITEM_ROLE) if idx is not None and idx.isValid() else None
        if it is not None:
            self.opened.emit(it)

    def _menu_at(self, pos):
        idx = self.view.indexAt(pos)
        it = idx.data(ITEM_ROLE) if idx.isValid() else None
        if it is None:
            return
        menu = QMenu(self)
        menu.addAction(_("Auf der Zeitleiste öffnen")).triggered.connect(lambda _c=False: self.opened.emit(it))
        menu.addAction(_("Im Explorer zeigen")).triggered.connect(lambda _c=False: self.shown.emit(it))
        self._menu = menu
        menu.popup(self.view.viewport().mapToGlobal(pos))

    def import_files(self):
        """Qt's own non-modal file dialog (no second message loop); the files join the list for this session."""
        start = os.path.dirname(self.items[0].path) if self.items else os.path.expanduser("~")
        dlg = QFileDialog(self, _("Videodatei importieren"), start,
                          _("Videos") + " (*.mp4 *.mkv *.mov *.webm *.flv *.ts *.m4v *.avi);;* (*.*)")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.filesSelected.connect(self.add_files)
        dlg.open()
        self._dialog = dlg

    def add_files(self, paths):
        added = None
        for path in paths or ():
            if not path or not os.path.isfile(path):
                continue
            if self.item_for(path) is None:
                it = medialib.from_file(path)
                self.extra.insert(0, it)
                added = it
        self._refill()
        if added is not None:
            row = self.model.row_of(added.path)
            if row >= 0:
                self.view.setCurrentIndex(self.model.index(row, 0))
        return added

    def selected_item(self):
        idx = self.view.currentIndex()
        return idx.data(ITEM_ROLE) if idx.isValid() else None

    def closeEvent(self, e):
        self.loader.stop()
        super().closeEvent(e)
