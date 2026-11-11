"""1.50 (user: "alles in der entsprechenden Sprache" – map names stayed English with the UI in another language): map
and realm names are shown in the language of the user interface; what is stored keeps the English label."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import catalog, i18n  # noqa: E402
from fogscout.catalog import Catalog  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def lang():
    before = i18n.current()
    yield i18n.set_language
    i18n.set_language(before)


def test_names_follow_the_language_of_the_interface_and_the_stored_label_stays_english(lang):
    cat = Catalog(ROOT, ["en", "de"])
    coal = cat.maps["coal-tower"]
    lang("ru")
    assert coal.label(2) == "Coal Tower II"                      # rounds.jsonl, recordings, official data
    assert coal.shown_label(2) == coal.names["ru"] + " II" and coal.title == coal.names["ru"]
    assert coal.realm_title == coal.realm_names["ru"] and cat.realm_display(coal) == coal.realm_names["ru"]
    assert catalog.shown("Coal Tower II") == coal.names["ru"] + " II"
    assert catalog.shown("Coal Tower") == coal.names["ru"]       # older rounds without the layout number
    lang("zh")                                                     # the UI says zh, maps.json zh-Hans
    assert coal.title == coal.names["zh-Hans"] and catalog.shown("Coal Tower II") == coal.names["zh-Hans"] + " II"
    lang("de")
    assert coal.title == coal.names["de"]
    lang("en")
    assert coal.title == "Coal Tower" and catalog.shown("Coal Tower II") == "Coal Tower II"


def test_unknown_labels_stay_as_they_are_and_own_pictures_keep_their_name(lang):
    Catalog(ROOT, ["en"])
    lang("ja")
    assert catalog.shown("Some Own Map") == "Some Own Map" and catalog.shown("") == ""


def test_every_map_has_its_name_in_every_language_of_the_interface(lang):
    cat = Catalog(ROOT, ["en"])
    for code in i18n.CODES:
        lang(code)
        want = catalog.shown_lang()
        missing = [m.id for m in cat.maps.values() if not m.custom and want not in m.names]
        assert missing == [], (code, missing)


def test_the_maps_page_finds_a_map_by_its_name_in_another_script(lang):
    cat = Catalog(ROOT, ["en"])
    lang("ru")
    coal = cat.maps["coal-tower"]
    assert coal in cat.search(coal.names["ru"][:5]) and coal in cat.search("coal")
    assert coal in cat.search(cat.maps["coal-tower"].names["ja"])
