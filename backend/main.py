from helper_functions import *

# Constants
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "calendars/josh-calendar-export.ics")
example_csv_name = os.path.join(base_dir, "data/student_schedules.csv")
example_user_database = os.path.join("./backend/data/user_database.csv")
example_userid = 1

if __name__ == "__main__":
    # Test creating an csv file
    # register_student_data(example_ics_name, example_csv_name, 1, "Daniel")
    """
    print(f"Student 1 is named {id_to_name(example_csv_name, example_userid)}")

    # Example usage
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv_path = os.path.join(base_dir, "./data/student_schedules.csv")
    output_csv_path = os.path.join(base_dir, "./data/class_schedule.csv")
    create_class_schedule(input_csv_path, output_csv_path)
    """

    register_new_student("fortnitejonesy", "password69", "Jonesy Battler", 
                         "English, German", "I love kicking babies", example_ics_name, example_user_database)