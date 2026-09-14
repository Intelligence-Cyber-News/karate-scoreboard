from fastapi import APIRouter, HTTPException

from app import store
from app.models import Bracket, Division

router = APIRouter(tags=["divisions"])


@router.get("/divisions", response_model=list[Division])
def list_divisions():
    return store.divisions


@router.get("/divisions/{division_id}/bracket", response_model=Bracket)
def get_bracket(division_id: str):
    bracket = store.brackets.get(division_id)
    if bracket is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return bracket
