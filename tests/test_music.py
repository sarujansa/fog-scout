"""1.21 (user: "eigene Tonspur" – eine Spur A2, Spielton automatisch leiser unter der Musik mit Regler, Ausblenden
am Ende; nur eigene Dateien): the track as data (musictrack.py), project format 5, the export graph, a real export
whose game sound ducks under the music, the preview's sound, and the editor's lane and section. Real ffmpeg / Qt
parts are skipped without imageio-ffmpeg / PySide6."""
import array
import json
import os
import subprocess
import sys
import wave

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, musictrack, obsrec, project, sequence  # noqa: E402
from fogscout.clipedit import Part  # noqa: E402
from fogscout.musictrack import AudioClip, MusicSpec  # noqa: E402

FF = obsrec.ffmpeg_exe()


def spec(path="m.mp3", **kw):
    s = MusicSpec([AudioClip(path, 1.0, 5.0, 8.0, 0.9), AudioClip(path, 6.0, 0.0, 2.0)])
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def test_the_track_round_trips_and_broken_clips_drop_out():
    d = musictrack.to_dict(spec())
    assert musictrack.from_dict(json.loads(json.dumps(d))) == spec()
    assert musictrack.to_dict(MusicSpec()) is None and musictrack.to_dict(None) is None
    bad = {"clips": [["a.mp3", 0, 3, 1], ["", 0, 0, 2], [3, 0, 0, 2], ["b.mp3", -1, 0, 2], ["c.mp3", "x", 0, 2],
                     ["d.mp3", 2, 0, 3, 99], ["e.mp3", 2.5, 0, 1]],
           "game_vol": "laut", "music_vol": 7, "duck": "maximal", "fade_in": -2, "fade_out": 99}
    got = musictrack.from_dict(bad)
    assert [c.path for c in got.clips] == ["d.mp3", "e.mp3"]
    assert got.clips[0].volume == musictrack.VOL_MAX
    assert got.clips[1].at == 5.0                                    # pushed behind the one before: no overlap
    assert (got.game_vol, got.music_vol, got.duck, got.fade_in, got.fade_out) == \
        (1.0, musictrack.VOL_MAX, "medium", 0.0, musictrack.FADE_MAX)
    assert musictrack.is_audio("Lied.MP3") and not musictrack.is_audio("bild.png")


def test_project_format_5_keeps_the_track_and_old_cuts_keep_their_hash():
    st = sequence.EditState([Part(1, 5)], music=spec())
    d = project.to_dict2(project.content_dict(st, {"name": "m"}), "a" * 32, {}, {}, None)
    assert d["version"] == project.CURRENT == 5 and len(d["music"]["clips"]) == 2
    back = project.validate(json.loads(json.dumps(d)), 60.0, [])[0]
    assert back.music == spec()
    assert "music" not in project.content_dict(sequence.EditState([Part(1, 5)]))
    assert back.copy().music is not back.music and back.copy().music == back.music


def test_the_window_and_the_chain(tmp_path):
    song = tmp_path / "song.mp3"
    song.write_bytes(b"x")
    s = spec(str(song))
    s.clips.append(AudioClip(str(tmp_path / "fehlt.mp3"), 9.0, 0, 1))       # a missing file drops out
    got = musictrack.window_inputs(s, 2.0, 5.0)                              # 2..7 of the finished clip
    assert [(round(ss, 3), round(t, 3), round(d, 3)) for _c, ss, t, d in got] == [(6.0, 2.0, 0.0), (0.0, 1.0, 4.0)]
    flt, label = musictrack.chain(s, 0.0, 10.0, 10.0, 3, "[a0]", tag="x")
    assert label == "[mxx]" and "[3:a]" in flt and "[4:a]" in flt and "adelay=1000:all=1" in flt
    assert "sidechaincompress=threshold=0.05:ratio=6" in flt and "amix=inputs=2:normalize=0:duration=first" in flt
    assert "(10.000-(t+0.000))/2.000" in flt                                 # the fade-out at the end of the cut
    off = musictrack.chain(spec(str(song), duck="off", fade_out=0), 0.0, 10.0, 10.0, 3, "[a0]")[0]
    assert "sidechaincompress" not in off and "/2.000" not in off
    assert musictrack.chain(spec(str(song)), 20.0, 5.0, 30.0, 1, None) == ("", "")     # nothing in the window
    alone = musictrack.chain(spec(str(song), game_vol=0.5), 20.0, 5.0, 30.0, 1, "[g]")
    assert alone == ("[g]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.500[mx]", "[mx]")
    assert musictrack.input_args(s, 2.0, 5.0)[:6] == ["-ss", "6.000", "-t", "2.000", "-i", str(song)]


