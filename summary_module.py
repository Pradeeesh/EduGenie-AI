from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text for quick revision.

TEXT:
{text}

Requirements:
- Preserve the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use short paragraphs and bullet points where helpful.
- Do not introduce information that is not present in the source.
"""
    return generate_text(
        prompt,
        system_instruction="You create clear, faithful study summaries.",
        temperature=0.25,
        max_output_tokens=1200,
    )
