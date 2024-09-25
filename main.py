import calendar 
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, events


cc = CalendarCreation()



generate = generate_dates_with_events_until_2100()

event_manager = events(generate)


date = cc.DateObject(25, 9, 2024) #takes numbers for days

calendar_print = cc.CalendarPrint(10, 2024)

#print(date)

