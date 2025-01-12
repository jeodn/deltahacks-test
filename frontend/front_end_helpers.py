import os
import csv
from datetime import datetime

def read_class_schedule(file_path):
    class_schedule = {}

    with open(file_path, newline='', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            day = row["Day"]
            time_start = row["Time Start"]
            class_name = row["Class"]
            names = row["List of Names"].split(", ")
            time_start_hour = datetime.strptime(time_start, "%H:%M").hour
            key = (day, time_start_hour)
            class_schedule[key] = [class_name, names]

    return class_schedule

# Example usage
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "..", "backend", "data", "class_schedule.csv")
schedule_dict = read_class_schedule(file_path)
print(schedule_dict)