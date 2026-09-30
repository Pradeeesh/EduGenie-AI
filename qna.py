from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
Answer the following educational question accurately and concisely.

Question:
{question}

Requirements:
- Explain the answer in simple language.
- Use examples or a short step-by-step explanation when useful.
- Do not invent facts.
- If the question is ambiguous, state the assumption you are making.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a helpful academic learning assistant.",
        temperature=0.3,
        max_output_tokens=1000,
    )
