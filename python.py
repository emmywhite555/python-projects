import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
from pathlib import Path
from datetime import datetime

# Updated Question Bank
questions_bank = [
    {
        "question": "Which of the following protocols is responsible for automatically assigning IP addresses to devices in a network?",
        "options": ["DNS", "SNMP", "DHCP", "NetFlow"],
        "answer": "DHCP"
    },
    {
        "question": "What command is used in Windows to check the network configuration of a device?",
        "options": ["ifconfig", "ping", "ipconfig", "traceroute"],
        "answer": "ipconfig"
    },
    {
        "question": "Which network management component is responsible for detecting and resolving network issues?",
        "options": ["Fault Management", "Configuration Management", "Performance Management", "Security Management"],
        "answer": "Fault Management"
    },
    {
        "question": "IPv6 addresses are 32-bit long, similar to IPv4.",
        "options": ["True", "False", "None of the above", "All of the above"],
        "answer": "False"
    },
    {
        "question": "Traceroute is used to monitor bandwidth usage in a network.",
        "options": ["True", "False", "None of the above", "All of the above"],
        "answer": "False"
    },
    {
        "question": "The physical layer contains information in the form of _______?",
        "options": ["Bytes", "Bits", "Terabyte", "Megabyte"],
        "answer": "Bits"
    },
    {
        "question": "Segment in the Network layer is referred to as _____________?",
        "options": ["Transmitter", "Repeater", "Packet", "Data"],
        "answer": "Packet"
    },
    {
        "question": "Which network topology is commonly used in the internet backbone?",
        "options": ["Star Topology", "Mesh Topology", "Bus Topology", "Ring Topology"],
        "answer": "Mesh Topology"
    },
    {
        "question": "Which topology provides high redundancy and reliability?",
        "options": ["Star Topology", "Point-to-Point Topology", "Bus Topology", "Mesh Topology"],
        "answer": "Mesh Topology"
    },
    {
        "question": "What protocol is commonly used in Mesh Topology for configuration?",
        "options": ["DHCP", "HTTP", "FTP", "TCP/IP"],
        "answer": "DHCP"
    },
    {
        "question": "Which network topology connects all devices to a central hub?",
        "options": ["Mesh", "Bus", "Star", "Ring"],
        "answer": "Star"
    },
    {
        "question": "Which type of cable is commonly used in Star Topology?",
        "options": ["TV cable", "Unshielded Twisted Pair cable", "Wireless cable", "Fibre Optic cable"],
        "answer": "Unshielded Twisted Pair cable"
    },
    {
        "question": "Which network topology is highly scalable due to its hierarchical structure?",
        "options": ["Star", "Ring", "Bus", "Tree"],
        "answer": "Tree"
    },
    {
        "question": "Which topology ensures that each device is connected to exactly two other devices in a closed loop?",
        "options": ["Star", "Bus", "Ring", "Tree"],
        "answer": "Ring"
    },
    {
        "question": "In a bus topology, what is required at both ends of the cable to prevent signal loss?",
        "options": ["Terminators", "Modems", "Repeaters", "Hubs"],
        "answer": "Terminators"
    },
    {
        "question": "Which topology combines characteristics of bus and star topology?",
        "options": ["Hybrid", "Tree", "Mesh", "Grid"],
        "answer": "Tree"
    },
    {
        "question": "Which network topology is the most cost-effective for simple connections?",
        "options": ["Bus", "Ring", "Tree", "Mesh"],
        "answer": "Bus"
    },
    {
        "question": "Which of the following protocols operates at the Transport Layer?",
        "options": ["HTTP", "IP", "TCP", "Ethernet"],
        "answer": "TCP"
    },
    {
        "question": "Which layer of the OSI model is responsible for managing device addressing and routing data packets?",
        "options": ["Physical", "Data Link", "Transport", "Network"],
        "answer": "Network"
    },
    {
        "question": "Which of the following protocols operates at the Application Layer?",
        "options": ["IP", "HTTP", "UDP", "TCP"],
        "answer": "HTTP"
    },
    {
        "question": "What command is used in Linux operating system to check the network configuration of a device?",
        "options": ["ifconfig", "ping", "ipconfig", "traceroute"],
        "answer": "ifconfig"
    },
    {
        "question": "In which network mode do devices communicate directly without a central access point?",
        "options": ["Mesh mode", "Infrastructure mode", "Ad-hoc mode", "Enterprise mode"],
        "answer": "Ad-hoc mode"
    },
    {
        "question": "Which of the following is a best practice for securing a wireless network?",
        "options": ["Using WEP Encryption", "Disabling SSID broadcast", "Keeping default router password", "Allowing all devices to connect freely"],
        "answer": "Disabling SSID broadcast"
    },
    {
        "question": "Which wireless technology operates within the 2.4 GHz frequency band and is commonly used for short-range communication?",
        "options": ["Zigbee", "Bluetooth", "RFID", "LTE"],
        "answer": "Bluetooth"
    },
    {
        "question": "Which of the following is considered a security threat to wireless networks?",
        "options": ["MITM attack", "MAC addresss filtering", "WPA3 encryption", "Firewall implementation"],
        "answer": "MITM attack"
    }
]

