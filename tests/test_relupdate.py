"""1.33 (.exe, stage 5): updates of the installed program from GitHub Releases – checked, never by themselves, the setup
only after its SHA-256 matched; the release job publishes only from main."""
import hashlib
import io
import json
import os
import re
import sys

import pytest

from fogscout import __main__ as entry
from fogscout import relupdate, restart

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP = b"MZ fake setup " * 1000
SUM = hashlib.sha256(SETUP).hexdigest()
BASE = relupdate.DOWNLOAD_PREFIX + "build-42/"


def _release(build=42, name="FogScout-Setup-1.33.exe", digest=True, **over):
    data = {"tag_name": f"build-{build}", "draft": False, "prerelease": False, "assets": [
        {"name": name, "size": len(SETUP), "browser_download_url": f"{relupdate.DOWNLOAD_PREFIX}build-{build}/{name}",
         **({"digest": "sha256:" + SUM} if digest else {})},
        {"name": name + ".sha256", "size": 90,
         "browser_download_url": f"{relupdate.DOWNLOAD_PREFIX}build-{build}/{name}.sha256"}]}
    data.update(over)
    return data


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


class FakeGitHub:
    """Only the URLs the updater may ask for; anything else fails the test."""

    def __init__(self, release=None, setup=SETUP, sha_text=None):
        self.release, self.setup = release or _release(), setup
        self.sha_text = sha_text if sha_text is not None else f"{SUM}  FogScout-Setup-1.33.exe\n"
        self.asked = []

    def open(self, req, timeout=None):
        url = req.full_url
        self.asked.append(url)
        assert req.get_header("User-agent") == relupdate.USER_AGENT
        if url == relupdate.API:
            return _Resp(json.dumps(self.release).encode())
        if url.endswith(".sha256"):
            return _Resp(self.sha_text.encode())
        if url.startswith(BASE) and url.endswith(".exe"):
            return _Resp(self.setup)
        raise AssertionError(f"unexpected request {url}")


def _info(tmp_path, build=40, version="1.32"):
    (tmp_path / relupdate.INFO_FILE).write_text(json.dumps({"build": build, "version": version, "commit": "abc"}),
                                               encoding="utf-8")
    return str(tmp_path)


def test_a_newer_build_is_offered_and_an_older_or_equal_one_is_not(tmp_path):
    root = _info(tmp_path)
    gh = FakeGitHub()
    state, msg, can, rel = relupdate.check(root, opener=gh)
    assert state == "available" and can and rel.build == 42 and rel.version == "1.33" and "1.32 → 1.33" in msg
    assert gh.asked == [relupdate.API]                       # looking is one request, nothing downloaded
    assert relupdate.check(_info(tmp_path, build=42), opener=FakeGitHub())[0] == "current"
    assert relupdate.check(_info(tmp_path, build=50), opener=FakeGitHub())[0] == "current"
    assert relupdate.own_build(str(tmp_path / "nothing")) == {}


@pytest.mark.parametrize("change", [
    {"tag_name": "v1.33"}, {"draft": True}, {"prerelease": True},
    {"assets": []},
])
def test_a_release_that_is_not_as_the_workflow_makes_it_is_refused(change, tmp_path):
    state, _msg, can, rel = relupdate.check(_info(tmp_path), opener=FakeGitHub(release=_release(**change)))
    assert state == "error" and not can and rel is None


def test_a_setup_from_anywhere_else_or_without_checksum_is_refused():
    other = _release()
    other["assets"][0]["browser_download_url"] = "https://example.com/FogScout-Setup-1.33.exe"
    for data in (other, _release(name="Setup.exe"), dict(_release(), assets=_release()["assets"][:1])):
        with pytest.raises(ValueError):
            relupdate.parse_release(data)
    big = _release()
    big["assets"][0]["size"] = relupdate.MAX_BYTES + 1
    with pytest.raises(ValueError):
        relupdate.parse_release(big)


def test_the_download_is_kept_only_when_its_sha256_matches(tmp_path):
    rel = relupdate.parse_release(_release())
    seen = []
    path = relupdate.download(rel, str(tmp_path), opener=FakeGitHub(), progress=lambda g, t: seen.append((g, t)))
    assert path == os.path.join(str(tmp_path), relupdate.UPDATE_DIR, "FogScout-Setup-1.33.exe")
    assert open(path, "rb").read() == SETUP and seen[-1] == (len(SETUP), len(SETUP))
    folder = os.path.dirname(path)
    for bad in (FakeGitHub(setup=SETUP[:-1] + b"X"),                      # changed on the way
                FakeGitHub(sha_text="0" * 64 + "  x\n"),                   # .sha256 says something else
                FakeGitHub(setup=SETUP + b"more")):                        # bigger than announced
        if os.path.exists(path):
            os.remove(path)
        with pytest.raises(ValueError):
            relupdate.download(rel, str(tmp_path), opener=bad)
        assert os.listdir(folder) == []                                     # nothing half or wrong stays


