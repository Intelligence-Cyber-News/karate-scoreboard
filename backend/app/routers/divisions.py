from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import repository
from app.db import get_db
from app.models import Bracket, Division

router = APIRouter(tags=["divisions"])


@router.get("/divisions", response_model=list[Division])
def list_divisions(db: Session = Depends(get_db)):
    return repository.get_all_divisions(db)


@router.get("/divisions/{division_id}/bracket", response_model=Bracket)
def get_bracket(division_id: str, db: Session = Depends(get_db)):
    bracket = repository.get_bracket(db, division_id)
    if bracket is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return bracket
