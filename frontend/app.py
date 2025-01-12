from flask import Flask, render_template
from front_end_helpers import *

EARLIEST_START_TIME = 8
LATEST_START_TIME = 20

app = Flask(__name__)

@app.route('/')
def index():
    test_schedule = {
        "Mon": range(LATEST_START_TIME - EARLIEST_START_TIME),
        "Tue": range(LATEST_START_TIME - EARLIEST_START_TIME),
        "Wed": range(LATEST_START_TIME - EARLIEST_START_TIME),
        "Thu": range(LATEST_START_TIME - EARLIEST_START_TIME),
        "Fri": range(LATEST_START_TIME - EARLIEST_START_TIME),
    }
    return render_template('index.html', test_schedule)

if __name__ == "__main__":
    app.run(debug = True)