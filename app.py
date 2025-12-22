from flask import Flask, render_template, request, session
from tutor_ai import (
    ask_explain,
    generate_test_question,
    check_answer,
    explain_correct_answer
)

app = Flask(__name__)
app.secret_key = "ai-tutor-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    session.setdefault("chat", [])
    session.setdefault("test", None)

    if request.method == "POST":
        mode = request.form.get("mode", "explain")
        user_input = request.form.get("question", "").strip()

        if not user_input:
            return render_template("index.html", chat=session["chat"])

        session["chat"].append(("user", user_input))

        # ===== EXPLAIN MODE =====
        if mode == "explain":
            reply = ask_explain(user_input)
            session["chat"].append(("tutor", reply))

        # ===== TEST MODE =====
        elif mode == "test":
            test = session.get("test")

            # No active test → generate question
            if not test:
                qa = generate_test_question(user_input)
                q = qa.split("ANSWER:")[0].replace("QUESTION:", "").strip()
                a = qa.split("ANSWER:")[1].strip()

                session["test"] = {
                    "question": q,
                    "answer": a
                }

                session["chat"].append(("tutor", f"📝 Test Question:\n{q}"))

            # Active test → check answer
            else:
                result = check_answer(user_input, test["answer"])

                if "CORRECT" in result:
                    session["chat"].append(("tutor", "✅ Correct! Well done 🎉"))
                else:
                    explanation = explain_correct_answer(
                        test["question"], test["answer"]
                    )
                    session["chat"].append((
                        "tutor",
                        f"❌ Incorrect.\n\nCorrect Answer:\n{test['answer']}\n\nExplanation:\n{explanation}"
                    ))

                session["test"] = None  # reset for next question

        session.modified = True

    return render_template("index.html", chat=session["chat"])

if __name__ == "__main__":
    app.run(debug=True)
