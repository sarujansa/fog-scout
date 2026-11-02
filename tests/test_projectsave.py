"""1.18.1: projectsave – the saving core of editor projects (Implementierungsplan Fassung 6, chapters 3 and 4).
Deterministic: waiting is done through events and an injected sleep/clock, never with time limits on the work."""
import errno
import json
import os
import random
import subprocess
import sys
import threading
import types

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import annotate, fsops, project, projectsave, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = b"k" * 32
WRITER = "0" * 32


def content(name="Clip", end=8.0):
    st = sequence.EditState([Part(2, end)], None, "none",
                            [annotate.Shape("arrow", [(0.1, 0.1), (0.2, 0.2)], t0=1.0, t1=4.0)], 0.0, 0.0, [], False,
                            "pixel")
    return project.content_dict(st, {"name": name})


def make_registry(tmp_path, **kw):
    kw.setdefault("sleep", lambda s: None)
    return projectsave.Registry(data_dir=str(tmp_path / "local"), key=KEY, writer=WRITER, **kw)


def main_path(tmp_path):
    folder = tmp_path / "Clips" / project.PROJECT_DIR
    folder.mkdir(parents=True, exist_ok=True)
    return str(folder / project.file_name2("rec.mkv", "p" * 32))


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def written_project(tmp_path, reg=None, name="Clip"):
    """A registry and a slot with a project file on disk (first write done)."""
    reg = reg or make_registry(tmp_path)
    path = main_path(tmp_path)
    slot, _mem = reg.claim(["p" * 32], "w1", path, "p" * 32)
    reg.submit(slot, "w1", content(name), view={"pos": 1.0, "span": 10.0, "offset": 0.0}, source={"file": "rec.mkv"})
    assert reg.wait_idle()
    assert os.path.exists(path) and slot.written_seq == 1
    return reg, slot, path


def _full_on(path):
    """write_tmp that fails with ENOSPC for the project's folder only (the local data folder is another disk)."""
    real = fsops.write_tmp
    folder = os.path.dirname(path)

    def write_tmp(p, data):
        if os.path.dirname(p) == folder:
            raise OSError(errno.ENOSPC, "no space")
        return real(p, data)
    return write_tmp


def backups(path, kind=None):
    folder = projectsave.backup_folder(path)
    if not os.path.isdir(folder):
        return []
    return sorted(n for n in os.listdir(folder) if n.endswith(".json")
                  and (kind is None or projectsave.parse_backup_name(n)["kind"] == kind))


# ---- writing, skipping, views
def test_a_change_is_written_once_and_identical_content_is_not_written_again(tmp_path):
    reg, slot, path = written_project(tmp_path)
    first = open(path, "rb").read()
    reg.submit(slot, "w1", content(), view={"pos": 1.0, "span": 10.0, "offset": 0.0})
    assert reg.wait_idle()
    assert open(path, "rb").read() == first and slot.written == [1] and slot.written_seq == 2
    assert projectsave.status_of(slot) == "saved"
    reg.submit(slot, "w1", content("Neu"))
    assert reg.wait_idle()
    assert load(path)["name"] == "Neu" and slot.written == [1, 3]
    assert len(backups(path, "sitzung")) == 1                                   # the state before, kept


def test_view_only_is_saved_on_a_save_event_and_never_on_a_seek(tmp_path):
    reg, slot, path = written_project(tmp_path)
    reg.submit(slot, "w1", content(), view={"pos": 7.0, "span": 10.0, "offset": 0.0}, view_event=False)   # a seek
    assert reg.wait_idle()
    assert load(path)["view"]["pos"] == 1.0 and slot.written == [1]
    reg.submit(slot, "w1", content(), view={"pos": 1.3, "span": 10.0, "offset": 0.0}, view_event=True)    # below 0.5 s
    assert reg.wait_idle()
    assert slot.written == [1]
    reg.submit(slot, "w1", content(), view={"pos": 7.0, "span": 12.0, "offset": 2.0}, view_event=True)    # closing
    assert reg.wait_idle()
    assert load(path)["view"] == {"pos": 7.0, "span": 12.0, "offset": 2.0} and slot.written == [1, 4]
    assert backups(path, "ansicht") == [] and backups(path, "sitzung") == []    # no lasting backup for a view


