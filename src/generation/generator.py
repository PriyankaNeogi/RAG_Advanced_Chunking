import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query, contexts):

    context = "\n\n".join(contexts)

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content