random.shuffle(questions_bank)

class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam - 30 Seconds Per Question")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.question_index = 0
        self.score = 0
        self.time_left = 30
        self.timer_id = None
        self.candidate_name = ""

        #Resize and load logo
        self.logo_img = Image.open("logo.png")
        self.logo_img = self.logo_img.resize((150, 150), Image.ANTIALIAS)
        self.logo_tk = ImageTk.PhotoImage(self.logo_img)

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_window()

        logo_label = tk.Label(self.root, image=self.logo_tk)
        logo_label.pack(pady=10)

        self.welcome_label = tk.Label(self.root, text="Enter your full name to begin:", font=("Arial", 14))
        self.welcome_label.pack(pady=10)

        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=40)
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Exam", font=("Arial", 12), command=self.start_quiz)
        self.start_button.pack(pady=20)

    def start_quiz(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your full name to start.")
            return

        self.candidate_name = name
        self.clear_window()
        self.create_widgets()
        self.display_question()

    def create_widgets(self):
        self.timer_label = tk.Label(self.root, text="Time left: 30", font=("Arial", 14), fg="red")
        self.timer_label.pack(pady=10)

        self.question_label = tk.Label(self.root, text="", font=("Arial", 16), wraplength=650, justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", font=("Arial", 12), width=40, command=lambda b=i: self.check_answer(b))
            btn.pack(pady=8)
            self.option_buttons.append(btn)

    def display_question(self):
        if self.question_index < len(questions_bank):
            self.time_left = 30
            self.update_timer()
            question_data = questions_bank[self.question_index]
            self.question_label.config(text=question_data["question"])
            for i, option in enumerate(question_data["options"]):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            self.show_result()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.times_up()

    def times_up(self):
        messagebox.showinfo("Time's up!", "You ran out of time for this question.")
        self.next_question()

    def check_answer(self, option_index):
        selected = self.option_buttons[option_index].cget("text")
        correct = questions_bank[self.question_index]["answer"]
        if selected == correct:
            self.score += 1
        self.root.after_cancel(self.timer_id)
        self.next_question()

    def next_question(self):
        self.question_index += 1
        self.display_question()

    def show_result(self):
        self.clear_window()
        percentage = (self.score / len(questions_bank)) * 100
        result_text = f"Exam Complete, {self.candidate_name}!\nYour Score: {percentage:.2f}%"

        logo_label = tk.Label(self.root, image=self.logo_tk)
        logo_label.pack(pady=10)

        result_label = tk.Label(self.root, text=result_text, font=("Arial", 16), wraplength=650, justify="center")
        result_label.pack(pady=50)

        self.save_result_to_file(percentage)

    def save_result_to_file(self, percentage):
        documents_path = Path.home() / "Documents"
        file_path = documents_path / "ExamResults.txt"

        now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        result_entry = (
            f"Name: {self.candidate_name}\n"
            f"Score: {percentage:.2f}%\n"
            f"Time: {now}\n"
            "-------------------------------\n"
        )

        try:
            with open(file_path, "a") as file:
                file.write(result_entry)
            print(f"Result saved to {file_path}")
        except Exception as e:
            print(f"Failed to save result: {e}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = ExamApp(root)
root.mainloop()


#pyinstaller --noconfirm --onefile --windowed --add-data "logo.png;." exam.py