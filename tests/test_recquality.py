"""1.29: how good OBS's recording is and what a click may change (recquality, pure)."""
from fogscout import recquality as rq


def _d(**kw):
    d = {"connected": True, "mode": "Advanced", "encoder": "NVENC H.264", "encoder_raw": "jim_nvenc",
         "width": 2560, "height": 1440, "base_width": 2560, "base_height": 1440, "fps": 60.0,
         "recording": True, "seconds": 60.0, "bytes": 0, "rescale": "false"}
    d.update(kw)
    return d


def _bytes(mbps, seconds=60.0):
    return int(mbps * 1e6 / 8 * seconds)


def test_bitrate_and_bits_per_pixel():
    assert rq.bitrate_mbps(_bytes(20), 60) == 20.0
    assert rq.bitrate_mbps(_bytes(20, 10), 10) is None                  # too early to say
    assert rq.bitrate_mbps(0, 60) is None and rq.bitrate_mbps("x", 60) is None
    assert round(rq.bpp(17.7, 2560, 1440, 60), 3) == 0.08
    assert rq.bpp(None, 2560, 1440, 60) is None and rq.bpp(10, 0, 1440, 60) is None


def test_six_megabits_at_1440p60_is_mushy_and_twenty_is_good():
    v = rq.verdict(_d(bytes=_bytes(6)))
    assert v.level == "err" and "matschig" in v.words and "6 Mbit/s" in v.words and "2560×1440@60" in v.words
    assert any("CQP 18" in h for h in v.hints) and not v.fixable    # advanced mode: the user sets the encoder
    v = rq.verdict(_d(bytes=_bytes(14)))
    assert v.level == "warn" and "knapp" in v.words
    v = rq.verdict(_d(bytes=_bytes(20)))
    assert v.level == "ok" and "gut" in v.words and not v.hints


def test_hevc_needs_fewer_bits():
    assert rq.verdict(_d(bytes=_bytes(12), encoder="NVENC HEVC")).level == "ok"
    assert rq.verdict(_d(bytes=_bytes(12))).level == "warn"


def test_downscaled_slow_and_simple_stream_quality_are_found_and_fixable():
    d = _d(mode="Simple", quality="Stream", encoder="x264 (CPU)", encoder_raw="x264", width=1920, height=1080,
           fps=30.0, recording=False, output_total=1000, output_skipped=50)
    v = rq.verdict(d)
    assert v.level == "warn" and v.fixable and len(v.hints) == 4 and "Einstellungen" in v.words
    p = rq.plan(d, nvidia=True)
    assert p["video"] == {"outputWidth": 2560, "outputHeight": 1440, "fpsNumerator": 60, "fpsDenominator": 1}
    assert p["profile"] == [("SimpleOutput", "RecQuality", "HQ"), ("SimpleOutput", "RecEncoder", "nvenc")]
    assert ("SimpleOutput", "RecEncoder", "nvenc") not in rq.plan(d)["profile"]   # no NVIDIA driver: x264 stays
    assert all(tuple(x[:2]) in rq.QUALITY_KEYS for x in p["profile"])
    lines = rq.plan_lines(p)
    assert len(lines) == 4 and "2560×1440" in lines[0] and "NVENC" in lines[3]


def test_nothing_known_says_nothing_and_a_good_setup_waits_for_a_recording():
    assert rq.verdict({}).level == "" and rq.verdict({"connected": False}).words == ""
    v = rq.verdict(_d(recording=False))
    assert v.level == "" and "Aufnahme" in v.words and not v.fixable and rq.plan(_d()) == {}
    assert rq.plan(_d(rescale="true")) == {"profile": [("AdvOut", "RecRescale", "false")]}
    assert rq.plan(_d(fps=59.94)) == {}                                 # 59.94 is 60


def test_the_steps_fit_the_mode_and_encoder():
    adv = rq.steps("Advanced", "jim_nvenc")
    assert any("CQP" in s for s in adv) and not any("CRF" in s for s in adv)
    assert any("CRF" in s for s in rq.steps("Advanced", "obs_x264"))
    assert any("Kaum unterscheidbare" in s for s in rq.steps("Simple"))
