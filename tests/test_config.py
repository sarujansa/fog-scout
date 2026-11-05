import json
import os

from fogscout import config


def test_a_broken_settings_file_is_kept_and_never_overwritten_with_defaults(tmp_path):
    """1.8.38 (QA audit): a file that could not be read gave the defaults – and the next save replaced the user's
    hotkeys, layouts and OBS password with them."""
    path = tmp_path / "settings.json"
    path.write_text('{"overlay": {"height": 0.7}, "hotkeys": ', encoding="utf-8")       # cut off
    s = config.Settings(str(path))
    assert s.load_error and s["overlay"]["height"] == config.DEFAULTS["overlay"]["height"]
    assert (tmp_path / "settings.json.broken").read_text(encoding="utf-8").startswith('{"overlay"')
    s.save()                                                                    # the copy stays as it was
    assert (tmp_path / "settings.json.broken").read_text(encoding="utf-8").endswith('"hotkeys": ')


def test_odd_values_in_the_settings_file_do_not_stop_the_start(tmp_path):
    """1.8.38: a string version raised TypeError (the program did not start), "overlay": null left None behind."""
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"settings_version": "8", "overlay": None, "sysinfo": "left"}), encoding="utf-8")
    s = config.Settings(str(path))
    assert not s.load_error and s["sysinfo"] == "left"
    assert s["overlay"] == config.DEFAULTS["overlay"] and s["settings_version"] == config.SETTINGS_VERSION
    path.write_text(json.dumps([1, 2]), encoding="utf-8")
    assert config.Settings(str(path)).load_error                            # no object at all: defaults, kept aside
    path.write_text(json.dumps({"settings_version": 2, "overlay": {"custom_x": None}}), encoding="utf-8")
    s = config.Settings(str(path))
    assert s.load_error and isinstance(s["overlay"], dict)                  # a broken migration: nothing half-merged


def test_the_backup_leaves_out_the_obs_password_and_the_spotify_token(tmp_path):
    """1.8.38: backups get shared and synced – the OBS password (plain text) and the token stay on this PC."""
    data = dict(config.DEFAULTS, rec_password="hunter2", spotify_token="dpapi:AAAA", sysinfo="left")
    out = tmp_path / "backup.json"
    config.export_settings(data, str(out))
    text = out.read_text(encoding="utf-8")
    assert "hunter2" not in text and "dpapi:AAAA" not in text and '"sysinfo": "left"' in text
    back = config.read_backup(str(out), {"rec_password": "mine", "spotify_token": "dpapi:MINE"})
    assert back["rec_password"] == "mine" and back["spotify_token"] == "dpapi:MINE"


def test_the_backup_leaves_out_this_pcs_own_values_and_an_old_backup_still_imports(tmp_path):
    """Review F-01: folders, setup path, window geometry … (LOCAL_KEYS) never go into a backup file – an
    import never took them anyway; secrets and the YouTube queue stay out, portable settings stay in, and an older
    backup that still holds local values imports with this PC's values kept."""
    data = dict(config.DEFAULTS, setup_root="C:/Example/FogScout", rec_folder="C:/Example/Recordings",
                shots_folder="D:/Example/Shots", official_dir="C:/Example/Downloads", qt_geometry="AbC=",
                rec_obs_before={"video": {"outputWidth": 1920}}, palette_recent=["a:scan"],
                rec_password="hunter2", youtube_queue=[{"rel": "Clips/a.mp4"}], sysinfo="left")
    out = tmp_path / "backup.json"
    config.export_settings(data, str(out))
    raw = json.loads(out.read_text(encoding="utf-8"))
    assert not set(raw) & set(config.LOCAL_KEYS)
    text = out.read_text(encoding="utf-8")
    assert "Example" not in text and "hunter2" not in text and "Clips/a.mp4" not in text
    assert raw["sysinfo"] == "left" and raw["hotkeys"] == config.DEFAULTS["hotkeys"] and "overlay" in raw
    old = dict(raw, setup_root="C:/Example/Old", rec_folder="C:/Example/OldRecordings")   # a backup from before the fix
    out.write_text(json.dumps(old), encoding="utf-8")
    here = {"setup_root": "D:/Example/Here", "rec_folder": "E:/Example/Recordings"}
    back = config.read_backup(str(out), here)
    assert back["setup_root"] == "D:/Example/Here" and back["rec_folder"] == "E:/Example/Recordings"
    assert back["sysinfo"] == "left"


