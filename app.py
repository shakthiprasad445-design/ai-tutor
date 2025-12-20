from flask import Flask, render_template, request, session
from tutor_ai import ask_tutor

app = Flask(__name__)
app.secret_key = "ai-tutor-secret-key"  # required for session

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat" not in session:
        session["chat"] = []

    thinking = False

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            # Add user message
            session["chat"].append(("user", question))

            thinking = True
            reply = ask_tutor(question)
            thinking = False

            # Add tutor reply
            session["chat"].append(("tutor", reply))

            session.modified = True

    return render_template(
        "index.html",
        chat=session["chat"],
        thinking=thinking
    )

if __name__ == "__main__":
    app.run(debug=True)
