from flask import Flask, render_template, request, session
import sys
from calendar_custom import get_creds, authorize, insert_event
# from flask_session import Session

# create a new flask app
app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route('/', methods=['GET'])
def main():
    page_title = "Main"
    print("test")
    return render_template("main.html", page_title=page_title, result="")


@app.route('/', methods=['POST'])
def main_post():
    page_title = "Main"
    i = 1
    number_of_reps = float(request.form['number_of_reps'])
    percentage_increase = float(request.form['percentage_increase'])
    number_of_days = int(request.form["number_of_days"])
    reps = number_of_reps

    scope = 'events'
    creds = get_creds(scope)
    service = authorize(creds)

    for i in range(number_of_days):
        reps = reps + (percentage_increase * number_of_reps)
        insert_event(service, reps)

    return render_template("main.html", page_title=page_title, result="done")
