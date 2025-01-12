from flask import Flask, render_template, request, redirect, url_for
import os
import sys

# Add the backend directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from helper_functions import register_new_student, append_student_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'backend', 'calendars')

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
            user_name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            languages = request.form['languages']
            bio = request.form['bio']
            
            # Save the uploaded file
            filename = f"{user_name}-calendar-export.ics"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Register the new student and add to CSV
            register_new_student(user_name, password, user_name, languages, bio, file_path, os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'user_database.csv'))
            
            # Append student data to the student schedules CSV
            append_student_data(file_path, os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'student_schedules.csv'), user_name, user_name)
            
            return redirect(url_for('index', name=user_name))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)