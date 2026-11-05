"""1.38.27 (project review F1): one line about the session once DBD was closed (overview.session_text)."""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import history, official, overview  # noqa: E402
from fogscout.records import SESSION_GAP  # noqa: E402


def _round(t, seconds=600.0, **kw):
    return history.Round(t=t, seconds=seconds, map_id="coal", map="Coal Tower", **kw)


def test_the_session_that_just_ended_is_summed_up_in_one_line():
    """Rounds within SESSION_GAP form the session; an older session and custom/farming rounds stay out. Kills and
    bloodpoints appear only when the official data has them."""
    t0 = 1_700_000_000.0
    old = _round(t0 - 5 * 3600, role="killer")                             # yesterday's session
    a = _round(t0, role="killer")
    b = _round(t0 + 900, role="killer")
    c = _round(t0 + 1800, 300.0, custom=True)                               # custom: not counted
    d = _round(t0 + 2400, 700.0, role="killer")
    rounds = [old, a, b, c, d]
    assert overview.session_text(SimpleNamespace(rounds=rounds, off={}), t0 + 3200) == \
        ("Sitzung beendet", "3 Runden · 51:40")                              # first start → last end
    m1 = official.Match(t=t0, map="Coal Tower", role="killer", bp=20000)
    m1.__dict__["_kills"] = 3                                               # what official.kills() reads
    m2 = official.Match(t=t0 + 900, map="Coal Tower", role="killer", bp=12000)
    m2.__dict__["_kills"] = 4
    j = SimpleNamespace(rounds=rounds, off={id(a): m1, id(b): m2})
    title, text = overview.session_text(j, t0 + 3200)
    assert title == "Sitzung beendet" and text.startswith("3 Runden · 51:40 · Ø 3.5 Kills · ") and text.endswith(" BP")
    # one round alone, no official data; nothing without a normal round
    assert overview.session_text(SimpleNamespace(rounds=[a], off={}), t0 + 700) == ("Sitzung beendet", "1 Runde · 10:00")
    assert overview.session_text(SimpleNamespace(rounds=[c], off={}), t0 + 9000) is None
    assert overview.session_text(SimpleNamespace(rounds=[], off={}), t0) is None
    # a round further than the gap away starts a new session: only that one is reported
    e = _round(t0 + 2400 + 700 + SESSION_GAP + 1, role="survivor")
    assert overview.session_text(SimpleNamespace(rounds=rounds + [e], off={}), e.t + 601)[1] == "1 Runde · 10:00"