def test_content_and_view_together_are_one_write(tmp_path):
    reg, slot, path = written_project(tmp_path)
    reg.submit(slot, "w1", content("B"), view={"pos": 9.0, "span": 10.0, "offset": 0.0}, view_event=True)
    assert reg.wait_idle()
    d = load(path)
    assert d["name"] == "B" and d["view"]["pos"] == 9.0 and slot.written == [1, 2]


def test_a_view_alone_never_makes_a_project(tmp_path):
    reg = make_registry(tmp_path)
    path = main_path(tmp_path)
    c = content()
    slot, _m = reg.claim(["q" * 32], "w1", path, "q" * 32, base={"baseline_hash": project.content_hash(c)})
    reg.submit(slot, "w1", c, view={"pos": 5.0, "span": 10.0, "offset": 0.0}, view_event=True)
    assert reg.wait_idle()
    assert not os.path.exists(path) and projectsave.status_of(slot) == "new"


def test_a_failed_view_only_write_does_not_count_as_saved(tmp_path, monkeypatch):
    reg, slot, path = written_project(tmp_path)

    monkeypatch.setattr(projectsave.fsops, "write_tmp", _full_on(path))
    reg.submit(slot, "w1", content(), view={"pos": 8.0, "span": 10.0, "offset": 0.0}, view_event=True)
    assert reg.wait_idle()
    assert slot.written_seq == 1 and slot.disk_view["pos"] == 1.0
    assert slot.status == "error" and slot.reason == "full" and slot.rescued_seq == 2
    assert projectsave.status_of(slot) == "error_rescued"
    assert load(path)["view"]["pos"] == 1.0


def test_view_event_survives_coalescing(tmp_path):
    gate, reached = threading.Event(), threading.Event()

    def hook(slot, n):
        if n == 0 and not gate.is_set():
            reached.set()
            gate.wait(30)
    reg, slot, path = written_project(tmp_path)
    reg.hook = hook
    reg.submit(slot, "w1", content("busy"))                                    # holds the writer at step 0
    assert reached.wait(30)
    reg.submit(slot, "w1", content("busy"), view={"pos": 6.0, "span": 10.0, "offset": 0.0}, view_event=True)
    reg.submit(slot, "w1", content("busy"), view={"pos": 6.0, "span": 10.0, "offset": 0.0}, view_event=False)
    assert slot.pending.view_event is True
    gate.set()
    assert reg.wait_idle()
    assert load(path)["view"]["pos"] == 6.0


# ---- point 3: close and reopen while a write is slow
@pytest.mark.parametrize("variant", ["existing", "new", "first_fails"])
def test_closing_and_reopening_while_a_write_is_slow_never_loses_the_newer_state(tmp_path, monkeypatch, variant):
    gate, reached = threading.Event(), threading.Event()
    calls = []

    def hook(slot, n):
        if n == 0 and not gate.is_set():
            reached.set()
            gate.wait(30)
    if variant == "existing":
        reg, slot, path = written_project(tmp_path)
        reg.hook = hook
    else:
        reg = make_registry(tmp_path, hook=hook)
        path = main_path(tmp_path)
        slot, _m = reg.claim(["p" * 32, "src:rec.mkv"], "w1", path, "p" * 32)
    if variant == "first_fails":
        real = projectsave.fsops.write_tmp

        def once(*a, **k):
            if not calls:
                calls.append(1)
                raise OSError(errno.ENOSPC, "no space")
            return real(*a, **k)
        monkeypatch.setattr(projectsave.fsops, "write_tmp", once)
    s1 = reg.submit(slot, "w1", content("s1"))
    assert reached.wait(30)                                                   # the writer is held in that write
    s1b = reg.submit(slot, "w1", content("s1-closing"), view={"pos": 3.0, "span": 10.0, "offset": 0.0},
                     view_event=True)                                         # the window's last state on close
    reg.release(slot, "w1")
    slot2, memory = reg.claim(["src:rec.mkv", "p" * 32], "w2", path, "p" * 32)   # reopened at once
    assert slot2 is slot and memory is not None and memory.content["name"] == "s1-closing"   # from memory, not disk
    assert projectsave.status_of(slot2) in ("saving", "hang", "error", "error_rescued")
    s2 = reg.submit(slot2, "w2", content("s2"))
    assert reg.submit(slot, "w1", content("late from w1")) is None and reg.rejected == 1
    gate.set()
    assert reg.wait_idle()
    if variant == "first_fails":
        assert slot.status in ("error", "saved")
        slot.retry_at = None
        reg.submit(slot2, "w2", content("s2"))                                # the next change after the error
        assert reg.wait_idle()
    assert load(path)["name"] == "s2"
    assert slot.written == sorted(slot.written) and slot.written[-1] >= s2 > s1b > s1
    assert len([s for s in reg.slots if s.pid == "p" * 32]) <= 1
    files = [n for n in os.listdir(os.path.dirname(path)) if n.endswith(project.EXT)]
    assert files == [os.path.basename(path)]                                  # one project file, one id


