from flask import render_template, request
from flask_paginate import Pagination, get_page_parameter
import requests
import json

from app import app

questionData = None

@app.route('/', methods=["GET","POST"])
def index():
    global questionData

    if request.method == "POST":
        # if we want to submit the form
        if request.form['button'] == 'Submit':
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
                while (questionData[0]["invalid_count"] != None or len(questionData[0]['question']) == 0):
                    question = requests.get('http://jservice.io/api/random')
                    questionData = json.loads(question.text)

                pagination = Pagination(page=1, per_page=10, total=len(questionData), record_name='questionData', bs_version=4)
                errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
                return render_template("index.html", result=questionData, pagination=pagination, error=errorMsg)
            # we get questions back
            else:
                questionData = json.loads(question.text)

                offset = 100

                # query parsing to ensure proper command
                query2 = query + "?offset=" + str(offset) if (len(query) == 28) else query + "&offset=" + str(offset)
                question = requests.get(query2)

                # get up to 500 questions, if they exist
                while (offset < 500 and len(json.loads(question.text)) > 0):
                    questionData = questionData + json.loads(question.text) # I think this is the cause of the slow loading, but I'm not 100% sure
                    offset = offset + 100

                    query2 = query + "?offset=" + str(offset) if (len(query) == 28) else query + "&offset=" + str(offset)
                    question = requests.get(query2)


                # if we have at least one valid question, we can display them
                for questions in questionData:
                    if questions["invalid_count"] == None or len(question['question']) > 0:
                        page = request.args.get(get_page_parameter(), type=int, default=1)
                        pagination = Pagination(page=page, per_page=10, total=len(questionData), record_name='questionData', bs_version=4)
                        return render_template("index.html", result=questionData, pagination=pagination, error="")

                # if we somehow have no valid questions
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)

                # make sure the random question we get is valid
                while (questionData[0]["invalid_count"] != None or len(questionData[0]['question']) == 0):
                    question = requests.get('http://jservice.io/api/random')
                    questionData = json.loads(question.text)

                pagination = Pagination(page=1, per_page=10, total=len(questionData), record_name='questionData', bs_version=4)
                errorMsg = "No clues match those details. Please try again. A random clue has been provided instead."
                return render_template("index.html", result=questionData, pagination=pagination, error=errorMsg)
        # if they clicked the random button instead
        elif request.form['button'] == "Random":
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)

            # make sure the random question we get is valid
            while (questionData[0]["invalid_count"] != None or len(questionData[0]['question']) == 0):
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)

            pagination = Pagination(page=1, per_page=10, total=len(questionData), record_name='questionData', bs_version=4)
            return render_template("index.html", result=questionData, pagination=pagination, error="")
        else:
            print("This should never occur.") # this should never occur

    # GET requests
    else:
        # on first load, when we have no question data
        if questionData == None:
            question = requests.get('http://jservice.io/api/random')
            questionData = json.loads(question.text)

            while (questionData[0]["invalid_count"] != None or len(questionData[0]['question']) == 0):
                question = requests.get('http://jservice.io/api/random')
                questionData = json.loads(question.text)

        # display either recently received data or the data we already had, doesn't matter
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=10, total=len(questionData), record_name='questionData', bs_version=4)
        return render_template("index.html", result=questionData, pagination=pagination, error="")
