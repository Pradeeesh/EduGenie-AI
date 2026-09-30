from functools import lru_cache

from config import settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _load_local_explainer():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
        device=-1,
    )


def _local_explain(topic: str, level: str) -> str:
    generator = _load_local_explainer()
    prompt = (
        f"Explain {topic} for a {level} learner. "
        "Use simple language, a short analogy, and one example."
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str, level: str = "beginner") -> str:
    if settings.explainer_backend == "local":
        try:
            return _local_explain(topic, level)
        except Exception:
            # A local model can fail because model files are unavailable or hardware
            # is insufficient. Fall back to Gemini so the application remains usable.
            pass

    prompt = f"""
Explain the educational topic below for a {level} learner.

Topic: {topic}

Use this structure:
1. Simple definition
2. How it works
3. Everyday or practical analogy
4. One clear example
5. Three key points to remember

Keep it readable and avoid unnecessary jargon.
"""
    return generate_text(
        prompt,
        system_instruction="You simplify difficult educational concepts without losing correctness.",
        temperature=0.35,
        max_output_tokens=1200,
    )
