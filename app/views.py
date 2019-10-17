from flask import render_template
import requests
import json

from app import app

@app.route('/')
def index():
    question = requests.get('http://jservice.io/api/random')
    questionData = json.loads(question.text)[0]
    while (questionData["invalid_count"] == 1):
        question = requests.get('http://jservice.io/api/random')
        questionData = json.loads(question.text)[0]
    return render_template("index.html", result = questionData)

@app.route('/about')
def about():
    return render_template("about.html")
