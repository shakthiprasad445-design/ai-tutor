import os
from google import genai
from groq import Groq

gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY_1"))
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_explain(question):
    prompt = f"""
You are a friendly AI tutor.

Explain the following in very simple language.
Use step-by-step explanation.
Use examples if helpful.

Question:
{question}

End with:
Final Answer:
"""
    try:
        r = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return r.text.strip()
    except:
        c = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}]
        )
        return c.choices[0].message.content.strip()


def generate_test_question(topic):
    prompt = f"""
You are a school teacher.

Create ONE clear question on the topic below.
Also provide the correct answer separately.

Format exactly like this:
QUESTION:
<question>

ANSWER:
<answer>

Topic:
{topic}
"""
    try:
        r = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return r.text.strip()
    except:
        c = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}]
        )
        return c.choices[0].message.content.strip()


def check_answer(student_answer, correct_answer):
    prompt = f"""
A student answered a question.

Correct Answer:
{correct_answer}

Student Answer:
{student_answer}

If the student's answer is correct or mostly correct:
Reply exactly:
CORRECT

If wrong:
Reply exactly:
WRONG

Do not explain.
"""
    try:
        r = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return r.text.strip()
    except:
        c = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}]
        )
        return c.choices[0].message.content.strip()


def explain_correct_answer(question, correct_answer):
    prompt = f"""
Explain the correct answer in simple language.

Question:
{question}

Correct Answer:
{correct_answer}
"""
    try:
        r = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return r.text.strip()
    except:
        c = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"user","content":prompt}]
        )
        return c.choices[0].message.content.strip()