def test_the_two_checksums_must_agree(tmp_path):
    data = _release()
    data["assets"][0]["digest"] = "sha256:" + "1" * 64
    rel = relupdate.parse_release(data)
    with pytest.raises(ValueError):
        relupdate.download(rel, str(tmp_path), opener=FakeGitHub(release=data))
    rel = relupdate.parse_release(_release(digest=False))                   # no digest listed: the .sha256 decides
    assert relupdate.download(rel, str(tmp_path), opener=FakeGitHub())


def test_an_older_setup_in_the_update_folder_is_removed(tmp_path):
    folder = tmp_path / relupdate.UPDATE_DIR
    folder.mkdir(parents=True)
    (folder / "FogScout-Setup-1.32.exe").write_bytes(b"old")
    (folder / "notes.txt").write_text("keep", encoding="utf-8")
    relupdate.download(relupdate.parse_release(_release()), str(tmp_path), opener=FakeGitHub())
    assert sorted(os.listdir(folder)) == ["FogScout-Setup-1.33.exe", "notes.txt"]


@pytest.fixture
def update_folder(tmp_path, monkeypatch):
    exe_dir = tmp_path / "app"
    exe_dir.mkdir()
    monkeypatch.setattr(sys, "executable", str(exe_dir / "FogScout.exe"))
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    data = tmp_path / "data"
    monkeypatch.setenv("DBDMS_DATA_DIR", str(data))
    folder = data / relupdate.UPDATE_DIR
    folder.mkdir(parents=True)
    setup = folder / "FogScout-Setup-1.33.exe"
    setup.write_bytes(SETUP)
    return folder, setup


def test_the_setup_is_checked_again_right_before_it_starts(update_folder):
    """Audit H-3 (1.33.2: in the program itself): a setup changed or gone since the download is never started."""
    folder, setup = update_folder
    assert restart.setup_still_ours(str(setup), SUM, str(folder))
    assert restart.setup_still_ours(str(setup), SUM.upper(), str(folder))
    assert not restart.setup_still_ours(str(setup), "", str(folder))
    assert not restart.setup_still_ours(str(setup), "0" * 64, str(folder))
    elsewhere = folder.parent / setup.name                 # same bytes, but not in the update folder
    elsewhere.write_bytes(SETUP)
    assert not restart.setup_still_ours(str(elsewhere), SUM, str(folder))
    other = folder / "evil.exe"                            # in the folder, but not our setup name
    other.write_bytes(SETUP)
    assert not restart.setup_still_ours(str(other), SUM, str(folder))
    setup.write_bytes(SETUP + b"!")
    assert not restart.setup_still_ours(str(setup), SUM, str(folder))
    setup.unlink()
    assert not restart.setup_still_ours(str(setup), SUM, str(folder))


class _App:
    """Just what SettingsTab._release_install touches."""

    def __init__(self, data_dir):
        from fogscout import app_settings
        self.cls = app_settings.SettingsTab
        self.data_dir = data_dir
        self.status, self.logs, self.quits = [], [], []
        self.upd_status = type("V", (), {"set": lambda _s, v: self.status.append(v)})()

    def run(self, path, sha):
        fake = self
        obj = type("F", (self.cls,), {
            "__init__": lambda s: None, "_round_running": lambda s: False, "_clips_saving": lambda s: [],
            "_quit_phase1": lambda s, then: True, "quit": lambda s: fake.quits.append(True),
            "_log": lambda s, msg, kind="": fake.logs.append((kind, msg))})()
        obj.data_dir, obj.upd_status = self.data_dir, self.upd_status
        obj._release_install(path, sha)


