"""German/English: every text in the code has an English version with the same placeholders."""
import ast
import glob
import os
import string
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import i18n, update  # noqa: E402
from fogscout.i18n_en import EN  # noqa: E402

PKG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fogscout")
SOURCES = [p for p in sorted(glob.glob(os.path.join(PKG, "*.py")))
           if os.path.basename(p) != "update.py" and not os.path.basename(p).startswith("i18n_")]
OTHERS = [c for c in i18n.CODES if c not in ("de", "en")]          # 1.47: the languages that lie on English
UNTRANSLATED_OK = {"Sprache / Language", "Log", "Log ⚠", "Maps", "Layout ▸", "●", "Fog Scout", "Ping", "Realm"}

def _trees():
    for p in SOURCES:
        with open(p, encoding="utf-8") as fh:
            yield os.path.basename(p), ast.parse(fh.read())

def marked_texts():
    """Literals passed to _() or N_() anywhere in the package."""
    out = set()
    for _name, tree in _trees():
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("_", "N_") and n.args:
                a = n.args[0]
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    out.add(a.value)
    return out

def fields(text):
    return {f for _lit, f, _spec, _conv in string.Formatter().parse(text) if f is not None}

def tooltip_texts():
    from fogscout import tooltip
    return set(tooltip.TIPS) | set(tooltip.TIPS.values()) | {t for _p, t in tooltip._PREFIX}

def test_every_text_has_an_english_version():
    wanted = marked_texts() | {i18n.LANGUAGES[0][1]}
    missing = sorted(t for t in wanted if t not in EN)
    assert not missing, "missing in i18n_en.py:\n" + "\n".join(missing)

def test_tooltips_have_an_english_version():
    missing = sorted(t for t in tooltip_texts() if t not in EN)
    assert not missing, "missing in i18n_en.py:\n" + "\n".join(missing)

def test_placeholders_match():
    wrong = [(k, v) for k, v in list(EN.items()) + list(update.EN.items()) if fields(k) != fields(v)]
    assert not wrong

def test_no_stale_translations():
    used = marked_texts() | {i18n.LANGUAGES[0][1]} | tooltip_texts()
    assert not sorted(set(EN) - used)

def test_labels_in_the_code_are_translated():
    """text=/title= literals in widgets must go through _() (else they stay German in English)."""
    bad = []
    for name, tree in _trees():
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            for kw in n.keywords:
                v = kw.value
                if kw.arg in ("text", "title") and isinstance(v, ast.Constant) and isinstance(v.value, str) \
                        and sum(c.isalpha() for c in v.value) >= 2 and v.value not in UNTRANSLATED_OK:
                    bad.append(f"{name}:{n.lineno} {v.value!r}")
    assert not bad, "\n".join(bad)

QT_TEXT_CALLS = {"QLabel", "QPushButton", "QCheckBox", "QRadioButton", "QGroupBox", "QListWidgetItem", "QAction",
                 "setText", "setToolTip", "setWindowTitle", "setPlaceholderText", "addItem", "_label"}

def test_qt_texts_in_the_code_are_translated():
    """Qt takes its texts positionally (QLabel("…"), b.setText("…")): those literals must go through _() too."""
    bad = []
    for name, tree in _trees():
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call) or not n.args:
                continue
            f = n.func
            fname = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""
            a = n.args[0]
            if fname in QT_TEXT_CALLS and isinstance(a, ast.Constant) and isinstance(a.value, str) \
                    and sum(c.isalpha() for c in a.value) >= 2 and a.value not in UNTRANSLATED_OK:
                bad.append(f"{name}:{n.lineno} {a.value!r}")
    assert not bad, "\n".join(bad)

def test_underscore_is_never_shadowed():
    """A local variable named _ would break every _() call in that function."""
    bad = []
    for name, tree in _trees():
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.Lambda)):
                continue
            comp = set()
            for n in ast.walk(fn):
                if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                    for g in n.generators:
                        comp.update(id(t) for t in ast.walk(g.target))
            binds = any(isinstance(n, ast.Name) and n.id == "_" and isinstance(n.ctx, ast.Store) and id(n) not in comp
                        for n in ast.walk(fn))
            calls = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "_"
                        for n in ast.walk(fn))
            if binds and calls:
                bad.append(f"{name}:{fn.lineno}")
    assert not bad

