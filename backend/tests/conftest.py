import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db import get_db, init_db, make_engine
from backend.app.main import create_app


@pytest.fixture
def session_factory():
    """Fresh in-memory database per test."""
    engine = make_engine("sqlite://", poolclass=StaticPool)
    init_db(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture
def client(session_factory):
    app = create_app()

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # No `with` block: skips the lifespan, so the real database file is never touched.
    return TestClient(app)
