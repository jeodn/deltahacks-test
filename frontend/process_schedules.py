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

def get_availability_schedule(file_path: str, user: str) -> dict:
    '''
    Receives the file_path (intended to be student_schedules.csv) 
    and first name as seen on the csv as inputs, and outputs a schedule 
    as a dictionary of the form {(Start, Day): list[Name]}.
    The dictionary should not have keys included in the user's schedule,
    and list[Name] should be list of Name strings apart from the user that
    do not have class at a given (Start, Day)
    '''
    availability_schedule = {}
    user_schedule = get_user_schedule(file_path, user)
    
    # First, create a set of all students
    all_students = set()
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_students.add(row['Name'])
    
    # Create a dictionary to store busy students at each time slot
    busy_students = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start = int(row['Start'][:2])
            day = row['Day']
            name = row['Name']
            if (start, day) not in busy_students:
                busy_students[(start, day)] = set()
            busy_students[(start, day)].add(name)
    
    # For each possible time slot
    for hour in range(8, 22):  # 8 AM to 9 PM
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            # Skip if the user has class at this time
            if (hour, day) in user_schedule:
                continue
            
            # Find available students (all students minus busy ones)
            available = all_students - busy_students.get((hour, day), set())
            # Remove the user from the available list
            available.discard(user)
            
            # Only add to schedule if there are available students
            if available:
                availability_schedule[(hour, day)] = sorted(list(available))
    
    return availability_schedule

# # Test the function with a sample user
# test_dict = get_availability_schedule("backend/data/student_schedules.csv", "aidan")

# for item in test_dict.items():
#     print(item)