def test_switching_language():
    from fogscout.status import user_state
    try:
        assert i18n.set_language("en") == "en"
        assert i18n._("Im Match: {map}", map="Coal Tower") == "In match: Coal Tower"
        assert i18n._("gibt es nicht {x}", x=1) == "gibt es nicht 1"                  # fallback: German
        assert i18n.source("Test overlay") == "Overlay testen"
        assert user_state("", game_found=True).text == "Waiting for the next match"
        assert user_state(i18n._("Bildschirmaufnahme fehlgeschlagen: {error}", error="x")).kind == "err"
    finally:
        i18n.set_language("de")
    assert i18n._("Im Match: {map}", map="X") == "Im Match: X"

def test_language_setting():
    assert i18n.resolve("de") == "de" and i18n.resolve("en") == "en"
    assert i18n.resolve("auto") in i18n.CODES and i18n.resolve("xx") in i18n.CODES
    assert all(i18n.resolve(c) == c for c in i18n.CODES)


def test_the_program_speaks_the_languages_of_fog_translate():
    """1.47 (user: "in allen Sprachen wie die anderen Programme"): German, English and Fog Translate's Italian,
    Russian, Simplified Chinese, Japanese and Korean; Windows picks one by its language id, any other is English."""
    assert i18n.CODES == ("de", "en", "it", "ru", "zh", "ja", "ko")
    assert set(i18n.WINDOWS_IDS.values()) == set(i18n.CODES) and set(i18n.NAMES) == set(i18n.CODES)
    assert len({label for _c, label in i18n.LANGUAGES}) == len(i18n.LANGUAGES)


def test_every_language_has_every_text_with_the_same_placeholders():
    """Each i18n_<code>.T has exactly the keys of English (none missing, none stale), no empty text, the same
    {placeholders} and as many line breaks – a wrong name would raise in _() and show German instead."""
    import importlib
    for code in OTHERS:
        table = importlib.import_module(f"fogscout.i18n_{code}").T
        assert sorted(set(EN) - set(table))[:5] == [], code
        assert sorted(set(table) - set(EN))[:5] == [], code
        assert [k for k, v in table.items() if not isinstance(v, str) or not v.strip()][:5] == [], code
        assert [k for k, v in table.items() if fields(k) != fields(v)][:5] == [], code
        assert [k for k, v in table.items() if EN[k].count("\n") != v.count("\n")][:5] == [], code


def test_the_other_languages_show_their_text_and_english_where_one_is_missing(monkeypatch):
    import importlib
    try:
        for code in OTHERS:
            assert i18n.set_language(code) == code
            own = importlib.import_module(f"fogscout.i18n_{code}").T
            assert i18n._("Overlay testen") == own["Overlay testen"] != EN["Overlay testen"]
            assert i18n._("Im Match: {map}", map="Coal Tower").count("Coal Tower") == 1
            assert i18n.source(own["Overlay testen"]) == "Overlay testen"
            assert "Test overlay" in i18n.other(own["Overlay testen"]).split(" ") or \
                "Overlay testen" in i18n.other(own["Overlay testen"])
            assert i18n.is_program_text(own["Overlay testen"]) and i18n.language_name() == i18n.NAMES[code]
        mod = importlib.import_module("fogscout.i18n_ja")
        monkeypatch.delitem(mod.T, "Overlay testen")
        i18n.set_language("ja")
        assert i18n._("Overlay testen") == "Test overlay"                     # missing: English, not German
    finally:
        i18n.set_language("de")
    assert i18n._("Overlay testen") == "Overlay testen"


def test_the_start_script_speaks_english_for_the_other_languages(tmp_path, monkeypatch):
    monkeypatch.delenv("DBDMS_LANG", raising=False)
    for code in OTHERS:
        (tmp_path / "settings.json").write_text('{"ui_language": "%s"}' % code, encoding="utf-8")
        assert update._language(str(tmp_path)) == "en"

def test_update_messages_follow_the_setting(tmp_path, monkeypatch):
    monkeypatch.delenv("DBDMS_LANG", raising=False)
    (tmp_path / "settings.json").write_text('{"ui_language": "en", "auto_update": false}', encoding="utf-8")
    monkeypatch.setattr(update, "_lang", None)
    try:
        assert update.update(str(tmp_path)) == (update.SKIPPED, "Update check is switched off.")
    finally:
        update._lang = None
