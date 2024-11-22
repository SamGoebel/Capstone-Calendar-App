import pickle, pprint, os
from datetime import datetime, timedelta
from tkinter import messagebox


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
            'events': [],
            'notes': [],
            'importance': []
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
       #print("done")

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
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    
    with open(user_calendar_path, 'wb') as file:
        pickle.dump(user_calendar, file)


def add_events(event_calendar, date, event, importance, notes): 
    # loops through dict looking for date
    try: 
        x = 0
        found_date = None
       #print(event_calendar[0])
        for day_count in event_calendar:
            x = x + 1
            if day_count['date'] == date:
                found_date = x - 1
                break
    except TypeError:
        messagebox.showinfo(None, "Date Not Valid")
        return 0
    except KeyError:
        messagebox.showinfo(None, "Date Not Valid")
        return 0
    
    if found_date is not None:
        print(f"Appending to event_calendar at index {found_date}")
        event_calendar[found_date]['events'].append(event)
    
    # Only append to importance and notes if they are not None or empty
        if importance not in [None, '']:
            event_calendar[found_date]['importance'].append(importance)
        else:
            event_calendar[found_date]['importance'].append('')
    
        if notes not in [None, '']:
            event_calendar[found_date]['notes'].append(notes)
        else:
            event_calendar[found_date]['notes'].append('')
    else:
        messagebox.showinfo(None, "Date Not Valid")
        return 0
    return event_calendar

def save_event_list(gen, user):
    event_adder = gen   
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'wb') as file:
        pickle.dump(event_adder, file)
    messagebox.showinfo(None, "Event Saved")
    

def load_event_list(user): # Might need to remove due to it being the same as load_user_calendar
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')

    with open(user_calendar_path, 'rb') as file:
        return pickle.load(file)

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

def delete_event(pickle_path, event_to_delete, destroy_event_window):
    # Load the pickle file
    try:
        with open(pickle_path, 'rb') as file:
            calendar_data = pickle.load(file)
        
        # Ensure calendar_data is a list of dictionaries
        if isinstance(calendar_data, list):
            event_found = False
            for entry in calendar_data:
                # Check if 'events' is a list in the current dictionary entry
                if 'events' in entry and isinstance(entry['events'], list):
                    # Attempt to remove the event if it exists
                    try:
                        entry['events'].remove(event_to_delete)
                        event_found = True
                        messagebox.showinfo(None, f"Event deleted")
                    except ValueError:
                        # Skip if the event is not in this entry
                        pass
            
            # If the event was found, save the modified data back to the pickle file
            if event_found:
                with open(pickle_path, 'wb') as file:
                    pickle.dump(calendar_data, file)
            else:
                 messagebox(f"Event '{event_to_delete}' not found in any entry.")
        else:
             messagebox("Invalid file format: expected a list of dictionaries.")
    
    except FileNotFoundError:
         messagebox.showerror("Error:", f"File '{pickle_path}' not found.")
    except (EOFError, pickle.UnpicklingError):
         messagebox.showerror(None, f"Error loading pickle file. Ensure the file is valid.")
    destroy_event_window.destroy()