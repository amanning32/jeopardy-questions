from flask import render_template, request
import requests
import json

from app import app

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        # parse input into format for API call
        # note the weirdness if one of min_date and max_date are passed but not both. jService flips them? so I flip them back
        query = 'http://jservice.io/api/clues?'
        if (len(request.form['min_date']) == 10):
            if (len(request.form['max_date']) == 10):
                query = query + "min_date=" + request.form['min_date'] + "&max_date=" + request.form['max_date'] + "&"
            else:
                query = query + "max_date=" + request.form['min_date'] + "&"
        elif (len(request.form['max_date']) == 10):
            query = query + "min_date=" + request.form['max_date'] + "&"
        if (request.form['category'] != ""):
            query = query + "category=" + request.form['category'] + "&"
        if (request.form['value'] != "Select value"):
            query = query + "value=" + request.form['value'] + "&"

        query = query[:-1] # either trailing ? or trailing &

        question = requests.get(query) # make API call

        # parse return from API call; error when no questions presented
        if (len(json.loads(question.text)) == 0):
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)

            # make sure the random question we get is valid
            while (questionData[0]["invalid_count"] != None):
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)

            errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
            return render_template("index.html", result = questionData, error = errorMsg)
        else:
            questionData = json.loads(question.text)

            for questions in questionData:
                if questions["invalid_count"] == None:
                    return render_template("index.html", result = questionData, error = "")

            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)

            # make sure the random question we get is valid
            while (questionData[0]["invalid_count"] != None):
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)

            errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
            return render_template("index.html", result = questionData, error = errorMsg)
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
