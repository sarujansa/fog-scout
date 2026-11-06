"""The recordings/clips index without OBS (recindex), 1.38.57 (security review): the index files are user-writable –
pruning deletes only recording files named in them, never an index, and one malformed line breaks nothing."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import recindex  # noqa: E402


def _write(path, data=b"\0" * 100):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def test_pruning_never_deletes_an_index_or_a_file_that_is_no_recording(tmp_path):
    folder = str(tmp_path)
    _write(os.path.join(folder, recindex.INDEX), b"{}\n" * 50)
    _write(os.path.join(folder, recindex.CLIPS_DIR, recindex.CLIPS_INDEX), b"{}\n" * 50)
    _write(os.path.join(folder, "notes.txt"))
    _write(os.path.join(folder, "r0.mkv"))
    recs = [recindex.Recording(t=1.0, file=recindex.INDEX),
            recindex.Recording(t=2.0, file="Clips/" + recindex.CLIPS_INDEX, farming=True),
            recindex.Recording(t=3.0, file="notes.txt", pre=recindex.INDEX),
            recindex.Recording(t=4.0, file="r0.mkv")]
    left, deleted = recindex.prune(folder, recs, limit=1, reserve=0, free=10 ** 9)
    assert deleted == ["r0.mkv"]
    for name in (recindex.INDEX, os.path.join(recindex.CLIPS_DIR, recindex.CLIPS_INDEX), "notes.txt"):
        assert os.path.exists(os.path.join(folder, name))
    left, deleted = recindex.prune_farming(folder, recs, days=1, now=10 ** 9)
    assert deleted == [] and os.path.exists(os.path.join(folder, recindex.CLIPS_DIR, recindex.CLIPS_INDEX))
    assert not recindex.deletable(recindex.OLD_INDEX) and not recindex.deletable("x/" + recindex.OLD_CLIPS_INDEX)
    assert recindex.deletable("Farming/2026-10-17 21-40 Coal Tower.MKV")


def test_a_malformed_index_line_is_skipped_or_coerced(tmp_path):
    folder = str(tmp_path)
    lines = [{"t": 1.0, "file": ["a"]},                                    # no file name: skipped
             {"t": 2.0, "file": ""},
             {"t": 3.0, "file": "b.mkv", "size": "x", "end": "y", "label": 5, "marks": [1, "z", 2.5, None],
              "keep": "yes", "extra": [1]},
             {"t": "soon", "file": "c.mkv", "pre": 7}]
    with open(os.path.join(folder, recindex.INDEX), "w", encoding="utf-8") as f:
        f.write("".join(json.dumps(d) + "\n" for d in lines))
    recs = recindex.load_index(folder)
    assert [r.file for r in recs] == ["b.mkv", "c.mkv"]
    b, c = recs
    assert (b.size, b.end, b.label, b.marks, b.keep, b.extra) == (0, 0.0, "", [1.0, 2.5], False, {})
    assert (c.t, c.pre) == (0.0, "")
    _write(os.path.join(folder, "b.mkv"))
    left, _deleted = recindex.prune(folder, recs, limit=0, reserve=0, free=10 ** 9)   # nothing breaks on them
    assert [r.file for r in left] == ["b.mkv"]
    assert recindex.space(folder, recs).count == 2
    cdir = recindex.clips_dir(folder)
    os.makedirs(cdir)
    with open(os.path.join(cdir, recindex.CLIPS_INDEX), "w", encoding="utf-8") as f:
        f.write(json.dumps({"file": {"x": 1}}) + "\n" + json.dumps({"file": "a.mp4", "seconds": "long"}) + "\n")
    clips = recindex.load_clips(cdir)
    assert [(c.file, c.seconds) for c in clips] == [("a.mp4", 0.0)]
