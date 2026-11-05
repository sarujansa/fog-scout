"""Update on start (fogscout/update.py) against real git repositories in a temp folder."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import update as up  # noqa: E402

pytestmark = pytest.mark.skipif(up.shutil.which("git") is None, reason="git not installed")


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                   env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
                            GIT_COMMITTER_EMAIL="t@t"))


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


@pytest.fixture
def repos(tmp_path):
    """origin (the GitHub repository), dev (someone pushing there), user (the user's clone)."""
    origin, dev, user = tmp_path / "origin.git", tmp_path / "dev", tmp_path / "user"
    git(tmp_path, "init", "--bare", "-b", "main", str(origin))
    git(tmp_path, "clone", str(origin), str(dev))
    write(dev / "fogscout" / "__init__.py", '__version__ = "1.0.0"\n')
    write(dev / "start.bat", "echo old\n")
    git(dev, "add", "-A")
    git(dev, "commit", "-m", "first")
    git(dev, "push", "origin", "HEAD:main")
    git(tmp_path, "clone", str(origin), str(user))

    def release(version="1.1.0", subject="Neue Funktion"):
        write(dev / "fogscout" / "__init__.py", f'__version__ = "{version}"\n')
        write(dev / "start.bat", f"echo {version}\n")
        git(dev, "commit", "-am", subject)
        git(dev, "push", "origin", "HEAD:main")
    return user, release


def head(repo):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()


def test_nothing_new(repos):
    user, _ = repos
    assert up.update(str(user)) == (up.NOTHING, "")


def test_updates_fast_forward_and_reports_versions(repos):
    user, release = repos
    release("1.1.0", "Ping unter dem Standort")
    code, msg = up.update(str(user))
    assert code == up.UPDATED
    assert "1.0.0 → 1.1.0" in msg and "Ping unter dem Standort" in msg
    assert (user / "start.bat").read_text() == "echo 1.1.0\n"
    assert up.update(str(user))[0] == up.NOTHING                      # second start: up to date


def test_own_changes_are_never_overwritten(repos):
    user, release = repos
    release()
    write(user / "start.bat", "echo my own change\n")
    code, msg = up.update(str(user))
    assert code == up.SKIPPED and "eigene Änderungen" in msg
    assert (user / "start.bat").read_text() == "echo my own change\n"


def test_runtime_files_do_not_block(repos):
    user, release = repos
    release()
    write(user / "settings.json", "{}")                               # untracked (gitignored in the project)
    assert up.update(str(user))[0] == up.UPDATED


def test_other_branch_is_left_alone(repos):
    user, release = repos
    release()
    git(user, "switch", "-c", "test-branch")
    code, msg = up.update(str(user))
    assert code == up.SKIPPED and "test-branch" in msg


def test_local_commits_prevent_update(repos):
    user, release = repos
    release()
    write(user / "notes.txt", "x")
    git(user, "add", "notes.txt")
    git(user, "commit", "-m", "local")
    before = head(user)
    code, msg = up.update(str(user))
    assert code == up.SKIPPED and "eigene Commits" in msg and head(user) == before


def test_offline_starts_old_version(repos):
    user, release = repos
    release()
    git(user, "remote", "set-url", "origin", str(user.parent / "does-not-exist.git"))
    code, msg = up.update(str(user))
    assert code == up.SKIPPED and "nicht erreichbar" in msg


def test_can_be_switched_off(repos):
    user, release = repos
    release()
    write(user / "settings.json", json.dumps({"auto_update": False}))
    assert up.update(str(user))[0] == up.SKIPPED
    assert (user / "start.bat").read_text() == "echo old\n"


def test_unpacked_copy_without_git(tmp_path):
    assert up.update(str(tmp_path))[0] == up.SKIPPED


# ------------------------------------------------------------------ packages
def test_packages_installed_only_when_requirements_change(tmp_path):
    root, venv = tmp_path, tmp_path / ".venv"
    venv.mkdir()
    write(root / "requirements.txt", "numpy\n")
    write(root / "requirements-extra.txt", "windows-capture==2.0.1\n")
    calls = []
    run = lambda args: calls.append(args) or 0                      # noqa: E731
    up.sync_packages(str(root), str(venv), run)
    assert len(calls) == 2
    assert "--no-deps" in calls[1] and "--no-deps" not in calls[0]  # extra package never pulls opencv-python
    assert all("--only-binary=:all:" in c for c in calls)            # 1.12.3: no setup.py run as administrator
    up.sync_packages(str(root), str(venv), run)
    assert len(calls) == 2                                           # unchanged: nothing to do
    write(root / "requirements.txt", "numpy\nnew-package\n")
    up.sync_packages(str(root), str(venv), run)
    assert len(calls) == 3 and calls[2][-1].endswith("requirements.txt")


def test_failed_install_is_retried_next_start(tmp_path):
    root, venv = tmp_path, tmp_path / ".venv"
    venv.mkdir()
    write(root / "requirements.txt", "numpy\n")
    msgs = up.sync_packages(str(root), str(venv), lambda args: 1)
    assert "nicht installiert" in msgs[0]
    calls = []
    up.sync_packages(str(root), str(venv), lambda args: calls.append(args) or 0)
    assert len(calls) == 1


def test_run_as_script_like_start_bat(repos):
    """start.bat runs `python fogscout\\update.py`: standalone, exit code 3 after an update, status for the log."""
    user, release = repos
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fogscout", "update.py")
    script = user / "fogscout" / "update.py"
    script.write_text(open(src, encoding="utf-8").read(), encoding="utf-8")   # untracked copy: does not block
    (user / ".venv").mkdir()
    release("2.0.0", "Große Änderung")
    r = subprocess.run([sys.executable, str(script)], capture_output=True)
    assert r.returncode == up.UPDATED
    status = (user / ".venv" / up.STATUS_FILE).read_text(encoding="utf-8")
    assert "1.0.0 → 2.0.0" in status and "Große Änderung" in status
    r = subprocess.run([sys.executable, str(script)], capture_output=True)
    assert r.returncode == up.NOTHING                                   # restarted start.bat: nothing more to do


# ------------------------------------------------------------------ "Nach Updates suchen" button
def test_check_changes_nothing(repos):
    user, release = repos
    state, msg, can = up.check(str(user))
    assert state == "current" and "1.0.0" in msg and not can
    release("1.2.0", "Knopf für Updates")
    before = head(user)
    state, msg, can = up.check(str(user))
    assert state == "available" and can and "1.0.0 → 1.2.0" in msg and "Knopf für Updates" in msg
    assert head(user) == before and (user / "start.bat").read_text() == "echo old\n"     # only looked


def test_check_reports_own_changes(repos):
    user, release = repos
    release()
    write(user / "start.bat", "echo mine\n")
    state, msg, can = up.check(str(user))
    assert state == "available" and not can and "eigene Änderungen" in msg


def test_check_other_branch(repos):
    user, _ = repos
    git(user, "switch", "-c", "test-branch")
    assert up.check(str(user))[0] == "error"


def test_button_update_works_even_if_start_update_is_off(repos, monkeypatch):
    user, release = repos
    release()
    write(user / "settings.json", json.dumps({"auto_update": False}))
    assert up.update(str(user))[0] == up.SKIPPED
    monkeypatch.setenv("DBDMS_FORCE_UPDATE", "1")                    # set by "Aktualisieren und neu starten"
    assert up.update(str(user))[0] == up.UPDATED


def test_the_version_of_a_revision_before_the_rename_is_read(repos):
    """1.9: up to 1.8.91 the package was dbdmapscout/ – the update message names both versions across the rename."""
    user, _release = repos
    dev = user.parent / "dev"
    git(dev, "mv", "fogscout", "dbdmapscout")
    write(dev / "dbdmapscout" / "__init__.py", '__version__ = "1.8.91"\n')
    git(dev, "commit", "-am", "old layout")
    git(dev, "push", "origin", "HEAD:main")
    assert up._version(str(user), "HEAD") == "1.0.0"
    git(user, "fetch", "origin", "main")
    assert up._version(str(user), "FETCH_HEAD") == "1.8.91"
    assert up._version(str(user), "HEAD~9") == "?"


def test_git_runs_without_hooks_fsmonitor_or_user_config(tmp_path, monkeypatch):
    """1.38.21 (audit SEC-2): start.bat runs update.py as administrator in a folder the user writes to, and git reads
    the user's global config (core.fsmonitor = any command, hooks path) and GIT_* variables from HKCU\\Environment.
    Every git call now disables hooks, the fsmonitor command and credential helpers on the command line (which beats
    every config file – the system/global config itself stays: Git for Windows keeps core.autocrlf there) and drops
    GIT_*/SSL_CERT_*/PYTHON* from the environment – proxies stay."""
    seen = {}

    class Done:
        returncode, stdout, stderr = 0, "ok", ""

    def fake_run(args, **kw):
        seen["args"], seen["env"] = args, kw["env"]
        return Done()
    monkeypatch.setattr(up.subprocess, "run", fake_run)
    monkeypatch.setenv("GIT_SSL_CAINFO", "C:/evil/ca.pem")
    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", "'core.fsmonitor=evil.exe'")
    monkeypatch.setenv("SSL_CERT_FILE", "C:/evil/ca.pem")
    monkeypatch.setenv("PYTHONPATH", "C:/evil")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy:3128")
    assert up._git(str(tmp_path), "fetch", "origin") == (0, "ok")
    args, env = seen["args"], seen["env"]
    assert args[0] == "git" and args[-2:] == ["fetch", "origin"]
    assert "core.fsmonitor=false" in args and any(a.startswith("core.hooksPath=") for a in args)
    hooks = next(a for a in args if a.startswith("core.hooksPath=")).split("=", 1)[1]
    assert hooks.startswith(str(tmp_path)) and not os.path.exists(hooks)          # nothing there to run
    assert "credential.helper=" in args and "GIT_CONFIG_NOSYSTEM" not in env and "GIT_CONFIG_GLOBAL" not in env
    assert env["GIT_TERMINAL_PROMPT"] == "0" and env["HTTPS_PROXY"] == "http://proxy:3128"
    assert not any(k in env for k in ("GIT_SSL_CAINFO", "GIT_CONFIG_PARAMETERS", "SSL_CERT_FILE", "PYTHONPATH"))
