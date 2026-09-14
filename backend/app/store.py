"""In-memory mock database.

Mirrors the shape and behaviour of the frontend's mocked backend
(frontend/src/api/client.js), so both sides agree on what the real backend
should do once one exists. Swap this module for a real database later
without changing the routers' contracts.
"""

import uuid
from copy import deepcopy

from app.models import (
    Bracket,
    Competitor,
    Division,
    EliminationMatch,
    EliminationRound,
    KataPerformance,
    KumiteMatch,
    LogEntry,
    Penalties,
    PoolStanding,
)

_SEED_DIVISIONS = [
    Division(
        id="div-kumite-1",
        name="Cadet Male -63kg Kumite",
        discipline="kumite",
        ageGroup="Cadet",
        weightClass="-63kg",
        gender="Male",
        mat=1,
    ),
    Division(
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
    KumiteMatch(
        id="km-1",
        divisionId="div-kumite-1",
        mat=1,
        round="Pool - Match 3",
        aka=Competitor(name="Yuki Tanaka"),
        ao=Competitor(name="Marco Rossi"),
        pointsAka=0,
        pointsAo=0,
        penaltiesAka=Penalties(c1=0, c2=0),
        penaltiesAo=Penalties(c1=0, c2=0),
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
    KataPerformance(
        id="kt-1",
        divisionId="div-kata-1",
        mat=2,
        round="Pool - Performance 2",
        competitor=Competitor(name="Aiko Sato"),
        judgeScores=[None] * 7,
        finalScore=None,
        status="scoring",
    )
]

_SEED_BRACKETS = {
    "div-kumite-1": Bracket(
        pool=[
            PoolStanding(competitor="Yuki Tanaka", wins=2, losses=0),
            PoolStanding(competitor="Marco Rossi", wins=1, losses=1),
            PoolStanding(competitor="Ben Carter", wins=0, losses=2),
        ],
        elimination=[
            EliminationRound(
                round="Semifinal",
                matches=[
                    EliminationMatch(a="Yuki Tanaka", b="Ben Carter", winner="Yuki Tanaka"),
                    EliminationMatch(a="Marco Rossi", b="TBD", winner=None),
                ],
            ),
            EliminationRound(
                round="Final",
                matches=[EliminationMatch(a="Yuki Tanaka", b="TBD", winner=None)],
            ),
        ],
    ),
    "div-kata-1": Bracket(
        pool=[
            PoolStanding(competitor="Aiko Sato", wins=0, losses=0),
            PoolStanding(competitor="Lena Novak", wins=0, losses=0),
        ],
        elimination=[
            EliminationRound(
                round="Final",
                matches=[EliminationMatch(a="Aiko Sato", b="Lena Novak", winner=None)],
            )
        ],
    ),
}

divisions: list[Division] = []
kumite_matches: dict[str, KumiteMatch] = {}
kata_performances: dict[str, KataPerformance] = {}
brackets: dict[str, Bracket] = {}


def reset_store() -> None:
    """Restore the store to its seed state. Called before every test so
    tests don't leak mutations into each other."""
    global divisions, kumite_matches, kata_performances, brackets
    divisions = deepcopy(_SEED_DIVISIONS)
    kumite_matches = {m.id: m.model_copy(deep=True) for m in _SEED_KUMITE_MATCHES}
    kata_performances = {p.id: p.model_copy(deep=True) for p in _SEED_KATA_PERFORMANCES}
    brackets = {k: v.model_copy(deep=True) for k, v in _SEED_BRACKETS.items()}


def make_log_id() -> str:
    return f"log-{uuid.uuid4().hex[:8]}"


reset_store()
