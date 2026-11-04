"""1.33.4: the notes of a GitHub release from HISTORY.md (.github/workflows/build.yml, job ``release``).

    python tools/release_notes.py HISTORY.md <version> [<previous version>]

prints fogscout.whatsnew.release_notes – the versions since the release it replaces, newest first. Standard library
only; fogscout/__init__.py sets environment variables and loads nothing else."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fogscout.whatsnew import release_notes  # noqa: E402


def main(argv) -> int:
    if len(argv) not in (2, 3):
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[0], encoding="utf-8") as fh:
        text = fh.read()
    print(release_notes(text, argv[1], argv[2] if len(argv) == 3 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
