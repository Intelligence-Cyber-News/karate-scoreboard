from fastapi import APIRouter, HTTPException

from app import kata_rules, store
from app.models import KataPerformance, SubmitScoreRequest

router = APIRouter(tags=["kata"])


def _get_performance_or_404(performance_id: str) -> KataPerformance:
    performance = store.kata_performances.get(performance_id)
    if performance is None:
        raise HTTPException(status_code=404, detail="Performance not found")
    return performance


@router.get("/kata-performances", response_model=list[KataPerformance])
def list_kata_performances():
    return list(store.kata_performances.values())


@router.get("/kata-performances/{performance_id}", response_model=KataPerformance)
def get_kata_performance(performance_id: str):
    return _get_performance_or_404(performance_id)


@router.post("/kata-performances/{performance_id}/scores", response_model=KataPerformance)
def submit_judge_score(performance_id: str, body: SubmitScoreRequest):
    performance = _get_performance_or_404(performance_id)
    kata_rules.submit_judge_score(performance, body.judgeIndex, body.score)
    return performance


@router.post("/kata-performances/{performance_id}/reset", response_model=KataPerformance)
def reset_scores(performance_id: str):
    performance = _get_performance_or_404(performance_id)
    kata_rules.reset_scores(performance)
    return performance
