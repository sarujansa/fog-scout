"""Clip editor (1.5.1), the ffmpeg side: probing, single frames, the timeline's moments, cutting (stream copy and
frame exact), the sound stretch and the frame player – on a small clip ffmpeg generates itself. Skipped without
imageio-ffmpeg."""
import os
import subprocess
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, obsrec  # noqa: E402

FF = obsrec.ffmpeg_exe()
pytestmark = pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("clip") / "2026-10-17 21-40 Coal Tower – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=12:size=320x180:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=12",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-shortest", path], check=True, timeout=120)
    return path


@pytest.fixture(scope="module")
def two_track(tmp_path_factory):
    """A 1.8.5 recording with two audio tracks – track 1 with sound, track 2 (all but Discord) silent."""
    path = str(tmp_path_factory.mktemp("clip2") / "2026-10-18 20-10 Ormond – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=6:size=320x180:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a", "-map", "2:a",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-shortest", path], check=True, timeout=120)
    return path


@pytest.fixture(scope="module")
def four_track(tmp_path_factory):
    """1.8.6: a recording as OBS writes it with the four tracks – 1 everything (loud), 2 game (loud, 440 Hz),
    3 Discord (quiet, −20 dB), 4 microphone (silent)."""
    path = str(tmp_path_factory.mktemp("clip4") / "2026-10-18 20-30 Ormond – Nurse.mkv")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", "testsrc=duration=6:size=320x180:rate=30", "-f", "lavfi", "-i", "sine=frequency=440:duration=6",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=6", "-f", "lavfi", "-i", "sine=frequency=880:duration=6",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", "[3:a]volume=0.1[q]",
                    "-map", "0:v", "-map", "1:a", "-map", "2:a", "-map", "[q]", "-map", "4:a",
                    "-c:v", "libx264", "-preset", "veryfast", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-shortest", path], check=True, timeout=120)
    return path


def _max_volume(path, track=None):
    """Loudest moment of an audio track in dB (ffmpeg volumedetect); silence reads about -91 dB."""
    pick = [] if track is None else ["-map", f"0:a:{track}"]
    p = subprocess.run([FF, "-hide_banner", "-i", path, *pick, "-vn", "-af", "volumedetect", "-f", "null", "-"],
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=60)
    import re
    m = re.search(rb"max_volume: (-?[\d.]+) dB", p.stderr)
    return float(m.group(1)) if m else None


def test_probe_reads_length_size_and_frame_rate(clip, tmp_path):
    info = clipedit.probe(clip, FF)
    assert info.ok and 11.5 <= info.duration <= 12.5 and (info.width, info.height) == (320, 180) and info.fps == 30
    assert info.audio_tracks == 1                                                   # 1.8.5
    assert not clipedit.probe(str(tmp_path / "nothing.mkv"), FF).ok
    assert clipedit.scaled(info, 90) == (160, 90) and clipedit.scaled(info, 540) == (320, 180)   # never upscaled
    assert clipedit.scaled(clipedit.Info(), 90)[1] == 90


def test_a_single_frame_comes_as_a_small_picture(clip):
    info = clipedit.probe(clip, FF)
    t0 = time.time()
    img = clipedit.frame_at(clip, 7.5, height=90, info=info, ffmpeg=FF)
    assert img is not None and img.size == (160, 90) and img.mode == "RGB"
    assert time.time() - t0 < 5
    assert clipedit.frame_at(clip, 7.5, info=clipedit.Info(), ffmpeg=FF) is None     # nothing known: no picture
    a, b = clipedit.frame_at(clip, 1.0, 90, info, FF), clipedit.frame_at(clip, 9.0, 90, info, FF)
    assert a.tobytes() != b.tobytes()                                              # testsrc moves: other moment


def test_timeline_moments_names_and_positions():
    assert clipedit.thumb_times(10.0, 4) == [1.25, 3.75, 6.25, 8.75]
    assert clipedit.fmt_pos(192.46) == "3:12.5" and clipedit.fmt_pos(0) == "0:00.0" and clipedit.fmt_pos(-1) == "0:00.0"
    name = clipedit.clip_name("D:\\DBD\\2026-10-17 21-40 Coal Tower – Nurse.mkv", 192.4, 220.0)
    assert name == "2026-10-17 21-40 Coal Tower – Nurse – Clip 3m12s-3m40s"
    assert "/" not in clipedit.clip_name("a/b:c.mkv", 0, 1)


def test_cutting_by_copy_and_frame_exact(clip, tmp_path):
    out = clipedit.unique_path(str(tmp_path), "clip", ".mp4")
    ok, why = clipedit.cut(clip, 4.2, 7.9, out, "copy", FF)
    assert ok and why == "" and os.path.getsize(out) > 1000
    d = clipedit.probe(out, FF).duration
    assert 3.4 <= d <= 5.2                                            # starts at the key frame before 4.2 (GOP 1 s)
    out2 = clipedit.unique_path(str(tmp_path), "clip", ".mp4")
    assert out2.endswith("clip (2).mp4")
    ok, why = clipedit.cut(clip, 4.2, 7.9, out2, "exact", FF)
    assert ok and 3.5 <= clipedit.probe(out2, FF).duration <= 3.9     # frame exact: 3.7 s
    ok, why = clipedit.cut(clip, 5.0, 4.0, str(tmp_path / "x.mp4"), "copy", FF)
    assert not ok and "Ende" in why
    ok, why = clipedit.cut(str(tmp_path / "missing.mkv"), 0, 1, str(tmp_path / "y.mp4"), "copy", FF)
    assert not ok and why and not os.path.exists(str(tmp_path / "y.mp4"))
    ok, why = clipedit.cut(clip, 0, 1, str(tmp_path / "z.mp4"), "copy", FF, run=lambda a: (1, b"boom"))
    assert not ok and why == "boom"


def test_the_sound_stretch_is_a_wav(clip):
    wav = clipedit.sound_wav(clip, 2.0, 4.0, FF)
    try:
        assert wav and os.path.getsize(wav) > 44100 * 2 * 2 * 1.9 and open(wav, "rb").read(4) == b"RIFF"
    finally:
        if wav:
            os.remove(wav)
    assert clipedit.sound_wav(clip, 4.0, 2.0, FF) is None


def test_a_clip_is_mixed_from_the_recordings_own_tracks(four_track, two_track, tmp_path):
    """1.8.6: ``mix`` picks and levels the sources from OBS's tracks – one source as it is stays a stream copy,
    a level or several sources re-encode only the sound (also with censor boxes and in the preview sound); a 1.8.5
    two-track file still gives all or all-but-Discord."""
    assert clipedit.probe(four_track, FF).audio_tracks == 4 and obsrec.audio_tracks(four_track, FF) == 4
    assert _max_volume(four_track, 1) > -20 and -45 < _max_volume(four_track, 2) < -30 and _max_volume(four_track, 3) < -80
    out = lambda n: str(tmp_path / f"{n}.mp4")                                 # noqa: E731
    ok, why = clipedit.cut(four_track, 1.0, 3.0, out("mic"), "copy", FF, mix={"dbd": 0, "discord": 0, "mic": 1.0})
    assert ok, why
    assert clipedit.probe(out("mic"), FF).audio_tracks == 1 and _max_volume(out("mic")) < -80      # microphone only: silent
    ok, why = clipedit.cut(four_track, 1.0, 3.0, out("disc"), "copy", FF, mix={"dbd": 0, "discord": 1.0, "mic": 0})
    assert ok, why
    assert -45 < _max_volume(out("disc")) < -30                                                     # Discord only, as recorded
    ok, why = clipedit.cut(four_track, 1.0, 3.0, out("half"), "copy", FF, mix={"dbd": 0.5, "discord": 0, "mic": 0})
    assert ok, why
    assert -27 < _max_volume(out("half")) < -21                                                     # the game at −6 dB
    ok, why = clipedit.cut(four_track, 1.0, 3.0, out("both"), "copy", FF, mix={"dbd": 1.0, "discord": 1.0, "mic": 1.0})
    assert ok, why
    assert clipedit.probe(out("both"), FF).audio_tracks == 1 and _max_volume(out("both")) > -20
    ok, why = clipedit.cut(four_track, 1.0, 3.0, out("none"), "copy", FF, mix={"dbd": 0, "discord": 0, "mic": 0})
    assert ok, why
    assert clipedit.probe(out("none"), FF).audio_tracks == 0                                        # no sound at all
    ok, why = clipedit.cut(four_track, 1.0, 2.0, out("exact"), "exact", FF, censor=[[0.1, 0.1, 0.3, 0.3]],
                           mix={"dbd": 0, "discord": 0, "mic": 1.0})
    assert ok, why
    assert clipedit.probe(out("exact"), FF).audio_tracks == 1 and _max_volume(out("exact")) < -80
    assert clipedit.sound_wav(four_track, 1.0, 2.0, FF, mix={"dbd": 0, "discord": 0, "mic": 0}, n_tracks=4) is None
    wav = clipedit.sound_wav(four_track, 1.0, 2.0, FF, mix={"dbd": 0, "discord": 1.0, "mic": 0}, n_tracks=4)
    try:
        assert wav and -45 < _max_volume(wav) < -30
    finally:
        if wav:
            os.remove(wav)
    ok, why = clipedit.cut(two_track, 1.0, 3.0, out("legacy"), "copy", FF, mix={"dbd": 1.0, "discord": 0})
    assert ok, why
    assert _max_volume(out("legacy")) < -80                                                         # 1.8.5 file: track 2


def test_the_clip_window_mixes_the_sound_only_with_the_tracks_for_it(clip, four_track, tmp_path):
    """1.8.6: a four-track recording gets a box and a level per source (remembered, applied to the mix), a
    one-track recording only the hint."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    settings = {}
    win = qt_clip.ClipWindow(four_track, [], str(tmp_path / "Clips"), sound=False,
                             mix_on={"discord": False}, mix_vol={"dbd": 120},
                             on_setting=lambda k, v: settings.__setitem__(k, v))
    try:
        win.show()
        assert win.mix_hint.isHidden() and all(win.mix_boxes[k].isEnabled() for k in ("dbd", "discord", "mic"))
        assert win.mix() == {"dbd": 1.2, "discord": 0.0, "mic": 1.0} and win.mix_values["dbd"].text() == "120 %"
        win.mix_boxes["discord"].setChecked(True)
        win.mix_sliders["mic"].setValue(0)
        assert win.mix() == {"dbd": 1.2, "discord": 1.0, "mic": 0.0}
        assert settings["clip_mix_on"] == {"dbd": True, "discord": True, "mic": True, "other": True}
        assert settings["clip_mix_vol"] == {"dbd": 120, "discord": 100, "mic": 0, "other": 100}
        assert "Ton neu gemischt" in win.size_label.text()
        win.mix_boxes["dbd"].setChecked(False)
        win.mix_boxes["discord"].setChecked(False)
        assert "ohne Ton" in win.size_label.text()
        # 1.8.18 (user: "Discord hört man gar nicht"): a source whose track is silent says so – here the microphone
        assert clipedit.track_levels(four_track, 4, FF)[3] <= clipedit.SILENT_DB < clipedit.track_levels(four_track, 4, FF)[2]
        deadline = time.monotonic() + 20
        while not win._silent and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        assert win._silent == {"mic"} and "still" in win.mix_boxes["mic"].text()
        assert "still" not in win.mix_boxes["discord"].text() and win.mix_boxes["mic"].isEnabled()
        assert not win.mix_hint.isHidden() and "Mikrofon (Spur 4)" in win.mix_hint.text()
        from PySide6.QtCore import QPoint, QPointF, Qt
        from PySide6.QtGui import QWheelEvent
        from PySide6.QtWidgets import QAbstractSlider, QComboBox, QWidget

        def _wheel(w):                              # 1.11.13: the wheel guard sits on each widget, not on the app
            pos = QPointF(w.rect().center())
            app.sendEvent(w, QWheelEvent(pos, QPointF(w.mapToGlobal(pos.toPoint())), QPoint(0, 0), QPoint(0, -120),
                                         Qt.NoButton, Qt.NoModifier, Qt.NoScrollPhase, False))

        boxes = [w for w in win.findChildren(QWidget) if isinstance(w, (QComboBox, QAbstractSlider))
                 and not w.inherits("QScrollBar")]
        assert len(boxes) >= 3 + len(win.mix_sliders) and win.mix_sliders["mic"].isEnabled()
        for w in boxes:
            before = w.currentIndex() if isinstance(w, QComboBox) else w.value()
            if isinstance(w, QAbstractSlider):
                w.setValue(before := w.maximum() // 2)
            _wheel(w)
            assert (w.currentIndex() if isinstance(w, QComboBox) else w.value()) == before
    finally:
        win.close()
        app.processEvents()
    assert clipedit.track_levels(clip, 1, FF) == {}                                  # one track: nothing to tell
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    try:
        win.show()
        assert not win.mix_hint.isHidden() and win.mix_boxes["dbd"].isHidden() and win.mix() is None
        assert "Spur 1–4" in win.mix_hint.text()
    finally:
        win.close()
        app.processEvents()


def test_the_frame_player_streams_frames_at_the_files_pace_and_stops(clip):
    info = clipedit.probe(clip, FF)
    got, ended = [], threading.Event()
    pl = clipedit.FramePlayer(clip, 10.0, info, lambda t, img: got.append((t, img.size)), ended.set, height=90, ffmpeg=FF)
    t0 = time.monotonic()
    pl.start()
    assert ended.wait(10)
    took = time.monotonic() - t0
    assert got and got[0][1] == (160, 90) and abs(got[0][0] - 10.0) < 0.05 and got[-1][0] <= 12.1
    assert 1.5 <= took <= 4.0                                         # ~2 s of film took ~2 s
    # a stretch with an end, stopped early
    got, ended = [], threading.Event()
    pl = clipedit.FramePlayer(clip, 1.0, info, lambda t, img: got.append(t), ended.set, end=8.0, height=90, ffmpeg=FF)
    pl.start()
    time.sleep(0.6)
    pl.stop()
    assert ended.wait(5) and got and got[-1] < 3.0


def test_the_clip_window_shows_frames_cuts_at_the_marks_and_saves(clip, tmp_path):
    """1.5.1: the editor offscreen – thumbnails and a preview picture arrive from the threads, the range follows
    the first mark, I/O set start/end, the clip is written into "Clips" and reported."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)     # platform: conftest (offscreen on Linux only –
    # setting it here too made the Win32 window tests after this file run offscreen on Windows CI)
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    saved, settings, logs = [], {}, []
    clips = str(tmp_path / "Clips")
    win = qt_clip.ClipWindow(clip, [8.0], clips, mode="copy", sound=False, on_saved=saved.append,
                             on_setting=lambda k, v: settings.__setitem__(k, v), log=lambda t, k="System": logs.append((t, k)))
    try:
        win.show()
        assert win.info.ok and win.timeline.marks == [8.0]
        assert (win.timeline.start, win.timeline.end) == (0.0, pytest.approx(min(win.info.duration, 18.0)))   # 20 s before … 10 s after
        assert win.loading is not None and win.loading.isVisible() and not win.loading.finished   # 1.8.3: loading screen
        assert win.loading.geometry() == win.rect() and win.loading.bar.maximum() == clipedit.THUMBS + 1
        deadline = time.time() + 15
        while time.time() < deadline and not win.loading.finished:
            app.processEvents()
            time.sleep(0.02)
        assert win.loading.finished and win.loading.isHidden()       # gone once picture and strip are in, not by timeout
        assert win.loading.done_n == clipedit.THUMBS + 1 and "Bildern" in win.loading.detail.text()
        assert len(win.timeline.thumbs) == clipedit.THUMBS and not win.preview.pixmap().isNull()
        win.goto(3.0)
        win.set_start()
        win.goto(6.5)
        win.set_end()
        assert (win.timeline.start, win.timeline.end) == (3.0, 6.5) and "3.5 s" in win.range_label.text()
        assert win.name_edit.text().endswith("Clip 0m03s-0m06s")
        win.next_mark()
        assert win.timeline.pos == 8.0
        win.mode_box.setCurrentIndex(1)
        assert settings == {"clip_mode": "exact"}
        win.mode_box.setCurrentIndex(0)
        win.save()
        deadline = time.time() + 30
        while time.time() < deadline and not saved:
            app.processEvents()
            time.sleep(0.02)
        assert saved and saved[0].startswith(clips) and saved[0].endswith(".mp4") and os.path.getsize(saved[0]) > 1000
        assert "Gespeichert" in win.status.text() and logs and logs[-1][1] == "System"
        # playback: frames come, the playhead moves, pause stops it
        win.goto(1.0)
        win.toggle_play()
        assert win.playing and win.player is not None
        deadline = time.time() + 5
        while time.time() < deadline and win.timeline.pos < 1.3:
            app.processEvents()
            time.sleep(0.02)
        assert win.timeline.pos >= 1.3
        win.toggle_play()
        assert not win.playing and win.player is None
    finally:
        win.close()
        app.processEvents()


def test_the_discord_plan_fits_the_size_and_drops_resolution_when_room_is_short():
    info = clipedit.Info(duration=600, width=2560, height=1440, fps=60.0)
    kbps, h, fps = clipedit.discord_plan(30, 10, info)               # 30 s in 10 MB: ~2.3 Mbit/s
    assert 2000 <= kbps < 2500 and (h, fps) == (720, 30.0)
    assert (kbps + clipedit.AUDIO_KBPS) * 30 / 8 / 1024 < 10          # fits with room to spare
    assert clipedit.discord_plan(30, 500, info)[1:] == (1080, 60.0)   # Nitro: full HD, 60 fps
    assert clipedit.discord_plan(120, 10, info)[1] == 360             # two minutes in 10 MB: small picture
    small = clipedit.Info(duration=60, width=640, height=360, fps=24.0)
    assert clipedit.discord_plan(10, 500, small)[1:] == (360, 24.0)   # never bigger than the recording


def test_a_discord_cut_stays_under_its_target(clip, tmp_path):
    out = str(tmp_path / "d.mp4")
    ok, why = clipedit.cut(clip, 1.0, 9.0, out, "discord", target_mb=1, info=clipedit.probe(clip))
    assert ok, why
    assert os.path.getsize(out) < 1024 * 1024 and clipedit.probe(out).height <= 360


def test_the_clip_window_offers_discord_and_plays_just_the_clip(clip, tmp_path):
    """1.6.1: the format list has "Für Discord" with a target size (remembered), the size line says what comes
    out, "Clip ansehen" plays the clip and lands on its start again, the saved clip can be shown."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    saved, settings = [], {}
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), mode="discord", sound=False, on_saved=saved.append,
                             on_setting=lambda k, v: settings.__setitem__(k, v), target_mb=25)
    try:
        win.show()
        assert win.mode_box.currentData() == "discord" and not win.target_box.isHidden()
        assert win.target_box.currentData() == 25 and "unter 25 MB" in win.size_label.text()
        win.target_box.setCurrentIndex(0)
        assert settings == {"clip_target_mb": 10} and "unter 10 MB" in win.size_label.text()
        win.mode_box.setCurrentIndex(0)
        assert win.target_box.isHidden() and "MB" in win.size_label.text()
        win.goto(2.0)
        win.set_start()
        win.goto(3.0)
        win.set_end()
        win.watch_clip()
        assert win.playing and win.timeline.pos == 2.0
        deadline = time.time() + 10
        while time.time() < deadline and win.playing:
            app.processEvents()
            time.sleep(0.02)
        assert not win.playing and win.timeline.pos == 2.0             # back at the clip's start
        assert not win.show_btn.isEnabled()
        win.save()
        deadline = time.time() + 30
        while time.time() < deadline and not saved:
            app.processEvents()
            time.sleep(0.02)
        assert saved and win.show_btn.isEnabled() and "MB)" in win.status.text()
    finally:
        win.close()
        app.processEvents()


def test_the_strip_comes_from_parallel_key_frame_seeks(clip):
    """1.8.3 (user: "das Laden optimieren"; 1.7.1 streamed one run over the whole file): thumb_strip fetches every
    picture of the strip as a key frame, several at once, at the strip size; the order is the order of finishing;
    a stop ends it early. frame_at(keyframe=True) gives the key frame at or before the moment."""
    info = clipedit.probe(clip, FF)
    times = clipedit.thumb_times(info.duration, clipedit.THUMBS)
    t0 = time.time()
    got = list(clipedit.thumb_strip(clip, times, 54, info, FF))
    assert sorted(i for i, _img in got) == list(range(clipedit.THUMBS))
    assert all(img.size == (96, 54) and img.mode == "RGB" for _i, img in got)
    assert time.time() - t0 < 10
    by_index = dict(got)
    assert by_index[0].tobytes() != by_index[clipedit.THUMBS - 1].tobytes()   # key frames every second: the picture moves
    quick = clipedit.frame_at(clip, 7.5, 54, info, FF, keyframe=True)        # key frames at whole seconds (-g 30)
    assert quick is not None and quick.size == (96, 54)
    assert quick.tobytes() == clipedit.frame_at(clip, 7.0, 54, info, FF).tobytes()   # = the key frame at 7.0, not 7.5
    last = clipedit.frame_at(clip, info.duration - 0.2, 54, info, FF, keyframe=True)   # past the last key frame: the
    assert last is not None and last.tobytes() == clipedit.frame_at(clip, 11.0, 54, info, FF).tobytes()   # last one
    assert list(clipedit.thumb_strip(clip, times[:1], 54, info, FF)) == []       # one moment: nothing to space
    stopped = list(clipedit.thumb_strip(clip, times, 54, info, FF, stop=lambda: True))
    assert stopped == []


def test_censor_boxes_are_hidden_in_the_saved_clip(clip, tmp_path):
    """1.7.2 (user: censor the names on the left): names_box lies bottom left of the 16:9 game picture (shifted
    by the bars of a wider frame), the filter graph names every box, a black box really is black in the saved
    clip and the picture outside it stays, "copy" becomes a re-encode."""
    assert clipedit.names_box(2560, 1440) == pytest.approx(clipedit.NAMES_BOX)
    wide = clipedit.names_box(3440, 1440)                          # ultrawide: the game picture starts at 440 px
    nx, _ny, nw, _nh = clipedit.NAMES_BOX
    assert wide[0] == pytest.approx(440 / 3440 + nx * 2560 / 3440) and wide[2] == pytest.approx(nw * 2560 / 3440)
    assert clipedit.box_px((0.5, 0.5, 0.25, 0.25), 321, 181) == (160, 90, 80, 46)   # even, inside the frame
    g = clipedit.censor_graph([(0.1, 0.1, 0.2, 0.2), (0.5, 0.5, 0.1, 0.1)], "pixel", 320, 180, "scale=-2:90")
    assert g.count("overlay") == 2 and g.endswith("scale=-2:90[vout]") and "flags=neighbor" in g
    assert "drawbox" in clipedit.censor_graph([(0, 0, 0.5, 0.5)], "black", 320, 180)
    assert "boxblur" in clipedit.censor_graph([(0, 0, 0.5, 0.5)], "blur", 320, 180)
    info = clipedit.probe(clip, FF)
    out = str(tmp_path / "censored.mp4")
    ok, why = clipedit.cut(clip, 2.0, 4.0, out, "copy", FF, info=info, censor=[(0.0, 0.5, 0.5, 0.5)],
                           censor_style="black")
    assert ok, why
    img = clipedit.frame_at(out, 1.0, 180, info=clipedit.probe(out, FF), ffmpeg=FF)
    assert img is not None
    assert max(img.getpixel((40, 150))) < 24 and max(img.getpixel((200, 150))) > 60     # black box left, colour right
    for style in ("pixel", "blur"):
        ok, why = clipedit.cut(clip, 2.0, 3.0, str(tmp_path / f"{style}.mp4"), "discord", FF, target_mb=5,
                               info=info, censor=[clipedit.names_box(320, 180)], censor_style=style)
        assert ok, why


def test_the_clip_window_censors_with_remembered_boxes(clip, tmp_path):
    """1.7.2: the window shows remembered boxes, "Namen links unten" adds one and switches the censoring on,
    the tool draws/removes boxes, every change is saved as a setting, and saving passes the boxes to cut()."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    settings, saved = {}, []
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), mode="copy", sound=False, on_saved=saved.append,
                             on_setting=lambda k, v: settings.__setitem__(k, v), censor_on=False,
                             censor_boxes=[[0.5, 0.5, 0.2, 0.2]])
    try:
        win.show()
        assert win.preview.boxes == [[0.5, 0.5, 0.2, 0.2]] and not win.preview.active
        win._add_names_box()
        assert len(win.preview.boxes) == 2 and win.censor_box.isChecked() and settings["clip_censor_on"] is True
        assert settings["clip_censor_boxes"][1][0] == pytest.approx(clipedit.NAMES_BOX[0], abs=1e-3)
        assert "neu kodiert" in win.size_label.text()
        win.tool_btn.setChecked(True)
        win._tool_toggled()
        assert win.preview.editing
        deadline = time.time() + 15                                  # drawing needs the picture on display
        while time.time() < deadline and win.preview.pixmap().isNull():
            app.processEvents()
            time.sleep(0.02)
        assert not win.preview.pixmap().isNull()
        f = win.preview.frame_rect()                                 # draw a box by dragging on the picture

        def mouse(kind, fx, fy):
            pt = QPointF(f.left() + fx * f.width(), f.top() + fy * f.height())
            ev = QMouseEvent(kind, pt, pt, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            getattr(win.preview, {QMouseEvent.Type.MouseButtonPress: "mousePressEvent",
                                  QMouseEvent.Type.MouseMove: "mouseMoveEvent",
                                  QMouseEvent.Type.MouseButtonRelease: "mouseReleaseEvent"}[kind])(ev)
        mouse(QMouseEvent.Type.MouseButtonPress, 0.1, 0.1)
        mouse(QMouseEvent.Type.MouseMove, 0.3, 0.25)
        mouse(QMouseEvent.Type.MouseButtonRelease, 0.3, 0.25)
        assert len(win.preview.boxes) == 3 and win.preview.boxes[2] == pytest.approx([0.1, 0.1, 0.2, 0.15], abs=0.02)
        assert win.preview.selected == 2
        win.preview.remove_selected()
        assert len(win.preview.boxes) == 2 and len(settings["clip_censor_boxes"]) == 2
        win.style_box.setCurrentIndex(2)
        assert settings["clip_censor_style"] == "black" and win.preview.style == "black"
        calls = []
        real_cut = clipedit.cut
        qt_clip.clipedit.cut = lambda *a, **k: (calls.append(k), real_cut(*a, **k))[1]
        try:
            win.goto(1.0)
            win.set_start()
            win.goto(2.0)
            win.set_end()
            win.save()
            deadline = time.time() + 30
            while time.time() < deadline and not saved:
                app.processEvents()
                time.sleep(0.02)
        finally:
            qt_clip.clipedit.cut = real_cut
        assert saved and calls and calls[0]["censor_style"] == "black" and len(calls[0]["censor"]) == 2
        win.censor_box.setChecked(False)
        assert win._censor_args() == {} and "neu kodiert" not in win.size_label.text()
    finally:
        win.close()
        app.processEvents()


def test_the_retouch_style_paints_the_box_over_from_its_surroundings(clip, tmp_path):
    """1.7.3 (user: "retouch, make it unrecognisable"): delogo hides the box without a visible block; a box at
    the frame edge is moved EDGE_PX inwards (delogo refuses boxes touching the edge); the preview knows the style."""
    g = clipedit.censor_graph([(0.0, 0.5, 0.5, 0.5)], "retouch", 320, 180)
    assert g.startswith("[0:v]delogo=x=2:y=90:w=160:h=88[c0]") and g.endswith("null[vout]")
    info = clipedit.probe(clip, FF)
    out = str(tmp_path / "retouch.mp4")
    ok, why = clipedit.cut(clip, 2.0, 3.0, out, "copy", FF, info=info, censor=[clipedit.names_box(320, 180)],
                           censor_style="retouch")
    assert ok, why
    before = clipedit.frame_at(clip, 2.5, 180, info=info, ffmpeg=FF)
    after = clipedit.frame_at(out, 0.5, 180, info=clipedit.probe(out, FF), ffmpeg=FF)
    x, y, w, h = clipedit.box_px(clipedit.names_box(320, 180), 320, 180)
    inside = sum(abs(a - b) for px in ((x + w // 2, y + h // 2),) for a, b in zip(before.getpixel(px), after.getpixel(px)))
    outside = sum(abs(a - b) for a, b in zip(before.getpixel((250, 60)), after.getpixel((250, 60))))
    assert inside > 30 and outside < 30                     # changed inside the box, untouched outside
    assert "retouch" in clipedit.CENSOR_STYLES


def test_marking_a_recording_shows_the_compact_editor_beside_the_table(four_track, tmp_path):
    """1.8.8 (user: "click on it and a preview comes where I can play it and quickly edit, sound tracks on/off"):
    marking a row puts a compact clip editor beside the recordings table – picture, sources on/off, start/end,
    save; another row replaces it, no row hides it, "Grosser Editor" opens the full window at the same range."""
    if sys.platform == "win32":
        pytest.skip("Linux: the whole program offscreen (like tests/test_uimodel.py)")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    import json
    import shutil
    from PySide6.QtWidgets import QApplication
    from fogscout.app import App
    from fogscout.app_qt import ui_shown
    root = os.path.join(os.path.dirname(__file__), "..")
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.abspath(os.path.join(root, name)), tmp_path / name)
    (tmp_path / "sim").mkdir()
    folder = tmp_path / "rec"
    folder.mkdir()
    shutil.copy(four_track, folder / "one.mkv")
    t1 = time.time() - 600
    obsrec.save_index(str(folder), [obsrec.Recording(t=t1, file="one.mkv", label="Ormond", end=t1 + 6, size=1,
                                                     marks=[2.0])])
    (tmp_path / "settings.json").write_text(json.dumps({"rec_on": True, "rec_folder": str(folder),
                                                       "welcome_seen": True,
                                                       "clip_mix_on": {"discord": False}}), encoding="utf-8")
    app = App(str(tmp_path), simulate=str(tmp_path / "sim"))
    import threading
    probed = []                                                 # 1.12.3: (thread, ffmpeg really run?)
    real_run = clipedit._probe
    clipedit._probe = lambda *a: probed.append(threading.current_thread()) or real_run(*a)
    clipedit._PROBED.clear()
    try:
        qapp = QApplication.instance()
        app._rec_render()
        host = app.qt.host(str(app.rec_host))
        assert host is not None and host.content is None and not ui_shown(app.rec_host)
        app.rec_table.selection_set(repr(t1))
        app.rec_table.event_generate("<<TreeviewSelect>>")
        assert host.content is None                                 # 1.8.11: built a moment later
        deadline = time.time() + 3
        while time.time() < deadline and host.content is None:
            qapp.processEvents()
            time.sleep(0.01)
        ed = host.content
        assert ed is not None and ed.compact and not ed.isWindow() and ui_shown(app.rec_host)
        assert ed.info.audio_tracks == 4 and ed.mix() == {"dbd": 1.0, "discord": 0.0, "mic": 1.0}
        # 1.12.3 (audit): ffmpeg ran in the window's thread for every marked row – now in a thread, and only once
        assert len(probed) == 1 and probed[0] is not threading.main_thread()
        assert ed.mix_boxes["dbd"].isVisibleTo(ed) and not ed.mix_sliders["dbd"].isVisibleTo(ed)   # on/off only
        assert ed.expand_btn is not None and not ed.open_btn.isVisibleTo(ed)
        app._rec_buttons()                                          # the same row again: the same editor
        assert host.content is ed
        ed.timeline.set_range(1.0, 3.0)
        ed.goto(2.0)
        ed.expand_btn.click()
        full = app._clip_windows[-1]
        assert full is not ed and full.isWindow() and not full.compact
        assert (full.timeline.start, full.timeline.end) == (1.0, 3.0)
        assert len(probed) == 1 and full.info == ed.info and full.info is not ed.info    # the kept probe, a copy
        full.close()
        app.rec_table.selection_remove(repr(t1))
        app.rec_table.event_generate("<<TreeviewSelect>>")
        qapp.processEvents()
        assert host.content is None and not ui_shown(app.rec_host)
    finally:
        clipedit._probe = real_run
        app.quit()


def test_the_timeline_menu_sets_start_and_end_and_saves_a_still(clip, tmp_path):
    """1.8.10: right click on the strip – the clip starts/ends there, the playhead goes there, a still picture of
    that moment lands as PNG next to the clips."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QContextMenuEvent
    from PySide6.QtWidgets import QApplication
    from PIL import Image
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    clips = str(tmp_path / "Clips")
    win = qt_clip.ClipWindow(clip, [], clips, sound=False)
    try:
        win.show()
        tl = win.timeline
        tl.contextMenuEvent(QContextMenuEvent(QContextMenuEvent.Mouse, QPoint(tl.width() // 2, 20),
                                              tl.mapToGlobal(QPoint(tl.width() // 2, 20))))
        labels = [a.text() for a in tl._menu.actions() if not a.isSeparator()]
        assert len(labels) == 4 and labels[1].startswith("Clip beginnt hier  (0:0")
        tl._menu.close()
        tl.picked.emit("start", 2.0)
        tl.picked.emit("end", 5.0)
        assert (tl.start, tl.end) == (2.0, 5.0)
        tl.picked.emit("end", 1.0)                                 # before the start: ignored
        assert tl.end == 5.0
        tl.picked.emit("still", 3.0)
        deadline = time.time() + 10
        while time.time() < deadline and "Standbild gespeichert" not in win.status.text():
            app.processEvents()
            time.sleep(0.02)
        files = os.listdir(clips)
        assert len(files) == 1 and files[0].endswith(".png") and "Bild 0-03.0" in files[0]
        assert Image.open(os.path.join(clips, files[0])).size == (320, 180)       # full size of the recording
        assert win.show_btn.isEnabled()
    finally:
        win.close()
        app.processEvents()


def test_a_source_obs_did_not_have_says_so_instead_of_silent(four_track, tmp_path):
    """1.8.23 (user's pick 3): the recording's index entry names the sources OBS had – a silent track of a source
    that was not there (microphone off, no background source) is not reported as "OBS recorded nothing"."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    win = qt_clip.ClipWindow(four_track, [], str(tmp_path / "Clips"), sound=False, sources=["dbd", "discord"])
    try:
        win.show()
        deadline = time.monotonic() + 20
        while not win._absent and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        assert win._absent == {"mic"} and not win._silent
        assert "in OBS aus" in win.mix_boxes["mic"].text() and "still" not in win.mix_boxes["mic"].text()
        assert win.mix_hint.isHidden()                       # nothing is wrong with OBS here
        assert win.mix_boxes["mic"].isEnabled()
    finally:
        win.close()
        app.processEvents()


def test_threads_never_touch_qt_and_a_closed_editor_ignores_them(clip, four_track, tmp_path):
    """1.8.66 (user: "das Programm crasht ab und zu, wenn ich Videos öffne"): the worker threads emitted Qt signals
    of a QObject; a window closed while a thread still sent a frame, the strip or the levels gave "Signal source has
    been deleted" (seen in a stress run: another recording picked in the preview, the editor shut), and a deletion
    inside the emit took the whole program down. Now the threads only queue; the window's timer runs the handlers in
    the GUI thread, a closed window runs none – the same stress (many editors opened and dropped while their strip,
    levels, scrub and playback threads run) leaves no exception in any thread."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtCore import QCoreApplication, QEvent, QObject
    from fogscout import qt_clip, qt_window
    from fogscout.qt_pages import HostView
    app = qt_window.application()
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    assert not isinstance(win.bridge, QObject)                       # nothing Qt for the threads to hit
    seen = []
    win.bridge.handlers["levels"] = [lambda levels: seen.append((levels, threading.current_thread()))]
    t = threading.Thread(target=lambda: win.bridge.levels.emit({1: -5.0}))
    t.start()
    t.join()
    assert seen == []                                                # queued, not run in the thread
    deadline = time.time() + 10
    while not seen and time.time() < deadline:
        app.processEvents()
        time.sleep(0.01)
    assert seen == [({1: -5.0}, threading.main_thread())]            # the window's pump ran it in the GUI thread
    win.close()
    win.bridge.levels.emit({1: -6.0})
    for _ in range(10):
        app.processEvents()
        time.sleep(0.02)
    assert len(seen) == 1                                            # closed: pictures, levels … run no more
    saved = []
    win.on_saved = saved.append                                      # a save that ends after the window closed
    threading.Thread(target=lambda: win.bridge.saved.emit(True, str(tmp_path / "late.mp4"), "")).start()
    deadline = time.time() + 10
    while not saved and time.time() < deadline:
        app.processEvents()
        time.sleep(0.01)
    assert saved == [str(tmp_path / "late.mp4")]                     # still reaches the clips list
    errors = []
    old_hook = threading.excepthook
    threading.excepthook = lambda a: errors.append(f"{a.thread.name}: {a.exc_type.__name__}: {a.exc_value}")
    host = HostView()
    try:
        host.show()
        for n in range(12):                                           # the preview beside the recordings table
            w = qt_clip.ClipWindow((clip, four_track)[n % 2], [], str(tmp_path / "Clips"), sound=False, compact=True)
            host.set_content(w)
            if n % 3 == 0:
                w.toggle_play()
            end = time.time() + 0.05 * (n % 4)
            while time.time() < end:
                app.processEvents()
                time.sleep(0.005)
            QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        host.set_content(None)
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        deadline = time.time() + 20                                   # let the dropped editors' threads run out
        while time.time() < deadline and any(th.name.startswith("clip-") for th in threading.enumerate()):
            app.processEvents()
            time.sleep(0.05)
    finally:
        threading.excepthook = old_hook
        host.close()
        app.processEvents()
    assert errors == []


def test_marking_a_clip_shows_the_compact_editor_beside_the_clips_table(four_track, tmp_path):
    """1.11.4 (user: "Clips soll ebenfalls eine Vorschau wie normale Videos erhalten"): marking a clip puts the
    compact editor beside the clips table like a recording – with the sources of the recording the clip came from;
    a still hides it; "Grosser Editor" opens the full editor at the same range; leaving the tab stops it."""
    if sys.platform == "win32":
        pytest.skip("Linux: the whole program offscreen (like tests/test_uimodel.py)")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    import json
    import shutil
    from PySide6.QtWidgets import QApplication
    from fogscout.app import App
    from fogscout.app_qt import ui_shown
    root = os.path.join(os.path.dirname(__file__), "..")
    for name in ("maps", "models", "maps.json"):
        os.symlink(os.path.abspath(os.path.join(root, name)), tmp_path / name)
    (tmp_path / "sim").mkdir()
    folder = tmp_path / "rec"
    cdir = folder / obsrec.CLIPS_DIR
    cdir.mkdir(parents=True)
    shutil.copy(four_track, cdir / "one.mkv")
    (cdir / "still.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    t1 = time.time() - 600
    obsrec.save_index(str(folder), [obsrec.Recording(t=t1, file="gone.mkv", label="Ormond", end=t1 + 6, size=1,
                                                     extra={"sources": ["dbd", "discord", "mic"]})])
    obsrec.save_clips(str(cdir), [obsrec.Clip(file="one.mkv", t=t1 + 100, kind="instant", source=t1, label="Ormond",
                                              role="killer", killer="The Nurse", seconds=6.0),
                                  obsrec.Clip(file="still.png", t=t1 + 200, kind="still", source=t1, label="Ormond")])
    (tmp_path / "settings.json").write_text(json.dumps({"rec_on": True, "rec_folder": str(folder),
                                                       "welcome_seen": True,
                                                       "clip_mix_on": {"discord": False}}), encoding="utf-8")
    app = App(str(tmp_path), simulate=str(tmp_path / "sim"))
    try:
        qapp = QApplication.instance()
        app._rec_render()
        host = app.qt.host(str(app.clip_host))
        assert host is not None and host.content is None and not ui_shown(app.clip_host)
        rows = {app._clip_rows[i].file: i for i in app.clip_table.get_children()}
        app.clip_table.selection_set(rows["one.mkv"])
        app.clip_table.event_generate("<<TreeviewSelect>>")
        assert host.content is None                                 # built a moment later, like a recording
        deadline = time.time() + 3
        while time.time() < deadline and host.content is None:
            qapp.processEvents()
            time.sleep(0.01)
        ed = host.content
        assert ed is not None and ed.compact and not ed.isWindow() and ui_shown(app.clip_host)
        assert ed.info.audio_tracks == 4 and ed.mix() == {"dbd": 1.0, "discord": 0.0, "mic": 1.0}
        assert ed.expand_btn is not None
        app._clip_buttons()                                         # the same row again: the same editor
        assert host.content is ed
        ed.timeline.set_range(1.0, 3.0)
        ed.goto(2.0)
        ed.expand_btn.click()
        full = app._clip_windows[-1]
        assert full is not ed and full.isWindow() and not full.compact
        assert (full.timeline.start, full.timeline.end) == (1.0, 3.0)
        full.close()
        app.clip_table.selection_set(rows["still.png"])                   # a still: nothing to play
        app.clip_table.event_generate("<<TreeviewSelect>>")
        qapp.processEvents()
        assert host.content is None and not ui_shown(app.clip_host)
        app.clip_table.selection_set(rows["one.mkv"])
        app.clip_table.event_generate("<<TreeviewSelect>>")
        deadline = time.time() + 3
        while time.time() < deadline and host.content is None:
            qapp.processEvents()
            time.sleep(0.01)
        assert host.content is not None
        app._rec_preview_stop()                                     # leaving the tab stops the clip preview too
        assert not host.content.playing
    finally:
        app.quit()


# ------------------------------------------------------------------ 1.12: the edit plan
def test_the_tempo_chain_and_the_parts_are_cleaned():
    assert clipedit.atempo(1.0) == "anull" and clipedit.atempo(2.0) == "atempo=2"
    assert clipedit.atempo(0.25) == "atempo=0.5,atempo=0.5" and clipedit.atempo(4.0) == "atempo=2,atempo=2"
    parts = clipedit.clean_parts([clipedit.Part(8, 9), clipedit.Part(1, 1.05), clipedit.Part(2, 30, 9.0)], 12)
    assert [(p.start, p.end, p.speed) for p in parts] == [(2, 12, 4.0), (8, 9, 1.0)]
    e = clipedit.Edit([clipedit.Part(0, 4, 2.0), clipedit.Part(6, 8)])
    assert e.seconds() == pytest.approx(4.0) and not e.simple()
    assert clipedit.Edit([clipedit.Part(0, 4)]).simple()


def test_the_graph_cuts_parts_crops_draws_and_fades_in_that_order():
    info = clipedit.Info(12, 320, 180, 30, 1)
    e = clipedit.Edit([clipedit.Part(2, 4), clipedit.Part(6, 10, 2.0)], crop=(0.25, 0, 0.5, 1.0), fade_in=0.5,
                      fade_out=1.0)
    g, v, a, enc = clipedit.edit_graph(e, info, start=2.0, shape_inputs=[(1, 3.0, 5.0)])
    assert v == "[vout]" and a == "[aend]" and "libx264" in enc
    assert "overlay=0:0:format=auto:enable='between(t,1.000,3.000)'" in g      # 3–5 s of the recording, input from 2
    placed, _v, _a, _e = clipedit.edit_graph(e, info, 2.0, shape_inputs=[(1, None, None, 40, 12)])
    assert "[1:v]overlay=40:12:format=auto[vs0]" in placed                    # a drawing cut to its size, at its spot
    assert g.index("overlay") < g.index("crop=160:180:80:0") < g.index("split=2")   # drawn on the whole picture
    assert "trim=start=0.000:end=2.000" in g and "trim=start=4.000:end=8.000,setpts=(PTS-STARTPTS)/2" in g
    assert "atempo=2" in g and "concat=n=2:v=1:a=1" in g
    assert "fade=t=in:st=0:d=0.500" in g and "fade=t=out:st=3.000:d=1.000" in g and "afade=t=out" in g
    gif, _v, a2, enc2 = clipedit.edit_graph(e, info, 2.0, mode="gif")
    assert a2 is None and "palettegen" in gif and enc2 == [] and "atrim" not in gif
    d, _v, _a, enc3 = clipedit.edit_graph(clipedit.Edit([clipedit.Part(0, 4, 0.5)]), info, 0.0, mode="discord")
    assert "scale=-2:" in d and "-b:v" in enc3


def test_an_edit_with_parts_tempo_crop_drawings_and_fades_is_written(clip, tmp_path):
    """1.12: two parts (the second twice as fast), cut to 9:16-ish, an arrow for a second, faded – one mp4 of the
    right length and size with sound."""
    from fogscout import annotate
    e = clipedit.Edit([clipedit.Part(1, 3), clipedit.Part(5, 9, 2.0)], crop=(0.25, 0.0, 0.5, 1.0),
                      shapes=[annotate.Shape("arrow", [(0.3, 0.3), (0.6, 0.6)], t0=1.5, t1=2.5)],
                      fade_in=0.3, fade_out=0.3)
    out = str(tmp_path / "edit.mp4")
    ok, why = clipedit.export(clip, e, out, "copy", FF)
    assert ok, why
    info = clipedit.probe(out, FF)
    assert info.width == 160 and info.height == 180 and info.audio_tracks == 1
    assert info.duration == pytest.approx(4.0, abs=0.25)                      # 2 s + 4 s at double speed
    frame = clipedit.frame_at(out, 0.75, 180, info, FF)                       # 1.75 s of the recording: arrow on
    plain = clipedit.frame_at(clip, 1.75, 180, None, FF).crop((80, 0, 240, 180))
    assert frame is not None and plain is not None
    assert sum(abs(x - y) for x, y in zip(frame.convert("L").tobytes(), plain.convert("L").tobytes())) > 50_000


def test_drawings_go_to_ffmpeg_cut_to_their_size_and_land_on_their_spot(clip, tmp_path):
    """1.12 optimisation: each drawing is a PNG only as large as the drawing, laid at its spot (a full-size picture
    per drawing cost ffmpeg as much again); an empty text is left out. The arrow still lands where annotate draws
    it on the whole picture."""
    from PIL import Image, ImageChops
    from fogscout import annotate
    arrow = annotate.Shape("arrow", [(0.55, 0.2), (0.8, 0.7)], "#ff4d4d", 0.02)
    e = clipedit.Edit([clipedit.Part(1, 3)], shapes=[arrow, annotate.Shape("text", [(0.1, 0.1)], text="  ")])
    info = clipedit.probe(clip, FF)
    seen = []

    def run(args):
        pngs = [args[i + 1] for i, a in enumerate(args) if a == "-i" and args[i + 1].endswith(".png")]
        seen.extend(Image.open(p).size for p in pngs)
        seen.append(next(args[i + 1] for i, a in enumerate(args) if a == "-filter_complex"))
        import subprocess
        r = subprocess.run(args, capture_output=True)
        return r.returncode, r.stderr
    out = str(tmp_path / "drawn.mp4")
    ok, why = clipedit.export(clip, e, out, "exact", FF, run=run, info=info)
    assert ok, why
    (pw, ph), graph = seen
    x0, y0, _x1, _y1 = annotate.layer(info.width, info.height, [arrow]).getbbox()
    assert pw < info.width // 2 and ph < info.height and f"overlay={x0}:{y0}:" in graph
    frame = clipedit.frame_at(out, 1.0, 180, None, FF).convert("RGB")
    plain = clipedit.frame_at(clip, 2.0, 180, None, FF).convert("RGB")
    want = annotate.draw(plain, [arrow]).convert("RGB")
    mask = annotate.layer(*frame.size, [arrow]).getchannel("A").point(lambda v: 255 if v > 200 else 0)

    def off(a, b):                                                       # mean difference where the arrow is
        d = ImageChops.difference(a, b).convert("L")
        return sum(ImageChops.multiply(d, mask).tobytes()) / max(1, mask.histogram()[255])
    assert off(frame, want) < off(frame, plain) / 3                     # the arrow, and in the right place


def test_a_gif_and_a_simple_edit(clip, tmp_path):
    gif = str(tmp_path / "clip.gif")
    ok, why = clipedit.export(clip, clipedit.Edit([clipedit.Part(2, 4)], fade_in=0.2), gif, "gif", FF, gif_h=120)
    assert ok, why
    with open(gif, "rb") as fh:
        assert fh.read(6) in (b"GIF89a", b"GIF87a")
    from PIL import Image
    im = Image.open(gif)
    assert im.size[1] == 120 and getattr(im, "n_frames", 1) > 20
    simple = str(tmp_path / "simple.mkv")
    calls = []
    real = clipedit.cut
    try:
        clipedit.cut = lambda *a, **k: calls.append(a[4]) or real(*a, **k)
        ok, why = clipedit.export(clip, clipedit.Edit([clipedit.Part(2, 5)]), simple, "copy", FF)
    finally:
        clipedit.cut = real
    assert ok and calls == ["copy"]                                          # one part: stream copy as before


def test_the_clip_window_saves_parts_with_tempo_a_crop_a_drawing_and_a_gif(clip, tmp_path):
    """1.12 (user: "Bearbeitungstool top machen mit allen Funktionen"): parts with a tempo each, a 9:16 crop, an
    arrow from the playhead on, fades – the window's plan becomes one mp4 of the right length; a GIF too."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtWidgets import QApplication
    from fogscout import annotate, qt_clip
    app = QApplication.instance() or QApplication([])
    saved = []
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), mode="copy", sound=False, on_saved=saved.append)
    try:
        win.show()
        win.timeline.set_range(1.0, 3.0)
        win.add_part()
        win.timeline.set_range(5.0, 9.0)
        win.add_part()
        assert [(p.start, p.end) for p in win._parts] == [(1.0, 3.0), (5.0, 9.0)]
        assert win.timeline.parts == [(1.0, 3.0), (5.0, 9.0)] and "2 Abschnitte" in win.parts_hint.text()
        win.part_list.setCurrentRow(1)
        assert (win.timeline.start, win.timeline.end) == (5.0, 9.0)
        win.speed_box.setCurrentIndex(win.speed_box.findData(2.0))
        assert win._parts[1].speed == 2.0 and win.edit_plan().seconds() == pytest.approx(4.0)
        win.crop_box.setCurrentIndex(win.crop_box.findData("9:16"))
        assert win.preview.crop is not None and win.preview.crop_edit
        win.tools.setCurrentIndex(3)                                     # leaving the picture tab ends the crop tool
        assert not win.preview.crop_edit
        win.goto(1.5)
        win.draw_when_box.setCurrentIndex(win.draw_when_box.findData(1.0))
        win.preview._new_shape(annotate.Shape("arrow", [(0.4, 0.3), (0.5, 0.6)]))
        shape = win.preview.shapes[0]
        assert (shape.t0, shape.t1) == (1.5, 2.5)                          # from the playhead, for a second
        win.fade_out_box.setCurrentIndex(win.fade_out_box.findData(0.5))
        plan = win.edit_plan()
        assert plan.crop and len(plan.shapes) == 1 and plan.fade_out == 0.5 and not plan.simple()
        assert "neu kodiert" in win.size_label.text() and "Ausschnitt" in win.size_label.text()
        win.save()
        deadline = time.time() + 60
        while time.time() < deadline and not saved:
            app.processEvents()
            time.sleep(0.02)
        assert saved and saved[0].endswith(".mp4"), win.status.text()
        info = clipedit.probe(saved[0], FF)
        assert info.duration == pytest.approx(4.0, abs=0.3) and info.height == 180 and info.width < 120
        assert win.saved_seconds[saved[0]] == pytest.approx(4.0)
        win.mode_box.setCurrentIndex(win.mode_box.findData("gif"))
        assert win.gif_box.isVisibleTo(win) and "GIF" in win.size_label.text()
        win.save()
        deadline = time.time() + 60
        while time.time() < deadline and len(saved) < 2:
            app.processEvents()
            time.sleep(0.02)
        assert len(saved) == 2 and saved[1].endswith(".gif"), win.status.text()
    finally:
        win.close()
        app.processEvents()


def test_the_sound_line_beside_the_recordings_table_keeps_its_hint_below_the_sources(clip, four_track, tmp_path):
    """1.12.2 (user's screenshot: "Silent in this recording …" squeezed into a column of single words beside the
    sources, the format box cut off): the hint goes into a line of its own below the sources (indented to them), or
    beside the label when there are no sources; the format box shows its whole (short) name, the long one is the
    item's tip. Every source box sits in the window – a box added to a layout after it was placed got no parent."""
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication
    from fogscout import qt_clip
    app = QApplication.instance() or QApplication([])
    win = qt_clip.ClipWindow(four_track, [], str(tmp_path / "Clips"), sound=False, compact=True)
    try:
        win.resize(600, 820)
        win.show()
        deadline = time.monotonic() + 20
        while not win._silent and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        app.processEvents()
        assert win._silent == {"mic"} and not win.mix_hint.isHidden()
        for box in win.mix_boxes.values():
            assert box.window() is win and box.isVisibleTo(win)
        top = lambda w: w.mapTo(win, w.rect().topLeft())                     # noqa: E731
        assert top(win.mix_hint).y() > top(win.mix_boxes["dbd"]).y() + win.mix_boxes["dbd"].height() // 2
        assert abs(top(win.mix_hint).x() - top(win.mix_boxes["dbd"]).x()) <= 12   # indented to the sources
        assert win.mix_hint.width() > 300 and win.mix_hint.height() < 4 * win.fontMetrics().height()
        box = win.mode_box
        assert box.currentText() == qt_clip._(qt_clip.MODE_LABELS["copy"]) == "Schnell (ohne Neukodieren)"
        assert box.itemData(0, Qt.ToolTipRole).startswith("Schnell (an Schlüsselbildern")
        assert box.fontMetrics().horizontalAdvance(box.currentText()) < box.width()   # not cut off
    finally:
        win.close()
        app.processEvents()
    win = qt_clip.ClipWindow(clip, [], str(tmp_path / "Clips"), sound=False, compact=True)
    try:
        win.resize(600, 820)
        win.show()
        app.processEvents()
        label, hint = win.mix_label, win.mix_hint
        assert not hint.isHidden() and hint.window() is win
        assert abs(label.mapTo(win, label.rect().center()).y() - hint.mapTo(win, hint.rect().topLeft()).y()) \
            < 2 * win.fontMetrics().height()                                  # beside the label, not a line below
    finally:
        win.close()
        app.processEvents()
