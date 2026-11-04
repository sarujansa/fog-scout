"""1.36: the start asks once after a real crash of the last run (diagnose.real_crash / last_crash,
SettingsTab._crash_check) – never for the C++ exceptions faulthandler writes on Windows although nothing crashed."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import diagnose  # noqa: E402

CAUGHT = ("Windows fatal exception: code 0xe06d7363\n\nThread 0x00001a2c (most recent call first):\n"
          '  File "qt_clip.py", line 10 in _paint\n')
REAL = ("Windows fatal exception: access violation\n\nCurrent thread 0x00002b10 (most recent call first):\n"
        '  File "qt_clip.py", line 20 in _show\n')


def test_only_real_crashes_count():
    assert not diagnose.real_crash("") and not diagnose.real_crash(CAUGHT)
    assert not diagnose.real_crash(CAUGHT + "Windows fatal exception: code 0x406d1388\n")
    assert diagnose.real_crash(REAL) and diagnose.real_crash(CAUGHT + REAL)
    assert diagnose.real_crash("Fatal Python error: Segmentation fault\n")
    assert diagnose.real_crash("Windows fatal exception: stack overflow\n")
    assert diagnose.real_crash("Windows fatal exception: code 0xc0000409\n")


def _stub(tmp_path):
    from fogscout import app_settings
    from fogscout.config import Settings

    class Root:
        def __init__(self):
            self.later = []

        def after(self, ms, fn):
            self.later.append(fn)

    class Stub(app_settings.SettingsTab):
        def __init__(self):
            self.data_dir = str(tmp_path)
            self.settings = Settings(str(tmp_path / "settings.json"))
            self.root = Root()
            self.asked, self.diag = [], 0

        def _save_soon(self):
            pass

        def _ask(self, title, text, retry, ok_text=None, **kw):
            self.asked.append(text)
            return self.answer

        def show_diagnose(self):
            self.diag += 1
    return Stub()


def test_the_start_asks_once_per_real_crash_and_copies_on_yes(tmp_path):
    s = _stub(tmp_path)
    s._crash_check()                                         # no crash file
    assert s.root.later == []
    path = tmp_path / diagnose.CRASH_LAST
    path.write_text(CAUGHT, encoding="utf-8")
    s._crash_check()                                         # only a caught C++ exception: no question
    assert s.root.later == []
    path.write_text(REAL, encoding="utf-8")
    os.utime(path, (1_800_000_000, 1_800_000_000))
    s._crash_check()
    assert len(s.root.later) == 1 and s.settings.get("crash_seen") == 1_800_000_000
    s.answer = False
    s.root.later[0]()
    assert len(s.asked) == 1 and "unerwartet beendet" in s.asked[0] and s.diag == 0
    s.answer = True
    s.root.later[0]()
    assert s.diag == 1
    s._crash_check()                                         # the same crash again: not asked twice
    assert len(s.root.later) == 1