def test_a_cut_with_a_track_is_never_the_stream_copy():
    assert clipedit.Edit([Part(0, 3)]).simple()
    assert not clipedit.Edit([Part(0, 3)], music=spec()).simple()


def _wav_levels(path, step=0.5):
    """RMS per ``step`` seconds of a 16-bit WAV."""
    with wave.open(path) as w:
        rate, ch = w.getframerate(), w.getnchannels()
        data = array.array("h", w.readframes(w.getnframes()))
    n = int(rate * step) * ch
    out = []
    for i in range(0, len(data) - n + 1, n):
        chunk = data[i:i + n]
        out.append((sum(v * v for v in chunk) / len(chunk)) ** 0.5)
    return out


def _tone(ff, path, seconds, freq, volume=1.0, video=False):
    src = ["-f", "lavfi", "-i", f"sine=frequency={freq}:duration={seconds}"]
    if video:
        subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        f"testsrc2=size=320x180:rate=30:duration={seconds}", *src, "-af", f"volume={volume}",
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                        path], check=True, timeout=120)
    else:
        subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", *src, "-af", f"volume={volume}", path],
                       check=True, timeout=120)


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_a_real_export_ducks_the_game_under_the_music_and_fades_out(tmp_path):
    src = str(tmp_path / "round.mp4")
    _tone(FF, src, 8, 440, volume=0.5, video=True)
    song = str(tmp_path / "song.wav")
    _tone(FF, song, 10, 1000, volume=0.5)
    info = clipedit.probe(src, FF)
    music = MusicSpec([AudioClip(song, 3.0, 0.0, 5.0)], music_vol=1.0, duck="strong", fade_in=0.0, fade_out=1.0)
    out = str(tmp_path / "cut.mp4")
    ok, why = clipedit.export(src, clipedit.Edit([Part(0, 8)], music=music), out, "exact", FF, info=info)
    assert ok, why
    got = clipedit.probe(out, FF)
    assert got.duration == pytest.approx(8.0, abs=0.2) and got.audio_tracks == 1
    wav = str(tmp_path / "out.wav")
    flt = "bandpass=f=440:width_type=q:w=8"                                  # the game's tone alone
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", out, "-af", flt, "-ac", "1", wav],
                   check=True, timeout=120)
    game = _wav_levels(wav)
    assert game[8] < game[2] * 0.6                                           # 4–4.5 s: ducked under the music
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", out, "-af",
                    "bandpass=f=1000:width_type=q:w=8", "-ac", "1", wav], check=True, timeout=120)
    song_lv = _wav_levels(wav)
    assert song_lv[2] < song_lv[8] * 0.2                                     # before 3 s: no music yet
    assert song_lv[15] < song_lv[12] * 0.6                                   # the last half second: fading out
    plain = str(tmp_path / "plain.mp4")                                      # without music: the game alone
    ok, why = clipedit.export(src, clipedit.Edit([Part(0, 2), Part(4, 6)]), plain, "exact", FF, info=info)
    assert ok, why


@pytest.mark.skipif(FF is None, reason="imageio-ffmpeg not installed")
def test_the_preview_sound_mixes_the_track_and_without_game_sound_too(tmp_path):
    src = str(tmp_path / "round.mp4")
    _tone(FF, src, 4, 440, volume=0.3, video=True)
    song = str(tmp_path / "song.wav")
    _tone(FF, song, 4, 1000, volume=0.5)
    music = MusicSpec([AudioClip(song, 0.0, 0.0, 4.0)], duck="off", fade_out=0.0)
    wav = clipedit.sound_wav(src, 0.0, 2.0, FF, n_tracks=1, music=(music, 0.0, 2.0, 2.0))
    try:
        assert wav and _wav_levels(wav)[1] > 300
    finally:
        os.remove(wav)
    silent = str(tmp_path / "silent.mp4")                                    # a recording without sound
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=320x180:rate=30:duration=3", "-c:v", "libx264", "-preset", "ultrafast", silent],
                   check=True, timeout=120)
    wav = clipedit.sound_wav(silent, 0.0, 2.0, FF, n_tracks=0, music=(music, 0.0, 2.0, 2.0))
    try:
        assert wav and _wav_levels(wav)[1] > 300
    finally:
        os.remove(wav)
    info = clipedit.probe(silent, FF)
    out = str(tmp_path / "silent-cut.mp4")
    ok, why = clipedit.export(silent, clipedit.Edit([Part(0, 2)], music=music), out, "exact", FF, info=info)
    assert ok, why and clipedit.probe(out, FF).audio_tracks == 1


