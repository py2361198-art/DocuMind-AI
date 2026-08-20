import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


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

    response = model.generate_content(prompt)
    return response.text
