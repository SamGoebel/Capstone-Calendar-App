import customtkinter as ctk

def toggle_circle(canvas, condition):
    # Delete all items from the canvas (clear it)
    canvas.delete("all")
    
    # Draw the circle if the condition is True
    if condition:
        # Coordinates for the bounding box of the circle
        x1, y1, x2, y2 = 50, 50, 250, 250  # Circle bounding box
        hex_color = "#FF6347"  # Example hex color (Tomato color)
        canvas.create_oval(x1, y1, x2, y2, fill=hex_color, outline="black", width=2)
    else:
        # Draw a message if the condition is False
        canvas.create_text(150, 150, text="No Circle", font=("Arial", 16), fill="black")

def toggle_condition(circle_condition):
    # Toggle the condition (True <-> False)
    circle_condition[0] = not circle_condition[0]

def main():
    # Create the main window
    app = ctk.CTk()
    app.geometry("400x400")

    # Create a CTkCanvas widget
    canvas = ctk.CTkCanvas(app, width=300, height=300)
    canvas.pack(pady=20, padx=20)
    
    # Initial condition (True to show circle, False to hide it)
    circle_condition = [True]  # Use a list to allow mutability in lambda function

    # Create the circle initially based on the condition
    toggle_circle(canvas, circle_condition[0])

    # Button to toggle the condition and circle visibility
    toggle_button = ctk.CTkButton(app, text="Toggle Circle", command=lambda: [toggle_condition(circle_condition), toggle_circle(canvas, circle_condition[0])])
    toggle_button.pack(pady=10)

    # Run the app
    app.mainloop()

if __name__ == "__main__":
    main()
