from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data')

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/schedule')
def index():
    user_name = request.args.get('name', 'User')
    test_schedule = {
        "Mon": range(8, 20),
        "Tue": range(8, 20),
        "Wed": range(8, 20),
        "Thu": range(8, 20),
        "Fri": range(8, 20),
    }
    return render_template('index.html', schedule=test_schedule, user_name=user_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'ics_file' not in request.files:
            return 'No file part'
        file = request.files['ics_file']
        if file.filename == '':
            return 'No selected file'
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'user.ics'))
            user_name = request.form['name']
            return redirect(url_for('index', name=user_name))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)