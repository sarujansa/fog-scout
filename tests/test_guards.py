"""1.38.25 (project review, M16): three of CLAUDE.md's hard rules were culture, not code – no input to the game, no
network in detection and overlay, every event the threads post has a handler. These keep them."""
import ast
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = ROOT / "fogscout"

# Win32 calls that send input or messages to another window / process, and the Python packages that wrap them.
# fogscout never uses them (CLAUDE.md "Harte Regeln": keine Eingaben, kein PrintWindow, kein Prozesszugriff).
INPUT_APIS = ("SendInput", "keybd_event", "mouse_event", "PrintWindow", "SetWindowsHookEx", "SetWindowsHookExW",
              "PostMessage", "PostMessageW", "SendMessage", "SendMessageW", "SendMessageTimeout", "SendMessageTimeoutW",
              "PostThreadMessage", "WriteProcessMemory", "SendNotifyMessage")
INPUT_PACKAGES = ("pyautogui", "pynput", "pydirectinput", "keyboard", "mouse", "pywinauto")

# Detection and overlay never reach the network (CLAUDE.md: "Map-Erkennung und Overlay bauen keine Internetverbindung
# auf"); these modules, with everything they import, must stay away from the socket/HTTP layers.
OFFLINE_MODULES = ("worker", "detector", "ocr", "catalog", "textnorm", "matchend", "matchstart", "lobby",
                   "bloodpoints", "capture", "wincapture", "overlay", "overlay_win32", "overlay_qt", "layout", "skin",
                   "app_place", "preview", "mapimage", "mapstyle")
NETWORK = {"urllib", "socket", "http", "ssl", "webbrowser", "requests", "net", "ftplib", "smtplib", "asyncio"}


def _sources():
    return sorted(p for p in PKG.glob("*.py"))


def test_no_input_or_window_message_api_is_called():
    """Nothing in the package simulates input or sends a window message; no input package is imported."""
    api = re.compile(r"\.\s*(" + "|".join(INPUT_APIS) + r")\b")
    bad = []
    for path in _sources():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                if any(n.split(".")[0] in INPUT_PACKAGES for n in names):
                    bad.append(f"{path.name}:{node.lineno} import {names}")
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("#", 1)[0]
            if api.search(code):
                bad.append(f"{path.name}:{n} {code.strip()}")
    assert bad == []


def _imports(path: pathlib.Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:                                            # from . import x / from .x import y
                out.update([node.module.split(".")[0]] if node.module else [a.name for a in node.names])
            elif node.module:
                out.add(node.module.split(".")[0])
    return out


def test_detection_and_overlay_never_reach_the_network():
    """Transitively: a module of the detection or the overlay must not import (or import something that imports)
    the socket/HTTP layers – not even lazily inside a function."""
    graph = {p.stem: _imports(p) for p in _sources()}
    missing = [m for m in OFFLINE_MODULES if m not in graph]
    assert missing == [], missing                                     # a renamed module needs this list updated
    hits = {}
    for start in OFFLINE_MODULES:
        seen, todo = set(), [start]
        while todo:
            m = todo.pop()
            if m in seen:
                continue
            seen.add(m)
            for dep in graph.get(m, ()):
                if dep in NETWORK:
                    hits.setdefault(start, set()).add(f"{m} -> {dep}")
                elif dep in graph and dep not in seen:
                    todo.append(dep)
    assert hits == {}


def _string_constants(func: ast.FunctionDef) -> set:
    return {n.value for n in ast.walk(func) if isinstance(n, ast.Constant) and isinstance(n.value, str)}


def test_every_event_a_thread_posts_has_a_handler():
    """Every ``events.put(("kind", …))`` in the app and every ``self.post("kind", …)`` of the detection worker is
    named in App._dispatch or App._event – an unknown kind would fall through silently."""
    posted = {}
    for path in _sources():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            attr, owner = node.func.attr, node.func.value
            if attr == "put" and isinstance(owner, ast.Attribute) and owner.attr == "events" and node.args:
                first = node.args[0]
                if isinstance(first, ast.Tuple) and first.elts and isinstance(first.elts[0], ast.Constant):
                    posted.setdefault(first.elts[0].value, set()).add(path.name)
            if (attr == "post" and path.name == "worker.py" and node.args and isinstance(node.args[0], ast.Constant)
                    and isinstance(owner, ast.Name) and owner.id == "self"):
                posted.setdefault(node.args[0].value, set()).add(path.name)
    assert len(posted) >= 30, sorted(posted)                          # the scan found the real calls
    app = ast.parse((PKG / "app.py").read_text(encoding="utf-8"))
    handled = set()
    for node in ast.walk(app):
        if isinstance(node, ast.FunctionDef) and node.name in ("_dispatch", "_event"):
            handled |= _string_constants(node)
    unhandled = {k: sorted(v) for k, v in posted.items() if k not in handled}
    assert unhandled == {}
