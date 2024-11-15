from calendar_generator import add_events, load_event_list


def adding_events(calendar, date, event, user, importance, notes):
    event_add = add_events(calendar, date, event, importance, notes)
    if event_add != 0:
        return event_add
    else:
        return 0
    

def loading_events(user):
    event_list_load = load_event_list(user)
    return event_list_load




