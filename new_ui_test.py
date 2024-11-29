import customtkinter as ctk
import pickle, calendar
from calendar_generator import check_template
from frame_functions import update_user_dropdown, template_maker, load_user_calendar, new_user, check_event_list, load_user_calendar_for_events, adding_events
from frame_functions import update_dropdown, open_event_editor_window, delete_user_window, set_theme, get_current_theme, set_color, get_current_color
from datetime import datetime

# Initializing the app
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calendar App Project")
        self.geometry("800x600")

        # Main container for frames
        self.frame_container = ctk.CTkScrollableFrame(self, corner_radius=0, width= 800, height = 600)
        self.frame_container.pack(fill="both", expand=True)

        # Create frames
        self.frames = {}
        self.frames["home"] = HomeFrame(self.frame_container, self)
        self.frames["uconfig"] = UserConfigFrame(self.frame_container, self)
        self.frames["uviewer"] = UserViewerFrame(self.frame_container, self)
        self.frames["cviewer"] = CalendarViewerFrame(self.frame_container, self)
        self.frames["eadder"] = EventAdderFrame(self.frame_container, self)
        self.frames["eeditor"] = EventEditorFrame(self.frame_container, self)
        self.frames["settings"] = SettingsFrame(self.frame_container, self)

        # Configure grid weights for proper expansion
        self.frame_container.grid_rowconfigure(0, weight=1, uniform="equal")  # Allow vertical expansion
        self.frame_container.grid_columnconfigure(0, weight=1, uniform="equal")  # Allow horizontal expansion

        # Pack all frames into the container
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame("home")

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()


# Frames
class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Sam's Calendar App", font=("Arial", 18))
        label.pack(pady=20)

        user_select_button = ctk.CTkButton(self, text="Select User", command= lambda: update_user_dropdown(app, controller.frames["uconfig"].dropdown))
        user_select_button.pack(pady=10)

        check_template_button = ctk.CTkButton(self, text="Check Template", command= lambda: check_template)
        check_template_button.pack(pady=10)

        restore_template_button = ctk.CTkButton(self, text="Restore Template", command= lambda: template_maker)
        restore_template_button.pack(pady=10)

        settings = ctk.CTkButton(self, text="Settings", command= lambda: controller.show_frame("settings"))
        settings.pack(pady=10)

        calendar = ctk.CTkButton(self, text="Calendar", command= lambda: controller.show_frame("cviewer"))
        calendar.pack(pady=10)

        quit = ctk.CTkButton(self, text="Quit", command= lambda: app.destroy())
        quit.pack(pady=10)


class UserConfigFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Users", font=("Arial", 18))
        label.pack(pady=10)

        self.label = ctk.CTkLabel(self, text="Select an option:", font=("Arial", 16))
        self.label.pack(pady=20)

        add_user_button = ctk.CTkButton(self, text="Add User", command=lambda: new_user(app, controller.frames["uconfig"].dropdown))
        add_user_button.pack(pady=10)

        self.dropdown = ctk.CTkOptionMenu(self, dynamic_resizing = False)
        self.dropdown.pack(pady=(20, 10))
        self.dropdown.set("No Users Found")

        load_user_button = ctk.CTkButton(self, text="Load User", command=lambda: load_user_calendar(app, controller.frames["uconfig"].dropdown.get(), controller.frames["uviewer"].welcome_label, controller.frames["uviewer"].image_label))
        load_user_button.pack(pady=10)

        load_user_button = ctk.CTkButton(self, text="Delete User", command=lambda: delete_user_window(app, controller.frames["uconfig"].dropdown.get(), controller.frames["uconfig"].dropdown))
        load_user_button.pack(pady=10)
    
        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)


class UserViewerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.image_label = ctk.CTkLabel(self, text="")  # Set text="" for image-only label
        self.image_label.place(relx=1.0, rely=0.0, anchor="ne")
        
        self.image_holder = ctk.CTkLabel(self, text="") 
        self.image_holder.pack(pady=5)

        self.welcome_label = ctk.CTkLabel(self, font=("Arial", 18), wraplength = 100)
        self.welcome_label.pack(pady=20)

        button = ctk.CTkButton(self, text="Add Event", command=lambda: controller.show_frame("eadder"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Edit Event", command=lambda: update_dropdown(app, controller.frames["uconfig"].dropdown.get(), controller.frames["eeditor"].event_edit_dropdown))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Print User Event List", command=lambda: check_event_list(app, controller.frames["uconfig"].dropdown.get()))
        button.pack(pady=10)
        
        button = ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("uconfig"))
        button.pack(pady=10)

class EventAdderFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="New Event", font=("Arial", 18))
        label.pack(pady=20)

        date_label = ctk.CTkLabel(self, text="Enter Date (DD-MM-YYYY)")
        date_label.pack(pady=10)

        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.pack(pady=10)

        title_label = ctk.CTkLabel(self, text="Enter Title")
        title_label.pack(pady=10)

        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(pady=10)

        importance_label = ctk.CTkLabel(self, text="Enter Importance Level")
        importance_label.pack(pady=10)

        self.importance_entry = ctk.CTkEntry(self)
        self.importance_entry.pack(pady=10)

        notes_label = ctk.CTkLabel(self, text="Enter Notes")
        notes_label.pack(pady=10)

        self.notes_entry = ctk.CTkEntry(self)
        self.notes_entry.pack(pady=10)

        save_button = ctk.CTkButton(self, text="Save Event", command=lambda: adding_events(app, load_user_calendar_for_events(controller.frames["uconfig"].dropdown.get()), controller.frames["eadder"].date_entry.get(), controller.frames["eadder"].title_entry.get(), controller.frames["eadder"].importance_entry.get(), controller.frames["eadder"].notes_entry.get(), controller.frames["uconfig"].dropdown.get()))
        save_button.pack(pady=10)

        back_button = ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("uviewer"))
        back_button.pack(pady=10)


class EventEditorFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Event Editor", font=("Arial", 18))
        label.pack(pady=20)

        self.event_edit_dropdown = ctk.CTkOptionMenu(self, dynamic_resizing = False)
        self.event_edit_dropdown.pack(pady=10)
        self.event_edit_dropdown.set("Select an Event")

        edit_window_button = ctk.CTkButton(self, text = "Edit Selected Event", command=lambda: open_event_editor_window(app, controller.frames["uconfig"].dropdown.get(), controller.frames["eeditor"].event_edit_dropdown.get()))
        edit_window_button.pack(pady=20)

        refresh_button = ctk.CTkButton(self, text="Refresh Events", command=lambda: update_dropdown(app, controller.frames["uconfig"].dropdown.get(), controller.frames["eeditor"].event_edit_dropdown))
        refresh_button.pack(pady=10) 
        
        button = ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("uviewer"))
        button.pack(pady=10)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        settings_label = ctk.CTkLabel(self, text="Settings", font=("Arial", 18))
        settings_label.pack(pady=20)

        self.theme_dropdown = ctk.CTkOptionMenu(self, values = ["Light", "Dark", "System"])
        self.theme_dropdown.pack(pady=10)
        self.theme_dropdown.set("Select Theme")

        set_theme_button = ctk.CTkButton(self, text = "Set Theme", command=lambda: set_theme(controller.frames["settings"].theme_dropdown.get()))
        set_theme_button.pack(pady=10) 

        self.color_dropdown = ctk.CTkOptionMenu(self, values = ["Green", "Blue", "Dark-blue"])
        self.color_dropdown.pack(pady=(30, 10))
        self.color_dropdown.set("Select Color")

        set_color_button = ctk.CTkButton(self, text = "Set Color", command=lambda: set_color(controller.frames["settings"].color_dropdown.get()))
        set_color_button.pack(pady= (10, 0)) 

        reset_label = ctk.CTkLabel(self, text= "(Applies on Reset)", font=("Arial", 12))
        reset_label.pack(pady= (0, 10))
        
        button = ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("home"))
        button.pack(pady=20)

class CalendarViewerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
         # Load calendar data from pickle file
        self.calendar_data = self.load_calendar_data()

        # Determine the earliest and latest dates in the data
        self.start_date, self.end_date = self.get_date_range()

        # Debugging: Print the date range
        print(f"Start date: {self.start_date}")
        print(f"End date: {self.end_date}")

        # Initialize the current date to the start date
        self.current_date = self.start_date

        # Header: Month and Year
        self.header = ctk.CTkLabel(self, text="", font=("Arial", 20))
        self.header.grid(row=0, column=1, pady=10)

        # Calendar Frame (ensure it's within the fixed size window)
        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Navigation buttons (arrows)
        self.prev_button = ctk.CTkButton(self, text="<", command=self.prev_month, width=20, height=8)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ctk.CTkButton(self, text=">", command=self.next_month, width=20, height=8)
        self.next_button.grid(row=0, column=2, padx=10)

        # Update calendar 
        self.update_calendar()

        # Configure grid row and column weights to fill the screen
        self.grid_rowconfigure(1, weight=1, uniform="equal")  # Row for the calendar
        self.grid_columnconfigure(0, weight=1, uniform="equal")  # Left side
        self.grid_columnconfigure(1, weight=5, uniform="equal")  # Center (calendar)
        self.grid_columnconfigure(2, weight=1, uniform="equal")  # Right side

        # Make sure the calendar frame expands within the window
        self.calendar_frame.grid_rowconfigure(0, weight=1)
        for i in range(7):  # 7 columns in the calendar
            self.calendar_frame.grid_columnconfigure(i, weight=1)
       
        self.calendar_back_button = ctk.CTkButton(self, width= 150, font = ("Arial", 18), text = "Go Back", command=lambda: controller.show_frame("home"))
        self.calendar_back_button.grid(row=2, column=1, pady=10, sticky="nsew")  # Place below the calendar (row=1)

        # Set row configuration for the button to make sure it takes space below the calendar
        self.grid_rowconfigure(1, weight=1)  # Button row does not expand, just takes its required space
        self.grid_columnconfigure(1, weight= 1)


    def load_calendar_data(self):
        # Load the calendar data from a pickle file
        try:
            with open('test_calendar.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Pickle file not found. Using empty calendar data.")
            return []

    def get_date_range(self):
        # Determine the earliest and latest dates in the calendar data
        if not self.calendar_data:
            return datetime.today(), datetime.today()  # Return today's date if no data

        dates = [entry['date'] for entry in self.calendar_data]
        date_objects = [datetime.strptime(date, "%m-%d-%Y") for date in dates]

        # Return the earliest and latest dates as a tuple (start, end)
        return min(date_objects), max(date_objects)

    def get_events_for_date(self, date_str):
        # Find events for a given date from the loaded calendar data
        for entry in self.calendar_data:
            if entry['date'] == date_str:
                return entry['events']
        return []

    def update_calendar(self):
        # Get current month and year
        year = self.current_date.year
        month = self.current_date.month

        # Update header text
        self.header.configure(text=f"{calendar.month_name[month]} {year}")

        # Clear previous calendar grid
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Get the calendar for the current month
        cal = calendar.monthcalendar(year, month)

        # Create the grid of buttons
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:  # Skip zeros (days outside the current month)
                    date_str = f"{month:02d}-{day:02d}-{year}"
                    events = self.get_events_for_date(date_str)

                    # Set button text to only the day number, no events count
                    button_text = str(day)

                    # Change button color based on events
                    button_color = "darkblue" if not events else "lightblue"
                    font_color = "black" if events else "white"

                    # Create button with grey outline and consistent size
                    button = ctk.CTkButton(self.calendar_frame, text=button_text, width=5, height=3,
                                           command=lambda day=day, month=month, year=year: self.on_date_selected(day, month, year),
                                           font = ("Arial", 20), fg_color=button_color, text_color= font_color, border_color="grey", border_width=1)
                    button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

        # Make sure all grid cells expand equally
        for i in range(6):  # 6 rows in a calendar
            self.calendar_frame.grid_rowconfigure(i, weight=1, uniform="equal")
        for j in range(7):  # 7 columns (days of the week)
            self.calendar_frame.grid_columnconfigure(j, weight=1, uniform="equal")

    def prev_month(self):
        # Go to the previous month
        if self.current_date.month > 1:
            new_date = self.current_date.replace(month=self.current_date.month - 1)
        else:
            new_date = self.current_date.replace(month=12, year=self.current_date.year - 1)

        # Make sure we don't go before the start date
        if new_date >= self.start_date:
            self.current_date = new_date
            self.update_calendar()
            self.reset_window_size()

    def next_month(self):
        # Go to the next month
        if self.current_date.month < 12:
            new_date = self.current_date.replace(month=self.current_date.month + 1)
        else:
            new_date = self.current_date.replace(month=1, year=self.current_date.year + 1)

        # Make sure we don't go beyond the end date
        if new_date <= self.end_date:
            self.current_date = new_date
            self.update_calendar()

    def on_date_selected(self, day, month, year):
        date_str = f"{month:02d}-{day:02d}-{year}"
        events = self.get_events_for_date(date_str)
        print(f"Date {date_str} selected!")
        if events:
            print("Events:")
            for event in events:
                print(f"- {event}")
        else:
            print("No events for this date.")        

try:
    ctk.set_appearance_mode(get_current_theme("config.txt"))  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme(get_current_color("config.txt"))  # Options: "blue", "green", "dark-blue"
except AttributeError:
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

app = App()
app.mainloop()
