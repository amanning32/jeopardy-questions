# jeopardy-questions

This Flask website interfaces with the jService API to display *Jeopardy!* questions per user requests based on date, category, and question value.

**NOTE: This is a work of progress which is constantly being updated. There are incomplete features and features yet-to-be-implemented.**

To build, ensure that all of the dependencies in `requirements.txt` are downloaded on your machine. If you have pip, this can be done in the terminal or command line by running `pip install -r requirements.txt` in the home directory of the repository. I recommend setting up a virtual environment to ensure no conflicts with other python versions and dependencies.

Then navigate to the home directory of this repository in the terminal or command line and run `flask run`. The website will then appear at `127.0.0.1:5000`.

Known bugs:
- Search only reliably works when all fields are filled.
- No way to find category IDs natively.
- Can only display up to 100 valid questions.
