"""1.34.2 (review W5): App is one object built from 16 mixins (~600 names on one ``self``). A method of the same name
in two of them silently hides one – whichever comes first in the class order wins, and nothing says so."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# (no QT_QPA_PLATFORM here: set at collection it made the whole run offscreen – test_windows needs real windows)

ALLOWED = {}            # name -> classes that define it on purpose (none today); say why when adding one


def test_no_name_is_defined_in_two_parts_of_the_app():
    from fogscout import app
    seen = {}
    for cls in app.App.__mro__:
        if not cls.__module__.startswith("fogscout"):
            continue
        for name in vars(cls):
            if not (name.startswith("__") and name.endswith("__")):
                seen.setdefault(name, []).append(cls.__name__)
    clashes = {n: c for n, c in seen.items() if len(c) > 1 and set(c) != set(ALLOWED.get(n, ()))}
    assert len(app.App.__mro__) > 10 and len(seen) > 400          # (the check still looks at the whole App)
    assert clashes == {}
