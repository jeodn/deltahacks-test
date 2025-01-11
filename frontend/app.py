from flask import Flask, render_template

EARLIEST_START_TIME = 8
LATEST_START_TIME = 20

app = Flask(__name__)

@app.route('/')
def index():
    calendar_data = {
        13
    }
    return render_template('index.html', num = 3, str = 'a')

if __name__ == "__main__":
    app.run(debug = True)