# ---- conflicts: never overwrite, never recreate
def test_a_foreign_change_of_the_same_size_and_old_mtime_is_never_overwritten(tmp_path):
    reg, slot, path = written_project(tmp_path)
    st = os.stat(path)
    raw = bytearray(open(path, "rb").read())
    i = raw.index(b'"Clip"')
    raw[i + 1:i + 5] = b"Fake"                                                # same length
    open(path, "wb").write(bytes(raw))
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))                         # a sync client restoring the mtime
    reg.submit(slot, "w1", content("ours"))
    assert reg.wait_idle()
    assert open(path, "rb").read() == bytes(raw) and slot.status == "conflict"
    conflicts = backups(path, "konflikt")
    assert len(conflicts) == 1
    assert load(os.path.join(projectsave.backup_folder(path), conflicts[0]))["name"] == "ours"


def test_a_file_appearing_in_the_gap_is_kept_and_ours_becomes_a_conflict(tmp_path):
    reg, slot, path = written_project(tmp_path)

    def hook(s, n):
        if n == 5:                                                            # after the move aside, before create
            open(path, "wb").write(b"foreign")
    reg.hook = hook
    reg.submit(slot, "w1", content("ours"))
    assert reg.wait_idle()
    assert open(path, "rb").read() == b"foreign" and slot.status == "conflict"
    assert len(backups(path, "konflikt")) == 1 and len(backups(path, "sitzung")) == 1   # the old one is a backup


def test_an_externally_deleted_project_is_never_recreated(tmp_path):
    reg, slot, path = written_project(tmp_path)
    os.remove(path)
    for name in ("a", "b", "c"):
        reg.submit(slot, "w1", content(name))
        assert reg.wait_idle()
    assert not os.path.exists(path) and slot.status == "missing"
    local = projectsave.local_candidates(reg.local_folder(), projectsave.local_key(slot.pid, path))
    assert local and local[0][1] == "fehlt" and load(local[0][2])["name"] == "c"


def test_a_renamed_or_copied_project_file_is_offered_never_followed(tmp_path):
    reg, slot, path = written_project(tmp_path)
    other = os.path.join(os.path.dirname(path), "renamed" + project.EXT)
    os.rename(path, other)
    reg.submit(slot, "w1", content("x"))
    assert reg.wait_idle()
    assert slot.status == "missing" and slot.reason == "renamed" and not os.path.exists(path)
    assert load(other)["name"] == "Clip"                                       # the renamed one untouched
    twin = os.path.join(os.path.dirname(path), "twin" + project.EXT)
    open(twin, "wb").write(open(other, "rb").read())
    slot.status = "saved"
    reg.submit(slot, "w1", content("y"))
    assert reg.wait_idle()
    assert slot.status == "ambiguous" and load(other)["name"] == "Clip" and load(twin)["name"] == "Clip"


def test_an_unreachable_drive_is_an_error_not_a_deletion(tmp_path, monkeypatch):
    reg, slot, path = written_project(tmp_path)
    os.remove(path)
    monkeypatch.setattr(projectsave, "classify", lambda p: "drive")
    reg.submit(slot, "w1", content("x"))
    assert reg.wait_idle()
    assert slot.status == "error" and slot.reason == "drive" and slot.rescued_seq == 2


