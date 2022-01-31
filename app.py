from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'shhhh'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def index():
    """ start survey page showing title, instructions, start button """

    return render_template("start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """ clear session & go to first question """

    session['responses'] = []
    
    return redirect("/questions/0")


@app.route('/questions/<int:q_id>')
def quest(q_id):
    """ show 1 question per page """
    responses = session.get('responses')

    if responses is None: 
        # trying to access question page too soon
        return redirect('/')

    if len(responses) == len(survey.questions):
        # They've answered all the questions! Thank them.
        return redirect("/thanks")

    if len(responses) != q_id :
        # Trying to access questions out of order.
        flash(f"Error 400{q_id}: You can't go there.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[q_id]
    return render_template("questions.html", question_num=q_id, question=question)


@app.route('/answer', methods=["POST"])
def ans():
    """ Save response and redirect to next question """

    # get the response choice
    choice = request.form['answer']

    # add response to session
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/thanks")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def complete():
    """ Survey complete. Show thanks page """

    return render_template("thanks.html")