import json

from pydantic import BaseModel, Field, ValidationError

from gemini_client import generate_text


class QuizItem(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def generate_quiz(text: str, question_count: int = 3) -> list[QuizItem]:
    prompt = f"""
Create exactly {question_count} multiple-choice questions from the educational passage below.

PASSAGE:
{text}

Rules:
- Each question must have exactly four options.
- correct_answer must exactly match one option.
- Include a short explanation for the correct answer.
- Questions must be answerable from the passage or straightforwardly from its concepts.
- Return ONLY a JSON array.
"""

    raw = generate_text(
        prompt,
        system_instruction="You generate reliable educational assessment questions.",
        temperature=0.2,
        max_output_tokens=1800,
        response_mime_type="application/json",
    )

    try:
        data = json.loads(clean_json_block(raw))
        items = [QuizItem.model_validate(item) for item in data]
    except (json.JSONDecodeError, ValidationError, TypeError) as exc:
        raise RuntimeError(f"Quiz generation returned invalid JSON: {exc}") from exc

    if len(items) != question_count:
        raise RuntimeError(
            f"Expected {question_count} quiz questions but received {len(items)}."
        )

    for item in items:
        if item.correct_answer not in item.options:
            raise RuntimeError("Quiz validation failed: correct answer is not an option.")
    return items
