import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def generate_answer(question, context):
    if not API_KEY:
        return "GEMINI_API_KEY is not configured."

    prompt = f"""
You are DocuMind AI, a document question-answering assistant.

Answer the user's question using ONLY the provided document context.
If the answer is not present in the context, say:
"I could not find this information in the uploaded document."

Document Context:
{context}

User Question:
{question}

Give a clear and concise answer.
"""

    response = model.generate_content(prompt)

    return response.text