def test_reset_data_keeps_only_the_pc_specific_values():
    """1.2.19: "Alle Einstellungen zurücksetzen" – defaults, the PC-specific keys and welcome_seen stay."""
    current = {"overlay": {"anchor": "custom", "height": 0.7}, "sysinfo": "left", "qt_geometry": "AAAA",
               "setup_version": 3, "setup_root": "C:/x", "official_dir": "D:/dl", "welcome_seen": True,
               "layouts": {"3440x1440": {}}, "layout_key": "3440x1440", "hotkeys": {"toggle_overlay": "ctrl+alt+q"}}
    data = config.reset_data(current)
    assert data["overlay"]["anchor"] == config.DEFAULTS["overlay"]["anchor"] and data["sysinfo"] == config.DEFAULTS["sysinfo"]
    assert data["hotkeys"] == config.DEFAULTS["hotkeys"]
    assert (data["qt_geometry"], data["setup_version"], data["setup_root"], data["official_dir"]) == ("AAAA", 3, "C:/x", "D:/dl")
    assert data["welcome_seen"] is True and data.get("layouts", {}) == config.DEFAULTS.get("layouts", {})
    assert config.reset_data({}).get("welcome_seen") in (None, False)


def test_old_settings_forget_the_detection_page(tmp_path):
    """1.8.78: the page "Erkennung" is gone – a saved navigation/card/tab order that names it is cleaned once."""
    import json
    from fogscout.config import Settings, SETTINGS_VERSION
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"settings_version": 9, "nav_order": ["log", "detect", "overview"],
                             "card_order": {"detect": {}, "settings": {"a": ["x"]}},
                             "tab_order": {"detect": {}, "overlay": {"t": ["a"]}}, "hotkeys": {}}))
    s = Settings(str(p))
    assert s["nav_order"] == ["log", "overview"] and s["card_order"] == {"settings": {"a": ["x"]}}
    assert s["tab_order"] == {"overlay": {"t": ["a"]}} and s["settings_version"] == SETTINGS_VERSION


def test_the_old_instant_clip_sound_default_follows_the_new_one(tmp_path):
    """1.11.4 (user: "es soll auch Discord-Sound etc. beinhalten in Clips"): F8 clips keep every source by default;
    a settings file still on the 1.8.6 default (game + microphone) is moved along once, an own choice stays."""
    import json
    from fogscout import obsrec
    from fogscout.config import DEFAULTS, Settings, SETTINGS_VERSION
    assert DEFAULTS["rec_clip_sources"] == list(obsrec.SOURCES) == ["dbd", "discord", "mic", "other"]
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"settings_version": 10, "rec_clip_sources": ["dbd", "mic"], "hotkeys": {}}))
    s = Settings(str(p))
    assert s["rec_clip_sources"] == ["dbd", "discord", "mic", "other"] and s["settings_version"] == SETTINGS_VERSION
    p.write_text(json.dumps({"settings_version": 10, "rec_clip_sources": ["dbd"], "hotkeys": {}}))
    assert Settings(str(p))["rec_clip_sources"] == ["dbd"]
    p.write_text(json.dumps({"settings_version": 11, "rec_clip_sources": ["dbd", "mic"], "hotkeys": {}}))
    assert Settings(str(p))["rec_clip_sources"] == ["dbd", "mic"]                 # chosen after 1.11.4: kept


