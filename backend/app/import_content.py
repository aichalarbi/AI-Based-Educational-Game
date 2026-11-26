"""Import challenge JSON into the database.

Usage (repo root):  python -m backend.app.import_content <file.json> [<file.json> ...]
"""

import sys
from pathlib import Path

from pydantic import ValidationError

from .db import SessionLocal, init_db
from .services.content_import import ContentError, import_content, load_content_file


def main(argv) -> int:
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    # Validate every file before touching the database.
    contents = []
    for name in argv:
        try:
            contents.append((name, load_content_file(Path(name))))
        except (OSError, ValueError, ValidationError) as exc:
            print(f"ERROR {name}: {exc}", file=sys.stderr)
            return 1

    init_db()
    for name, content in contents:
        with SessionLocal() as db:
            try:
                missions, challenges = import_content(db, content)
            except ContentError as exc:
                db.rollback()
                print(f"ERROR {name}: {exc}", file=sys.stderr)
                return 1
        print(f"{name}: imported {missions} mission(s), {challenges} challenge(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
