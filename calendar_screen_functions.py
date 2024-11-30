import pickle, calendar, os
from datetime import datetime
import customtkinter as ctk 
from collections import defaultdict

def load_calendar_data():
    current_dir = os.path.dirname(__file__)
    users_folder = os.path.join(current_dir, 'users')
    output_pickle_file = os.path.join(current_dir, "universal_calendar.pkl")
    universal_calendar_data(users_folder, output_pickle_file)
    try:
        with open('universal_calendar.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def calendar_transition(app):
    app.show_frame("cviewer")
    load_calendar_data()

def get_date_range(self):
    if not self.calendar_data:
        return datetime.today(), datetime.today()

    dates = [entry['date'] for entry in self.calendar_data]
    date_objects = [datetime.strptime(date, "%m-%d-%Y") for date in dates]
    return min(date_objects), max(date_objects)

def get_events_for_date(self, date_str):
    for entry in self.calendar_data:
        if entry['date'] == date_str:
            return entry['events']
    return []

def update_calendar(self):
    year = self.current_date.year
    month = self.current_date.month
    self.header.configure(text=f"{calendar.month_name[month]} {year}")

    for widget in self.calendar_frame.winfo_children():
        widget.destroy()

    cal = calendar.monthcalendar(year, month)

    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day != 0:
                date_str = f"{month:02d}-{day:02d}-{year}"
                events = get_events_for_date(self, date_str)
                button_text = str(day)
                button_color = "darkblue" if not events else "lightblue"
                font_color = "black" if events else "white"

                button = ctk.CTkButton(
                    self.calendar_frame, 
                    text=button_text, 
                    width=5, 
                    height=3,
                    command=lambda day=day, month=month, year=year: on_date_selected(self, day, month, year),
                    font=("Arial", 20), 
                    fg_color=button_color, 
                    text_color=font_color, 
                    border_color="grey", 
                    border_width=1
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    for i in range(6):
        self.calendar_frame.grid_rowconfigure(i, weight=1, uniform="equal")
    for j in range(7):
        self.calendar_frame.grid_columnconfigure(j, weight=1, uniform="equal")

def prev_month(self):
    if self.current_date.month > 1:
        new_date = self.current_date.replace(month=self.current_date.month - 1)
    else:
        new_date = self.current_date.replace(month=12, year=self.current_date.year - 1)

    if new_date >= self.start_date:
        self.current_date = new_date
        update_calendar(self)

def next_month(self):
    if self.current_date.month < 12:
        new_date = self.current_date.replace(month=self.current_date.month + 1)
    else:
        new_date = self.current_date.replace(month=1, year=self.current_date.year + 1)

    if new_date <= self.end_date:
        self.current_date = new_date
        update_calendar(self)
        #self.reset_window_size()

def on_date_selected(self, day, month, year):
    date_str = f"{month:02d}-{day:02d}-{year}"
    events = get_events_for_date(self, date_str)
    users = next((entry['some_users'] for entry in self.calendar_data if entry['date'] == date_str), [])

    popup = ctk.CTkToplevel(self)
    popup.title(f"Events on {date_str}")
    popup.geometry("400x300")  

    # Scrollable frame for events
    scrollable_frame = ctk.CTkScrollableFrame(popup)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Header for the popup
    header = ctk.CTkLabel(scrollable_frame, text=f"Events on {date_str}:", font=("Arial", 18))
    header.pack(pady=(10, 15))

    # Display events and their corresponding users in the scrollable frame
    if events:
        for event, user in zip(events, users):
            event_label = ctk.CTkLabel(scrollable_frame, text=f"{event} ({user})", font=("Arial", 16))
            event_label.pack(anchor="w", padx=10, pady=2)
    else:
        no_events_label = ctk.CTkLabel(scrollable_frame, text="No Events Present", font=("Arial", 16))
        no_events_label.pack(pady=10)

    # Create a frame for the close button (to keep it at the bottom of the window)
    button_frame = ctk.CTkFrame(popup)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    # Close button
    close_button = ctk.CTkButton(button_frame, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

def reset_calendar(self):
    # Reset the calendar to the initial state
    self.current_date = self.start_date  # Reset the current date to the start date
    update_calendar(self)  # Update the calendar view with the initial date
    self.calendar_data = load_calendar_data()  # Re-load the calendar data from the pickle file

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



