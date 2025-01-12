from helper_functions import append_student_data

users = [
    'aidan',
    'carol',
    'daniel',
    'dora',
    'josh',
    'liz'
]

for i, user in enumerate(users):
    append_student_data(f"backend/calendars/{user}-calendar-export.ics","backend/data/student_schedules.csv",i,user)