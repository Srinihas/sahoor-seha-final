import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
import os
from googletrans import Translator

# Access the variable passed as a command line argument
variable_received = sys.argv[1]  # Use index 1 to access the first argument

def translate_text(text, destination):
    translator = Translator()
    translated_text = translator.translate(text, dest=destination).text
    return translated_text

def check_input():
    root.destroy()
    os.system(f"python food.py {variable_received}")

def prayer_times():
    try:
        root.destroy()
        os.system(f"python date-and-times.py {variable_received}")
    except Exception as e:
        messagebox.showerror(translate_text("Error", variable_received), translate_text(f"An error occurred: {e}", variable_received))

def close_program():
    root.quit()
    root.destroy()

root = tk.Tk()
root.title(translate_text("Other Home-Screen", variable_received))
root.configure(bg="#090619")

# Increase font size for better readability on mobile
button_font = ("Helvetica", 18)

# Button to go to check food
check_food_button = tk.Button(root, text=translate_text("Go to check food", variable_received), command=check_input, font=button_font, bg="white", fg="black")
check_food_button.pack(pady=10, padx=20, fill=tk.X)

# Button to go to prayer times
prayer_times_button = tk.Button(root, text=translate_text("Go to prayer times", variable_received), command=prayer_times, font=button_font, bg="white", fg="black")
prayer_times_button.pack(pady=10, padx=20, fill=tk.X)

# Button to close the program
close_button = tk.Button(root, text=translate_text("Close Program", variable_received), command=close_program, font=button_font, bg="white", fg="black")
close_button.pack(pady=10, padx=20, fill=tk.X)

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - root.winfo_reqwidth()) // 2
y_coordinate = (screen_height - root.winfo_reqheight()) // 2
root.geometry(f"+{x_coordinate}+{y_coordinate}")

# Set window size relative to screen dimensions
root.attributes('-fullscreen', True)

# Set style for buttons
style = ttk.Style()
style.configure('TButton', font=button_font)

root.mainloop()
