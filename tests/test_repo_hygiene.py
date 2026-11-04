"""The repository is public (security check, Oct 2026): no runtime files and nothing that looks like a secret in the
tracked files. A cheap guard, not a scanner – it only catches the obvious kinds again."""
import os
import re
import shutil
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CLAUDE.md "Laufzeitdateien, nicht committen"
RUNTIME = re.compile(r"(^|/)(settings\.json(\.broken)?|(fogscout|dbdmapscout)\.log|diagnose\.txt|rounds\.jsonl|"
                     r"official\.jsonl|update_status\.txt|(fogscout|dbdmapscout)-crash(-last)?\.txt|"
                     r"(fogscout|dbdmapscout)-matches.*\.json|(fogscout|dbdmapscout)-structure\.json)$|"
                     r"(^|/)(debug|user_maps|cache|backup|\.venv)/")
SECRET = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|"
                    r"github_pat_[A-Za-z0-9_]{40,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|"
                    r"sk-ant-(?:api|admin)\d{2}-[A-Za-z0-9_-]{40,}")      # review F-02: the user's own Claude key
TEXT = (".py", ".js", ".md", ".bat", ".txt", ".json", ".yml", ".yaml", ".cfg", ".toml", ".ini")


def _tracked():
    if not shutil.which("git") or not os.path.isdir(os.path.join(ROOT, ".git")):
        pytest.skip("not a git checkout")
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, timeout=30)
    if out.returncode != 0:
        pytest.skip("git ls-files failed")
    return [p for p in out.stdout.decode("utf-8", "replace").split("\0") if p]


def test_no_runtime_file_is_tracked():
    assert [p for p in _tracked() if RUNTIME.search(p)] == []


def test_no_tracked_text_file_holds_a_key_or_token():
    found = []
    for p in _tracked():
        if not p.lower().endswith(TEXT) or not os.path.isfile(os.path.join(ROOT, p)):
            continue
        with open(os.path.join(ROOT, p), encoding="utf-8", errors="replace") as fh:
            for n, line in enumerate(fh, 1):
                if SECRET.search(line):
                    found.append(f"{p}:{n}")                # the place only, never the value
    assert found == []


def test_an_anthropic_key_is_recognised_but_not_the_prefix_in_texts():
    """Review F-02: askclaude stores the user's own API key (sk-ant-…) – one pasted into a tracked file must be
    caught. The synthetic key is put together here at run time, so no line of this file matches itself; the
    prefix alone, as the program's texts name it, and a cut-off key are no alarm."""
    head = "sk-" + "ant-"
    assert SECRET.search(head + "api03-" + "A" * 80 + "-x_Q")
    assert SECRET.search("key = '" + head + "admin01-" + "b" * 48 + "'")
    for harmless in (head, head + "api03-", "beginnt mit " + head + ".", head + "api03-" + "x" * 12,
                     "(" + head + "…)"):
        assert not SECRET.search(harmless), harmless


def test_every_package_is_pinned_to_a_tested_version():
    """1.8.53 (user: pin the packages): start.bat installs with administrator rights – a new release of a package
    must never come in by itself, only after it was tested and written here."""
    loose = []
    for name in ("requirements.txt", "requirements-extra.txt", "requirements-build.txt",     # build: 1.31 (.exe)
                 "requirements-dev.txt"):                                                  # 1.34.2: the checks' tools
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                spec = line.split("#", 1)[0].split(";", 1)[0].strip()
                if spec and not re.fullmatch(r"[A-Za-z0-9_.\-]+==[0-9][0-9A-Za-z.\-]*", spec):
                    loose.append(f"{name}:{n}: {spec}")
    assert loose == []


PIP_VERSION = "26.2.1"


def test_ci_and_start_bat_install_only_pinned_tools():
    """1.34.2 (review W2): the checks installed the newest pytest/pyflakes and upgraded pip to whatever came out –
    start.bat too, with administrator rights. Now every pip install names a pinned file or the one pip version."""
    loose = []
    for name in (".github/workflows/tests.yml", ".github/workflows/build.yml", "start.bat"):
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                if " -m pip install" not in line:
                    continue
                if "--upgrade" in line or re.search(r"install(?: --only-binary=:all:)? pip(?!==)", line):
                    loose.append(f"{name}:{n}: {line.strip()}")
                for word in re.findall(r"(?<![-=\w])(pytest|pyflakes|pytest-timeout)(?![\w.=-])", line):
                    loose.append(f"{name}:{n}: {word} without a version")
                if " pip==" in line and f"pip=={PIP_VERSION}" not in line:
                    loose.append(f"{name}:{n}: another pip than {PIP_VERSION}")
    assert loose == []


def test_claude_md_stays_a_short_map_of_every_module():
    """1.34.2 (review W4): CLAUDE.md had grown to 133 KB with rows of up to 9 600 characters of version history
    (which belongs in HISTORY.md), and two modules were missing. Now: the rules, and per module what it does and
    which names to look for – every module in the first column of an architecture row, no row over 1 600 bytes,
    the whole file under 80 KB (the hard rules alone are ~27 KB and stay word for word)."""
    with open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8") as fh:
        text = fh.read()
    assert len(text.encode("utf-8")) < 80_000
    arch = text[text.index("## Architektur"):text.index("## Wichtige Designentscheidungen")]
    long_rows = [line[:60] for line in arch.splitlines() if len(line.encode("utf-8")) > 1600]
    assert long_rows == []
    first = " ".join(re.findall(r"(?m)^\| ([^|]+) \|", arch))
    modules = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, "fogscout")) if f.endswith(".py"))
    assert [m for m in modules if f"`{m}.py`" not in first] == []
