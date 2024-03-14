import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import firebase_admin
from firebase_admin import credentials, db
import os
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from googletrans import Translator
import threading

def translate_text(text, dest):
    if dest == "Arabic":
        return text
    else:
        translator = Translator()
        translated_text = translator.translate(text, dest=dest).text
        return translated_text

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = data.get('city') + ', ' + data.get('region') + ', ' + data.get('country')
        return location
    except Exception as e:
        print("Error getting user location:", e)

def get_primary_language_for_location(location):
    try:
        geolocator = Nominatim(user_agent="language_app")
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            country_code = location_data.raw.get('address', {}).get('country_code')
            if country_code:
                primary_language = get_primary_language(country_code)
                return primary_language
            else:
                print("Country code not found for:", location)
        else:
            print("Location not found:", location)
    except Exception as e:
        print("Error getting location data:", e)

def get_primary_language(country_code):
    try:
        url = f"http://www.unicode.org/cldr/charts/latest/summary/{country_code}.html"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            language_tag = soup.find('td', string='Primary language:')
            if language_tag:
                primary_language = language_tag.find_next_sibling('td').get_text(strip=True)
                return primary_language
            else:
                print("Primary language not found for country code:", country_code)
        else:
            print("Failed to fetch data:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)

try:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("sahoor-seha-firebase-adminsdk-4igja-e4925dcd41.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sahoor-seha-default-rtdb.firebaseio.com'
    })

    # Reference to your Firebase Realtime Database
    admin_ref = db.reference('/credentials/Admins', app=firebase_admin.get_app())
    user_ref = db.reference('/credentials/Users', app=firebase_admin.get_app())

except Exception as e:
    messagebox.showerror("Firebase Initialization Error", f"Error initializing Firebase: {e}")
    exit()

lang = "Arabic"  # Default language if initialization fails
user_location = None
primary_language = None

def load_user_data():
    global lang, user_location, primary_language
    user_location = get_user_location()
    if user_location:
        print("User's location:", user_location)

    primary_language = get_primary_language_for_location(user_location)
    if primary_language:
        lang = str(primary_language)
    else:
        lang = "Arabic"

    print("Language selected:", lang)

    options = ["-------", "English", lang]
    language_enter.config(values=options)

    # Enable widgets after data loading
    username_label.config(state="normal")
    username_entry.config(state="normal")
    password_label.config(state="normal")
    password_entry.config(state="normal")
    language_enter.config(state="readonly")
    submit_button.config(state="normal")
    register_button.config(state="normal")

def open_home_screen():
    variable_to_pass = language_enter.get()
    root.destroy()
    os.system(f"python redirection-all-screen.py {variable_to_pass}")

def login():
    username = username_entry.get().strip().lower()
    password = password_entry.get().strip()

    admin_data = admin_ref.get()
    if admin_data and username in admin_data:
        if password == str(admin_data[username]):
            messagebox.showinfo("Login Successful", f"Welcome, {username}! (Admin)")
            open_home_screen()
            return

    user_data = user_ref.get()
    if user_data and username in user_data:
        if password == str(user_data[username]):
            messagebox.showinfo("Login Successful", f"Welcome, {username}! (User)")
            open_home_screen()
            return

    messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

def register_screen_redirect():
    variable_to_pass = language_enter.get()
    root.destroy()
    os.system(f"python register-screen--firebase.py {variable_to_pass}")

root = tk.Tk()
root.title("Login")
root.attributes('-fullscreen', True)
root.configure(bg="#090619")

username_label = tk.Label(root, text="Username: / اسم المستخدم:", bg="#090619", fg="white", state="disabled")
username_label.pack(anchor="w", padx=10, pady=5)
username_entry = tk.Entry(root, show="", bg="white", fg="black", state="disabled")
username_entry.pack(fill="x", padx=10, pady=5)

password_label = tk.Label(root, text="Password: / كلمة المرور:", bg="#090619", fg="white", state="disabled")
password_label.pack(anchor="w", padx=10, pady=5)
password_entry = tk.Entry(root, show="*", bg="white", fg="black", state="disabled")
password_entry.pack(fill="x", padx=10, pady=5)

language_label = tk.Label(root, text="Language: / :اللغة", bg="#090619", fg="white", state="disabled")
language_label.pack(anchor="w", padx=10, pady=5)
language_enter = ttk.Combobox(root, state="disabled")
language_enter.pack()

submit_button = tk.Button(root, text="Login", command=login, bg="white", fg="black", state="disabled")
submit_button.pack(fill="x", padx=10, pady=10)

register_button = tk.Button(root, text="Register", command=register_screen_redirect, bg="white", fg="black", state="disabled")
register_button.pack(fill="x", padx=10, pady=10)

# Start a new thread to load user data
thread = threading.Thread(target=load_user_data)
thread.start()

root.mainloop()
