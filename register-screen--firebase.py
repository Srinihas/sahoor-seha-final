import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import sys
import os
from googletrans import Translator

# Access the variable passed as a command line argument
variable_received = sys.argv[1]

# Function to translate text to the language specified by variable_received
def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest=variable_received).text
    return translated_text

try:
    # Reference to your Firebase Realtime Database
    admin_ref = db.reference(translate_text('/credentials/Admins'))
    user_ref = db.reference(translate_text('/credentials/Users'))

except Exception as e:
    messagebox.showerror(translate_text("Firebase Initialization Error"), translate_text(f"Error initializing Firebase: {e}"))
    exit()

def register_user():
    new_username = new_username_entry.get().strip().lower()
    new_password = new_password_entry.get().strip().lower()

    try:
        if type(new_password) != "<class 'int'>":
            messagebox.showerror(translate_text("Error"), translate_text("Password can only be made of numbers"))
        else:
            # Check if username already exists
            new_password = int(new_password)
            if user_ref.child(new_username).get():
                messagebox.showerror(translate_text("Registration Failed"), translate_text("Username already exists. Please choose a different username."))
            else:
                # Create new user in Firebase
                user_ref.child(new_username).set({'password': new_password})
                messagebox.showinfo(translate_text("Registration Successful"), translate_text("User registered successfully!"))
                os.system(translate_text("python redirection-all-screen.py"))

    except firebase_admin.exceptions.NotFoundError:
        # Create the necessary path before setting user data
        user_ref.child(new_username).set({'password': new_password})
        messagebox.showinfo(translate_text("Registration Successful"), translate_text("User registered successfully!"))
        os.system(translate_text("python redirection-all-screen.py"))
        
def login_screen():
    os.system(translate_text("python login-screen--firebase.py"))

# Create the main window
root = tk.Tk()
root.title(translate_text("Registration"))
root.attributes('-fullscreen', True)
root.configure(bg=translate_text("#090619"))

# Create new username label and entry field
new_username_label = tk.Label(root, text=translate_text("New Username:"), bg=translate_text("#090619"), fg=translate_text("white"))
new_username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
new_username_entry = tk.Entry(root)
new_username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

# Create new password label and entry field
new_password_label = tk.Label(root, text=translate_text("New Password:"), bg=translate_text("#090619"), fg=translate_text("white"))
new_password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
new_password_entry = tk.Entry(root, show="*")
new_password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

# Create register button
register_button = tk.Button(root, text=translate_text("Register"), command=register_user, bg=translate_text("white"), fg=translate_text("black"))
register_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

login_button = tk.Button(root, text=translate_text("Login"), command=login_screen, bg=translate_text("white"), fg=translate_text("black"))
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Run the application
root.mainloop()
