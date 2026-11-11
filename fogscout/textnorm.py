"""Text folding shared by the catalog (candidate names) and the OCR scorer.

Everything is reduced to the 36 symbols A-Z and 0-9. Spaces, apostrophes,
hyphens and other punctuation disappear, accents are stripped and case is
ignored, so "Azarov’s Resting Place", "AZAROVS RESTING PLACE" and
"Azarov's Resting-Place" all fold to the same key.
"""
import functools
import re
import unicodedata

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

_SPECIAL = {
    "ß": "SS", "ẞ": "SS", "ł": "L", "Ł": "L", "ı": "I", "İ": "I",
    "ø": "O", "Ø": "O", "æ": "AE", "Æ": "AE", "œ": "OE", "Œ": "OE",
    "đ": "D", "Đ": "D", "þ": "TH", "Þ": "TH",
}

# 1.49: the recognition model per game language – "main" (PP-OCRv4) reads the languages in Latin letters, i.e.
# every language not named here; for them nothing changes (same model, same crop, same 36 symbols). A file ``<model>.txt`` beside a model is its character list (PP-OCRv5 has none inside).
MAIN = "main"
MODEL_FILES = {MAIN: "ch_PP-OCRv4_rec_infer.onnx", "cjk": "PP-OCRv5_mobile_rec.onnx",
               "cyrillic": "cyrillic_PP-OCRv5_mobile_rec.onnx", "korean": "korean_PP-OCRv5_mobile_rec.onnx"}
LANG_MODEL = {"zh-Hans": "cjk", "zh-Hant": "cjk", "ja": "cjk", "ru": "cyrillic", "ko": "korean"}


def model_of(lang: str) -> str:
    return LANG_MODEL.get(lang, MAIN)


def alphabet_for(strings) -> str:
    """The symbols a scorer needs for ``strings`` (folded with fold_any): A-Z0-9 first and in their old order –
    with Latin names alone this is ALPHABET, and everything computes as before – then the other letters."""
    extra = sorted({c for s in strings for c in s} - set(ALPHABET))
    return ALPHABET + "".join(extra)


_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}


@functools.lru_cache(maxsize=8192)
def fold(text: str) -> str:
    """Uppercase A-Z0-9 only; accents stripped, everything else removed. Cached: the statistics fold the same
    killer and map names thousands of times per view."""
    out = []
    for ch in unicodedata.normalize("NFKC", text or ""):
        if ch in _SPECIAL:
            out.append(_SPECIAL[ch])
            continue
        base = unicodedata.normalize("NFKD", ch)
        base = "".join(c for c in base if not unicodedata.combining(c))
        out.append(base.upper())
    return re.sub(r"[^A-Z0-9]", "", "".join(out))


@functools.lru_cache(maxsize=8192)
def fold_any(text: str) -> str:
    """1.49: ``fold`` for the names of every game language – Latin letters and digits exactly as ``fold`` makes
    them, the letters of other scripts kept (Cyrillic upper-case with Ё as Е, Chinese, Kana, Hangul, Thai with its
    marks); spaces and punctuation go as before. For a text in Latin letters this is ``fold``."""
    out = []
    # NFKC splits the Thai vowel SARA AM (ำ) into two signs – the models read it as the one sign it is written as
    for ch in unicodedata.normalize("NFKC", text or "").replace("\u0e4d\u0e32", "\u0e33"):
        if ch in _SPECIAL:
            out.append(_SPECIAL[ch])
            continue
        base = unicodedata.normalize("NFKD", ch)
        base = "".join(c for c in base if not unicodedata.combining(c)).upper()
        if base and re.fullmatch(r"[A-Z0-9]+", base):
            out.append(base)
        elif not base or ord(ch) < 0x250:
            # a combining mark of a Latin letter, or a Latin letter fold does not know either
            if unicodedata.category(ch)[0] == "M" and ord(ch) >= 0x0E00:
                out.append(ch)                       # Thai vowel and tone marks are letters of their own
        elif unicodedata.category(ch)[0] in ("L", "M", "N"):
            up = ch.upper()
            out.append("Е" if up == "Ё" else up if len(up) == 1 else ch)
    return "".join(out)


def roman(n: int) -> str:
    return _ROMAN.get(int(n), str(n))


# Leading articles that the game might or might not render in front of a name.
_ARTICLES = {
    "en": ("The ",),
    "de": ("Der ", "Die ", "Das "),
    "fr": ("Le ", "La ", "Les ", "L'", "L’"),
    "es": ("El ", "La ", "Los ", "Las "),
    "es-MX": ("El ", "La ", "Los ", "Las "),
    "it": ("Il ", "La ", "Lo ", "I ", "L'", "L’"),
    "pt-BR": ("O ", "A ", "Os ", "As "),
}


def name_forms(name: str, lang: str):
    """The name itself plus, if it starts with an article, the form without it."""
    forms = [name]
    for art in _ARTICLES.get(lang, ()):
        if name.lower().startswith(art.lower()) and len(name) > len(art) + 2:
            forms.append(name[len(art):])
            break
    return forms


def pretty(text: str) -> str:
    """Collapse whitespace for display."""
    return re.sub(r"\s+", " ", text or "").strip()


def fmt_duration(seconds: float) -> str:
    """12:34 or 1:02:03 (round timer)."""
    s = max(0, int(seconds))
    h, m, s = s // 3600, s // 60 % 60, s % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
