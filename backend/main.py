from helper_functions import ics_to_csv

# Constants
example_ics_name = "./backend/data/josh-calendar-export.ics"
example_csv_name = "./backend/data/export.csv"

if __name__ == "__main__":
    # Test creating an csv file
    ics_to_csv(example_ics_name, example_csv_name)