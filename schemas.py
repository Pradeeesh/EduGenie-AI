from pydantic import BaseModel, Field


class QARequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)
    level: str = Field(default="beginner", min_length=3, max_length=50)


class QuizRequest(BaseModel):
    text: str = Field(min_length=20, max_length=12000)
    question_count: int = Field(default=3, ge=1, le=10)


class SummaryRequest(BaseModel):
    text: str = Field(min_length=30, max_length=20000)


class LearnRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)
    level: str = Field(default="beginner", min_length=3, max_length=50)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QAResponse(BaseModel):
    answer: str


class ExplainResponse(BaseModel):
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class SummaryResponse(BaseModel):
    summary: str


class LearnResponse(BaseModel):
    recommendations: str


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
