from calendar_generator import add_events, load_event_list, save_event_list

def adding_events(calendar, date, event, user):
    event_add = add_events(calendar, date, event)
    event_save = save_event_list(event_add, user)
    return event_save

def loading_events(user):
    event_list_load = load_event_list(user)
    return event_list_load