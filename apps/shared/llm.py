import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message["content"].strip()
