"""SQLAlchemy ORM tables.

Scalar, queryable fields get real columns. Nested/list-shaped data that
the API always reads and writes as a whole (match log entries, kata judge
scores, bracket pool/elimination trees) is stored as JSON columns rather
than fully normalized into extra tables — this is a mock/prototype
database standing in for a future real one, so the schema favors staying
close to the API shape over full normalization.
"""

from sqlalchemy import JSON, Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DivisionORM(Base):
    __tablename__ = "divisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    discipline: Mapped[str] = mapped_column(String)
    ageGroup: Mapped[str] = mapped_column(String)
    weightClass: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String)
    mat: Mapped[int] = mapped_column(Integer)


class KumiteMatchORM(Base):
    __tablename__ = "kumite_matches"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    divisionId: Mapped[str] = mapped_column(ForeignKey("divisions.id"))
    mat: Mapped[int] = mapped_column(Integer)
    round: Mapped[str] = mapped_column(String)
    akaName: Mapped[str] = mapped_column(String)
    aoName: Mapped[str] = mapped_column(String)
    pointsAka: Mapped[int] = mapped_column(Integer, default=0)
    pointsAo: Mapped[int] = mapped_column(Integer, default=0)
    penaltiesAkaC1: Mapped[int] = mapped_column(Integer, default=0)
    penaltiesAkaC2: Mapped[int] = mapped_column(Integer, default=0)
    penaltiesAoC1: Mapped[int] = mapped_column(Integer, default=0)
    penaltiesAoC2: Mapped[int] = mapped_column(Integer, default=0)
    senshu: Mapped[str | None] = mapped_column(String, nullable=True)
    clockSeconds: Mapped[int] = mapped_column(Integer)
    clockRunning: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, default="in_progress")
    winner: Mapped[str | None] = mapped_column(String, nullable=True)
    endReason: Mapped[str | None] = mapped_column(String, nullable=True)
    log: Mapped[list] = mapped_column(JSON, default=list)


class KataPerformanceORM(Base):
    __tablename__ = "kata_performances"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    divisionId: Mapped[str] = mapped_column(ForeignKey("divisions.id"))
    mat: Mapped[int] = mapped_column(Integer)
    round: Mapped[str] = mapped_column(String)
    competitorName: Mapped[str] = mapped_column(String)
    judgeScores: Mapped[list] = mapped_column(JSON, default=list)
    finalScore: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String, default="scoring")


class BracketORM(Base):
    __tablename__ = "brackets"

    divisionId: Mapped[str] = mapped_column(
        ForeignKey("divisions.id"), primary_key=True
    )
    pool: Mapped[list] = mapped_column(JSON, default=list)
    elimination: Mapped[list] = mapped_column(JSON, default=list)
