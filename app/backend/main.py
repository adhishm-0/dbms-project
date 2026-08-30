from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class AnalyzeRequest(BaseModel):
    resume: str
    job: str


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    # This is a mocked implementation that simulates an AI analysis
    resume = req.resume or ""
    job = req.job or ""

    # crude keyword overlap for demo
    resume_words = set([w.lower() for w in resume.split() if len(w) > 2])
    job_words = set([w.lower() for w in job.split() if len(w) > 2])
    common = resume_words & job_words

    match_score = int(100 * (len(common) / (len(job_words) + 1)))

    missing = list(job_words - resume_words)[:10]

    questions = [
        f"Explain your experience with {w}." for w in list(common)[:5]
    ]

    return {
        "match_score": match_score,
        "common_keywords": list(common)[:30],
        "missing_keywords": missing,
        "suggested_questions": questions,
    }