def test_a_briefly_missing_file_is_written_once_it_is_back(tmp_path):
    reg, slot, path = written_project(tmp_path)
    hidden = path + ".away"
    os.rename(path, hidden)
    looks = []

    def sleep(s):
        looks.append(s)
        if len(looks) == 1:
            os.rename(hidden, path)                                           # the sync client put it back
    reg.sleep = sleep
    reg.submit(slot, "w1", content("after"))
    assert reg.wait_idle()
    assert slot.status == "saved" and load(path)["name"] == "after" and looks[0] == projectsave.MISSING_LOOKS_S[0]


def test_classify_only_looks_at_the_project_path(tmp_path):
    proj = tmp_path / "A" / "Projekte"
    proj.mkdir(parents=True)
    f = proj / "x.json"
    f.write_text("{}")
    assert projectsave.classify(str(f)) == "ok"
    f.unlink()
    assert projectsave.classify(str(f)) == "missing"
    assert projectsave.classify(str(tmp_path / "gone" / "Projekte" / "x.json")) == "dir_missing"


# ---- disk errors, rescue, unwritable folders
def test_a_full_disk_leaves_the_file_and_rescues_locally(tmp_path, monkeypatch):
    reg, slot, path = written_project(tmp_path)
    before = open(path, "rb").read()

    monkeypatch.setattr(projectsave.fsops, "write_tmp", _full_on(path))
    reg.submit(slot, "w1", content("lost?"))
    assert reg.wait_idle()
    assert open(path, "rb").read() == before and slot.status == "error" and slot.reason == "full"
    local = projectsave.local_candidates(reg.local_folder(), projectsave.local_key(slot.pid, path))
    assert local[0][1] == "rettung" and load(local[0][2])["name"] == "lost?"
    assert [n for n in os.listdir(os.path.dirname(path)) if n.endswith(".tmp")] == []


def test_an_unwritable_project_folder_rescues_locally_and_the_copy_can_be_restored(tmp_path):
    reg = make_registry(tmp_path)
    blocker = tmp_path / "Clips"
    blocker.write_bytes(b"a file where the folder should be")
    path = str(blocker / project.PROJECT_DIR / "x--pppppppppp.fogscout-project.json")
    slot, _m = reg.claim(["p" * 32], "w1", path, "p" * 32)
    reg.submit(slot, "w1", content("rescued"))
    assert reg.wait_idle()
    assert slot.status == "error" and slot.rescued_seq == 1
    assert not os.path.exists(os.path.join(ROOT, "backup", "editor"))          # never the program folder
    local = projectsave.local_candidates(reg.local_folder(), projectsave.local_key(slot.pid, path))
    target = tmp_path / "ok" / "restored.json"
    target.parent.mkdir()
    projectsave.restore_copy(local[0][2], str(target))
    assert load(str(target))["name"] == "rescued"
    with pytest.raises(FileExistsError):
        projectsave.restore_copy(local[0][2], str(target))                     # never over a file


def test_a_successful_write_removes_the_rescue_copies_it_covers(tmp_path, monkeypatch):
    reg, slot, path = written_project(tmp_path)
    real = projectsave.fsops.write_tmp
    calls = []

    def once(*a, **k):
        if not calls:
            calls.append(1)
            raise OSError(errno.ENOSPC, "no space")
        return real(*a, **k)
    monkeypatch.setattr(projectsave.fsops, "write_tmp", once)
    reg.submit(slot, "w1", content("a"))
    assert reg.wait_idle()
    lkey = projectsave.local_key(slot.pid, path)
    assert [a for _s, a, _p in projectsave.local_candidates(reg.local_folder(), lkey)] == ["rettung"]
    slot.retry_at = None
    reg.submit(slot, "w1", content("b"))
    assert reg.wait_idle()
    assert slot.status == "saved" and projectsave.local_candidates(reg.local_folder(), lkey) == []


