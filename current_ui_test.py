import tkinter as tk
import os, pickle
from tkinter import messagebox, Frame, simpledialog
from calendar_object import CalendarCreation
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, no_date_event_search, delete_event
from event_maker import adding_events, loading_events

# Function to switch between frames (screens)
def show_frame(frame):
    Frame.tkraise(frame)

# Create the main window
root = tk.Tk()
root.title("Calendar App Project")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to screen width and height (There if I need to change it)
window_width = screen_width 
window_height = screen_height
root.geometry(f"{window_width}x{window_height}-2+0")


# Create two frames (screens) in the same window
main_frame = tk.Frame(root)
user_viewer_frame = tk.Frame(root)
user_config_frame = tk.Frame(root)
event_adder_frame = tk.Frame(root)
event_editor_frame = tk.Frame(root)

for frame in (main_frame, user_viewer_frame, user_config_frame, event_adder_frame, event_editor_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# ----- Main Screen -----
main_label = tk.Label(main_frame, text="Sam's Calendar App")
main_label.pack(pady=20)

def user_grabber():
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users')
    folders = [f.name for f in os.scandir(users_path) if f.is_dir()]
    
    return folders

def update_user_dropdown():
    show_frame(user_config_frame)
    folder_names = user_grabber()
    
    if folder_names:  # If there are dates with events
        user_select_dropdown.set(folder_names[0])  # Set default selection to the first event detail
        user_select_menu['menu'].delete(0, 'end')  # Clear existing options in the dropdown

        # Add new options with date and event details
        for users in folder_names:
            user_select_menu['menu'].add_command(label=users, command=tk._setit(user_select_dropdown, users))
    else:
        user_select_dropdown.set("No Users found")

# Restore Template Function
def template_maker():
    template = generate_dates_with_events_until_2100()
    save_calendar(template)

# Startup Screen Buttons
uc_button = tk.Button(main_frame, text="Go to User Screen", command= update_user_dropdown)
uc_button.pack(pady=10)

restore_template_button = tk.Button(main_frame, text= "Restore Calendar Template", command= template_maker, fg="black", bg="lightgray")
restore_template_button.pack(pady=20)

check_template_button = tk.Button(main_frame, text= "Check Status of Calendar Template", command= check_template, fg="black", bg="lightgray")
check_template_button.pack(pady=20)

# ----- User Config Screen -----

def load_user_calendar():
    user = user_select_dropdown.get()
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    try:
        with open(user_calendar_path, 'rb') as file:
            user_calendar_path = pickle.load(file)
            #messagebox.showinfo(message=f"User found")
            
            # Pass user info to the calendar screen
            calendar_label.config(text=f"Welcome, {user}")
            show_frame(user_viewer_frame)
            
    except FileNotFoundError:
        if user == "No Users Found":
            messagebox.showerror(message=f"Please make a User.")
        if user == "":
            messagebox.showerror(message=f"Please select a User.")
        else:
            messagebox.showerror(message=f"User {user} not found. Please try again.")

def new_user():
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users')
    user_input = simpledialog.askstring("Input", "Enter name of user:")
    if user_input:
        try:
            new_users_path = os.path.join(users_path, user_input)
            os.makedirs(new_users_path, exist_ok=False)
            messagebox.showinfo(None, "User Created")
            save_user_calendar(load_calendar, user_input)
            update_user_dropdown()
        except FileExistsError:
            messagebox.showinfo(None, "User already exists")
    
user_select_dropdown = tk.StringVar(user_config_frame)
user_select_dropdown.set("Select User")  # Initial dropdown text
#event_edit_dropdown.trace_add("write", on_select_event)  # Trigger on dropdown selection change

user_select_menu = tk.OptionMenu(user_config_frame, user_select_dropdown, "No Users Found")
user_select_menu.pack(pady=20)

add_user_button = tk.Button(user_config_frame, text= "Add User", command= new_user, fg="black", bg="lightgray")
add_user_button.pack(pady=20)

load_user_button = tk.Button(user_config_frame, text= "Load User", command= load_user_calendar, fg="black", bg="lightgray")
load_user_button.pack(pady=20)

uc_back_button = tk.Button(user_config_frame, text= "Go back", command=lambda: show_frame(main_frame))
uc_back_button.pack(pady=10)

# ----- User Calendar Screen Widgets -----
def check_event_list():
    user = user_select_dropdown.get()
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
        return 0

def load_edit_screen():
    show_frame(event_editor_frame)
    update_dropdown()


calendar_label = tk.Label(user_viewer_frame, text="")
calendar_label.pack(pady=20)

add_event_screen_button = tk.Button(user_viewer_frame, text="Add Event", command=lambda: show_frame(event_adder_frame))
add_event_screen_button.pack(pady=10)

edit_event_screen_button = tk.Button(user_viewer_frame, text="Edit Event", command= load_edit_screen)
edit_event_screen_button.pack(pady=10) 

check_user_events_button = tk.Button(user_viewer_frame, text= "Print User Event List", command= check_event_list, fg="black", bg="lightgray")
check_user_events_button.pack(pady=20)

back_button = tk.Button(user_viewer_frame, text="Back to Main", command=lambda: show_frame(main_frame))
back_button.pack(pady=10)

# ----- Event Adder Screen -----

def load_user_calendar_for_events():
    user = user_select_dropdown.get()
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

add_event_button = tk.Button(event_adder_frame, text="Save Event", command=lambda: adding_events(load_user_calendar_for_events(), event_date_entry.get(), event_name_entry.get(), user_select_dropdown.get()))
add_event_button.pack(pady=10)

add_event_back_button = tk.Button(event_adder_frame, text="Go Back", command=lambda: show_frame(user_viewer_frame))
add_event_back_button.pack(pady=10)


# ----- Event Editor Screen -----
space1 = tk.Label(event_editor_frame, text="") # Formats better 
space1.pack(pady=20)

def load_event_dates_with_details():
    user = user_select_dropdown.get()
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
        messagebox.showerror("Error", f"Calendar for user {user} not found.")
        return []
    except (KeyError, TypeError):
        messagebox.showerror("Error", "Invalid calendar format.")
        return []

# Function to update the dropdown menu with dates and event details
def update_dropdown():
    event_details = load_event_dates_with_details()
    
    if event_details:  # If there are dates with events
        event_edit_dropdown.set(event_details[0])  # Set default selection to the first event detail
        event_menu['menu'].delete(0, 'end')  # Clear existing options in the dropdown

        # Add new options with date and event details
        for detail in event_details:
            event_menu['menu'].add_command(label=detail, command=tk._setit(event_edit_dropdown, detail))
    else:
        event_edit_dropdown.set("No events found")

event_edit_dropdown = tk.StringVar(event_editor_frame)
event_edit_dropdown.set("Select an Event")  # Initial dropdown text
#event_edit_dropdown.trace_add("write", event_edit_dropdown.get())  # Trigger on dropdown selection change

event_menu = tk.OptionMenu(event_editor_frame, event_edit_dropdown, None)
event_menu.pack(pady=20)

def open_event_editor_window():
    user = user_select_dropdown.get()
    user_calendar_path = os.path.join(os.path.dirname(__file__), 'users', f'{user}', f'{user}_calendar.pkl')
    selected_event = event_edit_dropdown.get()
    event_text = selected_event.split(":", 1)[1].strip()
    

    # Create a new Toplevel window
    event_editor_window = tk.Toplevel(root)
    event_editor_window.title("Event Editor")
    event_editor_window.geometry("500x300")
    
    # Add a label in the temporary window
    label = tk.Label(event_editor_window, text="Edit your events here:")
    label.pack(pady=20)

    
    # Add a close button in the temporary window
    delete_event_button = tk.Button(event_editor_window, text="Delete Event", command= lambda: delete_event(user_calendar_path, event_text))
    delete_event_button.pack(pady=5)
    
    
    close_button = tk.Button(event_editor_window, text="Close Window", command=event_editor_window.destroy)
    close_button.pack(pady=5)
    

edit_window_button = tk.Button(event_editor_frame, text = "Edit Selected Event", command = open_event_editor_window)
edit_window_button.pack(pady=20)

# Button to load events into dropdown
load_button = tk.Button(event_editor_frame, text="Refresh Events", command=update_dropdown)
load_button.pack(pady=10) 

edit_event_back_button = tk.Button(event_editor_frame, text="Go Back", command=lambda: show_frame(user_viewer_frame))
edit_event_back_button.pack(pady=10)



# Show the main screen initially
show_frame(main_frame)

# Run the application
root.mainloop()
