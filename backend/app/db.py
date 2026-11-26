"""SQLAlchemy engine, session factory and declarative base."""

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


def make_engine(url: str, **kwargs):
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args, **kwargs)


engine = make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db(bind=None) -> None:
    """Create all tables that do not exist yet."""
    from . import models  # noqa: F401  (registers the tables on Base.metadata)

    Base.metadata.create_all(bind=bind or engine)


def get_db() -> Iterator[Session]:
    """FastAPI dependency that yields one session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
