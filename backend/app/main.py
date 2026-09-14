from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import divisions, kata, kumite, public

app = FastAPI(title="Karate Scoreboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(divisions.router)
app.include_router(kumite.router)
app.include_router(kata.router)
app.include_router(public.router)
