# Convert ICS file to CSV
import csv
from collections import defaultdict
from icalendar import Calendar
from datetime import datetime
import os
import json
from random import *
import ast 

# Functions to implement
# store students without a class
# store students with a class
# register new user (generate user id, store calendar/name, etc)
# generate a random study session time based on class_schedule

# FAQ
# How do Students log in?
#   Students log in using a username and a password. 
#   The backend identification identifies students using an assigned user ID.
#   But they log in using the username.

# Constants
NUM_TO_WEEKDAY = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

WEEKDAY_TO_NUM = {
    "Monday":0,
    "Tuesday":1,
    "Wednesday":2,
    "Thursday":3,
    "Friday":4,
    "Saturday":5,
    "Sunday":6
}

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

# student_schedules.csv columns
STUSCHED_USERID = 0
STUSCHED_NAME = 1
STUSCHED_DAY = 2
STUSCHED_STARTTIME = 3
STUSCHED_ENDTIME = 4
STUSCHED_COURSECODE = 5
STUSCHED_COURSENAME = 6
STUSCHED_LOCATION = 7

# Directories
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "calendars/josh-calendar-export.ics")
example_student_schedules_name = os.path.join(base_dir, "data/student_schedules.csv")
example_user_database = os.path.join("./backend/data/user_database.csv")
example_noclasses_database = os.path.join("./backend/data/available_timeslots.csv")
example_timeslots_database = os.path.join("./backend/data/timeslots_with_frequency.csv")
example_userid = 1

# Student Schedules Headers
SSCH_USERID = "UserID"
SSCH_NAME = "Name"
SSCH_DAY = "Day" 
SSCH_START = "Start"
SSCH_END = "End"
SSCH_COURSECODE = "Course Code"
SSCH_COURSENAME = "Course Name"
SSCH_LOCATION = "Location"

def ics_to_csv(ics_file_path: str, csv_file_path: str) -> None: # OLD FUNCTION
    """
    Converts an .ics (iCalendar) file to a .csv file. 
    Columns are: Start,End,Summary,Description,Location
    
    Args:
        ics_file_path (str): Path to the input .ics file.
        csv_file_path (str): Path to the output .csv file.
    
    Raises:
        FileNotFoundError: If the .ics file does not exist.
        ValueError: If the .ics file is invalid or has no events.
    """
    # Check if the input file exists
    if not os.path.exists(ics_file_path):
        raise FileNotFoundError(f"The file {ics_file_path} does not exist.")

    # Read and parse the .ics file
    with open(ics_file_path, "r", encoding="utf-8") as file:
        try:
            calendar = Calendar.from_ical(file.read())
        except Exception as e:
            raise ValueError(f"Error parsing .ics file: {e}")

    # Extract events and prepare data for CSV
    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            start_date = component.get("dtstart").dt if component.get("dtstart") else ""
            end_date = component.get("dtend").dt if component.get("dtend") else ""

            event = {
                "Day": datetime.fromisoformat(str(start_date)).strftime("%A"), # datetime to day
                "Start": datetime.fromisoformat(str(start_date)).strftime("%H:%M"), # datetime to time
                "End": datetime.fromisoformat(str(end_date)).strftime("%H:%M"),
                "Course Code": component.get("summary", ""),
                "Course Name": component.get("description", "").split('\n')[0], # GET ANYTHING BEFORE \N
                "Location": component.get("location", "")
            }
            events.append(event)
            # REMOVE ANYTHING AFTER \n, AND DISREGARD IF EVENT LOCATION IS "ZZ TBA"

    if not events:
        raise ValueError("No events found in the .ics file.")

    # Write events to a CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Day", "Start", "End", "Course Code", "Course Name", "Location"])
        writer.writeheader()
        writer.writerows(events)

    print(f"Successfully converted {ics_file_path} to {csv_file_path}")

