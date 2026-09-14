"""Persistence layer: converts between SQLAlchemy rows and the Pydantic
API models, so routers and the scoring rules (kumite_rules.py,
kata_rules.py) keep working with plain Pydantic objects and never see
SQLAlchemy directly.
"""

import uuid

from sqlalchemy.orm import Session

from app.db import Base, engine
from app.db_models import BracketORM, DivisionORM, KataPerformanceORM, KumiteMatchORM
from app.models import (
    Bracket,
    Competitor,
    Division,
    KataPerformance,
    KumiteMatch,
    LogEntry,
    Penalties,
)


def make_log_id() -> str:
    return f"log-{uuid.uuid4().hex[:8]}"


# ---- Divisions -------------------------------------------------------


def _division_to_model(row: DivisionORM) -> Division:
    return Division(
        id=row.id,
        name=row.name,
        discipline=row.discipline,
        ageGroup=row.ageGroup,
        weightClass=row.weightClass,
        gender=row.gender,
        mat=row.mat,
    )


def get_all_divisions(db: Session) -> list[Division]:
    rows = db.query(DivisionORM).all()
    return [_division_to_model(row) for row in rows]


def get_bracket(db: Session, division_id: str) -> Bracket | None:
    row = db.get(BracketORM, division_id)
    if row is None:
        return None
    return Bracket(pool=row.pool, elimination=row.elimination)


# ---- Kumite ----------------------------------------------------------


def _match_to_model(row: KumiteMatchORM) -> KumiteMatch:
    return KumiteMatch(
        id=row.id,
        divisionId=row.divisionId,
        mat=row.mat,
        round=row.round,
        aka=Competitor(name=row.akaName),
        ao=Competitor(name=row.aoName),
        pointsAka=row.pointsAka,
        pointsAo=row.pointsAo,
        penaltiesAka=Penalties(c1=row.penaltiesAkaC1, c2=row.penaltiesAkaC2),
        penaltiesAo=Penalties(c1=row.penaltiesAoC1, c2=row.penaltiesAoC2),
        senshu=row.senshu,
        clockSeconds=row.clockSeconds,
        clockRunning=row.clockRunning,
        status=row.status,
        winner=row.winner,
        endReason=row.endReason,
        log=[LogEntry(**entry) for entry in row.log],
    )


def get_all_kumite_matches(db: Session) -> list[KumiteMatch]:
    rows = db.query(KumiteMatchORM).all()
    return [_match_to_model(row) for row in rows]


def get_kumite_match(db: Session, match_id: str) -> KumiteMatch | None:
    row = db.get(KumiteMatchORM, match_id)
    return _match_to_model(row) if row else None


def save_kumite_match(db: Session, match: KumiteMatch) -> None:
    row = db.get(KumiteMatchORM, match.id)
    row.mat = match.mat
    row.round = match.round
    row.akaName = match.aka.name
    row.aoName = match.ao.name
    row.pointsAka = match.pointsAka
    row.pointsAo = match.pointsAo
    row.penaltiesAkaC1 = match.penaltiesAka.c1
    row.penaltiesAkaC2 = match.penaltiesAka.c2
    row.penaltiesAoC1 = match.penaltiesAo.c1
    row.penaltiesAoC2 = match.penaltiesAo.c2
    row.senshu = match.senshu
    row.clockSeconds = match.clockSeconds
    row.clockRunning = match.clockRunning
    row.status = match.status
    row.winner = match.winner
    row.endReason = match.endReason
    row.log = [entry.model_dump() for entry in match.log]
    db.commit()


# ---- Kata --------------------------------------------------------------


def _performance_to_model(row: KataPerformanceORM) -> KataPerformance:
    return KataPerformance(
        id=row.id,
        divisionId=row.divisionId,
        mat=row.mat,
        round=row.round,
        competitor=Competitor(name=row.competitorName),
        judgeScores=row.judgeScores,
        finalScore=row.finalScore,
        status=row.status,
    )


def get_all_kata_performances(db: Session) -> list[KataPerformance]:
    rows = db.query(KataPerformanceORM).all()
    return [_performance_to_model(row) for row in rows]


