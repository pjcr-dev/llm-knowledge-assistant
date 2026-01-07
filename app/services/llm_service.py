from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)
#client = OpenAI()

SYSTEM_PROMPT = """
You are a knowledge assistant. Answer the user's questions using ONLY the provided context.

If multiple facts about the same entity are present, combine them into a
single coherent answer.

You may combine and summarize information from multiple context passages,
as long as each statement in your answer is directly supported by at least
one passage in the provided context.

Rules:
- If the answer is not explicitly stated in the context, respond with "I don't know based on the provided documents."
- Do NOT use prior knowledge.
- Do NOT guess.
- Do NOT invent names, facts, or details.
- Be concise and factual.
"""


def generate_answer(question: str, context: str) -> str:

    if not context.strip():
        return "I don't know based on the provided documents."

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question: 
{question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0
    )

    return response.output_text.strip()