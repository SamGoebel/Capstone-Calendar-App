import calendar, event_maker
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, all_events, event_search, save_calendar, load_calendar, check_template, save_user_calendar, load_user_calendar, check_event_list, no_date_event_search, event_delete


cc = CalendarCreation()
emr = event_maker

generate_calendar = False # Keep as false unless template becomes corrupted

if generate_calendar == True:
    generate = generate_dates_with_events_until_2100()
    calendar_save = save_calendar(generate)

calendar_check = load_calendar() # Loads calendar file to be used for other methods

set_user = input("Enter name of user: ")

#save_user_calendar(calendar_check, set_user)
user_calendar = load_user_calendar(set_user)

add_date = input("Enter Date (DD-MM-YYYY): ")
add_event = input("Enter name of event: ")

custom_event = emr.adding_events(user_calendar, add_date, add_event, set_user)
event_list = emr.loading_events(set_user)

event_manager = all_events(event_list)

search_date = input("Enter Search Date (DD-MM-YYYY): ")
search_event = input("Enter name of event: ")

if search_date == None:
    no_date_event_search(event_list, search_event)
else:
    event_search(event_list, search_date, search_event)

event_delete(event_list, "Sonic")


#date = cc.DateObject(25, 9, 2024) #takes numbers for days

#calendar_print = cc.CalendarPrint(10, 2024)

#print(date)

