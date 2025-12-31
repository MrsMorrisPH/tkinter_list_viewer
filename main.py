# ================================================
# List Viewer with Tkinter Graphics
# ================================================
# This program demonstrates:
#   1. Creating and storing data in a list
#   2. Using a global variable to track position in the list
#   3. Building a graphical window using tkinter
#   4. Displaying list items in a label
#   5. Using a button to navigate through the list
# When the button is clicked, the next item from the list appears on screen.

# Import the tkinter library for creating graphical user interfaces (GUIs)
import tkinter as tk

# Declare global variables so they can be used in functions
global my_list
global index

# Create a list to store the items we want to display
my_list = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
# Create an index variable to track which item in the list we're currently showing
index = 0

# Define a function that runs when the button is clicked
def on_button_click():
    # Tell Python to use the global 'index' variable so we can change it
    global index
    # Increase the index by 1 to move to the next item in the list
    index = index + 1
    # Check if we've reached the end of the list
    # len(my_list) returns the total number of items in the list
    if index >= len(my_list):
        # If we're at the end, go back to the beginning (index = 0)
        index = 0

    # Update the label on the screen to display the current item
    # my_list[index] gets the item at the current position in the list
    list_label.config(text= my_list[index] )








# Create the main window that will hold all the graphics and buttons
# tk.Tk() creates a new window object
window = tk.Tk()
window.title("Text and Button")  # Set the title shown at the top of the window
window.geometry("600x400")       # Set the window size: 600 pixels wide by 400 pixels tall
window.configure(bg="white")     # Set the background color of the window to white


# Create a Button widget (a clickable button on the screen)
# Parameters (inputs) we're giving to the Button:
#   - window: the parent container where this button will appear (the main window)
#   - text: the label that shows on the button
#   - command: the function to run when the button is clicked
#   - bg: background color of the button
#   - fg: text color (foreground) - the color of the button's label
#   - font: the typeface and size of the text on the button
next_button = tk.Button(
    window,
    text="Next Item",  # button label
    command=on_button_click, #bind the callback function
    bg="#0080FF",     # blue background
    fg="white",       # white text
    font=("Arial", 18)
)

# Create a Label widget (a text display area on the screen)
# Parameters (inputs) we're giving to the Label:
#   - window: the parent container where this label will appear (the main window)
#   - text: the text to display on the label (starting with the first list item)
#   - font: the typeface and size of the displayed text
#   - bg: background color of the label
#   - fg: text color (foreground) - the color of the displayed text
list_label = tk.Label(
    window,
    text= my_list[index],
    font=("Arial", 20),
    bg="white",
    fg="black"
)

# Place the label on the screen using the pack geometry manager
# pady=50 adds padding (empty space) above and below the label
list_label.pack(pady=50)

# Place the button in the center of the window using the pack geometry manager
# expand=True makes the button expand to fill available space
# This helps center the button both vertically and horizontally in the window
next_button.pack(expand=True)

# Start the Tkinter event loop (mainloop)
# This keeps the window open and continuously listens for user actions
# such as button clicks and window events
# Without this line, the window would appear and immediately close
window.mainloop()