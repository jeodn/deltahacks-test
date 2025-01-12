import sys
import pygame
from pygame.locals import *
from helper_functions import *

# Directories
base_dir = os.path.dirname(os.path.abspath(__file__))
example_ics_name = os.path.join(base_dir, "calendars/josh-calendar-export.ics")
example_student_schedules_name = os.path.join(base_dir, "data/student_schedules.csv")
example_user_database = os.path.join("./backend/data/user_database.csv")
example_noclasses_database = os.path.join("./backend/data/available_timeslots.csv")
example_timeslots_database = os.path.join("./backend/data/timeslots_with_frequency.csv")
example_userid = 1





list_of_days = generate_timeslot_freq_database(example_timeslots_database)

NUM_DAYS = len(list_of_days)
NUM_HOURS = 23

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
fontsize = 30
my_font = pygame.font.SysFont('Comic Sans MS', 30)

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1000, 400
screen = pygame.display.set_mode((width, height))
 
# Game loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  
  
  # Draw.
  x = 2
  for day in range(NUM_DAYS):
    i = day + 1
    for hour in range(NUM_HOURS):
        j = hour + 1
        freq_at_hour = list_of_days[day][hour]
        rec_width = width/NUM_HOURS
        rec_height = height/NUM_DAYS
        rec_x = j * rec_width - rec_width
        rec_y = i * rec_height - rec_height
        pygame.draw.rect(screen, (0, 255/freq_at_hour+100, 0), (rec_x, rec_y, rec_width, rec_height))
        
        screen.blit(my_font.render(f"{freq_at_hour}", False, (0, 0, 0)), (rec_x,rec_y+rec_height//2-fontsize))

  pygame.display.flip()
  fpsClock.tick(fps)