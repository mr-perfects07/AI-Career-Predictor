"""FastAPI adapter for the AI Career Predictor service."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict

from .core import CAREERS, QUESTIONS, public_career, recommend


class Answers(BaseModel):
    model_config = ConfigDict(extra="forbid")

    interests: list[str]
    skills: list[str]
    subjects: list[str]
    work: list[str]
    priorities: list[str]


app = FastAPI(
    title="AI Career Predictor API",
    description="Exploratory career matches based on a small, explainable starter catalogue.",
    version="1.0.0",
)

origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000,https://aicareerpredictor.vercel.app",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/questions")
def get_questions():
    return QUESTIONS


@app.get("/careers")
def list_careers():
    return [public_career(career) for career in CAREERS]


@app.get("/careers/{career_id}")
def get_career(career_id: str):
    career = next((item for item in CAREERS if item["id"] == career_id), None)
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return public_career(career, include_details=True)


@app.post("/recommend")
def get_recommendations(answers: Answers):
    try:
        return recommend(answers.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


frontend = Path(__file__).resolve().parents[2] / "frontend"
if frontend.is_dir():
    app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
