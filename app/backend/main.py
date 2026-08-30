from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select

app = FastAPI()

# SQLite DB - stored at app/backend/db.sqlite
DATABASE_URL = "sqlite:///./app/backend/db.sqlite"
engine = create_engine(DATABASE_URL, echo=False)


class AnalyzeRequest(BaseModel):
    resume: str
    job: str


class AnalysisResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resume_text: str
    job_text: str
    match_score: int
    common_keywords: str
    missing_keywords: str
    suggested_questions: str


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    resume = req.resume or ""
    job = req.job or ""

    resume_words = set([w.lower().strip('.,()') for w in resume.split() if len(w) > 2])
    job_words = set([w.lower().strip('.,()') for w in job.split() if len(w) > 2])
    common = sorted(list(resume_words & job_words))

    match_score = int(100 * (len(common) / (len(job_words) + 1)))

    missing = sorted(list(job_words - resume_words))[:50]

    questions = [f"Explain your experience with {w}." for w in common[:10]]

    # persist to DB
    result = AnalysisResult(
        resume_text=resume,
        job_text=job,
        match_score=match_score,
        common_keywords=','.join(common),
        missing_keywords=','.join(missing),
        suggested_questions='||'.join(questions),
    )

    with Session(engine) as session:
        session.add(result)
        session.commit()
        session.refresh(result)

    return {
        "id": result.id,
        "match_score": match_score,
        "common_keywords": common,
        "missing_keywords": missing,
        "suggested_questions": questions,
    }
