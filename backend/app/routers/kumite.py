from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import kumite_rules, repository
from app.db import get_db
from app.models import (
    AwardPenaltyRequest,
    AwardPointRequest,
    HanteiRequest,
    KumiteMatch,
    SetClockRequest,
)

router = APIRouter(tags=["kumite"])


def _get_match_or_404(db: Session, match_id: str) -> KumiteMatch:
    match = repository.get_kumite_match(db, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/kumite-matches", response_model=list[KumiteMatch])
def list_kumite_matches(db: Session = Depends(get_db)):
    return repository.get_all_kumite_matches(db)


@router.get("/kumite-matches/{match_id}", response_model=KumiteMatch)
def get_kumite_match(match_id: str, db: Session = Depends(get_db)):
    return _get_match_or_404(db, match_id)


@router.post("/kumite-matches/{match_id}/points", response_model=KumiteMatch)
def award_point(match_id: str, body: AwardPointRequest, db: Session = Depends(get_db)):
    match = _get_match_or_404(db, match_id)
    kumite_rules.award_point(match, body.side, body.points)
    repository.save_kumite_match(db, match)
    return match


@router.post("/kumite-matches/{match_id}/penalties", response_model=KumiteMatch)
def award_penalty(match_id: str, body: AwardPenaltyRequest, db: Session = Depends(get_db)):
    match = _get_match_or_404(db, match_id)
    kumite_rules.award_penalty(match, body.side, body.category)
    repository.save_kumite_match(db, match)
    return match


@router.patch("/kumite-matches/{match_id}/clock", response_model=KumiteMatch)
def set_clock(match_id: str, body: SetClockRequest, db: Session = Depends(get_db)):
    match = _get_match_or_404(db, match_id)
    kumite_rules.set_clock(match, body.running, body.seconds)
    repository.save_kumite_match(db, match)
    return match


@router.post("/kumite-matches/{match_id}/hantei", response_model=KumiteMatch)
def record_hantei(match_id: str, body: HanteiRequest, db: Session = Depends(get_db)):
    match = _get_match_or_404(db, match_id)
    kumite_rules.record_hantei(match, body.side)
    repository.save_kumite_match(db, match)
    return match
