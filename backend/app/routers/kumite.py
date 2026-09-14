from fastapi import APIRouter, HTTPException

from app import kumite_rules, store
from app.models import (
    AwardPenaltyRequest,
    AwardPointRequest,
    HanteiRequest,
    KumiteMatch,
    SetClockRequest,
)

router = APIRouter(tags=["kumite"])


def _get_match_or_404(match_id: str) -> KumiteMatch:
    match = store.kumite_matches.get(match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.get("/kumite-matches", response_model=list[KumiteMatch])
def list_kumite_matches():
    return list(store.kumite_matches.values())


@router.get("/kumite-matches/{match_id}", response_model=KumiteMatch)
def get_kumite_match(match_id: str):
    return _get_match_or_404(match_id)


@router.post("/kumite-matches/{match_id}/points", response_model=KumiteMatch)
def award_point(match_id: str, body: AwardPointRequest):
    match = _get_match_or_404(match_id)
    kumite_rules.award_point(match, body.side, body.points)
    return match


@router.post("/kumite-matches/{match_id}/penalties", response_model=KumiteMatch)
def award_penalty(match_id: str, body: AwardPenaltyRequest):
    match = _get_match_or_404(match_id)
    kumite_rules.award_penalty(match, body.side, body.category)
    return match


@router.patch("/kumite-matches/{match_id}/clock", response_model=KumiteMatch)
def set_clock(match_id: str, body: SetClockRequest):
    match = _get_match_or_404(match_id)
    kumite_rules.set_clock(match, body.running, body.seconds)
    return match


@router.post("/kumite-matches/{match_id}/hantei", response_model=KumiteMatch)
def record_hantei(match_id: str, body: HanteiRequest):
    match = _get_match_or_404(match_id)
    kumite_rules.record_hantei(match, body.side)
    return match
