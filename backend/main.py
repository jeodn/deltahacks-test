from helper_functions import *

# Constants
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "data/josh-calendar-export.ics")
example_csv_name = os.path.join(base_dir, "data/student_schedules.csv")
example_id_database = "./backend/data/id_to_name.json"
example_userid = 1

if __name__ == "__main__":
    # Test creating an csv file
    # register_student_data(example_ics_name, example_csv_name, 1, "Daniel")
    print(f"Student 1 is named {id_to_name(example_csv_name, example_userid)}")