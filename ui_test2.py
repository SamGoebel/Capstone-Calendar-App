import tkinter as tk
import os, pickle, pprint
from tkinter import messagebox, Frame
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, check_event_list, no_date_event_search, event_delete

# Function to switch between frames (screens)
def show_frame(frame):
    Frame.tkraise(frame)

# Create the main window
root = tk.Tk()
root.title("Switching Screens Example")
root.geometry("1200x800")

# Create two frames (screens) in the same window
main_frame = tk.Frame(root)
greeting_frame = tk.Frame(root)
user_config_frame = tk.Frame(root)

for frame in (main_frame, greeting_frame, user_config_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# ----- Main Screen -----
main_label = tk.Label(main_frame, text="This is the Main Screen")
main_label.pack(pady=20)

# Buttons to go to other Screens
main_button = tk.Button(main_frame, text="Go to Greeting Screen", command=lambda: show_frame(greeting_frame))
main_button.pack(pady=10)

uc_button = tk.Button(main_frame, text="Go to User Screen", command=lambda: show_frame(user_config_frame))
uc_button.pack(pady=10)

# ----- Greeting Screen -----
def greet_user():
    name = entry.get()
    if name:
        messagebox.showinfo("Greeting", f"Hello, {name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

greeting_label = tk.Label(greeting_frame, text="Enter your name:")
greeting_label.pack(pady=10)

entry = tk.Entry(greeting_frame)
entry.pack(pady=10)


greet_button = tk.Button(greeting_frame, text="Greet", command=greet_user)
greet_button.pack(pady=10)

# Button to go back to the Main Screen
back_button = tk.Button(greeting_frame, text="Go back", command=lambda: show_frame(main_frame))
back_button.pack(pady=10)


# ----- User Config Screen -----
def load_user_calendar():
    user = user_entry.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'rb') as file:
        messagebox.showinfo(message= "User " f'{user}' " was found")
        return pickle.load(file)
    
def check_event_list():
    user = user_entry_events.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'rb') as file:
        user_calendar = pickle.load(file)
    
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

    # Get the dates with events
    dates_with_events = get_dates_with_events(user_calendar)

    # Print the dates with events
    if dates_with_events != 0:
        entries_list = []
        #print("Dates with Events are:\n")
        for entry in dates_with_events:
            entries_list.append(str(entry))
        combined_string = "\n".join(entries_list)
        messagebox.showinfo(message = "Dates with Events are:\n" f"{combined_string}")
    else:
        print("No dates with events found")
        return None
    
user_label = tk.Label(user_config_frame, text="Enter User:")
user_label.pack(pady=10)

user_entry = tk.Entry(user_config_frame)
user_entry.pack(pady=10)

load_user_button = tk.Button(user_config_frame, text="Load User", command= load_user_calendar, fg="black", bg="lightgray")
load_user_button.pack(pady=20)

uc_back_button = tk.Button(user_config_frame, text="Go back", command=lambda: show_frame(main_frame))
uc_back_button.pack(pady=10)

user_entry_events = tk.Entry(user_config_frame)
user_entry_events.pack(pady=10)

check_user_events_button = tk.Button(user_config_frame, text="Print User Event List", command= check_event_list, fg="black", bg="lightgray")
check_user_events_button.pack(pady=20)

# Show the main screen initially
show_frame(main_frame)

# Run the application
root.mainloop()
