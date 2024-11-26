import customtkinter as ctk
import os, pickle, shutil
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, no_date_event_search, delete_event, save_event_list, add_events
from calendar_object import CalendarCreation
from customtkinter import CTkInputDialog

def show_message(app, title, message):
    # Create a new Toplevel window 
    message_box = ctk.CTkToplevel(app)
    
    if title != None:
        message_box.title(title)
    else:
         message_box.title("Success")

    # Add a label to show the message
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 16))
    label.pack(ipady= 20)

    # Add a button to close the message box
    close_button = ctk.CTkButton(message_box, text="OK", command=message_box.destroy)
    close_button.pack(side = "bottom", pady= 5)

    # Center the message box on the screen
   # message_box.geometry(f"+{int(app.winfo_x() + app.winfo_width() // 2 - 150)}+{int(app.winfo_y() + app.winfo_height() // 2 - 100)}")
    message_box.geometry("200x110")

# ----- Main Screen -----

def user_grabber():
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users')
    folders = [f.name for f in os.scandir(users_path) if f.is_dir()]
    
    return folders


def update_user_dropdown(app, user_select_dropdown):
    
    app.show_frame("uconfig")
    
    folder_names = user_grabber()  # Assume this returns a list of user names

    if folder_names:  # If there are names returned
        user_select_dropdown.configure(values=folder_names)  # Set the dropdown options
        user_select_dropdown.set(folder_names[0])  # Set the default selection to the first name
    else:
        user_select_dropdown.configure(values=["No Users Found"])
        user_select_dropdown.set("No Users Found")


# Restore Template Function
def template_maker():
    template = generate_dates_with_events_until_2100()
    save_calendar(template)


# ----- User Config Screen -----

def load_user_calendar(app, user, label):
    
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    try:
        with open(user_calendar_path, 'rb') as file:
            user_calendar_path = pickle.load(file)
            
            # Pass user info to the calendar screen
            label.configure(text=f"Welcome, {user}")
            app.show_frame("uviewer")
            
    except FileNotFoundError:
        if user == "No Users Found":
            show_message(app, "Error", "Please make a user")
        if user == "":
            show_message(app, "Error", "Please select a user")
        else:
            show_message(app, "Error", f"User {user} not found. Please try again.")


def new_user(app, user_dropdown):
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users')
    
    user_maker_window = ctk.CTkToplevel(app)
    user_maker_window.title("Add User Details")
    user_maker_window.geometry("375x225")

    enter_name = ctk.CTkEntry(user_maker_window, placeholder_text = "Enter Name")
    enter_name.pack(pady= (20, 10))

    color_name = ctk.CTkEntry(user_maker_window, placeholder_text = "Enter Color (Hex)")
    color_name.pack(pady= 10)

    edit_name = ctk.CTkEntry(user_maker_window, placeholder_text = "Image")
    edit_name.pack(pady= 10)
    
    make_user_button = ctk.CTkButton(user_maker_window, text= "Make User", command = lambda: make_user(enter_name.get()))
    make_user_button.pack(side = "bottom", pady= 20)
    
    def make_user(the_user):
        if the_user:
            try:
                new_users_path = os.path.join(users_path, the_user)
                os.makedirs(new_users_path, exist_ok=False)
                show_message(app, "Success", "User Created")
                save_user_calendar(load_calendar(), the_user)
                update_user_dropdown(app, user_dropdown)
                user_maker_window.destroy()
            except FileExistsError:
                show_message(app, "Error", "User Already Exists")
            except TypeError:
                return 0

def delete_user_window(app, selected_user, user_dropdown):
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users', f"{selected_user}")
    
    user_deleter_window = ctk.CTkToplevel(app)
    user_deleter_window.title(f"Delete User")
    user_deleter_window.geometry("300x100")

    delete_label = ctk.CTkLabel(user_deleter_window, text= f"Would you like to delete user {selected_user}?")
    delete_label.pack(pady = 10)

    delete_yes = ctk.CTkButton(user_deleter_window, text = "Yes", command= lambda: delete_user(users_path), width = 100) 
    delete_yes.pack(side = "left", padx = 5)
    delete_no = ctk.CTkButton(user_deleter_window, text = "No", command= lambda: user_deleter_window.destroy(), width = 100)
    delete_no.pack(side = "right", padx = 5)
    

    def delete_user(path):
        shutil.rmtree(path)
        user_deleter_window.destroy()
        show_message(app, "Success", "User Deleted")
        update_user_dropdown(app, user_dropdown)
        return 0



# ----- User Screen -----

