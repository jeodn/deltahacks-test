# Convert ICS file to CSV
import csv
from icalendar import Calendar
import os

# Constants
example_ics_name = "./test-assets/josh-calendar-export.ics"
example_csv_name = "./test-assets/export.csv"

def ics_to_csv(ics_file_path: str, csv_file_path: str) -> None:
    """
    Converts an .ics (iCalendar) file to a .csv file.
    
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
            event = {
                "Start": component.get("dtstart").dt if component.get("dtstart") else "",
                "End": component.get("dtend").dt if component.get("dtend") else "",
                "Summary": component.get("summary", ""),
                "Description": component.get("description", ""),
                "Location": component.get("location", "")
            }
            events.append(event)

    if not events:
        raise ValueError("No events found in the .ics file.")

    # Write events to a CSV file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Start", "End", "Summary", "Description", "Location"])
        writer.writeheader()
        writer.writerows(events)

    print(f"Successfully converted {ics_file_path} to {csv_file_path}")

