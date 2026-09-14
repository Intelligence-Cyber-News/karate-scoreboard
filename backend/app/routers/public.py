from fastapi import APIRouter

from app import store
from app.models import PublicBoard, PublicKataEntry, PublicKumiteEntry

router = APIRouter(tags=["public"])


@router.get("/public-board", response_model=PublicBoard)
def get_public_board():
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
        for m in store.kumite_matches.values()
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
        for p in store.kata_performances.values()
    ]
    return PublicBoard(kumite=kumite, kata=kata)
