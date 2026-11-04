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
    p = rq.plan(d)
    assert p["video"] == {"outputWidth": 2560, "outputHeight": 1440, "fpsNumerator": 60, "fpsDenominator": 1}
    assert p["profile"] == [("SimpleOutput", "RecQuality", "HQ")]      # review F-03: the encoder is never switched
    assert all(tuple(x[:2]) in rq.QUALITY_KEYS for x in p["profile"])
    lines = rq.plan_lines(p)
    assert len(lines) == 3 and "2560×1440" in lines[0] and not any("NVENC" in x for x in lines)


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


BRANDED = ("NVIDIA", "NVENC", "P5", "CQ-Level", "Mehrfachdurchlauf", "AMD", "QuickSync", "Target Usage")


def _text(rows):
    return "\n".join(rows)


def test_each_encoder_family_gets_its_own_steps_and_none_gets_anothers():
    """Review F-03: the advanced mode's steps gave AMD AMF and Intel Quick Sync the NVENC lines (NVIDIA, CQ-Level,
    P5, multipass); now per family, and an unknown encoder gets neutral steps without any brand's settings."""
    for raw in ("jim_nvenc", "ffmpeg_nvenc", "jim_hevc_nvenc", "obs_nvenc_h264_tex", "NVENC H.264", "nvenc"):
        assert rq.encoder_family(raw) == "nvenc", raw
    for raw in ("h264_texture_amf", "h265_texture_amf", "amd", "amd_hevc", "AMD AMF H.264", "AMD_HEVC"):
        assert rq.encoder_family(raw) == "amf", raw
    for raw in ("obs_qsv11_v2", "obs_qsv11_hevc", "qsv", "QSV", "Quick Sync H.264"):
        assert rq.encoder_family(raw) == "qsv", raw
    for raw in ("obs_x264", "x264", "OBS_X264", "x264_lowcpu", "x264 (CPU)"):
        assert rq.encoder_family(raw) == "cpu", raw
    for raw in ("", "none", "odd_encoder", "ffmpeg_svt_av1", "obs_x265", None):
        assert rq.encoder_family(raw) == "unknown", raw
    nv = _text(rq.steps("Advanced", "jim_nvenc"))
    assert "NVIDIA NVENC" in nv and "CQ-Level" in nv and "P5" in nv
    amf = _text(rq.steps("Advanced", "h264_texture_amf"))
    assert "AMD" in amf and "CQP" in amf
    assert not any(w in amf for w in ("NVIDIA", "NVENC", "P5", "CQ-Level", "Mehrfachdurchlauf", "QuickSync"))
    qsv = _text(rq.steps("Advanced", "obs_qsv11_v2"))
    assert "QuickSync" in qsv and "ICQ" in qsv
    assert not any(w in qsv for w in ("NVIDIA", "P5", "CQ-Level", "Mehrfachdurchlauf", "AMD"))
    cpu = _text(rq.steps("Advanced", "obs_x264"))
    assert "CRF" in cpu and "NVIDIA" not in cpu and "P5" not in cpu
    for raw in ("", "none", "odd_encoder", "ffmpeg_svt_av1"):
        neutral = _text(rq.steps("Advanced", raw))
        assert "CQP" in neutral and not any(w in neutral for w in BRANDED), raw
    for rows in (rq.steps("Advanced", "jim_nvenc"), rq.steps("Advanced", "amd"), rq.steps("Advanced", "qsv"),
                 rq.steps("Advanced", "x264"), rq.steps("Advanced", "odd")):
        assert rows[0].startswith("OBS") and "Basisauflösung" in _text(rows) and "MKV" in _text(rows)


def test_the_plan_never_switches_the_encoder():
    """Review F-03: an NVIDIA driver on the PC is no proof that OBS offers NVENC (obs-websocket cannot list the
    encoders) – a click never switches it, also in the simple mode with x264."""
    for raw in ("x264", "obs_x264", "nvenc", "amd", "qsv"):
        p = rq.plan(_d(mode="Simple", quality="Small", encoder_raw=raw, encoder=""))
        assert not any(x[1] == "RecEncoder" for x in p.get("profile", [])), raw
    assert not hasattr(rq, "nvidia_present")
