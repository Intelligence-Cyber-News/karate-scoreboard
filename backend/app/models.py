from typing import Literal, Optional

from pydantic import BaseModel, Field

Side = Literal["aka", "ao"]


class Division(BaseModel):
    id: str
    name: str
    discipline: Literal["kumite", "kata"]
    ageGroup: str
    weightClass: Optional[str] = None
    gender: str
    mat: int


class Competitor(BaseModel):
    name: str


class Penalties(BaseModel):
    c1: int
    c2: int


class LogEntry(BaseModel):
    id: str
    text: str


class KumiteMatch(BaseModel):
    id: str
    divisionId: str
    mat: int
    round: str
    aka: Competitor
    ao: Competitor
    pointsAka: int
    pointsAo: int
    penaltiesAka: Penalties
    penaltiesAo: Penalties
    senshu: Optional[Side] = None
    clockSeconds: int
    clockRunning: bool
    status: Literal["in_progress", "ended"]
    winner: Optional[Side] = None
    endReason: Optional[Literal["points", "time", "hantei", "disqualification"]] = None
    log: list[LogEntry]


class KataPerformance(BaseModel):
    id: str
    divisionId: str
    mat: int
    round: str
    competitor: Competitor
    judgeScores: list[Optional[float]] = Field(min_length=7, max_length=7)
    finalScore: Optional[float] = None
    status: Literal["scoring", "scored"]


class PoolStanding(BaseModel):
    competitor: str
    wins: int
    losses: int


class EliminationMatch(BaseModel):
    a: str
    b: str
    winner: Optional[str] = None


class EliminationRound(BaseModel):
    round: str
    matches: list[EliminationMatch]


class Bracket(BaseModel):
    pool: list[PoolStanding]
    elimination: list[EliminationRound]


class PublicKumiteEntry(BaseModel):
    id: str
    mat: int
    round: str
    aka: str
    ao: str
    pointsAka: int
    pointsAo: int
    clockSeconds: int
    status: Literal["in_progress", "ended"]
    winner: Optional[Side] = None


class PublicKataEntry(BaseModel):
    id: str
    mat: int
    round: str
    competitor: str
    finalScore: Optional[float] = None
    status: Literal["scoring", "scored"]


class PublicBoard(BaseModel):
    kumite: list[PublicKumiteEntry]
    kata: list[PublicKataEntry]


# ---- Request bodies -------------------------------------------------------


class AwardPointRequest(BaseModel):
    side: Side
    points: Literal[1, 2, 3]


class AwardPenaltyRequest(BaseModel):
    side: Side
    category: Literal["c1", "c2"]


class SetClockRequest(BaseModel):
    running: Optional[bool] = None
    seconds: Optional[int] = Field(default=None, ge=0)


class HanteiRequest(BaseModel):
    side: Side


class SubmitScoreRequest(BaseModel):
    judgeIndex: int = Field(ge=0, le=6)
    score: float = Field(ge=0, le=10)