def check_event_list(app, current_user):
    user = current_user
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
                dates_with_real_events.append(f"{events} ({date})")
        
        return dates_with_real_events

    # Get the dates with events
    dates_with_events = get_dates_with_events(user_calendar)

    # Print the dates with events
    if dates_with_events != 0:
        entries_list = []
        for entry in dates_with_events:
            entries_list.append(str(entry))
        combined_string = "\n".join(entries_list)
        show_message(app, title = "Event List", message = "Dates with Events are:\n" f"{combined_string}")
    else:
        print("No dates with events found")
        return 0
    

# ----- Event Adder Screen -----
def load_user_calendar_for_events(current_user):
    user = current_user
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    with open(user_calendar_path, 'rb') as file:
        return pickle.load(file)

def adding_events(app, calendar, date, event, importance, notes, user):
    
    event_add = add_events(calendar, date, event, importance, notes)
    if event_add != 0:
        save_event_list(event_add, user)
        app.show_frame("uviewer")

    else:
        return 0

def load_event_dates_with_details(app, current_user):
    user = current_user
    current_dir = os.path.dirname(__file__)
    user_calendar_path = os.path.join(current_dir, 'users', f'{user}', f'{user}_calendar.pkl')
    
    try:
        with open(user_calendar_path, 'rb') as file:
            calendar_data = pickle.load(file) 
            
            # Filter for dates with events and format "date: event, event2, ect"
            event_details = [
            f"{entry['date']}: {', '.join(str(event) for event in entry['events'] if isinstance(event, str))}"
            for entry in calendar_data if entry.get('events')
            ]
        return event_details

    except FileNotFoundError:
        show_message(app, "Error", f"Calendar for user {user} not found.")
        return []
    except (KeyError, TypeError):
        show_message(app, "Error", "Invalid calendar format.")
        return []
    
def update_dropdown(app, current_user, event_dropdown):
    
    event_details = load_event_dates_with_details(app, current_user)
    
    if event_details:  
        
        event_dropdown.configure(values = event_details)
        event_dropdown.set(event_details[0])  # Set default selection to the first event detail
        

        # Add new options with date and event details
       # for detail in event_details:
        #    event_menu['menu'].add_command(label=detail, command=ctk._setit(event_dropdown, detail))
    else:
        event_dropdown.configure(values = ["No Events Found"])
        event_dropdown.set("No Events Found")
    app.show_frame("eeditor")

def find_event_details(event_name, path):
    
    with open(path, 'rb') as file:
        data = pickle.load(file)
    
    for entry in data:
        if event_name in entry.get('events', []):  # Check if the event exists in the 'events' list
            return entry  # Return the matching dictionary

    return None


def open_event_editor_window(app, current_user, event):
    user = current_user
    user_calendar_path = os.path.join(os.path.dirname(__file__), 'users', f'{user}', f'{user}_calendar.pkl')
    selected_event = event
    event_text = selected_event.split(":", 1)[1].strip()
    
    details = find_event_details(event_text, user_calendar_path)

    event_text = details['events']
    event_date = details['date']
    event_importance = details['importance']
    event_notes = details['notes']
    
    # Create a new Toplevel window
    event_editor_window = ctk.CTkToplevel(app)
    event_editor_window.title("Edit Event")
    event_editor_window.geometry("500x300")
    
    
    # Add a label in the temporary window
    label = ctk.CTkLabel(event_editor_window, text="Edit your events here:")
    label.pack(pady=20)

    edit_name = ctk.CTkEntry(event_editor_window, placeholder_text = "Name")
    edit_name.pack(pady= 5)
    edit_name.insert(0, event_text)

    edit_date = ctk.CTkEntry(event_editor_window, placeholder_text= "Date")
    edit_date.pack(pady= 5)
    edit_date.insert(0, event_date)

    edit_importance = ctk.CTkEntry(event_editor_window, placeholder_text = "Importance Level")
    edit_importance.pack(pady= 5)
    if event_importance != ['']:
        edit_importance.insert(0, event_importance)

    edit_notes = ctk.CTkEntry(event_editor_window, placeholder_text= "Notes")
    edit_notes.pack(pady= 5)
    if event_notes != ['']:
        edit_notes.insert(0, event_notes)

    # Add a close button in the temporary window
    delete_event_button = ctk.CTkButton(event_editor_window, text="Delete Event", command= lambda: delete_event(user_calendar_path, event_text, event_editor_window))
    delete_event_button.pack(pady=5)
    
    close_button = ctk.CTkButton(event_editor_window, text="Close Window", command=event_editor_window.destroy)
    close_button.pack(pady=5)

