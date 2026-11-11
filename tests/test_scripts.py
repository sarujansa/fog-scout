"""1.49: game languages in other scripts (Russian, Chinese, Japanese, Korean) – their models, their names in
maps.json, the crop for scripts that are not Latin capitals, and that nothing changed for the Latin languages.
The banners in tests/data/banner_synth are rendered (see its README), not game pictures."""
import glob
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import gamelang  # noqa: E402
from fogscout.catalog import Catalog  # noqa: E402
from fogscout.textnorm import ALPHABET, LANG_MODEL, MAIN, MODEL_FILES, alphabet_for, fold, fold_any, model_of  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATIN = ["en", "de", "fr", "es", "es-MX", "it", "pl", "pt-BR", "tr"]
OTHERS = ["ru", "zh-Hans", "zh-Hant", "ja", "ko"]
SAMPLES = sorted(glob.glob(os.path.join(ROOT, "tests", "data", "banner_synth", "*.json")))


def test_nothing_changes_for_the_latin_game_languages():
    """Same folded names, the main model alone, exactly the 36 symbols A-Z0-9 – so the scorer computes as before."""
    cat = Catalog(ROOT, LATIN)
    assert cat.models == [MAIN] and cat.alphabet == ALPHABET and all(h.model == MAIN for h in cat.hypotheses)
    texts = [n for m in cat.maps.values() for c, n in m.names.items() if c in LATIN]
    texts += [n for m in cat.maps.values() for c, n in m.realm_names.items() if c in LATIN]
    assert [t for t in texts if fold_any(t) != fold(t)] == []
    assert all(model_of(code) == MAIN for code in LATIN) and alphabet_for(["COALTOWER", "KOHLELAGER"]) == ALPHABET


