"""Entry of the packaged program (PyInstaller, installer/fogscout.spec): the same as ``python -m fogscout`` –
including ``--helper`` (the elevated helpers) and ``--restart``, which the .exe runs on itself."""
from fogscout.__main__ import main

if __name__ == "__main__":
    main()
