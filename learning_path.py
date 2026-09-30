from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""
Create a personalized learning path for the topic "{topic}" for a {level} learner.

Organize it from beginner to advanced. For each stage include:
- Concepts to learn
- Suggested practice
- A realistic time estimate
- What the learner should be able to do afterward
- Resource types to look for (videos, articles, books, documentation)

End with a simple weekly study routine and a self-checklist.
"""
    return generate_text(
        prompt,
        system_instruction="You design practical, learner-friendly educational roadmaps.",
        temperature=0.45,
        max_output_tokens=1800,
    )
