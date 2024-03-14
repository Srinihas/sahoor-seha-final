import datetime
import geocoder
import requests
import tkinter as tk
from tkinter import messagebox
import os, sys
from googletrans import Translator

# Access the variable passed as a command line argument
variable_received = sys.argv[1]

# Define the list of Islamic months
islamic_months = [
    "Muharram", "Safar", "Rabi Al Awwal", "Rabi' Atb-Thaani",
    "Jumada Al Awwal", "Jumada Ath Thaant", "Rajab", "Shabaan",
    "Ramadan", "Shawwaal", "Dhul Qadan", "Dhul Hijah"
]

def translate_text(text, dest):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest).text
    return translated_text

def get_islamic_date():
    try:
        current_datetime = datetime.datetime.now()
        response = requests.get("http://api.aladhan.com/v1/gToH?date=" + current_datetime.strftime("%d-%m-%Y"))
        response.raise_for_status()
        response_data = response.json()
        hijri_month = response_data['data']['hijri']['month']['number']
        hijri_date = response_data['data']['hijri']['day']
        return islamic_months[int(hijri_month) - 1], int(hijri_date)
    except Exception as e:
        messagebox.showerror(translate_text("Error", variable_received), translate_text(f"An error occurred while retrieving Islamic date: {e}", variable_received))
        return None, None

def get_prayer_times(city, country):
    try:
        url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["data"]["timings"]
        return data["Fajr"], data["Dhuhr"], data["Asr"], data["Maghrib"], data["Isha"]
    except Exception as e:
        messagebox.showerror(translate_text("Prayer Times Error", variable_received), translate_text(f"Failed to retrieve prayer times: {e}", variable_received))
        return None, None, None, None, None

def update_message_label():
    city, country = get_location()
    if city and country:
        fajr, dhuhr, asr, maghrib, isha = get_prayer_times(city, country)
        islamic_month, hijri_date = get_islamic_date()
        if all([fajr, dhuhr, asr, maghrib, isha]) and islamic_month is not None and hijri_date is not None:
            prayer_message = translate_text("Today's Prayer Times:\nFajr: {fajr}\nDhuhr: {dhuhr}\nAsr: {asr}\nMaghrib: {maghrib}\nIsha: {isha}", variable_received)
            islamic_date_message = translate_text("Islamic Date: {islamic_month}, {hijri_date}", variable_received)
            text.config(text=prayer_message + "\n" + islamic_date_message)
        else:
            text.config(text=translate_text("Failed to retrieve prayer times or Islamic date.", variable_received))
    else:
        text.config(text=translate_text("Failed to retrieve location.", variable_received))

def get_location():
    try:
        location = geocoder.ip('me')
        city = location.city
        country = location.country
        return city, country
    except Exception as e:
        print(f"Error retrieving location: {e}")
        return None, None

def home():
    root.destroy()
    os.system(f"python redirection-all-screen.py {variable_received}")

root = tk.Tk()
root.title(translate_text("Islamic Date and Prayer Times Display", variable_received))
root.attributes("-fullscreen", True)
root.configure(bg="#090619")

# Button to update the Islamic date and prayer times
update_button = tk.Button(root, text=translate_text("Update", variable_received), command=update_message_label, bg="white", fg="black")
update_button.pack()

# Button to go back home
go_home = tk.Button(root, text=translate_text("Go Home", variable_received), command=home, bg="white", fg="black")
go_home.pack()

# Label to display the Islamic date and prayer times
text = tk.Label(root, text="", font=("Helvetica", 24), bg="#090619", fg="white")  # Increase font size for readability
text.pack()

# Add image at the bottom
image = tk.PhotoImage(file="image.png")
image_label = tk.Label(root, image=image, bg="#090619")
image_label.pack(side=tk.BOTTOM, pady=20)

# Run initial update
update_message_label()

root.mainloop()
