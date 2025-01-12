import os
import sys
from flask import Flask, render_template, request, redirect, url_for
import csv
from process_schedules import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from helper_functions import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'backend', 'calendars')

@app.route('/')
def start():
    print("Accessing start page")  # Debugging line
    return render_template('start.html')

@app.route('/schedule')
def index():
    user_schedule = get_user_schedule(os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'student_schedules.csv'), user_name)
    availability_schedule = get_availability_schedule(os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'student_schedules.csv'), user_name)
    
    max_available_students = max(
        len(students) 
        for students in availability_schedule.values()
    ) if availability_schedule else 1  # Prevent division by zero
    
    return render_template('schedule.html',
                         user_name=user_name,
                         user_schedule=user_schedule,
                         availability_schedule=availability_schedule,
                         max_available_students=max_available_students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'ics_file' not in request.files:
            return 'No file part'
        file = request.files['ics_file']
        if file.filename == '':
            return 'No selected file'
        if file:
            global user_name
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
            register_new_student(user_name, password, email, languages, bio, file_path, os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'user_database.csv'))
            
            # Append student data to the student schedules CSV
            append_student_data(file_path, os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'student_schedules.csv'), user_name, user_name)
            
            return redirect(url_for('index', name=user_name))
    return render_template('register.html')

@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    if request.method == 'POST':
        search_name = request.form['search_name'].lower()
        
        # Fix file paths using os.path.join
        schedules_path = os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'student_schedules.csv')
        user_db_path = os.path.join(app.config['UPLOAD_FOLDER'], '..', 'data', 'user_database.csv')
        
        schedule = get_user_schedule(schedules_path, search_name)
        
        # Get user info from user_database.csv
        user_info = {}
        with open(user_db_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'].lower() == search_name:
                    user_info = {
                        'Name': row['name'],
                        'Email': row['email'],
                        'Languages': row['languages'],
                        'Bio': row['bio']
                    }
                    break
        
        return render_template('profiles.html', user_info=user_info, schedule=schedule)
    return render_template('profile_search.html')

if __name__ == '__main__':
    app.run(debug=True)