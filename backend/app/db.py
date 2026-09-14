"""Database engine and session setup.

The connection target is controlled entirely by the DATABASE_URL
environment variable, so the same code runs against a local SQLite file
in development, an in-memory SQLite database in tests, or (later) a
different database entirely — nothing else in the app needs to change.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./karate.db")

_is_sqlite = DATABASE_URL.startswith("sqlite")
_is_in_memory_sqlite = _is_sqlite and (
    DATABASE_URL in ("sqlite://", "sqlite:///:memory:")
)

_engine_kwargs = {}
if _is_sqlite:
    # SQLite only allows a connection to be used by the thread that
    # created it by default; FastAPI may call us from a different thread.
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
if _is_in_memory_sqlite:
    # An in-memory SQLite database is private to the connection that
    # created it. StaticPool keeps a single connection alive for the
    # whole process so every session sees the same data (used in tests).
    _engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
