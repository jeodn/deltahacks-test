from helper_functions import *

# Constants
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "data/josh-calendar-export.ics")
example_csv_name = os.path.join(base_dir, "data/student_schedules.csv")

if __name__ == "__main__":
    # Test creating an csv file
    register_student_data(example_ics_name, example_csv_name, 1, "Daniel")