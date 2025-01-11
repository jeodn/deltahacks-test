# Convert ICS file to CSV
import csv
from icalendar import Calendar
from datetime import datetime
import os

# Functions to implement
# store students without a class
# store students with a class
# register new user (generate user id, store calendar/name, etc)
# id to name

# Constants
num_to_weekday = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

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
