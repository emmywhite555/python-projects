import tkinter as tk
import random

# Dice faces (Unicode characters)
dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

def roll_dice():
    roll = random.randint(0, 5)
    dice_label.config(text=dice_faces[roll], font=("Arial", 100))
    result_label.config(text=f"You rolled a {roll+1}")

# Main window
root = tk.Tk()
root.title("Dice Rolling Simulator")
root.geometry("300x300")

# Widgets
dice_label = tk.Label(root, text="🎲", font=("Arial", 100))
dice_label.pack(pady=20)

result_label = tk.Label(root, text="Click Roll to start!", font=("Arial", 14))
result_label.pack(pady=10)

roll_button = tk.Button(root, text="Roll Dice", command=roll_dice, font=("Arial", 14))
roll_button.pack(pady=20)

# Run the app
root.mainloop()