def test_a_hanging_slot_blocks_no_other_and_never_shows_saved(tmp_path):
    gate, reached = threading.Event(), threading.Event()
    now = [0.0]

    def hook(slot, n):
        if slot.pid == "a" * 32 and n == 0:
            reached.set()
            gate.wait(30)
    reg = make_registry(tmp_path, hook=hook, clock=lambda: now[0])
    folder = tmp_path / "P"
    folder.mkdir()
    a, _ = reg.claim(["a" * 32], "wa", str(folder / ("a" + project.EXT)), "a" * 32)
    b, _ = reg.claim(["b" * 32], "wb", str(folder / ("b" + project.EXT)), "b" * 32)
    reg.submit(a, "wa", content("a"))
    assert reached.wait(30)
    reg.submit(b, "wb", content("b"))
    tick = threading.Event()
    for _i in range(3000):                                                    # bounded: never hangs the run
        if b.written_seq == 1:
            break
        tick.wait(0.01)
    assert b.written_seq == 1 and os.path.exists(folder / ("b" + project.EXT))
    now[0] = projectsave.HANG_S + 1
    assert projectsave.status_of(a, now=now[0]) == "hang"
    reg.secure_all()                                                          # quit: the local copy secures it
    for _i in range(3000):
        if not reg.unsecured():
            break
        threading.Event().wait(0.01)
    assert reg.unsecured() == []
    gate.set()
    assert reg.wait_idle()


# ---- crashes at each step (child process, os._exit in the hook)
_KILL = r"""
import os, sys, json
sys.path.insert(0, sys.argv[1])
from fogscout import projectsave, project, sequence
from fogscout.clipedit import Part
path, step, local = sys.argv[2], int(sys.argv[3]), sys.argv[4]
def content(n):
    st = sequence.EditState([Part(2, 8)])
    return project.content_dict(st, {"name": n})
reg = projectsave.Registry(data_dir=local, key=b"k" * 32, writer="0" * 32, sleep=lambda s: None)
slot, _m = reg.claim(["p" * 32], "w", path, "p" * 32)
reg.submit(slot, "w", content("old"))
assert reg.wait_idle(), "first write"
def hook(s, n):
    if n == step:
        os._exit(7)
reg.hook = hook
reg.submit(slot, "w", content("new"))
reg.wait_idle()
print("survived")
"""


@pytest.mark.parametrize("step", [0, 2, 4, 5, 7, 8])
def test_a_crash_at_each_step_never_leaves_an_empty_or_half_file(tmp_path, step):
    """Fassung 6, 3.8 table: the main file is the old or the new state – or, killed between the move aside and the
    create, gone with the old state as a checked backup and the new one in a temp file; never half, never empty."""
    path = main_path(tmp_path)
    res = subprocess.run([sys.executable, "-c", _KILL, ROOT, path, str(step), str(tmp_path / "local")],
                         capture_output=True, text=True, timeout=120)
    assert res.returncode == 7, res.stdout + res.stderr
    folder = projectsave.backup_folder(path)
    if step in (0, 2, 4):
        assert load(path)["name"] == "old"
    elif step == 5:
        assert not os.path.exists(path)
        olds = backups(path, "sitzung")
        assert len(olds) == 1 and load(os.path.join(folder, olds[0]))["name"] == "old"
        side = projectsave.read_sidecar(os.path.join(folder, olds[0]) + projectsave.SIDECAR_EXT, KEY, WRITER)
        assert side is not None and side["file"] == olds[0]
        left = projectsave.leftovers(path)
        assert left and left[0][0] == 2 and load(left[0][1])["name"] == "new"
        projectsave.restore_copy(left[0][1], path)                            # only on the user's choice
        assert load(path)["name"] == "new"
        assert projectsave.adopt_leftovers(path, KEY, WRITER) == 1 and backups(path, "rest")
    else:
        assert load(path)["name"] == "new"
    if step == 4:                                                            # the sidecar exists, its file does not
        assert projectsave.clean_orphan_sidecars(folder, KEY, WRITER) == 1
    assert all(os.path.getsize(os.path.join(os.path.dirname(path), n)) > 0
               for n in os.listdir(os.path.dirname(path)) if n.endswith(project.EXT))


# ---- backups: rotation only with a valid own sidecar and the full hash
def _fill(folder, n, kind="sitzung", key=KEY, writer=WRITER):
    paths_ = []
    for i in range(n):
        paths_.append(projectsave.store_with_sidecar(str(folder), json.dumps({"i": i}).encode(), i + 1, kind, key, writer))
    return paths_


