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
            'events': []  # You can add events to this list later
        }
        
        # Append the date entry to the array
        date_array.append(date_entry)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_array

def events(gen):
    # Call the function and store the result
    event_days = gen

    # Example: Add an event to the first date
    event_days[0]['events'].append("Start working on project")
    event_days[20]['events'].append("Project End")


    #Function to grab dates with events
    def get_dates_with_events(dates_with_events):
        # List to store dates with events
        dates_with_real_events = []
        
        # Iterate over the dates and select those that have events
        for entry in dates_with_events:
            if entry['events']:  # Check if the events list is not empty
                date = entry['date']
                events = ', '.join(entry['events'])
                dates_with_real_events.append(f"{date} ({events})")
            
            # Stop once we have 5 dates with events
            if len(dates_with_real_events) == 100:
                break
        
        return dates_with_real_events

    # Get the first 5 dates with events
    first_5_dates_with_events = get_dates_with_events(event_days)

    # Print the first 5 dates with events
    for entry in first_5_dates_with_events:
        print(entry)

    

    