def append_student_data(ics_file_path: str, database_file_path: str, user_id:int, student_name:str) -> None:
    """
    Add student data to end of big data file (database_file_path)
    """

    # Check if the input file exists
    if not os.path.exists(ics_file_path):
        raise FileNotFoundError(f"The file {ics_file_path} does not exist.")

    # Read and parse the .ics file
    with open(ics_file_path, "r", encoding="utf-8") as file:
        try:
            calendar = Calendar.from_ical(file.read())
        except Exception as e:
            raise ValueError(f"Error parsing .ics file: {e}")

    # Extract events and prepare data for CSV
    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            start_date = component.get("dtstart").dt if component.get("dtstart") else ""
            end_date = component.get("dtend").dt if component.get("dtend") else ""

            event = {
                "UserID": user_id,
                "Name": student_name,
                "Day": datetime.fromisoformat(str(start_date)).strftime("%A"), # datetime to day
                "Start": datetime.fromisoformat(str(start_date)).strftime("%H:%M"), # datetime to time
                "End": datetime.fromisoformat(str(end_date)).strftime("%H:%M"),
                "Course Code": component.get("summary", ""),
                "Course Name": component.get("description", "").split('\n')[0], # GET ANYTHING BEFORE \N
                "Location": component.get("location", "")
            }
            events.append(event)
            # REMOVE ANYTHING AFTER \n, AND DISREGARD IF EVENT LOCATION IS "ZZ TBA"

    if not events:
        raise ValueError("No events found in the .ics file.")

    # Write events to a CSV file
    with open(database_file_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["UserID", "Name", "Day", "Start", "End", "Course Code", "Course Name", "Location"])
        #writer.writeheader()
        writer.writerows(events)

    print(f"Successfully added {ics_file_path} to {database_file_path}")