def test_rotation_keeps_the_newest_and_deletes_only_verified_old_ones(tmp_path):
    made = _fill(tmp_path, 12)
    _fill(tmp_path, 2, kind="konflikt")
    out = projectsave.rotate(str(tmp_path), KEY, WRITER)
    assert out["deleted"] == 2
    left = [n for n in os.listdir(tmp_path) if n.endswith(".json")]
    assert len([n for n in left if "-sitzung-" in n]) == 10 and len([n for n in left if "-konflikt-" in n]) == 2
    assert not os.path.exists(made[0]) and not os.path.exists(made[0] + projectsave.SIDECAR_EXT)


def test_a_backup_changed_under_the_same_name_is_never_deleted(tmp_path):
    made = _fill(tmp_path, 11)
    with open(made[0], "r+b") as fh:                                           # same length, other content
        raw = fh.read()
        fh.seek(0)
        fh.write(raw.replace(b"0", b"9"))
    out = projectsave.rotate(str(tmp_path), KEY, WRITER)
    assert out["deleted"] == 0 and out["protected"] == 1
    assert any("-spaet-geaendert-" in n for n in os.listdir(tmp_path))


@pytest.mark.parametrize("damage", ["missing", "broken", "forged_hash12", "other_key", "wrong_file"])
def test_a_backup_with_a_missing_or_tampered_sidecar_is_never_deleted(tmp_path, damage):
    made = _fill(tmp_path, 11)
    side = made[0] + projectsave.SIDECAR_EXT
    name = os.path.basename(made[0])
    raw = open(made[0], "rb").read()
    if damage == "missing":
        os.remove(side)
    elif damage == "broken":
        open(side, "wb").write(b"fogscout-backup 2\nsha256 short\n")
    elif damage == "forged_hash12":
        info = projectsave.parse_backup_name(name)
        fake = info["hash12"] + "0" * 52
        lines = open(side, encoding="utf-8").read().split("\n")
        lines[2] = "sha256 " + fake
        open(side, "w", encoding="utf-8").write("\n".join(lines))
    elif damage == "other_key":
        os.remove(side)
        open(side, "wb").write(projectsave.sidecar_bytes(name, projectsave.sha(raw), len(raw), WRITER, "sitzung",
                                                         b"x" * 32))
    elif damage == "wrong_file":
        os.remove(side)
        open(side, "wb").write(projectsave.sidecar_bytes("other.json", projectsave.sha(raw), len(raw), WRITER,
                                                         "sitzung", KEY))
    projectsave.rotate(str(tmp_path), KEY, WRITER)
    assert not os.path.exists(made[0])                                         # renamed, not deleted:
    kept = [n for n in os.listdir(tmp_path) if "-ohne-pruefsumme-" in n]
    assert len(kept) == 1 and open(os.path.join(tmp_path, kept[0]), "rb").read() == raw


def test_backups_of_another_installation_are_left_alone(tmp_path):
    made = _fill(tmp_path, 12, writer="f" * 32, key=b"o" * 32)
    out = projectsave.rotate(str(tmp_path), KEY, WRITER)
    assert out["deleted"] == 0 and all(os.path.exists(p) for p in made)


def test_an_orphan_sidecar_never_authorises_deleting_another_file(tmp_path):
    made = _fill(tmp_path, 11)
    raw = open(made[0], "rb").read()
    os.remove(made[0])                                                         # its file gone (crash)
    open(made[0], "wb").write(raw.replace(b"0", b"5"))                         # a foreign file under that name
    projectsave.clean_orphan_sidecars(str(tmp_path), KEY, WRITER)
    assert os.path.exists(made[0] + projectsave.SIDECAR_EXT)                   # its file exists: not an orphan
    projectsave.rotate(str(tmp_path), KEY, WRITER)
    assert any("-spaet-geaendert-" in n for n in os.listdir(tmp_path))          # not deleted
    os.remove(made[1])
    assert projectsave.clean_orphan_sidecars(str(tmp_path), KEY, WRITER) >= 1
    assert not os.path.exists(made[1] + projectsave.SIDECAR_EXT)


def test_leftovers_become_protected_rest_backups(tmp_path):
    path = main_path(tmp_path)
    good = fsops.write_tmp(path, json.dumps({"format": project.FORMAT, "rev": {"seq": 4}}).encode())
    junk_old = fsops.write_tmp(path, b"")
    os.utime(junk_old, (1, 1))
    junk_new = fsops.write_tmp(path, b"")
    assert projectsave.adopt_leftovers(path, KEY, WRITER) == 1
    assert not os.path.exists(good) and not os.path.exists(junk_old) and os.path.exists(junk_new)
    assert len(backups(path, "rest")) == 1


