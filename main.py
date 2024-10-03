import calendar 
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, events, event_search, save_calendar, load_calendar, add_events, load_event_list, save_event_list, check_template, check_event_list


cc = CalendarCreation()

#generate = generate_dates_with_events_until_2100()

#calendar_save = save_calendar(generate)
calendar_check = load_calendar() # loads calendar file to be used for other methods

event_add = add_events(calendar_check)
event_save = save_event_list(event_add)
event_list_load = load_event_list()
print(event_list_load)

event_manager = events(calendar_check)

custom_event_search = event_search(calendar_check, "01-01-2024", "Start working on project")


#date = cc.DateObject(25, 9, 2024) #takes numbers for days

#calendar_print = cc.CalendarPrint(10, 2024)



#print(date)

