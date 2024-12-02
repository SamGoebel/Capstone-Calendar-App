import os
import pickle
from collections import defaultdict

def universal_calendar_data(users_folder, output_file):
    # Dictionary to store aggregated data
    aggregated_data = defaultdict(lambda: {
        'events': [], 
        'importance': [], 
        'notes': [], 
        'present_users': [],
        'some_users': []  # New field to store users who have events on that date
    })

    # Walk through the 'users' directory and process all .pkl files
    for root, _, files in os.walk(users_folder):
        for filename in files:
            if filename.endswith(".pkl"):
                user = os.path.basename(root)  # Folder name as the user identifier
                file_path = os.path.join(root, filename)

                # Load the pickle file
                with open(file_path, 'rb') as f:
                    user_data = pickle.load(f)

                # Merge data into the aggregated structure
                for entry in user_data:
                    date = entry['date']
                    aggregated_data[date]['events'].extend(entry['events'])
                    aggregated_data[date]['importance'].extend(entry['importance'])
                    aggregated_data[date]['notes'].extend(entry['notes'])

                    # Add user to 'present_users'
                    if user not in aggregated_data[date]['present_users']:
                        aggregated_data[date]['present_users'].append(user)

                    # If there are events on the date, add user to 'some_users'
                    if entry['events']:
                        if user not in aggregated_data[date]['some_users']:
                            aggregated_data[date]['some_users'].append(user)

    # Convert aggregated_data back to list of dictionaries
    final_data = [{'date': date, **data} for date, data in aggregated_data.items()]

    # Save the aggregated data to a new pickle file
    with open(output_file, 'wb') as f:
        pickle.dump(final_data, f)

def pickle_to_text(pickle_file, text_file):
    # Load the pickle file
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)

    # Write data to a text file in a human-readable format
    with open(text_file, 'w') as f:
        for entry in data:
            f.write(f"Date: {entry['date']}\n")
            f.write(f"Events: {entry['events']}\n")
            f.write(f"Importance: {', '.join(entry['importance'])}\n")
            f.write(f"Notes: {', '.join(entry['notes'])}\n")
            #f.write(f"Present Users: {', '.join(entry['present_users'])}\n")
            #f.write(f"Users with Events: {', '.join(entry['some_users'])}\n")  # Added line for 'some_users'
            f.write("\n")  # Add a blank line between entries


current_dir = os.path.dirname(__file__)
users_folder = os.path.join(current_dir, 'users', 'Raden', 'raden_calendar.pkl')
#output_pickle_file = os.path.join(current_dir, "output_calendar.pkl")
output_text_file = os.path.join(current_dir, "output_calendar.txt")

#universal_calendar_data(users_folder, output_pickle_file)
pickle_to_text(users_folder, output_text_file)