# ---- registry rules and the status
def test_a_second_window_does_not_take_over_an_owned_slot(tmp_path):
    reg = make_registry(tmp_path)
    path = main_path(tmp_path)
    slot, _m = reg.claim(["p" * 32], "w1", path, "p" * 32)
    other, owned = reg.claim(["p" * 32], "w2", path, "p" * 32)
    assert other is slot and owned is False and slot.owner == "w1"
    assert reg.submit(slot, "w2", content()) is None


def test_seq_grows_strictly_under_many_threads(tmp_path):
    reg = make_registry(tmp_path)
    slot, _m = reg.claim(["p" * 32], "w", main_path(tmp_path), "p" * 32)
    got = []
    lock = threading.Lock()

    def worker():
        for _i in range(200):
            s = reg.submit(slot, "w", content())
            with lock:
                got.append(s)
    ts = [threading.Thread(target=worker) for _i in range(8)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert sorted(got) == list(range(1, 1601))
    assert reg.wait_idle()
    assert slot.written == sorted(slot.written)


def test_saved_is_shown_only_when_the_newest_state_reached_the_disk():
    """A model of the status rule (3.9): random slot states, fixed seed – "saved" implies written_seq == latest_seq,
    no dirty window, no gesture, no error, conflict or missing file, nothing in flight."""
    rnd = random.Random(1801)
    statuses = ("saved", "error", "conflict", "missing", "ambiguous", "readonly")
    for _i in range(10000):
        latest = rnd.randint(0, 5)
        slot = types.SimpleNamespace(status=rnd.choice(statuses), latest_seq=latest,
                                     written_seq=rnd.randint(0, latest), rescued_seq=rnd.randint(0, latest),
                                     in_flight=rnd.choice([None, None, latest]),
                                     in_flight_since=rnd.choice([None, 0.0, 5.0]), has_file=rnd.random() < 0.8)
        dirty, gesture = rnd.random() < 0.2, rnd.random() < 0.1
        word = projectsave.status_of(slot, dirty, gesture, now=rnd.choice([0.0, 20.0]))
        if word == "saved":
            assert slot.written_seq == slot.latest_seq and not dirty and not gesture and slot.in_flight is None
            assert slot.status == "saved" and slot.has_file


# ---- 1.18.1: wiring into the editor
def test_a_hash_known_after_the_first_write_is_written_by_itself(tmp_path):
    """The editor may save before the recording's full hash is known: the next job with the hash writes it even when
    the content is the same (otherwise the next open could never assign the project automatically)."""
    reg, slot, path = written_project(tmp_path)
    assert slot.disk_meta == (None, None)
    n = len(slot.written)
    reg.submit(slot, "w1", content(), source={"file": "rec.mkv"})            # same content, still no hash: nothing
    assert reg.wait_idle() and len(slot.written) == n
    reg.submit(slot, "w1", content(), source={"file": "rec.mkv", "sha256": "a" * 64})
    assert reg.wait_idle() and len(slot.written) == n + 1
    assert load(path)["source"]["sha256"] == "a" * 64 and slot.disk_meta == ("a" * 64, None)
    reg.submit(slot, "w1", content(), source={"file": "rec.mkv", "sha256": "a" * 64})
    assert reg.wait_idle() and len(slot.written) == n + 1


def test_a_new_project_makes_its_folder_but_a_vanished_folder_is_never_made_again(tmp_path):
    reg = make_registry(tmp_path)
    folder = tmp_path / "Clips" / project.PROJECT_DIR
    path = str(folder / project.file_name2("rec.mkv", "q" * 32))
    slot, _m = reg.claim(["q" * 32], "w1", path, "q" * 32)
    reg.submit(slot, "w1", content(), source={"file": "rec.mkv"})
    assert reg.wait_idle() and os.path.exists(path)
    import shutil
    shutil.rmtree(folder)                                                    # the whole folder gone (drive, user)
    reg.submit(slot, "w1", content("later"), source={"file": "rec.mkv"})
    assert reg.wait_idle()
    assert not folder.exists() and slot.status in ("missing", "error")