def test_the_kills_average_on_the_map_card_is_off_once_and_can_come_back(tmp_path):
    """1.11.11 (user: "entferne das Avg-Kill, damit falls es stockt nicht noch eine Zeile entsteht"): the record
    chip ("Ø 2.0 Kills · 3 Runden") is off by default and switched off once in older files – the amber "Verbindung
    stockt" then fits the chip row; ticked again afterwards, it stays on."""
    import json
    from fogscout.config import DEFAULTS, Settings
    assert DEFAULTS["overlay"]["show_record"] is False
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"settings_version": 11, "overlay": {"show_record": True}, "hotkeys": {}}))
    assert Settings(str(p))["overlay"]["show_record"] is False
    p.write_text(json.dumps({"settings_version": 12, "overlay": {"show_record": True}, "hotkeys": {}}))
    assert Settings(str(p))["overlay"]["show_record"] is True


def test_a_save_that_fails_says_so_once_in_the_log(tmp_path, caplog):
    """1.12.3 (audit): a failed save (disk full, file locked) was swallowed without a word."""
    import logging
    from fogscout import config
    s = config.Settings(str(tmp_path / "gone" / "settings.json"))     # the folder does not exist: every save fails
    with caplog.at_level(logging.WARNING):
        s.save()
        s.save()
    assert len([r for r in caplog.records if "nicht gespeichert" in r.getMessage()]) == 1
    os.makedirs(tmp_path / "gone")
    s.save()
    assert os.path.exists(tmp_path / "gone" / "settings.json") and not s._save_failed


def test_a_saved_order_of_the_statistics_tabs_is_dropped_once_for_the_new_groups(tmp_path):
    """1.12.7: Bloodpoints and Farming left "Sonstiges" for a group of their own, System moved to the maps – a
    saved tab order counts tabs by position and would put the wrong ones first, so it is dropped once (others stay)."""
    import json
    from fogscout.config import Settings, SETTINGS_VERSION
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"settings_version": 12, "tab_order": {"stats": {"x": ["2", "0", "1"]},
                                                                   "overlay": {"t": ["a"]}}, "hotkeys": {}}))
    s = Settings(str(p))
    assert s["tab_order"] == {"overlay": {"t": ["a"]}} and s["settings_version"] == SETTINGS_VERSION == 13
    p.write_text(json.dumps({"settings_version": 13, "tab_order": {"stats": {"x": ["1", "0"]}}, "hotkeys": {}}))
    assert Settings(str(p))["tab_order"] == {"stats": {"x": ["1", "0"]}}           # ordered after 1.12.7: kept


def test_the_obs_password_is_stored_protected_and_an_old_clear_one_still_works(tmp_path, monkeypatch):
    """1.16.2 (A14): rec_password like the Spotify/YouTube secrets (spotify.protect: DPAPI on Windows, encoded
    elsewhere). A clear-text password from before is read as it is and protected on the start; one that cannot
    be decrypted here gives an empty field and a log line – never the stored value, never the password itself."""
    from types import SimpleNamespace
    from fogscout import app_settings, spotify
    from fogscout.app_settings import SettingsTab, read_password
    assert read_password("") == ("", True) and read_password(None) == ("", True)
    assert read_password("hunter2") == ("hunter2", True)                       # before 1.16.2: clear text
    assert read_password(spotify.protect("hunter2")) == ("hunter2", True)
    assert read_password("dpapi:@@not-base64") == ("", False)
    assert read_password("plain:@@not-base64") == ("", False)

    def host(stored):
        s = config.Settings(str(tmp_path / "settings.json"))
        s.set("rec_password", stored)
        h = SimpleNamespace(settings=s, logged=[], saved=[])
        h._log = lambda text, cat="System": h.logged.append((cat, text))
        h._save_soon = lambda: h.saved.append(1)
        return h

    h = host("hunter2")
    assert SettingsTab._rec_password_load(h) == "hunter2" and h.saved and not h.logged
    stored = h.settings.get("rec_password")
    assert app_settings.is_protected(stored) and "hunter2" not in stored and read_password(stored)[0] == "hunter2"
    h = host(stored)                                                          # protected already: left as it is
    assert SettingsTab._rec_password_load(h) == "hunter2" and not h.saved and h.settings.get("rec_password") == stored
    h = host("dpapi:AAAA")                                                    # another PC / user account
    assert SettingsTab._rec_password_load(h) == "" and [c for c, _t in h.logged] == ["Fehler"]
    assert "AAAA" not in h.logged[0][1]



