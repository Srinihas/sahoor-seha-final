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

def translate_text(text, dest):
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
    # Reference to your Firebase Realtime Database
    admin_ref = db.reference('/credentials/Admins', app=firebase_admin.get_app())
    user_ref = db.reference('/credentials/Users', app=firebase_admin.get_app())

except Exception as e:
    messagebox.showerror(translate_text("Firebase Initialization Error", lang), translate_text(f"Error initializing Firebase: {e}", lang))
    exit()

lang = "Arabic"  # Default language if initialization fails

def open_home_screen():
    global lang
    lang = language_enter.get()
    variable_to_pass = lang
    root.destroy()
    os.system(f"python redirection-all-screen.py {variable_to_pass}")

def login():
    username = username_entry.get().strip().lower()
    password = password_entry.get().strip()

    admin_data = admin_ref.get()
    if admin_data and username in admin_data:
        if password == str(admin_data[username]):
            messagebox.showinfo(translate_text("Login Successful", lang), translate_text(f"Welcome, {username}! (Admin)", lang))
            open_home_screen()
            return

    user_data = user_ref.get()
    if user_data and username in user_data:
        if password == str(user_data[username]):
            messagebox.showinfo(translate_text("Login Successful", lang), translate_text(f"Welcome, {username}! (User)", lang))
            open_home_screen()
            return

    messagebox.showerror(translate_text("Login Failed", lang), translate_text("Invalid username or password. Please try again.", lang))

def register_screen_redirect():
    global lang
    lang = language_enter.get()
    variable_to_pass = lang
    root.destroy()
    os.system(f"python register-screen.py {variable_to_pass}")

root = tk.Tk()
root.title(translate_text("Login", lang))
root.attributes('-fullscreen', True)
root.configure(bg="#090619")

username_label = tk.Label(root, text="Username: / اسم المستخدم:", bg="#090619", fg="white")
username_label.pack(side="left")
username_entry = tk.Entry(root, show="", bg="white", fg="black")
username_entry.pack(fill="x")

password_label = tk.Label(root, text="Password: / كلمة المرور:", bg="#090619", fg="white")
password_label.pack(side="left")
password_entry = tk.Entry(root, show="*", bg="white", fg="black")
password_entry.pack(fill="x")

user_location = get_user_location()
if user_location:
    print(translate_text("User's location:", lang), user_location)

primary_language = get_primary_language_for_location(user_location)
if primary_language:
    lang = str(primary_language)
else:
    lang = "Arabic"

options = ["-------", "English", lang]

language_enter = ttk.Combobox(root, values=options, state="readonly")
language_enter.pack()

submit_button = tk.Button(root, text=translate_text("Login", lang), command=login, bg="white", fg="black")
submit_button.pack(fill="x")

register_button = tk.Button(root, text=translate_text("Register", lang), command=register_screen_redirect, bg="white", fg="black")
register_button.pack(fill="x")

root.mainloop()
