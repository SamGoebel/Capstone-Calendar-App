import os, pickle

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
output_text_file = os.path.join(current_dir, "output_calendar.txt")

pickle_to_text(users_folder, output_text_file)
