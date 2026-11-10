"""Language of the user interface and the log (German, English and – 1.47, like Fog Translate – Italian, Russian,
Simplified Chinese, Japanese, Korean).

The German text in the code is the key: ``_("Overlay testen")`` returns the text of the active language – English
from ``i18n_en.EN``, the others from ``i18n_<code>.T`` (same keys) – else the German one. Placeholders are named
and filled by ``_()``: ``_("Erkannt: {name}", name=label)``. A text missing in i18n_<code> shows in English, one
missing in English shows in German; tests/test_i18n.py makes sure there are none.

The language is chosen once at start (setting ``ui_language``: "auto" or a code of ``CODES``; "auto" = the
language of Windows when it is one of them, else English). Changing it takes effect after a restart.
"""
from __future__ import annotations

import json
import locale
import os
import sys

LANGUAGES = [("auto", "Automatisch (Windows-Sprache)"), ("de", "Deutsch"), ("en", "English"), ("it", "Italiano"),
             ("ru", "Русский"), ("zh", "简体中文"), ("ja", "日本語"), ("ko", "한국어")]   # "auto": translated
CODES = tuple(code for code, _label in LANGUAGES if code != "auto")
# Windows primary language ids (LANGID & 0x3FF) of the languages above
WINDOWS_IDS = {0x07: "de", 0x09: "en", 0x10: "it", 0x19: "ru", 0x04: "zh", 0x11: "ja", 0x12: "ko"}
# the language's name in English – what Claude is asked to answer in
NAMES = {"de": "German", "en": "English", "it": "Italian", "ru": "Russian", "zh": "Simplified Chinese",
         "ja": "Japanese", "ko": "Korean"}

_lang = "de"
_table: dict = {}
_reverse: dict = {}


def system_language() -> str:
    """The language of Windows (or the locale) when it is one of ``CODES``, else 'en'. DBDMS_LANG overrides
    (tests)."""
    if os.environ.get("DBDMS_LANG") in CODES:
        return os.environ["DBDMS_LANG"]
    try:
        if sys.platform == "win32":
            import ctypes
            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return WINDOWS_IDS.get(langid & 0x3FF, "en")
        code = (locale.getlocale()[0] or os.environ.get("LANG", "") or "").lower()
        return next((c for c in CODES if code.startswith(c)), "en")
    except Exception:
        return "en"


def resolve(setting: str | None) -> str:
    return setting if setting in CODES else system_language()


def table(code: str) -> dict:
    """German key -> text of ``code`` ({} for German). The other languages lie on English: a text they miss shows
    in English. Imported by name, so the .exe build finds every module (installer/fogscout.spec takes all)."""
    if code not in CODES or code == "de":
        return {}
    from .i18n_en import EN
    if code == "en":
        return EN
    import importlib
    own = importlib.import_module(f"{__package__}.i18n_{code}").T
    return {**EN, **own}


def set_language(code: str) -> str:
    """Activate a language of ``CODES`` ('auto'/None: from the system). Returns the active code."""
    global _lang, _table, _reverse
    _lang = resolve(code)
    _table = table(_lang)
    _reverse = {v: k for k, v in _table.items()}
    return _lang


def language_name() -> str:
    """The active language in English ("Japanese") – for asking Claude to answer in it."""
    return NAMES.get(_lang, "English")


def init_from_settings(path: str) -> str:
    """Language from settings.json before the app (and its Settings object) exists."""
    setting = "auto"
    try:
        with open(path, encoding="utf-8") as fh:
            setting = json.load(fh).get("ui_language", "auto")
    except (OSError, ValueError, AttributeError):
        pass
    return set_language(setting)


def current() -> str:
    return _lang


def _(msg: str, /, **kw) -> str:
    out = _table.get(msg, msg)
    if kw:
        try:
            return out.format(**kw)
        except (KeyError, IndexError, ValueError):
            return msg.format(**kw)
    return out


def source(text: str) -> str:
    """German original of a (translated) text – for lookups keyed by the German label."""
    return _reverse.get(text, text)


def other(text: str) -> str:
    """1.8.38: the same text in the languages not shown – German and English (the search finds a setting by either
    name); "" if none."""
    from .i18n_en import EN
    if _lang == "de":
        return EN.get(text, "")
    de = _reverse.get(text, "")
    words = [de] + ([EN.get(de, "")] if _lang != "en" else [])
    return " ".join(w for w in dict.fromkeys(words) if w and w != text)


_FIXED_NAMES = frozenset({"Maps", "Log", "Overlay", "OBS", "Discord", "Spotify", "YouTube", "Claude"})


def is_program_text(text: str) -> bool:
    """1.28 (audit F1): True only for a text that stands verbatim in the program's own table (German key or English
    translation) or is one of the few names never translated. A text formatted at run time (a status with a path, a
    ping, a map, a time) is never in the table – the positive list the Claude search builds its catalogue from."""
    t = str(text or "").strip()
    if not t:
        return False
    if t in _FIXED_NAMES:
        return True
    from .i18n_en import EN
    return t in EN or t in _english_values() or t in _reverse


_EN_VALUES = None


def _english_values():
    global _EN_VALUES
    if _EN_VALUES is None:
        from .i18n_en import EN
        _EN_VALUES = frozenset(EN.values())
    return _EN_VALUES


def N_(text: str) -> str:
    """Marks a text for translation where it is defined (lists, tables); translated later with _()."""
    return text
