"""1.15 (audit of the video system): the clip editor's exports pick an encoder – the graphics card's when ffmpeg
has it and it really works, else the CPU – with a quality step and a picture height. Pure parts without ffmpeg,
the self-test once with the bundled one."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fogscout import clipedit, encoders  # noqa: E402
from fogscout.encoders import Encoding  # noqa: E402

LISTING = """Encoders:
 V..... = Video
 ------
 V....D libx264              libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (codec h264)
 V....D h264_amf             AMD AMF H.264 Encoder (codec h264)
 V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
 V..... h264_qsv             H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (Intel Quick Sync Video acceleration) (codec h264)
 V....D libx265              libx265 H.265 / HEVC (codec hevc)
 V....D hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
 A....D aac                  AAC (Advanced Audio Coding)
"""


def test_the_cpu_default_keeps_the_arguments_of_every_clip_since_1_5_1():
    assert Encoding().video_args() == ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]
    assert Encoding().video_args(2500) == ["-c:v", "libx264", "-preset", "veryfast", "-b:v", "2500k", "-maxrate",
                                            "2750k", "-bufsize", "5000k", "-pix_fmt", "yuv420p"]
    assert Encoding().summary() == "H.264 · CPU (x264/x265) · Ausgewogen"


def test_every_encoder_family_has_arguments_for_every_quality():
    for codec in encoders.CODECS:
        for hw in ("",) + encoders.HW:
            for q in encoders.QUALITIES:
                e = Encoding(codec, q, 0, hw)
                a = e.video_args()
                assert a[:2] == ["-c:v", encoders.ENCODERS[(codec, hw)]] and "-pix_fmt" in a
                b = e.video_args(4000)
                assert "-b:v" in b and "-crf" not in b and "-cq" not in b and "-global_quality" not in b
    assert Encoding("hevc", "high", 0, "nvenc").video_args()[-2:] == ["-tag:v", "hvc1"]   # HEVC that MP4 players open
    assert "-tag:v" in Encoding("hevc").video_args()
    assert Encoding("h264", "fast", 0, "qsv").video_args()[-1] == "nv12"
    assert Encoding("h264", "high", 0, "amf").video_args()[2:4] == ["-quality", "quality"]
    assert Encoding("h264", "x", 0, "").video_args()[5] == "18"                     # unknown quality = balanced


def test_the_picture_height_never_grows_the_recording_and_stays_even():
    assert Encoding(height=1080).target_height(1440) == 1080
    assert Encoding(height=1080).target_height(1080) == 0 and Encoding(height=1080).target_height(720) == 0
    assert Encoding(height=0).target_height(1440) == 0
    assert Encoding(height=1080).target_height(0) == 1080                          # size unknown: as asked
    assert Encoding(height=1080).summary().endswith("1080p")


def test_the_listing_is_parsed_and_wishes_resolve_to_what_works():
    listed = encoders.parse_encoders(LISTING)
    assert listed == {"libx264", "h264_amf", "h264_nvenc", "h264_qsv", "libx265", "hevc_nvenc"}
    avail = {"libx264": True, "libx265": True, "h264_nvenc": True, "hevc_nvenc": True, "h264_amf": False,
             "h264_qsv": False, "hevc_amf": False, "hevc_qsv": False}
    assert Encoding(hw="auto").resolve(avail) == Encoding(hw="nvenc")
    assert Encoding(hw="amf").resolve(avail) == Encoding(hw="")                     # listed, but the card is not there
    assert Encoding("hevc", hw="auto").resolve(avail).encoder == "hevc_nvenc"
    assert Encoding("hevc", hw="qsv").resolve({"libx264": True, "libx265": False}) == Encoding("h264")
    assert Encoding(hw="auto").resolve(None) == Encoding()                           # nothing known yet: the CPU
    assert Encoding("odd", "odd", 999, "odd").resolve({}) == Encoding()
    assert encoders.hw_choices(avail) == [("", encoders.HW_LABELS[""]), ("nvenc", "NVIDIA NVENC")]
    assert encoders.hw_choices(None) == [("", encoders.HW_LABELS[""])]
    assert encoders.hw_choices(avail, "hevc")[-1][0] == "nvenc"


def test_detection_lists_then_tries_each_hardware_encoder_once_and_keeps_the_answer():
    encoders.forget()
    calls = []

    def run(args):
        calls.append(args)
        if args[1:3] == ["-hide_banner", "-encoders"]:
            return 0, LISTING
        enc = args[args.index("-c:v") + 1]
        assert args[args.index("-f") + 1] == "lavfi" and "-frames:v" in args and args[-2:] == ["-f", "null"] + [] or \
            args[-3:-1] == ["-f", "null"]
        return (0, "") if enc.endswith("_nvenc") else (1, "Cannot load amfrt64.dll")
    got = encoders.detect("/x/ffmpeg", run)
    assert got == {"libx264": True, "libx265": True, "h264_nvenc": True, "hevc_nvenc": True, "h264_amf": False,
                   "h264_qsv": False, "hevc_amf": False, "hevc_qsv": False}
    tried = [a[a.index("-c:v") + 1] for a in calls if "-c:v" in a]
    assert sorted(tried) == ["h264_amf", "h264_nvenc", "h264_qsv", "hevc_nvenc"]   # only listed hardware ones
    assert all("-i" in a and "color=" in a[a.index("-i") + 1] for a in calls if "-c:v" in a)   # no file, no network
    n = len(calls)
    assert encoders.detect("/x/ffmpeg", run) == got and len(calls) == n          # kept
    assert encoders.known("/x/ffmpeg") == got and encoders.known("/y") is None
    assert encoders.detect(None) == {} and encoders.detect("/z", lambda a: (1, "")) == {k: False for k in got}
    import queue
    q = queue.Queue()
    encoders.detect_async("/x/ffmpeg", q.put, run)
    assert q.get(timeout=5) == got
    encoders.detect_async("/x/ffmpeg", q.put, lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
    assert q.get(timeout=5) == got                                                # kept answer, the error swallowed
    encoders.forget()
    encoders.detect_async("/x/ffmpeg", q.put, lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
    assert q.get(timeout=5) == {}
    encoders.forget()


def test_the_settings_give_an_encoding():
    assert encoders.from_settings({}) == Encoding(hw="auto")
    assert encoders.from_settings({"clip_codec": "hevc", "clip_quality": "high", "clip_height": "1080",
                                   "clip_hw": ""}) == Encoding("hevc", "high", 1080, "")
    assert encoders.from_settings({"clip_height": "x"}).height == 0


def test_cut_and_the_graph_take_the_encoding(tmp_path):
    calls = []

    def run(args):
        calls.append(args)
        with open(args[-1], "wb") as f:
            f.write(b"x")
        return 0, b""
    src = str(tmp_path / "r.mp4")
    open(src, "wb").close()
    info = clipedit.Info(duration=30.0, width=2560, height=1440, fps=60.0, audio_tracks=1)
    enc = Encoding("hevc", "high", 1080, "nvenc")
    ok, _why = clipedit.cut(src, 1.0, 5.0, str(tmp_path / "c.mp4"), "exact", "/x/ffmpeg", run=run, info=info,
                            encoding=enc)
    a = calls[-1]
    assert ok and a[a.index("-c:v") + 1] == "hevc_nvenc" and a[a.index("-vf") + 1] == "scale=-2:1080"
    assert "-cq" in a and a[a.index("-preset") + 1] == "p6"
    ok, _why = clipedit.cut(src, 1.0, 5.0, str(tmp_path / "d.mp4"), "discord", "/x/ffmpeg", run=run, info=info,
                            encoding=enc)
    a = calls[-1]
    assert ok and a[a.index("-c:v") + 1] == "h264_nvenc" and "-b:v" in a and "-cq" not in a   # Discord: never HEVC
    g, _v, _s, args = clipedit.edit_graph(clipedit.Edit([clipedit.Part(0.0, 4.0, 2.0)]), info, "discord", encoding=enc)
    assert args[:2] == ["-c:v", "h264_nvenc"]
    edit = clipedit.Edit([clipedit.Part(0.0, 4.0, 2.0)])
    g, v, s, args = clipedit.edit_graph(edit, info, "exact", encoding=enc)
    assert "scale=-2:1080" in g and args[:2] == ["-c:v", "hevc_nvenc"]
    g2, _v, _s, args2 = clipedit.edit_graph(edit, info, "exact")
    assert "scale" not in g2 and args2[:2] == ["-c:v", "libx264"]                   # as before without a choice


@pytest.mark.skipif(not clipedit.ffmpeg_exe(), reason="imageio-ffmpeg not installed")
def test_the_real_ffmpeg_lists_x264_and_passes_the_self_test():
    ffmpeg = clipedit.ffmpeg_exe()
    listed = encoders.available(ffmpeg)
    assert "libx264" in listed
    assert encoders.works(ffmpeg, "libx264")
    assert not encoders.works(ffmpeg, "no_such_encoder")
