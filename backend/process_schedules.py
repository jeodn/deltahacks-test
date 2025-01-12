import csv

def get_user_schedule(file_path: str, user: str) -> dict:
    schedule = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Name'] == user:
                start = row['Start']
                day = row['Day']
                course_code = row['Course Code']
                schedule[(start, day)] = course_code
    return schedule


    
    