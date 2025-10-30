import datetime
import time
import os
import platform

def play_sound():
    # Cross-platform sound playing
    if platform.system() == "Windows":
        import winsound
        duration = 10000 # milliseconds
        freq = 980  # Hz
        winsound.Beep(freq, duration)
    elif platform.system() == "Darwin":
        os.system("say 'Time is up!'")  # macOS voice
    else:
        os.system("paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga")  # Linux

def get_alarm_time():
    while True:
        alarm_input = input("Set alarm (HH:MM 24-hour format): ")
        try:
            alarm_time = datetime.datetime.strptime(alarm_input, "%H:%M").time()
            return alarm_time
        except ValueError:
            print("Invalid time format. Please enter in HH:MM (24-hour) format.")

def main():
    print("⏰ Simple Alarm Clock ⏰")
    alarm_time = get_alarm_time()
    print(f"Alarm set for {alarm_time.strftime('%H:%M')}")

    while True:
        now = datetime.datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            print("🔔 Wake up! 🔔")
            play_sound()
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
