import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Для роботи з зображеннями та іконками

# Створення головного вікна з темною темою
root = ttkb.Window(themename="darkly")
root.title("The Greatest Converter")
root.geometry("600x450")
root.option_add('*TCombobox*Listbox.font', ('Arial', 12))

# Глобальні змінні для перекладу одиниць
current_language = "English"

# Функція для перевірки чи є введене значення числом
def validate_input(P):
    if P.isdigit() or P == "" or P.replace('.', '', 1).isdigit():
        return True
    else:
        return False

# Функція для конвертації одиниць виміру
def convert_units():
    try:
        value = float(entry_value.get())
        from_unit_translated = combo_from.get()
        to_unit_translated = combo_to.get()

        from_unit = unit_translation_reverse[current_language][from_unit_translated]
        to_unit = unit_translation_reverse[current_language][to_unit_translated]

        if (from_unit, to_unit) in conversion_factors:
            factor = conversion_factors[(from_unit, to_unit)]
            if callable(factor):  # Для температури (де є формули)
                result = factor(value)
            else:
                result = value * factor
            label_result_value.config(text=f"{result:.2f} {to_unit_translated}", foreground="#00cccc")  # Бірюзовий текст для результату
        else:
            label_result_value.config(text="Conversion not possible", foreground="red")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number.")

# Функція для перекладу інтерфейсу
def translate_interface(language):
    global current_language
    if language == "EN":
        current_language = "English"
        label_value.config(text="Value:")
        label_from.config(text="From Unit:")
        label_to.config(text="To Unit:")
        btn_convert.config(text="Convert")
        label_result.config(text="Result: ")
        update_units(unit_translation["English"])
    elif language == "UA":
        current_language = "Українська"
        label_value.config(text="Значення:")
        label_from.config(text="З одиниці:")
        label_to.config(text="До одиниці:")
        btn_convert.config(text="Конвертувати")
        label_result.config(text="Результат: ")
        update_units(unit_translation["Українська"])
    elif language == "SK":
        current_language = "Slovenský"
        label_value.config(text="Hodnota:")
        label_from.config(text="Z jednotky:")
        label_to.config(text="Na jednotku:")
        btn_convert.config(text="Previesť")
        label_result.config(text="Výsledok: ")
        update_units(unit_translation["Slovenský"])

# Оновлення одиниць виміру на основі вибраної мови
def update_units(units_translation):
    translated_units = [units_translation[unit] for unit in default_units]
    combo_from.config(values=translated_units)
    combo_to.config(values=translated_units)
    combo_from.set(units_translation["Select unit"])
    combo_to.set(units_translation["Select unit"])

# Словник з коефіцієнтами конвертації
conversion_factors = {
    ("Kilometers", "Miles"): 0.621371,
    ("Miles", "Kilometers"): 1.60934,
    ("Kilograms", "Pounds"): 2.20462,
    ("Pounds", "Kilograms"): 0.453592,
    ("Celsius", "Fahrenheit"): lambda c: (c * 9/5) + 32,
    ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
    ("Meters", "Feet"): 3.28084,
    ("Feet", "Meters"): 0.3048,
    ("Centimeters", "Inches"): 0.393701,
    ("Inches", "Centimeters"): 2.54,
    ("Liters", "Gallons"): 0.264172,
    ("Gallons", "Liters"): 3.78541,
    ("Grams", "Ounces"): 0.035274,
    ("Ounces", "Grams"): 28.3495,
}

# Одиниці виміру за замовчуванням на англійській мові
default_units = [
    "Kilometers", "Miles", "Kilograms", "Pounds", "Celsius", "Fahrenheit",
    "Meters", "Feet", "Centimeters", "Inches", "Liters", "Gallons",
    "Grams", "Ounces"
]

