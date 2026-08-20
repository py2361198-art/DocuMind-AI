import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


def ask_ai(question, context=""):
    prompt = f"""
You are DocuMind AI, a document question-answering assistant.

Answer the user's question using the provided document context.

Document Context:
{context}

Question:
{question}

If the answer is not available in the document, clearly say:
"I could not find this information in the document."
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text