def test_every_map_has_a_name_in_every_new_language_and_its_model_knows_every_sign():
    with open(os.path.join(ROOT, "maps.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    for code in OTHERS:
        assert LANG_MODEL[code] in MODEL_FILES and LANG_MODEL[code] != MAIN
        with open(os.path.join(ROOT, "models", os.path.splitext(MODEL_FILES[LANG_MODEL[code]])[0] + ".txt"),
                  encoding="utf-8", newline="") as fh:
            known = {c.rstrip("\r") for c in fh.read().split("\n")}       # a Windows checkout has CRLF line ends
        names = [m["names"].get(code, "") for m in data["maps"]] + [r.get(code, "") for r in data["realms"].values()]
        assert all(names), code
        assert len({fold_any(m["names"][code]) for m in data["maps"]}) == len(data["maps"]), code     # no two alike
        missing = sorted({c for n in names for c in fold_any(n) if c not in known})
        assert missing == [], (code, missing)


def test_folding_keeps_the_letters_of_other_scripts():
    assert fold_any("Угольная Башня") == "УГОЛЬНАЯБАШНЯ" and fold_any("ёлка") == "ЕЛКА"
    assert fold_any("コール・タワー") == "コールタワー" and fold_any("석탄 저장소") == "석탄저장소"
    assert fold_any("煤矿废塔 II") == "煤矿废塔II" and fold("煤矿废塔 II") == "II"
    assert fold_any("ที่พำนัก") == "ที่พำนัก"                      # the vowel ำ stays one sign
    assert fold_any("Père-Noël’s") == fold("Père-Noël’s") == "PERENOELS"


def test_a_name_of_two_signs_counts_as_a_name():
    from fogscout.detector import MIN_NAME_CHARS, name_chars
    assert name_chars("血屋") >= MIN_NAME_CHARS and name_chars("AB") < MIN_NAME_CHARS
    assert name_chars("COAL TOWER") == 9 and name_chars("Игра") == 4


def _roi(meta_path):
    import cv2
    import numpy as np
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    crop = cv2.imdecode(np.fromfile(meta_path[:-5] + ".jpg", dtype=np.uint8), cv2.IMREAD_COLOR)
    canvas = np.zeros((meta["roi"][1], meta["roi"][0], 3), np.uint8)
    x0, y0 = meta["offset"]
    canvas[y0:y0 + crop.shape[0], x0:x0 + crop.shape[1]] = crop
    return meta, canvas


@pytest.fixture(scope="module")
def readers():
    pytest.importorskip("onnxruntime")
    from fogscout.detector import BannerReader
    from fogscout.ocr import ModelPool, Recognizer
    models = os.path.join(ROOT, "models")
    rec, pool, made = Recognizer(os.path.join(models, MODEL_FILES[MAIN])), ModelPool(models), {}

    def reader(langs):
        key = tuple(langs)
        if key not in made:
            made[key] = BannerReader(rec, Catalog(ROOT, list(langs)), pool)
        return made[key]
    return reader


def test_there_are_rendered_banners_for_every_new_language():
    assert sorted({os.path.basename(p).rsplit("-", 99)[0].split("-")[0] for p in SAMPLES}) == ["ja", "ko", "ru", "zh"]
    assert len(SAMPLES) == 15


@pytest.mark.parametrize("path", SAMPLES, ids=[os.path.basename(p)[:-5] for p in SAMPLES])
def test_a_banner_in_another_script_is_read_when_its_language_is_ticked(path, readers):
    from fogscout.detector import Accumulator
    meta, roi = _roi(path)
    sep, res = readers(["en", "de", meta["lang"]]).read(roi, *meta["frame"])
    assert sep is not None and res is not None and res.best is not None
    assert res.best[0] == meta["map_id"] and res.name_fit >= -3.0, (res.best, res.name_fit, res.name_text)
    acc = Accumulator()
    d = acc.add(res) or acc.add(res)
    assert d is not None and d.map_id == meta["map_id"] and not d.unsure


@pytest.mark.parametrize("path", SAMPLES, ids=[os.path.basename(p)[:-5] for p in SAMPLES])
def test_without_its_language_it_names_no_map_but_its_language_is_found(path, readers):
    """EN/DE only: the banner is no evidence for any map (never a wrong map), and the models of the other scripts
    read which language it is (gamelang, as the worker asks them)."""
    from fogscout.detector import Accumulator
    meta, roi = _roi(path)
    reader = readers(["en", "de"])
    sep, res = reader.read(roi, *meta["frame"])
    acc = Accumulator()
    assert sep is not None and (res is None or (acc.add(res) or acc.add(res)) is None)
    maps, votes, hit = list(reader.catalog.maps.values()), {}, None
    for _look in range(gamelang.VOTES):
        for name, realm in reader.probe():
            hit = hit or gamelang.vote(votes, name, realm, maps, {"en", "de"})
    assert hit is not None and hit[1] == meta["map_id"], (hit, votes)
    names = reader.catalog.maps[meta["map_id"]].names
    assert names[hit[0]] == names[meta["lang"]] or {hit[0], meta["lang"]} == {"zh-Hans", "zh-Hant"}


def test_a_latin_banner_reads_the_same_with_other_scripts_ticked(readers):
    """The user's real banners (tests/data/corpus, English): ticking Russian, Japanese … changes neither the map
    nor the fit of the main model's read."""
    pytest.importorskip("onnxruntime")
    from fogscout import corpus
    base = corpus.check(os.path.join(ROOT, "tests", "data"), readers(["en", "de"]))
    more = corpus.check(os.path.join(ROOT, "tests", "data"), readers(["en", "de"] + OTHERS))
    assert base.total == more.total > 0 and base.hits == base.total and more.hits == more.total and not more.broken


def test_a_missing_model_only_loses_its_languages(tmp_path):
    pytest.importorskip("onnxruntime")
    from fogscout.detector import BannerReader
    from fogscout.ocr import ModelPool, Recognizer
    said = []
    pool = ModelPool(str(tmp_path), on_error=lambda model, e: said.append(model))      # an empty models folder
    assert pool.get("korean") is None and pool.get("korean") is None and said == ["korean"]   # said once
    assert pool.get(MAIN) is None                                                # the main model is not its business
    reader = BannerReader(Recognizer(os.path.join(ROOT, "models", MODEL_FILES[MAIN])), Catalog(ROOT, ["en", "ko"]), pool)
    assert [v.model for v in reader.views] == [MAIN] and reader.probe() == []


def test_a_name_of_two_signs_needs_its_realm_to_name_a_language():
    maps = list(Catalog(ROOT, ["en"]).maps.values())
    assert gamelang.match("煤矿废塔", "麦克米伦庄园", maps, {"en", "de"}) == ("zh-Hans", "coal-tower")
    assert gamelang.match("血屋", "", maps, {"en", "de"}) is None                  # two signs, but no realm read
    assert gamelang.match("ИГРА", "МЯСОКОМБИНАТ «ГИДЕОН»", maps, {"en", "de"}) == ("ru", "the-game")


def test_a_character_list_with_windows_line_ends_reads_the_same(tmp_path):
    """1.49 (Windows CI): git turned the lists' line ends into CRLF – every character carried a "\\r"."""
    pytest.importorskip("onnxruntime")
    import shutil
    from fogscout.ocr import Recognizer
    name = MODEL_FILES["cyrillic"]
    src = os.path.join(ROOT, "models", name)
    shutil.copyfile(src, tmp_path / name)
    with open(os.path.splitext(src)[0] + ".txt", "rb") as fh:
        raw = fh.read().replace(b"\r\n", b"\n")
    (tmp_path / (os.path.splitext(name)[0] + ".txt")).write_bytes(raw.replace(b"\n", b"\r\n"))
    crlf, plain = Recognizer(str(tmp_path / name)), Recognizer(src)
    assert crlf.chars == plain.chars and not any(c.endswith("\r") for c in crlf.chars) and "Я" in crlf.chars


def test_the_worker_names_the_language_of_a_banner_and_then_reads_it(tmp_path, monkeypatch):
    """1.49.1 (user: three Russian banners, no language ticked, no map – the worker raised right where it said
    which language it had found: ``lang_votes`` was dropped before its text was read, so every find died in the
    tick). The whole way: EN/DE ticked, a Russian banner on screen → event "game_language" (and no warning), the
    new catalog the App sends → the same banner names its map."""
    pytest.importorskip("onnxruntime")
    import queue
    import time
    import numpy as np
    from fogscout import config, worker
    from fogscout.detector import ROI
    meta, roi = _roi(os.path.join(ROOT, "tests", "data", "banner_synth", "ru-coal-tower.json"))
    w, h = meta["frame"]
    frame = np.zeros((h, w, 3), np.uint8)
    frame[int(ROI[1] * h):int(ROI[1] * h) + roi.shape[0], int(ROI[0] * w):int(ROI[0] * w) + roi.shape[1]] = roi

    class Source:
        def __init__(self, *_a, **_k):
            pass

        def current(self):
            return frame

    monkeypatch.setattr(worker, "ImageSource", Source)
    events = queue.Queue()
    wk = worker.DetectionWorker(ROOT, config.Settings(str(tmp_path / "settings.json")), Catalog(ROOT, ["en", "de"]),
                                events, simulate=str(tmp_path), data_dir=str(tmp_path))
    wk.start()
    seen, language, found = [], None, None
    try:
        deadline = time.time() + 90                                # generous: shared CI runners
        while found is None and time.time() < deadline:
            try:
                ev = events.get(timeout=0.5)
            except queue.Empty:
                continue
            seen.append(ev.kind)
            if ev.kind == "game_language" and language is None:
                language = ev.data
                wk.set_catalog(Catalog(ROOT, ["en", "de", language["code"]]))      # what App._game_language does
            elif ev.kind == "detected":
                found = ev.data
    finally:
        wk.stop()
        wk.join(timeout=10)
    assert language is not None and (language["code"], language["map_id"]) == ("ru", "coal-tower"), seen
    assert "УГОЛЬНАЯ" in language["name_text"] and "warn" not in seen and "error" not in seen, seen
    assert found is not None and found["map_id"] == "coal-tower"
