import os
from google import genai
from google.genai.errors import ClientError
from groq import Groq

# ---------- Clients ----------
gemini_clients = [
    genai.Client(api_key=os.getenv("GEMINI_API_KEY_1")),
    genai.Client(api_key=os.getenv("GEMINI_API_KEY_2")),
]

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

CACHE = {}

def build_prompt(question):
    return f"""
Explain step by step in simple language.
At the end, clearly write:
Final Answer:

Question: {question}
"""

def ask_gemini(prompt):
    for client in gemini_clients:
        if not client:
            continue
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
        except ClientError:
            continue
        except Exception:
            continue
    return None

def ask_groq(prompt):
    try:
        completion = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return None

def ask_tutor(question):
    if question in CACHE:
        return CACHE[question]

    prompt = build_prompt(question)

    # 1️⃣ Try Gemini (rotate keys)
    answer = ask_gemini(prompt)
    if answer:
        CACHE[question] = answer
        return answer

    # 2️⃣ Fallback to Groq
    answer = ask_groq(prompt)
    if answer:
        CACHE[question] = answer
        return answer

    return "⏳ The tutor is busy right now. Please try again shortly 😊"
