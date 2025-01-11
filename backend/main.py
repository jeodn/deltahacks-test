from backend.helper_functions import ics_to_csv

# Constants
example_ics_name = "./test-assets/josh-calendar-export.ics"
example_csv_name = "./test-assets/export.csv"

if __name__ == "__main__":
    ics_to_csv(example_ics_name, example_csv_name)