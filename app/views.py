from flask import render_template, request
import requests
import json

from app import app

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        # parse input into format for API call
        query = 'http://jservice.io/api/clues?'
        if (len(request.form['min_date']) == 10):
            query = query + "min_date=" + request.form['min_date'] + "&"
        if (len(request.form['max_date']) == 10):
            query = query + "max_date=" + request.form['max_date'] + "&"
        if (request.form['category'] != ""):
            query = query + "category=" + request.form['category'] + "&"
        if (request.form['value'] != "Select value"):
            query = query + "value=" + request.form['value'] + "&"

        query = query[:-1] # either trailing ? or trailing &

        question = requests.get(query)

        if (len(json.loads(question.text)) == 0):
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)
            # while (questionData["invalid_count"] != None):
            #     question = requests.get('http://jservice.io/api/random')
            #     questionData = json.loads(question.text)
            errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
            return render_template("index.html", result = questionData, error = errorMsg)
        else:
            questionData = json.loads(question.text)

            # while (questionData["invalid_count"] != None):
            #     question = requests.get('http://jservice.io/api/clues?value=100')
            #     questionData = json.loads(question.text)

            return render_template("index.html", result = questionData, error = "")
    else: # initial load only, since any other loading is from a POST
        question = requests.get('http://jservice.io/api/random')
        questionData = json.loads(question.text)

        # http://jservice.io/api/categories?offset=18400&count=100 is bound for categories

        # max_date < 2015-03-31; min_date > 1984-09-10

        # while (questionData["invalid_count"] != None):
        #     question = requests.get('http://jservice.io/api/random')
        #     questionData = json.loads(question.text)

        return render_template("index.html", result = questionData, error = "")

@app.route('/about')
def about():
    return render_template("about.html")
