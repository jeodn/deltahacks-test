from helper_functions import *

# Directories
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "calendars/josh-calendar-export.ics")
example_student_schedules_name = os.path.join(base_dir, "data/student_schedules.csv")
example_user_database = os.path.join("./backend/data/user_database.csv")
example_noclasses_database = os.path.join("./backend/data/available_timeslots.csv")
example_timeslots_database = os.path.join("./backend/data/timeslots_with_frequency.csv")
example_userid = 1

if __name__ == "__main__":
    # Test creating an csv file
    #append_student_data(example_ics_name, example_student_schedules_name, 67, "Dora")
    generate_timeslot_freq_database(example_timeslots_database)
    """
    print(f"Student 1 is named {id_to_name(example_csv_name, example_userid)}")

    # Example usage
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv_path = os.path.join(base_dir, "./data/student_schedules.csv")
    output_csv_path = os.path.join(base_dir, "./data/class_schedule.csv")
    create_class_schedule(input_csv_path, output_csv_path)
    
    register_new_student("fortnitejonesy", "password69", "Jonesy Battler", 
                         "English, German", "I love kicking babies", example_ics_name, example_user_database)
    """

    #generate_available_timeslot_database(example_noclasses_database)

    #print(generate_study_session_time(1))

    #generate_study_session_time(0)

    #print(int_to_time(23), int_to_time(23))
