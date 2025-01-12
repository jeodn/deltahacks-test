import csv

def get_user_schedule(file_path: str, user: str) -> dict:
    '''
    Receives the file_path (intended to be student_schedules.csv) 
    and first name as seen on the csv as inputs, and outputs a user's schedule
    as a dictionary of the form {(Start, Day): Course Code}
    '''
    schedule = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Name'] == user:
                start = int(row['Start'][:2])
                day = row['Day']
                course_code = row['Course Code']
                schedule[(start, day)] = course_code
    return schedule


    
    