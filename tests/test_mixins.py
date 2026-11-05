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


def test_no_mixin_imports_another_mixin():
    """1.38.36 (project review ARCH-1): the mixins shared choices by importing them from each other (app_overlay from
    app_sysinfo and app_spotify, app_recordings from app_stats, app_settings from app_hotkeys …) – a web of imports
    between parts of one class. Shared values live in appconst; no app_*.py imports another, not even lazily."""
    import ast
    import glob
    import os
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fogscout")
    bad = []
    for path in sorted(glob.glob(os.path.join(root, "app_*.py"))):
        for node in ast.walk(ast.parse(open(path, encoding="utf-8").read())):
            if isinstance(node, ast.ImportFrom) and node.level == 1 and (node.module or "").startswith("app_"):
                bad.append(f"{os.path.basename(path)}:{node.lineno} from .{node.module}")
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module is None:
                bad += [f"{os.path.basename(path)}:{node.lineno} {a.name}" for a in node.names if a.name.startswith("app_")]
    assert bad == []
    from fogscout import app_hotkeys, app_overlay, app_spotify, app_stats, app_sysinfo, appconst
    assert app_sysinfo.SELECTABLE is appconst.SELECTABLE and app_hotkeys.HOTKEY_LABELS is appconst.HOTKEY_LABELS
    assert app_overlay.INFO_SPOTS is appconst.INFO_SPOTS and app_stats.STATS_PERIODS is appconst.STATS_PERIODS
    assert app_spotify.MEDIA_NEXT_N is appconst.MEDIA_NEXT_N
