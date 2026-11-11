"""1.9.1 (user: "ändere ruhig auch das Logo"): the program icon – a compass star over fog – and its file.
1.50.2 (Saru: icons in higher quality, one family with the other tools): the pictures come from fogscout/assets."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout import icon  # noqa: E402


def test_the_logo_is_an_amber_compass_star_over_fog():
    img = icon.draw(256)
    assert img.size == (256, 256) and img.mode == "RGBA"
    assert img.getpixel((2, 2))[3] == 0                                   # rounded corner: transparent
    r, g, b, a = img.getpixel((128, 70))                                  # the north needle: amber
    assert a == 255 and r > 200 and 130 < g < 190 and b < 120
    r, g, b, a = img.getpixel((92, 111))                                  # the west point: light mist
    assert a == 255 and min(r, g, b) > 170
    fog = img.getpixel((128, 212))                                        # fog at the bottom: pale
    dark = img.getpixel((40, 60))                                         # beside the star: the dark ground
    assert fog[3] == 255 and sum(fog[:3]) > sum(dark[:3]) + 300 and max(dark[:3]) < 80
    assert icon.draw(16).size == (16, 16)
    for n in (16, 20, 24, 32):                                            # the needle survives the small sizes
        r, g, b, _a = icon.draw(n).getpixel((n // 2, n // 3))
        assert r > 170 and r > b + 80


def test_every_size_has_its_own_picture_and_the_file_keeps_them():
    import io
    from PIL import Image
    for n in icon.PICTURES:                                               # shipped, not scaled from one big one
        assert os.path.isfile(os.path.join(icon.ASSETS, f"icon-{n}.png"))
        assert icon.draw(n).size == (n, n)
    assert icon.draw(36).size == (36, 36) and icon.draw(1024).size == (1024, 1024)
    ico = Image.open(io.BytesIO(icon.ico_bytes()))
    assert sorted(ico.info["sizes"]) == [(n, n) for n in icon.SIZES]
    ico.size = (16, 16)                                                   # the 16 px entry is the small variant
    assert ico.convert("RGBA").tobytes() == icon.draw(16).tobytes()


def test_the_icon_file_is_written_once_per_version(tmp_path, monkeypatch):
    path = icon.ensure_ico(str(tmp_path))
    assert os.path.basename(path) == icon.FILE == f"fogscout-{icon.ICON_VERSION}.ico"
    data = open(path, "rb").read()
    assert data[:4] == b"\x00\x00\x01\x00" and data == icon.ico_bytes()  # an .ico, this version's picture
    assert sorted(os.listdir(str(tmp_path))) == [icon.FILE]                 # no temporary file left
    os.utime(path, (time.time() - 100, time.time() - 100))
    stamped = os.stat(path).st_mtime_ns
    def no_draw():
        raise AssertionError("drawn again")
    monkeypatch.setattr(icon, "ico_bytes", no_draw)
    assert icon.ensure_ico(str(tmp_path)) == path and os.stat(path).st_mtime_ns == stamped   # left alone, not drawn
    monkeypatch.setattr(icon, "ico_bytes", lambda: data)
    open(path, "wb").close()                                                # an empty file: written again
    assert icon.ensure_ico(str(tmp_path)) == path and open(path, "rb").read() == data
    assert icon.FILE not in icon.OLD_FILES and {"fogscout.ico", "fogscout-2.ico"} <= set(icon.OLD_FILES)
