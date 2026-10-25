"""1.12.2 (user on the recordings page: "ich find das nicht schön"): the screenshots as a gallery, one status
column, the file column hidden until shown, the gallery taking the page's height."""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import thumbs  # noqa: E402
from fogscout.app_recordings import RecordingsTab  # noqa: E402


def test_the_status_column_shows_kept_marks_and_youtube_as_symbols():
    status = RecordingsTab._rec_status
    assert status(False, 0, "") == ""
    assert status(True, 2, "✓") == "★  ⚑2  ▶"
    assert status(False, 1, "…") == "⚑1  ▶…"                              # waiting in the upload queue
    assert status(True, 0, "") == "★"


def test_a_jpeg_thumbnail_is_decoded_at_a_reduced_scale_and_fits_its_box(tmp_path):
    src = tmp_path / "20261025194138_1.jpg"
    Image.new("RGB", (3440, 1440), (40, 60, 90)).save(src, quality=90)
    pic = thumbs.thumbnail(str(src), (322, 182), str(tmp_path / "cache"))
    assert pic.size == (322, 135) and pic.mode == "RGBA"
    assert thumbs.thumbnail(str(src), (322, 182), str(tmp_path / "cache")).size == (322, 135)   # from the cache
    assert thumbs.Loader((10, 10), name="shot-thumbs").name == "shot-thumbs"


def test_the_gallery_fills_its_rows_takes_the_pictures_shape_and_reports_clicks(tmp_path):
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_gallery, qt_window
    app = qt_window.application()
    paths = []
    for i in range(7):
        p = tmp_path / f"shot{i}.jpg"
        Image.new("RGB", (2100, 900), (30 * i, 40, 60)).save(p)                # 21:9 like an ultrawide screen
        paths.append(str(p))
    picked, opened = [], []
    g = qt_gallery.ShotGallery(str(tmp_path / "cache"), on_pick=picked.append, on_open=opened.append)
    try:
        g.resize(1200, 700)
        g.show()
        g.set_items([(p, f"25.10.26 · 19:4{i}", "47 KB", "Bearbeitet" if i == 0 else "") for i, p in enumerate(paths)])
        app.processEvents()
        assert g.paths() == paths and g.selected_path() is None
        tile = g.tile_size()
        n = (g.viewport().width() - 4) // tile.width()
        assert n >= 3 and n * tile.width() <= g.viewport().width()             # a row ends at the edge, no wrap gap
        assert (n + 1) * tile.width() > g.viewport().width() - 4
        g.load_all()
        assert g.aspect == pytest.approx(2100 / 900, rel=0.01)                 # tiles took the pictures' shape
        assert all(not g.pixmap(p).isNull() for p in paths)
        g.select_path(paths[2])
        assert g.selected_path() == paths[2] and picked == []                  # set from the App: no report back
        g.item(4).setSelected(True)
        assert picked[-1] == paths[4]
        g.itemActivated.emit(g.item(4))
        assert opened == [paths[4]]
        g.set_items([(p, "x", "y", "") for p in paths[3:]], selected=paths[4])  # another list keeps the pick
        assert g.paths() == paths[3:] and g.selected_path() == paths[4]
        assert set(g._pix) <= set(paths[3:])                                     # pixmaps of gone pictures dropped
        grab = g.grab()
        assert not grab.isNull()
    finally:
        g.close()


def test_the_file_column_is_hidden_until_the_user_shows_it():
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_views, qt_window
    qt_window.application()
    posted = []
    t = qt_views.Table("rec", lambda *a: posted.append(a))
    st = {"columns": [("when", "Wann", "w"), ("map", "Map", "w"), ("file", "Datei", "w")],
          "rows": [("a", 0, "", ["1", "Coal Tower", "x.mkv"], [], True)], "stretch": 1, "widths": [100, 130, 110],
          "hide": ["file"]}
    t.show_state(st)
    assert t.isColumnHidden(2) and not t.isColumnHidden(1)
    t._toggle_column("file", True)                                            # shown from the heading's menu
    assert not t.isColumnHidden(2) and posted[-1] == ("table_cols", ("when|map|file", []))
    t2 = qt_views.Table("rec", lambda *a: None)
    t2.set_hidden_map({"when|map|file": []})                                  # the remembered choice wins
    t2.show_state(st)
    assert not t2.isColumnHidden(2)


def test_a_host_packed_to_expand_takes_the_free_height_of_its_page():
    from fogscout import app_qt, qt_pages, uimodel as ui
    root = ui.Frame(None)
    h = ui.Host(root)
    h.pack(fill="both", expand=True)
    node = app_qt.ui_layout(root, {})
    assert node["children"][0]["grow"] is True and qt_pages._grows(node)
    other = ui.Frame(None)
    ui.Host(other).pack(side="left", fill="both")                             # the clip preview beside a table
    assert not app_qt.ui_layout(other, {})["children"][0]["grow"]
