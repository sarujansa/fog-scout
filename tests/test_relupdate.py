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


def test_the_helper_installs_only_our_setup_after_the_program_ended(tmp_path, monkeypatch):
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
    states, launched = iter([True, True, False]), []
    assert restart.wait_and_install(str(setup), running=lambda: next(states),
                                    launch=lambda path, args: launched.append((path, args)))
    assert launched == [(str(setup), ["/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/update=1"])]
    elsewhere = tmp_path / "FogScout-Setup-1.33.exe"
    elsewhere.write_bytes(SETUP)
    other = folder / "evil.exe"
    other.write_bytes(b"x")
    for path in (elsewhere, other, folder / "FogScout-Setup-9.exe"):            # not ours / not there: nothing runs
        assert not restart.wait_and_install(str(path), running=lambda: False,
                                            launch=lambda *a: pytest.fail("started"))


def test_the_update_helper_runs_before_the_program(monkeypatch):
    import fogscout.restart as r
    seen = []
    monkeypatch.setattr(r, "wait_and_install", lambda path: seen.append(path) or True)
    monkeypatch.setattr(sys, "argv", ["FogScout.exe", "--install-update", "C:\\x\\FogScout-Setup-1.33.exe"])
    with pytest.raises(SystemExit) as stop:
        entry.main()
    assert stop.value.code == 0 and seen == ["C:\\x\\FogScout-Setup-1.33.exe"]


def test_the_setup_starts_fog_scout_again_only_after_an_update():
    with open(os.path.join(ROOT, "installer", "fogscout.iss"), encoding="utf-8") as fh:
        iss = fh.read()
    assert "Check: IsUpdate" in iss and "{param:update|0}" in iss
    assert relupdate.install_args()[-1] == "/update=1"


def test_only_a_push_to_main_publishes_and_only_that_job_may_write():
    with open(os.path.join(ROOT, ".github", "workflows", "build.yml"), encoding="utf-8") as fh:
        wf = fh.read()
    head, release = wf[:wf.index("\njobs:")], wf[wf.index("\n  release:"):]
    assert "permissions:\n  contents: read" in head
    assert "if: github.event_name == 'push' && github.ref == 'refs/heads/main'" in release
    assert len(re.findall(r"^ +contents: write$", wf, re.M)) == 1 and "    permissions:\n      contents: write" in release
    assert 'TAG: build-${{ github.run_number }}' in release and "sha256sum" in release and "--latest" in release
    assert "${{ github.event" not in release.split("run: |", 1)[1]           # no expression inside the script
    assert relupdate.TAG.match("build-123") and relupdate.SETUP.match("FogScout-Setup-1.33.exe")
    assert "build-info.json" in wf and "GITHUB_RUN_NUMBER" in wf
    with open(os.path.join(ROOT, "installer", "fogscout.spec"), encoding="utf-8") as fh:
        assert '"build-info.json"' in fh.read()
    assert re.search(r"/build-info\.json", open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read())
