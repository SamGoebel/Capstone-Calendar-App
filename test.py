import tkinter as tk
import customtkinter as ctk
from PyQt5.QtWidgets import QApplication, QFileDialog

def open_file_dialog():
    # Ensure QApplication is created before creating any PyQt5 widgets
    app = QApplication([])  # This is necessary to open the PyQt5 dialog
    
    file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif)")
    if file_path:
        print(f"Selected file: {file_path}")
    
    app.quit()  # Properly quit the QApplication when done

class UserConfigFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Users", font=("Arial", 18))
        label.pack(pady=10)

        # Create the button to open the file dialog
        add_user_button = ctk.CTkButton(self, text="Add User", command=open_file_dialog)
        add_user_button.pack(pady=10)

# Create the customtkinter window
root = ctk.CTk()
user_config = UserConfigFrame(root)
user_config.pack(padx=20, pady=20)

root.mainloop()
