from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db import get_db, init_db, make_engine
from backend.app.main import create_app
from backend.app.services.content_import import import_content, load_content_file

EXAMPLE_CONTENT = Path(__file__).resolve().parent.parent / "sample_content" / "EXAMPLE_missions.json"


@pytest.fixture
def session_factory():
    """Fresh in-memory database per test."""
    engine = make_engine("sqlite://", poolclass=StaticPool)
    init_db(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture
def seeded_session_factory(session_factory):
    with session_factory() as db:
        import_content(db, load_content_file(EXAMPLE_CONTENT))
    return session_factory


def _make_client(factory):
    app = create_app()

    def override_get_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # No `with` block: skips the lifespan, so the real database file is never touched.
    return TestClient(app)


@pytest.fixture
def client(session_factory):
    return _make_client(session_factory)


@pytest.fixture
def seeded_client(seeded_session_factory):
    return _make_client(seeded_session_factory)
