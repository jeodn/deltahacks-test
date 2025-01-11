from helper_functions import *

# Constants
example_ics_name = "./backend/data/josh-calendar-export.ics"
example_csv_name = "./backend/data/student_schedules.csv"

if __name__ == "__main__":
    # Test creating an csv file
    register_student_data(example_ics_name, example_csv_name, 1, "Daniel")