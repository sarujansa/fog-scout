"""The editor's sequence (1.16): clips in play order on the output axis, the two clocks, split/trim/move, the
ruler's steps and the undo history – pure, no Qt."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import annotate, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402


def test_output_and_source_time_translate_both_ways_with_tempo():
    parts = [Part(10, 14), Part(2, 6, 2.0), Part(20, 21, 0.5)]        # 4 s + 2 s + 2 s
    assert sequence.duration(parts) == pytest.approx(8.0)
    assert sequence.starts(parts) == pytest.approx([0.0, 4.0, 6.0, 8.0])
    assert sequence.source_at(parts, 1.0) == (0, pytest.approx(11.0))
    assert sequence.source_at(parts, 5.0) == (1, pytest.approx(4.0))      # 1 s into a ×2 part = 2 s of source
    assert sequence.source_at(parts, 7.0) == (2, pytest.approx(20.5))
    assert sequence.source_at(parts, 8.0) == (2, pytest.approx(21.0))     # the very end stays in the last part
    assert sequence.source_at(parts, 99.0) == (2, 21.0)
    assert sequence.output_at(parts, 1, 4.0) == pytest.approx(5.0)
    assert sequence.occurrences([Part(0, 5), Part(3, 8)], 4.0) == pytest.approx([4.0, 6.0])   # a moment used twice
    assert sequence.source_at([], 3.0) == (None, 3.0) and sequence.index_at([], 1.0) is None


def test_split_trim_move_and_remove_reflow_the_sequence():
    parts = [Part(0, 10), Part(20, 30, 2.0)]
    cut, i = sequence.split(parts, 4.0)
    assert i == 1 and [(p.start, p.end) for p in cut] == [(0, 4.0), (4.0, 10), (20, 30)]
    cut2, j = sequence.split(cut, 12.0)                                    # 2 s into the ×2 part = 4 s of source
    assert j == 3 and (cut2[2].start, cut2[2].end, cut2[3].start, cut2[3].speed) == (20, 24.0, 24.0, 2.0)
    same, none = sequence.split(parts, 10.0)                               # on the edge: nothing
    assert none is None and same == parts
    same, none = sequence.split(parts, 0.05)                               # would leave a sliver
    assert none is None
    trimmed = sequence.trim(parts, 0, "start", 3.0, 40.0)
    assert (trimmed[0].start, trimmed[0].end) == (3.0, 10) and sequence.duration(trimmed) == pytest.approx(12.0)
    assert sequence.trim(parts, 0, "start", 9.99, 40.0)[0].start == pytest.approx(10 - sequence.MIN_LEN)
    assert sequence.trim(parts, 1, "end", 35.0, 32.0)[1].end == 32.0      # never past the recording
    assert sequence.trim(parts, 0, "start", -3.0, 40.0)[0].start == 0.0
    moved = sequence.move(parts, 1, 0)
    assert [p.start for p in moved] == [20, 0] and [p.start for p in sequence.move(moved, 0, 1)] == [0, 20]
    assert sequence.remove(parts, 0) == [parts[1]] and sequence.remove(parts, 5) == parts
    assert sequence.with_speed(parts, 1, 0.1)[1].speed == 0.25 and sequence.with_speed(parts, 1, 1.5)[1].speed == 1.5
    assert sequence.drop_index(parts, 0, 13.0) == 1 and sequence.drop_index(parts, 0, 9.0) == 0   # the other's middle: 12.5
    assert sequence.drop_index(parts, 1, -2.0) == 0 and sequence.drop_index([], 0, 1.0) == 0


def test_the_ruler_picks_a_step_that_keeps_labels_apart():
    step, minor = sequence.ruler_step(10.0)                                # 10 px/s: 10 s between labels
    assert step == 10.0 and minor == 5
    assert sequence.ruler_step(400.0)[0] == 0.5 and sequence.ruler_step(0.01)[0] == 3600.0
    for px in (0.5, 3, 20, 80, 300, 1000):
        step, _m = sequence.ruler_step(px)
        assert step * px >= sequence.LABEL_GAP_PX
    assert sequence.fmt_ruler(65.0, 5.0) == "1:05" and sequence.fmt_ruler(0.5, 0.5) == "0:00.5"
    assert sequence.fmt_ruler(3599.6, 1.0) == "60:00" and sequence.fmt_ruler(59.96, 0.5) == "1:00.0"


def test_the_history_undoes_redoes_and_joins_typing_into_one_step():
    first = sequence.EditState([Part(0, 10)])
    h = sequence.History(first)
    assert not h.can_undo() and not h.can_redo() and h.undo() is None
    assert not h.push(first.copy())                                        # nothing changed: no step
    s1 = sequence.EditState([Part(0, 5)])
    assert h.push(s1) and h.can_undo()
    shape = annotate.Shape("text", [(0.1, 0.1)], text="K")
    s2 = sequence.EditState([Part(0, 5)], shapes=[shape])
    h.push(s2, key=("text", 0))
    s3 = sequence.EditState([Part(0, 5)], shapes=[annotate.Shape("text", [(0.1, 0.1)], text="Ki")])
    h.push(s3, key=("text", 0))                                            # typing on: the same step
    assert h.undo() == s1 and h.redo() == s3
    assert h.undo() == s1 and h.undo() == first and h.undo() is None
    h.push(sequence.EditState([Part(2, 4)]))                                # a new change drops the redo branch
    assert not h.can_redo() and h.current.parts == [Part(2, 4)]
    h.push(sequence.EditState([Part(2, 4)], crop=(0, 0, 0.5, 0.5)), key="crop")
    h.undo()
    h.push(sequence.EditState([Part(2, 4)], crop=(0, 0, 0.6, 0.6)), key="crop")   # after an undo: a step of its own
    assert h.undo().crop is None
    copy = s2.copy()
    copy.shapes[0].text = "changed"
    assert s2.shapes[0].text == "K"                                        # snapshots hold copies
    small = sequence.History(first, kept=3)
    for i in range(6):
        small.push(sequence.EditState([Part(0, 1 + i)]))
    assert sum(1 for _ in iter(lambda: small.undo(), None)) == 2
