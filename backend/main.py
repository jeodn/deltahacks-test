from helper_functions import *

# Constants
example_ics_name = "./backend/data/josh-calendar-export.ics"
example_csv_name = "./backend/data/student_schedules.csv"
example_id_database = "./backend/data/id_to_name.json"
example_userid = 1

if __name__ == "__main__":
    # Test creating an csv file
    # register_student_data(example_ics_name, example_csv_name, 1, "Daniel")
    print(f"Student 1 is named {id_to_name(example_csv_name, example_userid)}")