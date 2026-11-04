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
    (os.path.join(ROOT, "maps"), "maps"),
    (os.path.join(ROOT, "models"), "models"),
    (os.path.join(PACKAGE, "fonts"), os.path.join("fogscout", "fonts")),
    (os.path.join(PACKAGE, "matchexport.user.js"), "fogscout"),
]
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
