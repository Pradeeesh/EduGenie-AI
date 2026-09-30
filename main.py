from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import (
    ExplainRequest, LearnRequest, QARequest, QuizRequest, SummaryRequest,
    ExplainResponse, LearnResponse, QAResponse, QuizResponse, SummaryResponse,
    HealthResponse,
)
from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="EduGenie - Google Gemini powered learning assistant",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", gemini_configured=settings.gemini_configured)


@app.post("/qa", response_model=QAResponse)
async def qa(payload: QARequest):
    return QAResponse(answer=answer_question(payload.question))


@app.post("/explain", response_model=ExplainResponse)
async def explain(payload: ExplainRequest):
    return ExplainResponse(explanation=explain_topic(payload.topic, payload.level))


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: QuizRequest):
    return QuizResponse(questions=generate_quiz(payload.text, payload.question_count))


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(payload: SummaryRequest):
    return SummaryResponse(summary=summarize_text(payload.text))


@app.post("/learn/recommendations", response_model=LearnResponse)
async def learn(payload: LearnRequest):
    return LearnResponse(recommendations=get_learning_recommendations(payload.topic, payload.level))