def test_the_program_starts_the_checked_setup_itself_and_only_then_quits(update_folder, monkeypatch):
    """1.33.2 (Saru: after the update 1.33 → 1.33.1 python312.dll was gone): no helper from the program folder –
    it held the files the setup replaces. The program starts the setup itself with a log, then quits; the setup
    waits for the program's mutex (installer/fogscout.iss)."""
    from fogscout import app_settings
    folder, setup = update_folder
    monkeypatch.setattr(app_settings, "IS_WIN", True)
    started = []
    monkeypatch.setattr(restart, "_shell_open", lambda path, args: started.append((path, args)) or True)
    app = _App(str(folder.parent.parent))
    app.run(str(setup), SUM)
    (path, args), = started
    assert path == str(setup) and args[:4] == ["/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/update=1"]
    assert args[4] == f'/LOG="{os.path.join(str(folder), relupdate.LOG_FILE)}"'
    assert app.quits == [True]
    assert not hasattr(restart, "wait_and_install") and not hasattr(restart, "spawn_installer")


def test_a_changed_setup_or_a_failed_start_keeps_the_program_running(update_folder, monkeypatch):
    """Audit H-2/H-3: nothing is started from a changed file; when Windows cannot start the setup (declined prompt)
    Fog Scout stays open, says so with the path and can retry – it never quits into nothing."""
    from fogscout import app_settings
    folder, setup = update_folder
    monkeypatch.setattr(app_settings, "IS_WIN", True)
    monkeypatch.setattr(restart, "_shell_open", lambda path, args: False)
    app = _App(str(folder.parent.parent))
    app.run(str(setup), SUM)
    assert app.quits == [] and str(setup) in app.status[-1] and app.logs[-1][0] == "Fehler"
    monkeypatch.setattr(restart, "_shell_open", lambda *a: pytest.fail("a changed setup was started"))
    setup.write_bytes(b"changed")
    app.run(str(setup), SUM)
    assert app.quits == [] and "verändert" in app.status[-1]


def test_the_update_helper_entry_is_gone(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["FogScout.exe", "--install-update", "x.exe", SUM])
    with pytest.raises(SystemExit) as stop:
        entry.main()
    assert stop.value.code == 2                                         # argparse: unknown argument


def test_the_checked_checksum_travels_with_the_download(tmp_path):
    rel = relupdate.parse_release(_release())
    relupdate.download(rel, str(tmp_path), opener=FakeGitHub())
    assert rel.sha256 == SUM                                             # checked again before the start


def test_a_redirect_to_plain_http_is_refused():
    """Audit M-2: urllib follows https → http by default; the updater does not."""
    import urllib.error
    import urllib.request
    from fogscout import net
    handler = net.SafeRedirect()                      # 1.33.5: the program's one opener (net.py)
    assert isinstance(relupdate._opener(), urllib.request.OpenerDirector)
    req = urllib.request.Request("https://github.com/x")
    with pytest.raises(urllib.error.URLError):
        handler.redirect_request(req, None, 302, "Found", {}, "http://example.com/setup.exe")
    assert handler.redirect_request(req, None, 302, "Found", {}, "https://objects.githubusercontent.com/x")


class _Failing:
    def __init__(self, exc):
        self.exc = exc

    def open(self, req, timeout=None):
        raise self.exc


@pytest.mark.parametrize("exc", [
    __import__("urllib.error").error.URLError("no network"),
    __import__("urllib.error").error.HTTPError(relupdate.API, 403, "rate limit exceeded", {}, None),
    TimeoutError("timed out"),
])
def test_network_errors_and_rate_limits_are_an_error_state_never_a_crash(exc, tmp_path):
    state, msg, can, rel = relupdate.check(_info(tmp_path), opener=_Failing(exc))
    assert state == "error" and not can and rel is None and msg


def test_broken_release_metadata_is_an_error_state(tmp_path):
    class Garbage(FakeGitHub):
        def open(self, req, timeout=None):
            return _Resp(b"{not json")
    assert relupdate.check(_info(tmp_path), opener=Garbage())[0] == "error"
    assert relupdate.check(_info(tmp_path), opener=FakeGitHub(release=["no", "dict"]))[0] == "error"


def test_a_broken_connection_mid_download_leaves_nothing(tmp_path):
    class Breaks(FakeGitHub):
        def open(self, req, timeout=None):
            if req.full_url.endswith(".exe"):
                class R(_Resp):
                    def read(self, n=-1):
                        raise ConnectionResetError("reset")
                return R(b"")
            return super().open(req, timeout)
    with pytest.raises(OSError):
        relupdate.download(relupdate.parse_release(_release()), str(tmp_path), opener=Breaks())
    assert os.listdir(tmp_path / relupdate.UPDATE_DIR) == []


