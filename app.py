from flask import Flask, render_template, request
from tutor_ai import ask_tutor

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    reply = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            reply = ask_tutor(question)

    return render_template("index.html", question=question, reply=reply)

if __name__ == "__main__":
    app.run()
