import tkinter as tk
from tkinter import messagebox
import requests
import os, sys
from googletrans import Translator

# Pre-given language code variable
language = sys.argv[1]  # Change this to your desired language code

# Function to translate text
def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest=language).text
    return translated_text

def return_home():
    root.destroy()
    os.system(f"python redirection-all-screen.py {language}")

def fetch_food_nutrition(food_name):
    try:
        api_key = "ph3xROkfdTFBVCe4YvCUHOdV27DgofiJsgCribtI"
        api_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            "query": food_name,
            "api_key": api_key
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching food nutrition data:", e)
        return None

def check_meal_nutrition(foods, age, height, weight, meal_type):
    # Constants for recommended daily values (example values)
    RECOMMENDED_CALORIES = 2000
    RECOMMENDED_PROTEIN = 50  # grams
    RECOMMENDED_FAT = 70  # grams
    RECOMMENDED_CARBS = 310  # grams

    # Calculate total nutritional values for the meal
    total_calories = sum(food['calories'] for food in foods)
    total_protein = sum(food['protein'] for food in foods)
    total_fat = sum(food['fat'] for food in foods)
    total_carbs = sum(food['carbs'] for food in foods)

    # Check if the meal exceeds recommended values
    if (total_calories > RECOMMENDED_CALORIES or
            total_protein > RECOMMENDED_PROTEIN or
            total_fat > RECOMMENDED_FAT or
            total_carbs > RECOMMENDED_CARBS):
        return False  # Meal exceeds recommended values
    else:
        return True  # Meal meets recommended values

def submit_or_enter(event=None):
    food_name = entry.get()
    age = age_entry.get()
    height = height_entry.get()
    weight = weight_entry.get()
    meal_type = meal_type_entry.get()

    if not all((food_name, age, height, weight, meal_type)):
        error_label.config(text=translate_text("Please fill out all fields."), fg="red")
        for widget in (entry, age_entry, height_entry, weight_entry, meal_type_entry):
            if not widget.get():
                widget.config(highlightbackground=None, highlightcolor=None, highlightthickness=0)
    else:
        error_label.config(text="")
        for widget in (entry, age_entry, height_entry, weight_entry, meal_type_entry):
            widget.config(highlightbackground=None, highlightcolor=None, highlightthickness=0)

        try:
            height_cm = float(height)
            weight_kg = float(weight)
        except ValueError:
            bmi_label.config(text=translate_text("BMI: N/A (Invalid height/weight)"))
            return

        food_data = fetch_food_nutrition(food_name)
        if food_data:
            food_name_label.config(text=translate_text("Nutritional Information for") + " " + food_name + ":")
            nutrients = []
            for item in food_data['foods']:
                nutrients.append(f"{translate_text('Calories')}: {item['calories']} kcal")
                nutrients.append(f"{translate_text('Protein')}: {item['protein']} g")
                nutrients.append(f"{translate_text('Fat')}: {item['fat']} g")
                nutrients.append(f"{translate_text('Carbohydrates')}: {item['carbohydrates']} g")
            nutrition_label.config(text='\n'.join(nutrients))
            
            # Check meal nutrition
            foods = food_data['foods']  # Assuming 'foods' contains nutritional information for the meal
            if check_meal_nutrition(foods, int(age), float(height), float(weight), meal_type):
                recommendation_label.config(text=translate_text("Meal meets recommended nutrition values."))
            else:
                recommendation_label.config(text=translate_text("Meal exceeds recommended nutrition values."))
        else:
            food_name_label.config(text=translate_text("Food data not found."))
            nutrition_label.config(text="")

root = tk.Tk()
root.title(translate_text("Nutritional Info and Recommendations"))
root.configure(bg="#090619")
root.attributes("-fullscreen", True)

label = tk.Label(root, text=translate_text("Enter food name:"), bg='#090619', fg='white', font=("Helvetica", 16))
label.pack()

entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack()

age_label = tk.Label(root, text=translate_text("Enter your age:"), bg='#090619', fg='white', font=("Helvetica", 16))
age_label.pack()
age_entry = tk.Entry(root, font=("Helvetica", 14))
age_entry.pack()

height_label = tk.Label(root, text=translate_text("Enter your height (cm):"), bg='#090619', fg='white', font=("Helvetica", 16))
height_label.pack()
height_entry = tk.Entry(root, font=("Helvetica", 14))
height_entry.pack()

weight_label = tk.Label(root, text=translate_text("Enter your weight (kg):"), bg='#090619', fg='white', font=("Helvetica", 16))
weight_label.pack()
weight_entry = tk.Entry(root, font=("Helvetica", 14))
weight_entry.pack()

meal_type_label = tk.Label(root, text=translate_text("Enter meal type:"), bg='#090619', fg='white', font=("Helvetica", 16))
meal_type_label.pack()
meal_type_entry = tk.Entry(root, font=("Helvetica", 14))
meal_type_entry.pack()

error_label = tk.Label(root, text="", bg="#090619", fg="red", font=("Helvetica", 14))
error_label.pack()

button = tk.Button(root, text=translate_text("Submit"), command=submit_or_enter, bg="white", fg="black", font=("Helvetica", 16))
button.pack(pady=10)
root.bind("<Return>", submit_or_enter)

button2 = tk.Button(root, text=translate_text("Return to Home Screen"), command=return_home, bg="white", fg="black", font=("Helvetica", 16))
button2.pack()

food_name_label = tk.Label(root, text="", bg="#090619", fg="white", font=("Helvetica", 14))
food_name_label.pack()

nutrition_label = tk.Label(root, text="", bg="#090619", fg="white", font=("Helvetica", 14))
nutrition_label.pack()

bmi_label = tk.Label(root, text="", bg="#090619", fg="white", font=("Helvetica", 14))
bmi_label.pack()

recommendation_label = tk.Label(root, text="", bg="#090619", fg="white", font=("Helvetica", 14))
recommendation_label.pack()

root.mainloop()
