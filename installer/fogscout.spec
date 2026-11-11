# -*- mode: python -*-
# 1.31 (.exe, stage 3): PyInstaller build of Fog Scout as a folder app (onedir – nothing is unpacked at each start;
# the installer of stage 4 copies the folder to Program Files). Built in GitHub Actions on Windows
# (.github/workflows/build.yml); by hand, from the repository root, with requirements.txt, requirements-extra.txt
# (--no-deps) and requirements-build.txt installed:
#     python -m PyInstaller --noconfirm --clean installer/fogscout.spec
# Result: dist/FogScout/FogScout.exe, the program's own files under dist/FogScout/_internal/ – the same layout as the
# source checkout (maps/, models/, maps.json, HISTORY.md, fogscout/fonts/), so root_dir works unchanged.
# Check: FogScout.exe --selftest <result.json> (fogscout/selftest.py).
import os
import sys

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

ROOT = os.path.abspath(os.path.join(SPECPATH, os.pardir))
sys.path.insert(0, ROOT)
from fogscout import icon  # noqa: E402  (the program icon is drawn, not a file in the repository)

PACKAGE = os.path.join(ROOT, "fogscout")

# the program's own read-only files (root_dir), at the same relative place as in the checkout
datas = [
    (os.path.join(ROOT, "maps.json"), "."),
    (os.path.join(ROOT, "HISTORY.md"), "."),               # the overview's card "Neu seit …"
    (os.path.join(ROOT, "THIRD_PARTY.md"), "."),
    (os.path.join(ROOT, "PRIVACY.md"), "."),
    (os.path.join(ROOT, "LICENSE"), "."),               # 1.38.43: the terms, next to the program
    (os.path.join(ROOT, "licenses"), "licenses"),       # 1.38.44: Apache-2.0 text (maps.json, OCR models)
    (os.path.join(ROOT, "maps"), "maps"),
    (os.path.join(ROOT, "models"), "models"),
    (os.path.join(PACKAGE, "assets"), os.path.join("fogscout", "assets")),   # 1.50.2: the icon pictures (icon.ASSETS)
    (os.path.join(PACKAGE, "fonts"), os.path.join("fogscout", "fonts")),
    (os.path.join(PACKAGE, "matchexport.user.js"), "fogscout"),
]
# 1.33: build number/version/commit for the update check (relupdate.own_build) – written by CI before the build
if os.path.isfile(os.path.join(ROOT, "build-info.json")):
    datas.append((os.path.join(ROOT, "build-info.json"), "."))
datas += collect_data_files("imageio_ffmpeg", subdir="binaries")   # obsrec.ffmpeg_exe: only this ffmpeg, never PATH

# every module of the program (many are imported only inside functions), winrt's namespace packages (their .pyd
# import each other from C) and windows-capture's native module
hiddenimports = sorted(f"fogscout.{name[:-3]}" for name in os.listdir(PACKAGE)
                       if name.endswith(".py") and name != "__init__.py")
hiddenimports += collect_submodules("winrt") + collect_submodules("windows_capture")
binaries = collect_dynamic_libs("windows_capture")

os.makedirs(workpath, exist_ok=True)
ICON = os.path.join(workpath, "fogscout.ico")
icon.save_ico(ICON)

a = Analysis(
    [os.path.join(SPECPATH, "fogscout_exe.py")],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["tkinter"],
    noarchive=False,
)
# 1.35.1 (user: smaller setup, measured on the Windows wheels): files the program never uses, left out of the folder.
# - PySide6/opengl32sw.dll (20.6 MB): Qt's software OpenGL, loaded only for an OpenGL context – the window draws
#   with the raster engine, no QOpenGLWidget/QtQuick (test_the_bundle_leaves_out_only_what_is_never_used)
# - PySide6/translations (13.7 MB): Qt's own texts for its standard dialogs, only through a QTranslator – none here
# - cv2/opencv_videoio_ffmpeg*.dll (30.9 MB): OpenCV's video reader plugin, only for cv2.VideoCapture/VideoWriter –
#   recordings and clips go through the imageio-ffmpeg executable (obsrec.ffmpeg_exe), OpenCV only does pictures
UNUSED = ("opengl32sw.dll", "/translations/", "opencv_videoio_ffmpeg")


def used(entry) -> bool:
    dest = entry[0].replace("\\", "/").lower()
    return not any(u in "/" + dest for u in UNUSED)


a.binaries = [e for e in a.binaries if used(e)]
a.datas = [e for e in a.datas if used(e)]

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FogScout",
    icon=ICON,
    console=False,              # like pythonw.exe: no console window (the helpers start hidden as well)
    upx=False,                  # packed binaries trip virus scanners and gain little
    uac_admin=False,            # rights come from the scheduled task as before, never from the manifest
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="FogScout")
