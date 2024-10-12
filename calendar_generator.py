import pickle, pprint, os
from datetime import datetime, timedelta

def generate_dates_with_events_until_2100():
    # Create an empty list to store the dates and events
    date_array = []
    
    # Get today's date
    start_date = datetime(2024, 1, 1)
    
    # Set the end date to December 31, 2100
    end_date = datetime(2100, 12, 31)
    
    # Loop through each day from the start date to the end date
    current_date = start_date
    while current_date <= end_date:
        # Create a dictionary for each date with an empty list for events
        date_entry = {
            'date': current_date.strftime('%m-%d-%Y'),
            'events': [] 
        }
        
        # Append the date entry to the array
        date_array.append(date_entry)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_array

calendar_template = generate_dates_with_events_until_2100()

def save_calendar(calendar_template):
    
    current_dir = os.path.dirname(__file__)

    calendar_path = os.path.join(current_dir, 'resources', 'calendar_template.pkl')
    with open(calendar_path, 'wb') as file:
        pickle.dump(calendar_template, file)

def load_calendar():
    # Get the directory of the current file (main script location)
    current_dir = os.path.dirname(__file__)

    # Build the path to the calendar_template.pkl in the resources folder
    calendar_path = os.path.join(current_dir, 'resources', 'calendar_template.pkl')

    # Open and load the pickle file
    with open(calendar_path, 'rb') as file:
        return pickle.load(file)


def check_template():
    
    current_dir = os.path.dirname(__file__)
    calendar_path = os.path.join(current_dir, 'resources', 'calendar_template.pkl')
    
    obj = pickle.load(open(calendar_path, "rb"))

    with open("calendar_template_output.txt", "a") as f:
         pprint.pprint(obj, stream=f)

def save_user_calendar(user_calendar, user):
    
    current_dir = os.path.dirname(__file__)
    path = user_calendar_path = os.path.join(current_dir, 'users', f'{user}')
    if not os.path.exists(path):
        # Create the directory
        os.mkdir(path)
        print(f"User Folder '{path}' created successfully.")
    else:
        print(f"User Folder '{path}' already exists.")
    
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    
    
    with open(user_calendar_path, 'wb') as file:
        pickle.dump(user_calendar, file)

def load_user_calendar(user):
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'rb') as file:
        return pickle.load(file)

def add_events(calendar, date, event): 
    # loops through dict looking for date
    found_date = None
    x = 0
    for day_count in calendar:
        x = x + 1
        if day_count['date'] == date:
            found_date = x - 1
            print("Date Found")
            break
   
    calendar[found_date]['events'].append(event) # writes custom event to that date (doesn't remove the existing one)
    
    return calendar

def save_event_list(gen, user):
    event_adder = gen   
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'wb') as file:
        pickle.dump(event_adder, file)
    print ("Events Saved")

def load_event_list(user): # Might need to remove due to it being the same as load_user_calendar
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')

    with open(user_calendar_path, 'rb') as file:
        return pickle.load(file)

def check_event_list(user):
    obj = pickle.load(open("dates_with_events.pkl", "rb"))

    with open(f"{user}_events_output.txt", "a") as f:
         pprint.pprint(obj, stream=f)


def event_search(gen, event_date, searched_event):
        
        event_days = gen
        search_date = event_date
        search_event = searched_event
        
        found_event = None
        
        for event in event_days:
            if event['date'] == search_date and search_event in event['events']:
                found_event = event
                break

        # Output the result
        if found_event:
            print(f"\nEvent found on {found_event['date']}: {search_event}")
        else:
            print(f"\nNo event found on '{search_date}' with an event '{search_event}'")

def no_date_event_search(gen, searched_event):
        
        event_days = gen
        search_event = searched_event
        
        found_event = None
        
        for event in event_days:
            if search_event in event['events']:
                found_event = event
                break

        # Output the result
        if found_event:
            print(f"\nEvent found called {search_event} on {found_event['date']}")
        else:
            print(f"\nNo event found called '{search_event}'")

def event_delete(gen, searched_event):
        
        event_days = gen
        search_event = searched_event
        count = 0
        found_event = None
        
        
        for event in event_days:
            count = count + 1
            if search_event in event['events']:
                found_event = event
                break
        
        
        # Output the result
        if found_event:
            gen.remove(found_event)
            print(f"\nEvent deleted")
            return gen
        else:
            print(f"\nNo event found called '{found_event}'")
        