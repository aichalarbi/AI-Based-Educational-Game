"""Create the SQLite schema.  Usage (repo root):  python -m backend.app.init_db"""

from .config import settings
from .db import init_db

if __name__ == "__main__":
    init_db()
    print(f"Database initialised: {settings.database_url}")
