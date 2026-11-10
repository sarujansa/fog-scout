"""1.48: the game language found by itself (gamelang.py) – with the reads of the user's own banners (debug/*.txt
of a French and a Turkish custom game, 10.11.2026)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import gamelang  # noqa: E402
from fogscout.catalog import Catalog  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = list(Catalog(ROOT, ["en", "de"]).maps.values())
# (name, realm) as the program read them – DBD in French on Wreckers' Yard, in Turkish on Badham Preschool I
FRENCH = [("TERRAIN DE LA CASSE", "CASSEAUTOHAVENX"), ("TERRAIN DE LA CASSE", "CASSEAUTOHAVENTHMV"),
          ("TERRAIN DELA CASSE", "CASSEAUTOHAVENLINY")]
TURKISH = [("BADHAM ANAOKU", "SPRINGWOOD"), ("BADHAM ANAOKULU I", "SPRINGWOOD TATEIV"),
           ("BADHAM ANAOKULUI", "SPRINGWOODIANHN"), ("BADHAM ANAOKULU", "SPRiNGWOOD")]


def _run(reads, active):
    votes = {}
    for name, realm in reads:
        hit = gamelang.vote(votes, name, realm, MAPS, set(active))
        if hit is not None:
            return hit
    return None


def test_the_users_french_and_turkish_banners_name_their_language():
    assert _run(FRENCH, ["en", "de"]) == ("fr", "wreckers-yard")
    assert _run(TURKISH, ["en", "de"]) == ("tr", "badham-preschool")
    assert _run(TURKISH, ["en", "de", "fr"]) == ("tr", "badham-preschool")


def test_one_look_is_not_enough_and_a_read_cut_off_too_far_counts_for_nothing():
    votes = {}
    assert gamelang.vote(votes, *FRENCH[0], MAPS, {"en", "de"}) is None          # VOTES = 2
    assert gamelang.vote(votes, *FRENCH[1], MAPS, {"en", "de"}) == ("fr", "wreckers-yard")
    assert gamelang.match("BADHAM ANAOKU", "SPRINGWOOD", MAPS, {"en", "de"}) == ("tr", "badham-preschool")   # 2 short
    assert gamelang.match("BADHAM ANA", "SPRINGWOOD", MAPS, {"en", "de"}) is None        # too far from the whole name
    assert gamelang.match("CASSE", "CASSEAUTOHAVEN", MAPS, {"en", "de"}) is None       # too short to say anything


def test_nothing_when_the_language_is_ticked_or_the_ticked_ones_read_as_well():
    assert _run(FRENCH, ["en", "de", "fr"]) is None
    assert _run(TURKISH, ["en", "de", "tr"]) is None
    assert _run([("COAL TOWER", "THE MACMILLAN ESTATE")] * 3, ["en", "de"]) is None
    assert _run([("GAS HEAVEN", "AUTOHAVEN WRECKERS")] * 3, ["en", "de"]) is None     # the French name is English


def test_the_realm_must_fit_and_noise_never_names_a_language():
    assert _run([("TERRAIN DE LA CASSE", "SPRINGWOOD")] * 3, ["en", "de"]) is None       # name of one map, realm of another
    assert _run([("REDFORESTVAUNNN", "")] * 3, ["en", "de"]) is None
    assert _run([("HAWKINS NATIONAL LAB", "")] * 3, ["en", "de"]) is None
    assert _run([("EXTINCTION DES FEUX", "INFOS DE MODIFICATEUR")] * 3, ["en", "de"]) is None   # a lobby panel


def test_the_order_of_the_languages_matches_the_app():
    from fogscout.app import LANGS, LANG_NAMES
    assert tuple(c for c, _l in LANGS) == gamelang.ORDER and set(LANG_NAMES) == set(gamelang.ORDER)


def test_every_name_of_another_language_names_that_language_and_never_a_wrong_one():
    """All 283 names outside EN/DE as clean reads with their realm: each names its own language (or one that writes
    the name the same, es/es-MX) – except names written as in English and "Gra" (too short); never another."""
    found, missed = 0, []
    for m in MAPS:
        for code, name in m.names.items():
            if code in ("en", "de"):
                continue
            hit = gamelang.match(name, m.realm_names.get(code) or m.realm_names.get("en"), MAPS, {"en", "de"})
            if hit is None:
                missed.append(name)
                continue
            assert m.names.get(hit[0]) == name, (code, name, hit)
            found += 1
    assert found >= 270
    assert all(n == "Gra" or any(n == x.names.get("en") for x in MAPS) for n in missed), missed
