"""1.38.29 (project review F4): the local corpus of decided banners (fogscout/corpus.py)."""
import json
import os
import sys
import zipfile

import cv2
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import corpus, detector  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPD = os.path.join(ROOT, "tests", "data", "banner", "letterbox_rpd_east.jpg")   # ROI of a 1714×1360 frame
RPD_FRAME, RPD_BARS = (1714, 1360), (251, 250)


def _reader():
    pytest.importorskip("onnxruntime")
    from fogscout.catalog import Catalog
    from fogscout.ocr import Recognizer
    return detector.BannerReader(Recognizer(os.path.join(ROOT, "models", "ch_PP-OCRv4_rec_infer.onnx")), Catalog(ROOT))


def _decision(res):
    return detector.Decision(map_id=res.best[0], variant=res.best[1], probability=0.97, variant_probability=0.9,
                             frames=3, name_text=res.name_text, realm_text=res.realm_text, name_fit=res.name_fit)


def test_a_decided_banner_is_kept_as_a_crop_and_read_again_in_the_check(tmp_path):
    reader = _reader()
    img = cv2.imread(RPD)
    sep, res = reader.read(img, *RPD_FRAME, letterboxed=True, bars=RPD_BARS)
    assert res is not None and res.best[0] == "rpd-east"
    stamp = corpus.save(str(tmp_path), img, sep, res, _decision(res), RPD_FRAME, True, RPD_BARS, ["en", "de"], "1.38.29",
                        now=1_700_000_000.123)
    assert stamp and len(stamp) == 19 and corpus.count(str(tmp_path)) == 1
    (entry,) = corpus.entries(str(tmp_path))
    meta = entry.meta
    assert meta["format"] == corpus.FORMAT and meta["map_id"] == "rpd-east" and meta["frame"] == list(RPD_FRAME)
    assert meta["bars"] == list(RPD_BARS) and meta["letterboxed"] is True and meta["languages"] == ["en", "de"]
    assert meta["separator"]["y"] == sep.y and meta["roi"] == [img.shape[1], img.shape[0]]
    crop = cv2.imread(entry.picture)
    x0, y0, x1, y1 = corpus.crop_box(img.shape, sep)
    assert crop.shape[:2] == (y1 - y0, x1 - x0) and crop.size < img.size          # the band, not the whole strip
    assert y0 < sep.y < y1 and x0 <= sep.x0 and x1 >= sep.x1                     # the line and its text are in it
    rep = corpus.check(str(tmp_path), reader)
    assert (rep.total, rep.hits, rep.misses, rep.broken) == (1, 1, [], 0) and rep.seconds >= 0
    # a stored decision whose map the reader no longer gives is a miss, a broken picture is counted apart
    with open(os.path.join(corpus.folder(str(tmp_path)), stamp + ".json"), encoding="utf-8") as fh:
        wrong = json.load(fh)
    wrong["map_id"] = "coal-tower"
    from fogscout import fsops
    fsops.write_new(os.path.join(corpus.folder(str(tmp_path)), "20250101-000000-001.json"), json.dumps(wrong).encode())
    fsops.write_new(os.path.join(corpus.folder(str(tmp_path)), "20250101-000000-001.jpg"), open(entry.picture, "rb").read())
    fsops.write_new(os.path.join(corpus.folder(str(tmp_path)), "20250101-000000-002.json"), json.dumps(wrong).encode())
    fsops.write_new(os.path.join(corpus.folder(str(tmp_path)), "20250101-000000-002.jpg"), b"not a picture")
    rep = corpus.check(str(tmp_path), reader)
    assert (rep.total, rep.hits, rep.broken) == (3, 1, 1) and rep.misses[0][1:3] == ("coal-tower", "rpd-east")


def test_the_corpus_keeps_the_newest_decisions_skips_foreign_files_and_exports_a_zip(tmp_path, monkeypatch):
    import numpy as np
    sep = detector.Separator(y=300, x0=100, x1=900, frac=0.47, thickness=1.0)
    res = detector.FrameResult(scores={}, best=("coal-tower", 1), name_text="COAL TOWER", realm_text="MACMILLAN",
                               name_fit=-0.3)
    img = np.full((600, 1100, 3), 90, np.uint8)
    monkeypatch.setattr(corpus, "KEEP", 3)
    stamps = [corpus.save(str(tmp_path), img, sep, res, _decision(res), (1920, 1080), False, None, ["en"], "x",
                          now=1_700_000_000 + i) for i in range(5)]
    kept = corpus.entries(str(tmp_path))
    assert [e.stamp for e in kept] == stamps[2:] and corpus.count(str(tmp_path)) == 3   # the two oldest went, pairs
    assert sorted(os.listdir(corpus.folder(str(tmp_path)))) == sorted(s + ext for s in stamps[2:] for ext in (".jpg", ".json"))
    # a file that is not ours stays and is not listed
    other = os.path.join(corpus.folder(str(tmp_path)), "notes.json")
    with open(other, "w", encoding="utf-8") as fh:
        fh.write('{"format": "something else"}')
    corpus.prune(corpus.folder(str(tmp_path)), keep=1)
    assert os.path.exists(other) and corpus.count(str(tmp_path)) == 1 and len(corpus.entries(str(tmp_path))) == 1
    dest = tmp_path / "out" / "korpus.zip"
    dest.parent.mkdir()
    assert corpus.export_zip(str(tmp_path), str(dest)) == 2
    with zipfile.ZipFile(dest) as z:
        assert sorted(z.namelist()) == [stamps[4] + ".jpg", stamps[4] + ".json"]
    assert corpus.entries(str(tmp_path / "nowhere")) == [] and corpus.count(str(tmp_path / "nowhere")) == 0


# ------------------------------------------------------------------ the real corpus (user export 05.11.2026)
REAL = os.path.join(ROOT, "tests", "data")      # corpus.folder(REAL) = tests/data/corpus


def test_the_real_corpus_holds_only_our_pairs_without_names():
    """1.38.38: the banners Saru exported ("Korpus exportieren …") – each a JPEG of the strip around the line and its
    JSON; the first 9, 3440×1440 and a 1071×601 window. Only map and realm are in the picture (checked by eye)."""
    entries = corpus.entries(REAL)
    names = sorted(os.listdir(corpus.folder(REAL)))
    assert len(entries) >= 9 and len(names) == 2 * len(entries)
    for e in entries:
        assert set(e.meta) >= {"map_id", "frame", "roi", "offset"} and "path" not in json.dumps(e.meta).lower()


def test_every_banner_of_the_real_corpus_is_read_as_its_map_again():
    """1.38.38 (project review T1): the full banner pipeline on every exported crop, back on a black strip of the
    original size – any change to the separator search, the crop or the scoring that loses one of them fails here."""
    rep = corpus.check(REAL, _reader())
    assert rep.broken == 0 and rep.misses == [] and rep.hits == rep.total >= 9
