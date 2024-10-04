import pickle, pprint
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

#calendar_template = generate_dates_with_events_until_2100()
def save_calendar(calendar_template):
    with open('calendar_template.pkl', 'wb') as file:
        pickle.dump(calendar_template, file)

def load_calendar():
    with open('calendar_template.pkl', 'rb') as file:
        return pickle.load(file)

def check_template():
    obj = pickle.load(open("calendar_template.pkl", "rb"))

    with open("calendar_template_output.txt", "a") as f:
         pprint.pprint(obj, stream=f)

def save_user_calendar(user_calendar, user):
    with open(f'{user}_calendar.pkl', 'wb') as file:
        pickle.dump(user_calendar, file)

def load_user_calendar(user):
    with open(f'{user}_calendar.pkl', 'rb') as file:
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
    with open(f'{user}_calendar.pkl', 'wb') as file:
        pickle.dump(event_adder, file)
    print ("Events Saved")

def load_event_list(user):
    with open(f'{user}_calendar.pkl', 'rb') as file:
        return pickle.load(file)

def check_event_list(user):
    obj = pickle.load(open("dates_with_events.pkl", "rb"))

    with open(f"{user}_events_output.txt", "a") as f:
         pprint.pprint(obj, stream=f)

def all_events(gen):
    # Call the function and store the result
    event_days = gen
    
    #Function to grab dates with events
    def get_dates_with_events(dates_with_events):
        # List to store dates with events
        dates_with_real_events = []
        if dates_with_events == None:
            return 0
       
        # Iterate over the dates and select those that have events
        for entry in dates_with_events:
            if entry['events']:  # Check if the events list is not empty
                date = entry['date']
                events = ', '.join(entry['events'])
                dates_with_real_events.append(f"{date} ({events})")
            '''
            # Stop once we have 100 dates with events
            if len(dates_with_real_events) == 100:
                break
            '''
        return dates_with_real_events

    # Get the first 5 dates with events
    dates_with_events = get_dates_with_events(event_days)

    # Print the first 5 dates with events
    if dates_with_events != 0:
        print("Dates with Events are:\n")
        for entry in dates_with_events:
            print(entry)
    else:
        print("No dates with events found")
        return None

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
        