import customtkinter as ctk
import os, pickle
from calendar_generator import generate_dates_with_events_until_2100, event_search, save_calendar, load_calendar, check_template, save_user_calendar, no_date_event_search, delete_event, save_event_list
from event_maker import adding_events, loading_events
from calendar_object import CalendarCreation
from frame_functions import update_user_dropdown, template_maker, load_user_calendar, new_user

# Initializing the app
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calendar App Project")
        self.geometry("600x400")

        # Main container for frames
        self.frame_container = ctk.CTkFrame(self, corner_radius=0)
        self.frame_container.pack(fill="both", expand=True)

        # Create frames
        self.frames = {}
        self.frames["home"] = HomeFrame(self.frame_container, self)
        self.frames["uconfig"] = UserConfigFrame(self.frame_container, self)
        self.frames["uviewer"] = UserViewerFrame(self.frame_container, self)
        self.frames["eadder"] = EventAdderFrame(self.frame_container, self)
        self.frames["eeditor"] = EventEditorFrame(self.frame_container, self)

        # Pack all frames into the container
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame("home")

    def show_frame(self, frame_name):
        """Bring a specific frame to the front."""
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()


# Frames
class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Sam's Calendar App", font=("Arial", 18))
        label.pack(pady=20)

        button1 = ctk.CTkButton(self, text="Users", command= lambda: update_user_dropdown(app, controller.frames["uconfig"].dropdown))
        button1.pack(pady=10)

        button2 = ctk.CTkButton(self, text="Check Template", command=check_template)
        button2.pack(pady=10)

        button2 = ctk.CTkButton(self, text="Restore Template", command=template_maker)
        button2.pack(pady=10)


class UserConfigFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Users", font=("Arial", 18))
        label.pack(pady=10)

         # Label to display the selected option
        self.label = ctk.CTkLabel(self, text="Select an option:", font=("Arial", 16))
        self.label.pack(pady=20)

        # Dropdown (CTkOptionMenu)
        self.dropdown = ctk.CTkOptionMenu(self)
        self.dropdown.pack(pady=10)

        # Set default value
        self.dropdown.set("No Users Found")

        add_user_button = ctk.CTkButton(self, text="Add User", command=lambda: new_user(app, controller.frames["uconfig"].dropdown))
        add_user_button.pack(pady=10)

        load_user_button = ctk.CTkButton(self, text="Load User", command=lambda: load_user_calendar(app, controller.frames["uconfig"].dropdown.get(), controller.frames["uviewer"].welcome_label))
        load_user_button.pack(pady=10)
    
        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)


class UserViewerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.welcome_label = ctk.CTkLabel(self, font=("Arial", 18))
        self.welcome_label.pack(pady=20)

        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)

class EventAdderFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="About This App", font=("Arial", 18))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)

class EventEditorFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="About This App", font=("Arial", 18))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)




ctk.set_appearance_mode("system")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
app = App()
app.mainloop()
