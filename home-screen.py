import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys, os

def check_input():
    root.destroy()
    os.system("python login-screen.py")

def close_program():
    root.quit()
    root.destroy()

root = tk.Tk()
root.title("الشاشة الرئيسية")
root.configure(bg="#090619")

# Increase font size for better readability on mobile
button_font = ("Helvetica", 18)

# Button to go to check food
login_button_en = tk.Button(root, text="Login", command=check_input, font=button_font, bg="white", fg="black")
login_button_en.pack(pady=10, padx=20, fill=tk.X, side=tk.LEFT)

# Separator
separator_label = tk.Label(root, text=" / ", bg="#090619", fg="white")
separator_label.pack(side=tk.LEFT)

# Button to close the program
login_button_ar = tk.Button(root, text="تسجيل الدخول", command=check_input, font=button_font, bg="white", fg="black")
login_button_ar.pack(pady=10, padx=20, fill=tk.X, side=tk.RIGHT)

# Separator
separator_label = tk.Label(root, text=" / ", bg="#090619", fg="white")
separator_label.pack(side=tk.LEFT)

# Button to close the program
close_button_en = tk.Button(root, text="Close Program", command=close_program, font=button_font, bg="white", fg="black")
close_button_en.pack(pady=10, padx=20, fill=tk.X, side=tk.LEFT)

# Button to close the program
close_button_ar = tk.Button(root, text="إغلاق البرنامج", command=close_program, font=button_font, bg="white", fg="black")
close_button_ar.pack(pady=10, padx=20, fill=tk.X, side=tk.RIGHT)

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

# Add image at the bottom
image = tk.PhotoImage(file="image.png")
image_label = tk.Label(root, image=image, bg="#090619")
image_label.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
