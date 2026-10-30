"""1.8.79: "Neu seit …" on the overview – the HISTORY.md rows after the version last run (whatsnew.py)."""
import os

from fogscout import __version__, whatsnew

SAMPLE = """# History

| Datei | Aufgabe |
|---|---|
| `app.py` | Controller 1.8.2 (the version here is not a row version) |
| Overlay-Elemente | Fünf Elemente, keine Version |
| Maps-Seite und Start 1.8.72 (Auftrag: UI/UX prüfen) – Die Maps-Seite lädt die Kacheln im Hintergrund. | Details … |
| Farming-Gegner 1.8.73 (Nutzer: „Slasher 38× (safe vom Farmen)“) | Details … |
| Rechtsklick Gegner 1.8.74 | Details … |
| Navigation 1.8.78 (UI-Durchsicht Punkt 3) – {long} | Details … |
""".replace("{long}", "x" * 400)


def test_only_version_rows_are_entries_and_their_parts_are_split():
    """1.14.1 (user: "warum wird hier der Prompt reingeschrieben?"): the detail is the sentence after the
    background's parentheses, never the background itself (the user's request)."""
    rows = whatsnew.entries(SAMPLE)
    assert [r[0] for r in rows] == ["1.8.72", "1.8.73", "1.8.74", "1.8.78"]       # file and theme rows skipped
    assert rows[0] == ("1.8.72", "Maps-Seite und Start", "Die Maps-Seite lädt die Kacheln im Hintergrund.")
    assert rows[1] == ("1.8.73", "Farming-Gegner", "")          # nested parentheses, no sentence: nothing shown
    assert rows[2] == ("1.8.74", "Rechtsklick Gegner", "")      # no parentheses at all
    assert len(rows[3][2]) == whatsnew.DETAIL_CHARS and rows[3][2].endswith("…")   # cut, with an ellipsis
    broken = whatsnew.entries("| Kaputt 1.8.80 (Klammer ohne Ende – Satz | Details … |")
    assert broken == [("1.8.80", "Kaputt", "")]                  # unclosed parentheses: nothing rather than garbage


def test_news_is_everything_after_the_version_last_run_newest_first():
    assert [r[0] for r in whatsnew.news(SAMPLE, "1.8.73")] == ["1.8.78", "1.8.74"]
    assert whatsnew.news(SAMPLE, "1.8.78") == []                                 # the current version: nothing
    assert [r[0] for r in whatsnew.news(SAMPLE, "1.8.72", limit=2)] == ["1.8.78", "1.8.74"]
    # a version without a row of its own (skipped, or a hotfix): by the numbers
    assert [r[0] for r in whatsnew.news(SAMPLE, "1.8.73.1")] == ["1.8.78", "1.8.74"]
    assert whatsnew.news(SAMPLE, "") == [] and whatsnew.news(SAMPLE, "kaputt") == []
    assert whatsnew.news(SAMPLE, "1.9") == []                                    # a downgrade: nothing to tell
    assert whatsnew.parse_version("1.8.79") == (1, 8, 79) and whatsnew.parse_version("a.b") == ()


def test_the_file_is_read_and_a_missing_one_is_no_news(tmp_path):
    p = tmp_path / "HISTORY.md"
    p.write_text(SAMPLE, encoding="utf-8")
    assert [r[0] for r in whatsnew.load(str(p), "1.8.74")] == ["1.8.78"]
    assert whatsnew.load(str(tmp_path / "nope.md"), "1.8.74") == []


def test_the_real_history_ends_with_the_current_version():
    """Every version gets a row in HISTORY.md (CLAUDE.md → Arbeitsweise) – the card would otherwise miss it."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HISTORY.md")
    with open(path, encoding="utf-8") as fh:
        rows = whatsnew.entries(fh.read())
    assert rows and rows[-1][0] == __version__ and rows[-1][1] and rows[-1][2]
    assert all(not r[1].startswith("`") for r in rows)
    # 1.14.1: every version from 1.12 on tells the user in one sentence what is new (after the parentheses)
    late = [r for r in rows if whatsnew.parse_version(r[0]) >= (1, 12)]
    assert late and all(r[2] and "Nutzer" not in r[2][:8] for r in late), [r[0] for r in late if not r[2]]
    assert whatsnew.news(open(path, encoding="utf-8").read(), rows[-2][0]) == [rows[-1]]
