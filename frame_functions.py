import customtkinter as ctk
import os, pickle
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, no_date_event_search, delete_event, save_event_list
from event_maker import adding_events, loading_events
from calendar_object import CalendarCreation
from customtkinter import CTkInputDialog

def show_message(app, title, message):
    # Create a new Toplevel window (like a popup)
    message_box = ctk.CTkToplevel(app)
    
    if title != None:
        message_box.title(title)

    # Add a label to show the message
    label = ctk.CTkLabel(message_box, text=message, font=("Arial", 16))
    label.pack(padx=20, pady=20)

    # Add a button to close the message box
    close_button = ctk.CTkButton(message_box, text="OK", command=message_box.destroy)
    close_button.pack(pady=10)

    # Center the message box on the screen
    message_box.geometry(f"+{int(app.winfo_x() + app.winfo_width() // 2 - 150)}+{int(app.winfo_y() + app.winfo_height() // 2 - 100)}")

# Example of how to use the show_message function


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


def new_user(app, user_drowndown):
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'users')
    user_input = CTkInputDialog(title = None, text= "Enter name of user:")
    the_user = user_input.get_input()
    if user_input:
        try:
            new_users_path = os.path.join(users_path, the_user)
            os.makedirs(new_users_path, exist_ok=False)
            show_message(app, None, "User Created")
            save_user_calendar(load_calendar(), the_user)
            update_user_dropdown(app, user_drowndown)
        except FileExistsError:
            show_message(app, "Error", "User Already Exists")
        except TypeError:
            return 0
