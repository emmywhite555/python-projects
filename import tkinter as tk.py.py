import tkinter as tk
from tkinter import messagebox

TASKS_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def add_task():
    task = entry.get().strip()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks(listbox.get(0, tk.END))
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def delete_task():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected[0])
        save_tasks(listbox.get(0, tk.END))
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

def mark_done():
    selected = listbox.curselection()
    if selected:
        task = listbox.get(selected[0])
        if not task.startswith("✔️ "):
            listbox.delete(selected[0])
            listbox.insert(selected[0], "✔️ " + task)
            save_tasks(listbox.get(0, tk.END))

# GUI setup
root = tk.Tk()
root.title("To-Do List App")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

done_btn = tk.Button(root, text="Mark as Done", command=mark_done)
done_btn.pack()

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack()

# Load tasks from file
for task in load_tasks():
    listbox.insert(tk.END, task)

root.mainloop()