def test_the_update_folder_is_cleaned_at_start_but_only_of_our_files(tmp_path):
    """Audit M-3: the setup of an installed update (~120 MB) does not stay behind."""
    folder = tmp_path / relupdate.UPDATE_DIR
    folder.mkdir(parents=True)
    for name in ("FogScout-Setup-1.33.exe", "FogScout-Setup-1.34.exe.part", "readme.txt", "other.exe.part"):
        (folder / name).write_bytes(b"x")
    assert relupdate.clean_update_folder(str(tmp_path)) == 2
    assert sorted(os.listdir(folder)) == ["other.exe.part", "readme.txt"]
    (folder / relupdate.LOG_FILE).write_text("log", encoding="utf-8")
    relupdate.clean_update_folder(str(tmp_path))
    assert (folder / relupdate.LOG_FILE).exists()                       # the setup's log stays for diagnosis
    assert relupdate.clean_update_folder(str(tmp_path / "none")) == 0


def test_only_one_download_and_no_check_while_it_runs(monkeypatch):
    """Audit M-1: a second click while the setup downloads must not start a second writer of the same .part."""
    from fogscout import app_settings
    started = []
    monkeypatch.setattr(app_settings.threading, "Thread",
                        lambda target, **k: type("T", (), {"start": staticmethod(lambda: started.append(target))})())

    class Btn:
        def state(self, s):
            pass

        def pack_forget(self):
            pass

    class Fake(app_settings.SettingsTab):
        def __init__(self):
            self._release = relupdate.parse_release(_release())
            self.upd_btn = self.upd_apply_btn = Btn()
            self.upd_status = type("V", (), {"set": lambda self, v: None})()
            self.data_dir = "/nowhere"
            self.events = type("Q", (), {"put": staticmethod(lambda e: None)})()

        def _log(self, *a):
            pass

    f = Fake()
    f._release_download()
    f._release_download()
    f.check_update()
    assert len(started) == 1 and f._release_busy
    f._release_failed("x")
    assert not f._release_busy


def test_the_setup_starts_fog_scout_again_after_an_update_finished_or_not():
    with open(os.path.join(ROOT, "installer", "fogscout.iss"), encoding="utf-8") as fh:
        iss = fh.read()
    assert "Check: IsUpdate" in iss and "{param:update|0}" in iss
    assert relupdate.install_args()[-1] == "/update=1" and relupdate.install_args("x.log")[-1] == '/LOG="x.log"'
    code = iss[iss.index("\n[Code]"):]
    assert "procedure DeinitializeSetup" in code and "IsUpdate and (not Installed)" in code     # M-6
    assert "CurStep = ssPostInstall" in code and "UpdateWaitMs = 60000" in code
    assert "function InitializeUninstall" in code and "WizardSilent" in code


def test_only_a_push_to_main_publishes_and_only_that_job_may_write():
    with open(os.path.join(ROOT, ".github", "workflows", "build.yml"), encoding="utf-8") as fh:
        wf = fh.read()
    head, release = wf[:wf.index("\njobs:")], wf[wf.index("\n  release:"):]
    assert "permissions:\n  contents: read" in head
    assert "if: github.event_name == 'push' && github.ref == 'refs/heads/main'" in release
    assert len(re.findall(r"^ +contents: write$", wf, re.M)) == 1 and "    permissions:\n      contents: write" in release
    assert 'TAG: build-${{ github.run_number }}' in release and "sha256sum" in release and "--latest" in release
    assert "${{ github.event" not in release.split("run: |", 1)[1]           # no expression inside the script
    # 1.33.4: notes from HISTORY.md (checkout without a token), then only older build-<N> releases are removed
    assert "actions/checkout@11d5960a326750d5838078e36cf38b85af677262" in release
    assert "persist-credentials: false" in release and "tools/release_notes.py" in release
    assert 'gh release delete "$t" --cleanup-tag --yes' in release
    assert '[[ "$t" =~ ^build-[0-9]+$ ]] && [ "$t" != "$TAG" ]' in release
    assert release.index("gh release create") < release.index("gh release delete")   # the new one exists first
    # 1.33.5: tags left behind by releases deleted on the website go too – only build-<N>, never this one
    assert 'gh api -X DELETE "repos/$GH_REPO/git/refs/tags/$t"' in release
    assert release.count('[[ "$t" =~ ^build-[0-9]+$ ]] && [ "$t" != "$TAG" ]') == 2
    assert relupdate.TAG.match("build-123") and relupdate.SETUP.match("FogScout-Setup-1.33.exe")
    assert "build-info.json" in wf and "GITHUB_RUN_NUMBER" in wf
    with open(os.path.join(ROOT, "installer", "fogscout.spec"), encoding="utf-8") as fh:
        assert '"build-info.json"' in fh.read()
    assert re.search(r"/build-info\.json", open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read())