# ---- the editor
@pytest.fixture
def win(tmp_path):
    if FF is None:
        pytest.skip("imageio-ffmpeg not installed")
    pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)
    from fogscout import qt_editor, qt_window
    clip = str(tmp_path / "2026-11-02 21-00 Midwich – Pinhead.mkv")
    _tone(FF, clip, 8, 440, video=True)
    song = str(tmp_path / "Lied.wav")
    _tone(FF, song, 20, 1000)
    app = qt_window.application()
    w = qt_editor.EditorWindow(clip, [], str(tmp_path / "Clips"), sound=False)
    w.resize(1400, 860)
    w.show()
    assert _pump(app, lambda: w.preview._img is not None and w._pstate != "loading")
    w.app, w.song = app, song
    yield w
    w._closing_asked = True
    w.close()


def _pump(app, until, seconds=30):
    import time
    end = time.time() + seconds
    while time.time() < end and not until():
        app.processEvents()
        time.sleep(0.01)
    return until()


def test_adding_moving_trimming_and_undo_on_a2(win):
    tl = win.timeline
    assert win._music is None and win.edit_plan().music is None
    win.goto(2.0)
    win._music_add(win.song, win.pos)
    assert _pump(win.app, lambda: win._music is not None)
    clip = win._music.clips[0]
    assert (clip.at, clip.start) == (2.0, 0.0) and clip.end == pytest.approx(win.timeline.total() - 2.0)  # to the end
    assert tl.music_sel == 0 and win.music_clip_row.isVisibleTo(win) and "Lied.wav" in win.music_clip_label.text()
    assert win._music_lengths[win.song] == pytest.approx(20.0, abs=0.1)
    plan = win.edit_plan()
    assert plan.music.clips[0].path == win.song and not plan.simple()
    tl.music_edited.emit([musictrack.AudioClip(win.song, 0.5, 0.0, 6.0)])  # a drag on A2 moved it
    assert win._music.clips[0].at == 0.5 and tl.music_sel == 0
    tl.select_music(0)
    tl._drag = ("m_trim_end", 0, list(tl.music))
    tl._music_trim_to("m_trim_end", tl._x(60.0))                           # past the file's end: stops there
    assert tl._drag[2][0].end == pytest.approx(20.0, abs=0.1)
    tl._drag = None
    win.duck_box.setCurrentIndex(win.duck_box.findData("strong"))
    win.music_vol.setValue(50)
    win.music_vol.setValue(40)                                             # a slider's drag: one undo step
    assert (win._music.duck, win._music.music_vol) == ("strong", 0.4)
    win.undo()
    assert win._music.music_vol == 0.8 and win._music.duck == "strong" and win.music_vol.value() == 80
    win.undo()
    win.undo()
    assert win._music.clips[0].at == 2.0
    win.undo()
    assert win._music is None and not tl.music
    win.redo()
    assert win._music.clips[0].at == 2.0
    tl.select_music(0)
    win.delete_selected()                                                  # Entf on A2 removes the music clip
    assert win._music is None and len(win.parts) == 1


def test_the_music_menu_and_a_drop_on_a2(win, tmp_path):
    tl = win.timeline
    tl.music_dropped.emit(win.song, 1.0)
    assert _pump(win.app, lambda: win._music is not None)
    tl.picked.emit("m_volume", 1.5, 0)
    assert win._music.clips[0].volume == 1.5
    win.goto(3.0)
    tl.picked.emit("m_here", win.pos, 0)
    assert win._music.clips[0].at == 3.0
    picture = tmp_path / "bild.png"
    picture.write_bytes(b"x")
    tl.music_dropped.emit(str(picture), 0.0)                               # not a sound file: refused
    assert len(win._music.clips) == 1 and "Keine Ton" in win.status.text()
    tl.picked.emit("m_remove", 0.0, 0)
    assert win._music is None