def test_the_backup_leaves_out_the_youtube_queue_and_an_import_keeps_this_pcs(tmp_path):
    """1.28 (audit F10): the queue holds upload session URIs and recording paths – not in a file passed on."""
    queue = [{"rel": "Clips/a.mp4", "session": "https://www.googleapis.com/upload/youtube/v3/videos?upload_id=X"}]
    data = dict(config.DEFAULTS, youtube_queue=queue)
    path = str(tmp_path / "backup.json")
    config.export_settings(data, path)
    text = open(path, encoding="utf-8").read()
    assert "youtube_queue" not in text and "upload_id" not in text and "hotkeys" in text
    mine = [{"rel": "Clips/mine.mp4"}]
    merged = config.read_backup(path, dict(config.DEFAULTS, youtube_queue=mine))
    assert merged["youtube_queue"] == mine


def test_claude_switches_and_recent_picks_of_the_wrong_type_read_as_their_defaults(tmp_path):
    """1.28 (audit F11): a hand-edited "claude_on": "false" was a true value – Claude on against the user's will;
    palette_recent with numbers or lists in it broke the palette's ranking."""
    from fogscout import palette
    assert config.RECENT_KEPT == palette.RECENT_KEPT
    for bad, want in (("false", False), (5, False), (None, False), ([True], False), (True, True)):
        p = tmp_path / f"s{abs(hash(repr(bad)))}.json"
        p.write_text(json.dumps({"claude_on": bad, "claude_editor": bad}), encoding="utf-8")
        s = config.Settings(str(p))
        assert s.get("claude_on") is want and s.get("claude_editor") is want, bad
    p = tmp_path / "recent.json"
    for bad, want in (("a:scan", []), ([[1]], []), (["a:scan", 3, None, "p:stats"], ["a:scan", "p:stats"]),
                      ({"a": 1}, []), (["x"] * 20, ["x"] * config.RECENT_KEPT)):
        p.write_text(json.dumps({"palette_recent": bad}), encoding="utf-8")
        assert config.Settings(str(p)).get("palette_recent") == want, bad
    p.write_text(json.dumps({"palette_recent": ["a:scan"], "claude_on": True, "rec_port": "4455"}), encoding="utf-8")
    s = config.Settings(str(p))
    assert s.get("palette_recent") == ["a:scan"] and s.get("claude_on") is True
    assert s.get("rec_port") == "4455"                  # only the TYPED keys are checked, nothing else changes


def test_the_picked_claude_model_survives_a_restart(tmp_path):
    """1.38.17 (audit): _typed knew bool and list only – every str fell through to the default, so "haiku" or
    "sonnet" read back as "opus" at every start and each request cost the Opus price. A wrong type still reads as
    the default; a stored non-dict for a dict key too."""
    p = tmp_path / "model.json"
    for stored, want in (("haiku", "haiku"), ("sonnet", "sonnet"), ("opus", "opus"), (7, "opus"), (None, "opus"),
                         (["haiku"], "opus")):
        p.write_text(json.dumps({"claude_model": stored, "settings_version": config.SETTINGS_VERSION}),
                     encoding="utf-8")
        assert config.Settings(str(p)).get("claude_model") == want, stored
    p.write_text(json.dumps({"claude_spent": "3.5", "rec_obs_before": [1]}), encoding="utf-8")
    s = config.Settings(str(p))
    assert s.get("claude_spent") == config.DEFAULTS["claude_spent"]
    assert s.get("rec_obs_before") == config.DEFAULTS["rec_obs_before"]
