import tkinter as tk
import os, pickle, pprint
from tkinter import messagebox, Frame
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, no_date_event_search, event_delete, load_event_list
from event_maker import adding_events, loading_events

# Function to switch between frames (screens)
def show_frame(frame):
    Frame.tkraise(frame)

# Create the main window
root = tk.Tk()
root.title("Calendar App Test")
root.geometry("1200x800")

# Create two frames (screens) in the same window
main_frame = tk.Frame(root)
user_viewer_frame = tk.Frame(root)
user_config_frame = tk.Frame(root)
event_adder_frame = tk.Frame(root)
event_editor_frame = tk.Frame(root)

for frame in (main_frame, user_viewer_frame, user_config_frame, event_adder_frame, event_editor_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# ----- Main Screen -----
main_label = tk.Label(main_frame, text="This is the Main Screen")
main_label.pack(pady=20)

# Buttons to go to other Screens
uc_button = tk.Button(main_frame, text="Go to User Screen", command=lambda: show_frame(user_config_frame))
uc_button.pack(pady=10)

# Restore Template Function
def template_maker():
    template = generate_dates_with_events_until_2100()
    save_calendar(template)

restore_template_button = tk.Button(main_frame, text= "Restore Calendar Template", command= template_maker, fg="black", bg="lightgray")
restore_template_button.pack(pady=20)

check_template_button = tk.Button(main_frame, text= "Check Calendar Template", command= check_template, fg="black", bg="lightgray")
check_template_button.pack(pady=20)

# ----- User Config Screen -----
def load_user_calendar():
    user = user_entry.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    try:
        with open(user_calendar_path, 'rb') as file:
            user_calendar_path = pickle.load(file)
            messagebox.showinfo(message=f"User {user} was found")
            
            # Pass user info to the calendar screen
            calendar_label.config(text=f"Welcome, {user}")
            
            
            # Show the calendar screen
            show_frame(user_viewer_frame)
            
    
    except FileNotFoundError:
        messagebox.showerror(message=f"User {user} not found. Please try again.")
    
    
user_label = tk.Label(user_config_frame, text="Enter User:", padx = 200, anchor = "center")
user_label.pack(pady= 10)

user_entry = tk.Entry(user_config_frame)
user_entry.pack(pady=10)

load_user_button = tk.Button(user_config_frame, text= "Load User", command= load_user_calendar, fg="black", bg="lightgray")
load_user_button.pack(pady=20)

uc_back_button = tk.Button(user_config_frame, text= "Go back", command=lambda: show_frame(main_frame))
uc_back_button.pack(pady=10)


# ----- User Calendar Screen Widgets -----
def check_event_list():
    user = user_entry.get()
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
        for entry in dates_with_events:
            entries_list.append(str(entry))
        combined_string = "\n".join(entries_list)
        messagebox.showinfo(message = "Dates with Events are:\n" f"{combined_string}")
    else:
        print("No dates with events found")
        return None

calendar_label = tk.Label(user_viewer_frame, text="")
calendar_label.pack(pady=20)

back_button = tk.Button(user_viewer_frame, text="Back to Main", command=lambda: show_frame(main_frame))
back_button.pack(pady=10)

add_event_screen_button = tk.Button(user_viewer_frame, text="Add Event", command=lambda: show_frame(event_adder_frame))
add_event_screen_button.pack(pady=10)

edit_event_screen_button = tk.Button(user_viewer_frame, text="Edit Event", command=lambda: show_frame(event_editor_frame))
edit_event_screen_button.pack(pady=10) 

check_user_events_button = tk.Button(user_viewer_frame, text= "Print User Event List", command= check_event_list, fg="black", bg="lightgray")
check_user_events_button.pack(pady=20)


# ----- Event Adder Screen -----

def load_user_calendar_for_events():
    user = user_entry.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'rb') as file:
        return pickle.load(file)


space1 = tk.Label(event_adder_frame, text="") # Formats better 
space1.pack(pady=20)

event_date_label = tk.Label(event_adder_frame, text= "Enter Date (DD-MM-YYYY)")
event_date_label.pack()
event_date_entry = tk.Entry(event_adder_frame)
event_date_entry.pack()

space2 = tk.Label(event_adder_frame, text="")
space2.pack(pady=10)

event_name_label = tk.Label(event_adder_frame, text= "Enter Title")
event_name_label.pack()
event_name_entry = tk.Entry(event_adder_frame)
event_name_entry.pack()

add_event_button = tk.Button(event_adder_frame, text="Save Event", command=lambda: adding_events(load_user_calendar_for_events(), event_date_entry.get(), event_name_entry.get(), user_entry.get()))
add_event_button.pack(pady=10)

add_event_back_button = tk.Button(event_adder_frame, text="Go Back", command=lambda: show_frame(user_viewer_frame))
add_event_back_button.pack(pady=10)


# ----- Event Editor Screen -----
space1 = tk.Label(event_editor_frame, text="") # Formats better 
space1.pack(pady=20)

def load_event_dates_with_details():
    user = user_entry.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    
    try:
        with open(user_calendar_path, 'rb') as file:
            calendar_data = pickle.load(file)  # Load list of date dictionaries
            
            # Filter for dates with events and format "date: event1, event2"
            event_details = [
                f"{entry['date']}: {', '.join(entry['events'])}"
                for entry in calendar_data if entry.get('events')
            ]
            return event_details
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"Calendar for user {user} not found.")
        return []
    except (KeyError, TypeError):
        tk.messagebox.showerror("Error", "Invalid calendar format.")
        return []


# Function to update the dropdown menu with dates and event details
def update_dropdown():
    event_details = load_event_dates_with_details()
    
    if event_details:  # If there are dates with events
        dropdown_var.set(event_details[0])  # Set default selection to the first event detail
        event_menu['menu'].delete(0, 'end')  # Clear existing options in the dropdown

        # Add new options with date and event details
        for detail in event_details:
            event_menu['menu'].add_command(label=detail, command=tk._setit(dropdown_var, detail))
    else:
        dropdown_var.set("No events found")

dropdown_var = tk.StringVar(event_editor_frame)
dropdown_var.set("Select an Event")  # Initial dropdown text

event_menu = tk.OptionMenu(event_editor_frame, dropdown_var, "Select an Event")
event_menu.pack(pady=20)

# Button to load events into dropdown
load_button = tk.Button(event_editor_frame, text="Load Events", command=update_dropdown)
load_button.pack(pady=10)


# Show the main screen initially
show_frame(main_frame)

# Run the application
root.mainloop()
