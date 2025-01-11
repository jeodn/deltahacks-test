# Convert ICS file to CSV
import csv
from collections import defaultdict
from icalendar import Calendar
from datetime import datetime
import os
import json

# Functions to implement
# store students without a class
# store students with a class
# register new user (generate user id, store calendar/name, etc)
# id to name

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

# student_schedules.csv columns
STUSCHED_USERID = 0
STUSCHED_NAME = 1
STUSCHED_DAY = 2
STUSCHED_STARTTIME = 3
STUSCHED_ENDTIME = 4
STUSCHED_COURSECODE = 5
STUSCHED_COURSENAME = 6
STUSCHED_LOCATION = 7

def ics_to_csv(ics_file_path: str, csv_file_path: str) -> None:
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

def register_student_data(ics_file_path: str, database_file_path: str, user_id:int, student_name:str) -> None:
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
        file_path (str): Path to the CSV file.
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
            student_name = row["Student Name"]
            class_day = row["Day"]
            class_start_time = datetime.strptime(row["StartTime"], "%H:%M").time()
            class_end_time = datetime.strptime(row["EndTime"], "%H:%M").time()
            
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
            student_name = row["Name"]

            if day not in schedule:
                schedule[day] = {}
            if start_time not in schedule[day]:
                schedule[day][start_time] = {}
            if course_code not in schedule[day][start_time]:
                schedule[day][start_time][course_code] = []

            schedule[day][start_time][course_code].append(student_name)

    # Write to the output CSV file
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Day", "Time Start", "Class", "List of Names"])
        for day, times in schedule.items():
            for start_time, classes in times.items():
                for course_code, names in classes.items():
                    writer.writerow([day, start_time, course_code, ", ".join(names)])

    print(f"Successfully created class schedule at {output_csv_path}")

# Example usage
base_dir = os.path.dirname(os.path.abspath(__file__))
input_csv_path = os.path.join(base_dir, "./data/student_schedules.csv")
output_csv_path = os.path.join(base_dir, "./data/class_schedule.csv")
create_class_schedule(input_csv_path, output_csv_path)
