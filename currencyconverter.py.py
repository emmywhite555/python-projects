import tkinter as tk
from tkinter import ttk

# Fixed exchange rates relative to USD
RATES = {
    'USD': 1.0,      # US Dollar
    'EUR': 0.93,     # Euro
    'GBP': 0.80,     # British Pound
    'JPY': 151.50,   # Japanese Yen
    'CAD': 1.36,     # Canadian Dollar
    'AUD': 1.52,     # Australian Dollar
    'CHF': 0.90,     # Swiss Franc
    'CNY': 7.23,     # Chinese Yuan
    'INR': 83.30,    # Indian Rupee
    'MXN': 16.75,    # Mexican Peso
    'BRL': 5.05,     # Brazilian Real
    'RUB': 92.50,    # Russian Ruble
    'KRW': 1342.00,  # South Korean Won
    'SGD': 1.35,     # Singapore Dollar
    'NZD': 1.68,     # New Zealand Dollar
    'TRY': 32.00,    # Turkish Lira
    'ZAR': 18.90,    # South African Rand
    'SEK': 10.65,    # Swedish Krona
    'NOK': 10.75,    # Norwegian Krone
}

def convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        if from_currency not in RATES or to_currency not in RATES:
            result_label.config(text="Unsupported currency.")
            return

        # Convert to USD first, then to target
        amount_in_usd = amount / RATES[from_currency]
        converted_amount = amount_in_usd * RATES[to_currency]

        result = f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
        result_label.config(text=result)
    except ValueError:
        result_label.config(text="Please enter a valid number.")

# Create main window
root = tk.Tk()
root.title("Currency ConverT")
root.geometry("400x250")
root.resizable(False, False)

# Widgets
title_label = ttk.Label(root, text="Currency Converter", font=("Arial", 16))
title_label.pack(pady=10)

amount_entry = ttk.Entry(root, width=20, justify='center') 
amount_entry.pack(pady=5)
amount_entry.insert(0, "1")

from_currency_var = tk.StringVar(value="USD")
to_currency_var = tk.StringVar(value="JPY")

currency_options = list(RATES.keys())

from_menu = ttk.Combobox(root, textvariable=from_currency_var, values=currency_options, state="readonly")
from_menu.pack(pady=5)

to_menu = ttk.Combobox(root, textvariable=to_currency_var, values=currency_options, state="readonly")
to_menu.pack(pady=5)

convert_button = ttk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run the app
root.mainloop()
