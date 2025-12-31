# ----------------------------------------------
# Tutorial: Ceating and displaying a list in tkinter
# This program creates a window with a label single button.
# When the button is clicked, items form a list prints in the console.
# ----------------------------------------------

# Import the tkinter library
import tkinter as tk


global home_label
global my_list
global index

my_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
index = 0

# Define a function that runs when the button is clicked
def on_button_click():
    # specify that we are using the global variable 'index'
    global index
    # Increment the index to point to the next item in the list
    index = index + 1
    # If the index exceeds the list length, reset it to 0
    if index >= len(my_list):
        index = 0

    # Update the label text to show the current item from the list
    list_label.config(text= my_list[index] )








# Create the main window (the app screen)
window = tk.Tk()
window.title("Text and Button")  # Set the title of the window
window.geometry("600x400")       # Set the size of the window (width x height)
window.configure(bg="white")     # Set the background color to white


# Create a Button widget
# Parameters:
#   - window: the parent container (the main window)
#   - text: label on the button
#   - command: function to call when the button is clicked
#   - bg: background color
#   - fg: text color (foreground)
#   - font: text font and size
next_button = tk.Button(
    window,
    text="Next Item",  # button label
    command=on_button_click, #bind the callback function
    bg="#0080FF",     # blue background
    fg="white",       # white text
    font=("Arial", 18)
)

# Create a Label
# Parameters:
#   - window: the parent container (the main window)
#   - text: label on the screen
#   - font: font style and size
#   - bg: background color
#   - fg: text color (foreground)
list_label = tk.Label(
    window,
    text= my_list[index],
    font=("Arial", 20),
    bg="white",
    fg="black"
)

# Add Home screen label
list_label.pack(pady=50) # adds padding to the y

# Place the button in the center of the window using the pack geometry manager
# 'expand=True' and 'fill="none"' center the button both vertically and horizontally
next_button.pack(expand=True)

# Run the Tkinter event loop
# This keeps the window open and listens for user actions (like clicks)
window.mainloop()