def get_kata_performance(db: Session, performance_id: str) -> KataPerformance | None:
    row = db.get(KataPerformanceORM, performance_id)
    return _performance_to_model(row) if row else None


def save_kata_performance(db: Session, performance: KataPerformance) -> None:
    row = db.get(KataPerformanceORM, performance.id)
    row.mat = performance.mat
    row.round = performance.round
    row.competitorName = performance.competitor.name
    row.judgeScores = performance.judgeScores
    row.finalScore = performance.finalScore
    row.status = performance.status
    db.commit()


# ---- Seeding -----------------------------------------------------------

_SEED_DIVISIONS = [
    dict(
        id="div-kumite-1",
        name="Cadet Male -63kg Kumite",
        discipline="kumite",
        ageGroup="Cadet",
        weightClass="-63kg",
        gender="Male",
        mat=1,
    ),
    dict(
        id="div-kata-1",
        name="Junior Female Kata",
        discipline="kata",
        ageGroup="Junior",
        weightClass=None,
        gender="Female",
        mat=2,
    ),
]

_SEED_KUMITE_MATCHES = [
    dict(
        id="km-1",
        divisionId="div-kumite-1",
        mat=1,
        round="Pool - Match 3",
        akaName="Yuki Tanaka",
        aoName="Marco Rossi",
        pointsAka=0,
        pointsAo=0,
        penaltiesAkaC1=0,
        penaltiesAkaC2=0,
        penaltiesAoC1=0,
        penaltiesAoC2=0,
        senshu=None,
        clockSeconds=120,
        clockRunning=False,
        status="in_progress",
        winner=None,
        endReason=None,
        log=[],
    )
]

_SEED_KATA_PERFORMANCES = [
    dict(
        id="kt-1",
        divisionId="div-kata-1",
        mat=2,
        round="Pool - Performance 2",
        competitorName="Aiko Sato",
        judgeScores=[None] * 7,
        finalScore=None,
        status="scoring",
    )
]

_SEED_BRACKETS = [
    dict(
        divisionId="div-kumite-1",
        pool=[
            {"competitor": "Yuki Tanaka", "wins": 2, "losses": 0},
            {"competitor": "Marco Rossi", "wins": 1, "losses": 1},
            {"competitor": "Ben Carter", "wins": 0, "losses": 2},
        ],
        elimination=[
            {
                "round": "Semifinal",
                "matches": [
                    {"a": "Yuki Tanaka", "b": "Ben Carter", "winner": "Yuki Tanaka"},
                    {"a": "Marco Rossi", "b": "TBD", "winner": None},
                ],
            },
            {
                "round": "Final",
                "matches": [{"a": "Yuki Tanaka", "b": "TBD", "winner": None}],
            },
        ],
    ),
    dict(
        divisionId="div-kata-1",
        pool=[
            {"competitor": "Aiko Sato", "wins": 0, "losses": 0},
            {"competitor": "Lena Novak", "wins": 0, "losses": 0},
        ],
        elimination=[
            {
                "round": "Final",
                "matches": [{"a": "Aiko Sato", "b": "Lena Novak", "winner": None}],
            }
        ],
    ),
]


def seed(db: Session) -> None:
    db.add_all(DivisionORM(**row) for row in _SEED_DIVISIONS)
    db.add_all(KumiteMatchORM(**row) for row in _SEED_KUMITE_MATCHES)
    db.add_all(KataPerformanceORM(**row) for row in _SEED_KATA_PERFORMANCES)
    db.add_all(BracketORM(**row) for row in _SEED_BRACKETS)
    db.commit()


def init_db() -> None:
    """Create tables if they don't exist yet, and seed if empty. Safe to
    call every time the app starts."""
    Base.metadata.create_all(engine)
    from app.db import SessionLocal

    db = SessionLocal()
    try:
        if db.query(DivisionORM).count() == 0:
            seed(db)
    finally:
        db.close()


def reset_database() -> None:
    """Drop and recreate all tables, then reseed. Used between tests so
    each test starts from the same known state."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    from app.db import SessionLocal

    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