# Переклад одиниць виміру на різні мови
unit_translation = {
    "English": {
        "Kilometers": "Kilometers", "Miles": "Miles", "Kilograms": "Kilograms", "Pounds": "Pounds",
        "Celsius": "Celsius", "Fahrenheit": "Fahrenheit", "Meters": "Meters", "Feet": "Feet",
        "Centimeters": "Centimeters", "Inches": "Inches", "Liters": "Liters", "Gallons": "Gallons",
        "Grams": "Grams", "Ounces": "Ounces", "Select unit": "Select unit", "Result:": "Result:"
    },
    "Українська": {
        "Kilometers": "Кілометри", "Miles": "Милі", "Kilograms": "Кілограми", "Pounds": "Фунти",
        "Celsius": "Цельсії", "Fahrenheit": "Фаренгейти", "Meters": "Метри", "Feet": "Фути",
        "Centimeters": "Сантиметри", "Inches": "Дюйми", "Liters": "Літри", "Gallons": "Галони",
        "Grams": "Грами", "Ounces": "Унції", "Select unit": "Виберіть одиницю", "Result:": "Результат:"
    },
    "Slovenský": {
        "Kilometers": "Kilometre", "Miles": "Míle", "Kilograms": "Kilogramy", "Pounds": "Libry",
        "Celsius": "Celzius", "Fahrenheit": "Fahrenheit", "Meters": "Metre", "Feet": "Stopy",
        "Centimeters": "Centimetre", "Inches": "Palce", "Liters": "Litre", "Gallons": "Galóny",
        "Grams": "Gramy", "Ounces": "Unce", "Select unit": "Vyberte jednotku", "Result:": "Výsledok:"
    }
}

# Зворотний переклад одиниць для коректного пошуку в словнику
unit_translation_reverse = {
    "English": {v: k for k, v in unit_translation["English"].items()},
    "Українська": {v: k for k, v in unit_translation["Українська"].items()},
    "Slovenský": {v: k for k, v in unit_translation["Slovenský"].items()}
}

# Заголовок додатка
label_title = ttkb.Label(root, text="The Greatest Converter", font=("Arial", 24, "bold"), foreground="#00cccc")  # Бірюзовий заголовок
label_title.pack(pady=10)

# Віджети для введення даних та вибору одиниць
label_value = ttkb.Label(root, text="Value:", font=("Arial", 14, "bold"), foreground="orange")
label_value.pack(pady=5)

vcmd = (root.register(validate_input), '%P')
entry_value = ttkb.Entry(root, font=("Arial", 14), validate="key", validatecommand=vcmd)
entry_value.pack(pady=10)

label_from = ttkb.Label(root, text="From Unit:", font=("Arial", 14, "bold"), foreground="orange")
label_from.pack(pady=5)

combo_from = ttkb.Combobox(root, values=default_units, font=("Arial", 14), state="readonly")
combo_from.set(unit_translation["English"]["Select unit"])
combo_from.pack(pady=10)

label_to = ttkb.Label(root, text="To Unit:", font=("Arial", 14, "bold"), foreground="orange")
combo_to = ttkb.Combobox(root, values=default_units, font=("Arial", 14), state="readonly")
combo_to.set(unit_translation["English"]["Select unit"])
combo_to.pack(pady=10)

# Кнопка для виконання конвертації
btn_convert = ttkb.Button(root, text="Convert", bootstyle="success", command=convert_units, width=20)
btn_convert.pack(pady=20)

# Мітка для відображення результату
label_result = ttkb.Label(root, text="Result: ", font=("Arial", 16, "bold"), foreground="orange")
label_result.pack(side=tk.LEFT, padx=(50, 0))

label_result_value = ttkb.Label(root, text="", font=("Arial", 16, "bold"), foreground="#00cccc")  # Бірюзовий текст результату
label_result_value.pack(side=tk.LEFT, padx=(0, 50))

# Логотип зміни мови
img = Image.open("language_icon.png")  # Додайте іконку в кореневу директорію
img = img.resize((20, 20), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)

# Створення кнопки зі списком для зміни мови
btn_language = ttkb.Menubutton(root, image=photo, bootstyle="info", width=2)
btn_language.image = photo  # Зберігаємо посилання, щоб запобігти знищенню зображення
btn_language.place(relx=1.0, y=20, anchor="ne")

# Створення меню з мовами
menu_language = tk.Menu(btn_language, tearoff=0)
menu_language.add_command(label="EN", command=lambda: translate_interface("EN"))
menu_language.add_command(label="UA", command=lambda: translate_interface("UA"))
menu_language.add_command(label="SK", command=lambda: translate_interface("SK"))
btn_language["menu"] = menu_language

# Запуск головного циклу програми
root.mainloop()
