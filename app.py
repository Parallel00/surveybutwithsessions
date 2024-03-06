from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def show_start():
    return render_template("begin_survey.html", survey=survey)


@app.route("/begin", methods=["POST"])
def begin_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def question_handle():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_questions(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
        
    if len(responses) != qid:
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete_survey():
    return render_template("complete.html")
