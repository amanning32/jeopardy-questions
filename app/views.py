from flask import render_template, request
import requests
import json

from app import app

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":

        question = requests.get('http://jservice.io/api/clues?min_date='
            + request.form['min_date'] + "&max_date=" + request.form['max_date'])

        if (len(json.loads(question.text)) == 0):
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)[0]
            while (questionData["invalid_count"] != None):
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)[0]
            errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
            return render_template("index.html", result = questionData, error = errorMsg)
        else:
            questionData = json.loads(question.text)[0]

            print(len(json.loads(question.text)))

            while (questionData["invalid_count"] != None):
                question = requests.get('http://jservice.io/api/clues?value=100')
                questionData = json.loads(question.text)[0]

            return render_template("index.html", result = questionData, error = "")
    else:
        question = requests.get('http://jservice.io/api/random')
        questionData = json.loads(question.text)[0]

        # http://jservice.io/api/categories?offset=18400&count=100 is bound for categories

        # max_date < 2015-03-31; min_date > 1984-09-10

        while (questionData["invalid_count"] != None):
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)[0]

        return render_template("index.html", result = questionData, error = "") # add error = error

@app.route('/about')
def about():
    return render_template("about.html")
