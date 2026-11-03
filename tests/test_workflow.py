"""1.28 (audit F8): the CI workflow – read as text (no YAML package in the project): every action pinned to a full
commit SHA, older runs of a pull request cancelled (never on main), the Pythons start.bat accepts are the ones the
tests run on, and the jobs on 3.12 keep their old check names."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")


def _read(name):
    with open(os.path.join(WORKFLOWS, name), encoding="utf-8") as fh:
        return fh.read()


def test_every_action_is_pinned_to_a_full_commit_sha():
    for name in os.listdir(WORKFLOWS):
        if not name.endswith((".yml", ".yaml")):
            continue
        uses = re.findall(r"^\s*-?\s*uses:\s*(\S+)(.*)$", _read(name), re.M)
        assert uses, name
        for ref, comment in uses:
            assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", ref), (name, ref)
            assert re.search(r"#\s*v\d", comment), (name, ref, "the tag belongs in the comment")


def test_a_newer_push_cancels_only_runs_of_the_same_pull_request():
    text = _read("tests.yml")
    block = text[text.index("\nconcurrency:"):text.index("\njobs:")]
    assert "github.event.pull_request.number || github.ref" in block
    assert "cancel-in-progress: ${{ github.event_name == 'pull_request' }}" in block


def test_the_tests_run_on_every_python_start_bat_accepts():
    text = _read("tests.yml")
    linux = re.search(r"runs-on: ubuntu-latest.*?python: \[([^\]]*)\]", text, re.S).group(1)
    windows = re.search(r"runs-on: windows-latest.*?python: \[([^\]]*)\]", text, re.S).group(1)
    with open(os.path.join(ROOT, "start.bat"), encoding="utf-8", errors="replace") as fh:
        bat = fh.read()
    supported = re.findall(r"3\.1\d", re.search(r"Python (3\.1\d(?:, 3\.1\d)* oder 3\.1\d)", bat).group(1))
    assert re.findall(r"3\.1\d", linux) == supported                          # Linux: all of them
    win = re.findall(r"3\.1\d", windows)
    assert win == [supported[0], supported[-1]]                              # Windows: the lowest and highest
    assert "name: ${{ matrix.python == '3.12' && 'pytest'" in text            # required checks keep their names
    assert "name: ${{ matrix.python == '3.12' && 'windows'" in text
    assert "if: matrix.python == '3.12'" in text and "pyflakes fogscout tests tools" in text
