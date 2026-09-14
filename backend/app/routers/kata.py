from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import kata_rules, repository
from app.db import get_db
from app.models import KataPerformance, SubmitScoreRequest

router = APIRouter(tags=["kata"])


def _get_performance_or_404(db: Session, performance_id: str) -> KataPerformance:
    performance = repository.get_kata_performance(db, performance_id)
    if performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    return performance


@router.get("/kata-performances", response_model=list[KataPerformance])
def list_kata_performances(db: Session = Depends(get_db)):
    return repository.get_all_kata_performances(db)


@router.get("/kata-performances/{performance_id}", response_model=KataPerformance)
def get_kata_performance(performance_id: str, db: Session = Depends(get_db)):
    return _get_performance_or_404(db, performance_id)


@router.post("/kata-performances/{performance_id}/scores", response_model=KataPerformance)
def submit_judge_score(
    performance_id: str, body: SubmitScoreRequest, db: Session = Depends(get_db)
):
    performance = _get_performance_or_404(db, performance_id)
    kata_rules.submit_judge_score(performance, body.judgeIndex, body.score)
    repository.save_kata_performance(db, performance)
    return performance


@router.post("/kata-performances/{performance_id}/reset", response_model=KataPerformance)
def reset_scores(performance_id: str, db: Session = Depends(get_db)):
    performance = _get_performance_or_404(db, performance_id)
    kata_rules.reset_scores(performance)
    repository.save_kata_performance(db, performance)
    return performance
