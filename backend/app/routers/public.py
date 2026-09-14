from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import repository
from app.db import get_db
from app.models import PublicBoard, PublicKataEntry, PublicKumiteEntry

router = APIRouter(tags=["public"])


@router.get("/public-board", response_model=PublicBoard)
def get_public_board(db: Session = Depends(get_db)):
    kumite = [
        PublicKumiteEntry(
            id=m.id,
            mat=m.mat,
            round=m.round,
            aka=m.aka.name,
            ao=m.ao.name,
            pointsAka=m.pointsAka,
            pointsAo=m.pointsAo,
            clockSeconds=m.clockSeconds,
            status=m.status,
            winner=m.winner,
        )
        for m in repository.get_all_kumite_matches(db)
    ]
    kata = [
        PublicKataEntry(
            id=p.id,
            mat=p.mat,
            round=p.round,
            competitor=p.competitor.name,
            finalScore=p.finalScore,
            status=p.status,
        )
        for p in repository.get_all_kata_performances(db)
    ]
    return PublicBoard(kumite=kumite, kata=kata)
