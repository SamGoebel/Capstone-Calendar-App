import customtkinter as ctk
from calendar_generator import check_template
from calendar_object import CalendarCreation
from frame_functions import update_user_dropdown, template_maker, load_user_calendar, new_user, check_event_list, load_user_calendar_for_events, adding_events, load_event_dates_with_details, update_dropdown, open_event_editor_window, delete_user_window

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

        button2 = ctk.CTkButton(self, text="Check Template", command= lambda: check_template)
        button2.pack(pady=10)

        button3 = ctk.CTkButton(self, text="Restore Template", command= lambda: template_maker)
        button3.pack(pady=10)

        test_ui = ctk.CTkButton(self, text="Test UI", command=check_template)
        test_ui.pack(pady=10)


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

        load_user_button = ctk.CTkButton(self, text="Delete User", command=lambda: delete_user_window(app, controller.frames["uconfig"].dropdown.get(), controller.frames["uconfig"].dropdown))
        load_user_button.pack(pady=10)
    
        button = ctk.CTkButton(self, text="Back to Home", command=lambda: controller.show_frame("home"))
        button.pack(pady=10)


class UserViewerFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.welcome_label = ctk.CTkLabel(self, font=("Arial", 18))
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
        label = ctk.CTkLabel(self, text="About This App", font=("Arial", 18))
        label.pack(pady=20)

        self.event_edit_dropdown = ctk.CTkOptionMenu(self)
        self.event_edit_dropdown.pack(pady=10)
        self.event_edit_dropdown.set("Select an Event")

        edit_window_button = ctk.CTkButton(self, text = "Edit Selected Event", command=lambda: open_event_editor_window(app, controller.frames["uconfig"].dropdown.get(), controller.frames["eeditor"].event_edit_dropdown.get()))
        edit_window_button.pack(pady=20)

        refresh_button = ctk.CTkButton(self, text="Refresh Events", command=lambda: update_dropdown(app, controller.frames["uconfig"].dropdown.get(), controller.frames["eeditor"].event_edit_dropdown))
        refresh_button.pack(pady=10) 
        
        button = ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("uviewer"))
        button.pack(pady=10)




ctk.set_appearance_mode("system")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
app = App()
app.mainloop()