def count_students_without_classes(file_path: str, day: str, start_time: str, end_time:str) -> list:
    """
    Counts the number of students who do not have a class during the given time period on a specific day.
    
    Args:
        file_path (str): Path to the student schedule CSV file.
        day (str): The day to filter (e.g., "Monday").
        start_time (str): Start of the time range in HH:MM format (e.g., "12:00").
        end_time (str): End of the time range in HH:MM format (e.g., "13:00").
        
    Returns:
        int: Number of students without classes during the specified time range.
    """
    students_with_classes = set()
    all_students = set()
    
    # Convert start_time and end_time to time objects for comparison
    start_time = datetime.strptime(start_time, "%H:%M").time()
    end_time = datetime.strptime(end_time, "%H:%M").time()
    
    # Open and read the CSV file
    with open(file_path, newline='', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            student_name = row[SSCH_NAME]
            class_day = row[SSCH_DAY]
            class_start_time = datetime.strptime(row[SSCH_START], "%H:%M").time()
            class_end_time = datetime.strptime(row[SSCH_END], "%H:%M").time()
            
            # Add all students to the complete list
            all_students.add(student_name)
            
            # Check if the class overlaps with the given time range on the given day
            if class_day == day:
                if not (class_end_time <= start_time or class_start_time >= end_time):
                    # The class overlaps with the given time range
                    students_with_classes.add(student_name)
    
    # Students without classes = All students - Students with classes
    students_without_classes = all_students - students_with_classes
    
    return students_without_classes

def int_to_time(x:int) -> str:
    return datetime.strptime(str(x), "%H").strftime("%H:%M")

def time_to_int(timestr:str) -> int:
    return int(timestr[0:2])

def generate_available_timeslot_database(database_path: str) -> None:
    """
    For each hour on each day, generate list of which students do NOT have a class.
    Export to database_path.
    """
    END_OF_DAY = 23

    # Check if database file exists
    if not os.path.exists(database_path):
        raise FileNotFoundError(f"The file {database_path} does not exist.")
    
    with open(database_path, "w", newline='', encoding="utf-8") as database:
        writer = csv.DictWriter(database, fieldnames=[x for x in range(0,END_OF_DAY+1)])
        writer.writeheader()

        for day in range(MONDAY, SATURDAY):
            availability_by_hour = {}
            for hour in range(0, END_OF_DAY):
                list_without_classes = count_students_without_classes(example_student_schedules_name,
                                                                            NUM_TO_WEEKDAY[day], int_to_time(hour), int_to_time(hour + 1))
            availability_by_hour[hour] = str(list_without_classes).strip("\{").strip("\}")
            #print(availability_by_hour[22])
            writer.writerow(availability_by_hour)

    print("Successfully generated timeslot database.")

def student_available_this_hour(userid:int, day:int, hour:int) -> bool:
    with open(example_student_schedules_name) as schedules:
        L = schedules.readlines()
        i=0
        for l in L:
            if i == 0:
                i += 1
                continue
            line = l.split(',')
            A = line[STUSCHED_USERID]
            B = line[STUSCHED_DAY]
            C = line[STUSCHED_STARTTIME]
            if int(A)== userid and WEEKDAY_TO_NUM[B]==day and time_to_int(C)==hour:
                return False
            i += 1
    return True

def generate_timeslot_freq_database(database_path: str) -> list[list[int]]:
    """
    For each hour on each day, generate number of how many students do NOT have a class.
    Export to database_path.
    """
    END_OF_DAY = 23
    ids = [1, 2, 3, 4, 5]

    # Check if database file exists
    if not os.path.exists(database_path):
        raise FileNotFoundError(f"The file {database_path} does not exist.")
    
    list_of_days = [] # list of lists
    for day in range(5):
        list_of_days.append([])
        for hour in range(END_OF_DAY):
            list_of_days[day].append(0)
            for id in ids:
                student_available = student_available_this_hour(id, day, hour)
                list_of_days[day][hour] += student_available

    print("Successfully generated timeslot list of lists.")

    return list_of_days

    

def id_to_name(id_datafile:str, user_id:int) -> str:
    """
    Get name of student given their User ID (which is not student ID).
    User IDs are stored in a .json file with filename <id_datafile>
    """
    string_user_id = str(user_id)

    with open(id_datafile) as id_file:
        for line in id_file:
            row = line.split(",")
            row_id = row[STUSCHED_USERID]
            if string_user_id == str(row_id):
                user_name = row[STUSCHED_NAME]
                return user_name
    
def create_class_schedule(input_csv_path: str, output_csv_path: str) -> None:
    """
    Creates a new CSV file with the format: date | time start | class | list of names taking that class.
    
    Args:
        input_csv_path (str): Path to the input student schedules CSV file.
        output_csv_path (str): Path to the output CSV file.
    """
    schedule = defaultdict(dict)

    # Read the input CSV file
    with open(input_csv_path, newline='', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            day = row["Day"]
            start_time = row["Start"]
            course_code = row["Course Code"]
            UserID = row["UserID"]

            if day not in schedule:
                schedule[day] = {}
            if start_time not in schedule[day]:
                schedule[day][start_time] = {}
            if course_code not in schedule[day][start_time]:
                schedule[day][start_time][course_code] = []

            schedule[day][start_time][course_code].append(UserID)

    # Write to the output CSV file
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Day", "Time Start", "Class", "List of Names"])
        for day, times in schedule.items():
            for start_time, classes in times.items():
                for course_code, names in classes.items():
                    writer.writerow([day, start_time, course_code, ", ".join(names)])

    print(f"Successfully created class schedule at {output_csv_path}")

def generate_user_id():
    return random.randint(100, 999)

def register_new_student(username:str, password:str, name:str, languages:list, bio:str, 
                          calendar_filepath:str, database_filepath:str) -> None:
    """
    Creates new user in database.
    Generates user ID
    """

    # Check if the data file exists
    if not os.path.exists(database_filepath):
        raise FileNotFoundError(f"The file {database_filepath} does not exist.")

    UserID = generate_user_id()

    my_profile = {
        "Username" : username,
        "Password" : password,
        "UserID" : UserID,
        "Name" : name,
        "Languages" : languages,
        "Bio" : bio
    }

    with open(database_filepath, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Username","Password","UserID", "Name","Languages","Bio"])
        #writer.writeheader()
        writer.writerow(my_profile)

    print(f"Successfully added {name} with user {username}.")

def generate_study_session_time(day:int) -> tuple:
    """
    Generate a random study session time in tuple format (Day, Start Time, End Time)
    """

    a = randint(0, 23)
    return (NUM_TO_WEEKDAY[day], a, a + 1)
