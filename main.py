import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import threading

from alarm_manager import add_alarm, toggle_alarm, alarm_checker, stop_alarm, TONE_OPTIONS

# ============ Config ============
TONE_FOLDER = "tones"
TONE_OPTIONS = {
    "Beep": os.path.join(TONE_FOLDER, "beep.wav"),
    "Birds": os.path.join(TONE_FOLDER, "birds.wav"),
    "Digital": os.path.join(TONE_FOLDER, "digital.wav")
}

# ============ Root Window ============
root = tk.Tk()
root.title("Alarm Clock App")
root.geometry("450x500")
root.configure(bg="#f0f0f0")

# Fonts
HEADER_FONT = ("Helvetica", 20, "bold")
TIME_FONT = ("Helvetica", 36)
DATE_FONT = ("Helvetica", 16)

# ============ Time & Date ============
time_label = tk.Label(root, text="", font=TIME_FONT, fg="#333", bg="#f0f0f0")
time_label.pack(pady=10)

date_label = tk.Label(root, text="", font=DATE_FONT, fg="#666", bg="#f0f0f0")
date_label.pack()

def update_time():
    now = datetime.now()
    time_label.config(text=now.strftime("%H:%M:%S"))
    date_label.config(text=now.strftime("%A, %d %B %Y"))
    root.after(1000, update_time)

update_time()

# ============ Alarm List ============
alarm_list_frame = tk.Frame(root, bg="#f0f0f0")
alarm_list_frame.pack(pady=10)

alarm_items = []

def refresh_alarm_list():
    for widget in alarm_list_frame.winfo_children():
        widget.destroy()

    for idx, alarm in enumerate(alarm_items):
        row = tk.Frame(alarm_list_frame, bg="#f0f0f0")
        row.pack(fill="x", pady=2)

        tk.Label(row, text=alarm["time"], width=10, anchor="w", bg="#f0f0f0").pack(side="left")
        tk.Label(row, text=alarm["tone"], width=12, anchor="w", bg="#f0f0f0").pack(side="left")

        state = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(
            row, variable=state, bg="#f0f0f0",
            command=lambda i=idx, var=state: toggle_alarm(i, var.get())
        )
        chk.pack(side="right")

# ============ Alarm Setting Window ============
def open_alarm_screen():
    alarm_win = tk.Toplevel(root)
    alarm_win.title("Set Alarm")
    alarm_win.geometry("350x300")
    alarm_win.configure(bg="#ffffff")

    tk.Label(alarm_win, text="Set Alarm Time", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=10)

    # Time picker
    frame = tk.Frame(alarm_win, bg="#ffffff")
    frame.pack(pady=5)

    hour_var = tk.StringVar(value="07")
    minute_var = tk.StringVar(value="00")
    second_var = tk.StringVar(value="00")

    ttk.Spinbox(frame, from_=0, to=23, textvariable=hour_var, width=5, format="%02.0f").grid(row=1, column=0, padx=5)
    ttk.Spinbox(frame, from_=0, to=59, textvariable=minute_var, width=5, format="%02.0f").grid(row=1, column=1, padx=5)
    ttk.Spinbox(frame, from_=0, to=59, textvariable=second_var, width=5, format="%02.0f").grid(row=1, column=2, padx=5)

    # Tone Picker
    tk.Label(alarm_win, text="Choose Tone", font=("Helvetica", 12), bg="#ffffff").pack(pady=10)
    tone_var = tk.StringVar(value=list(TONE_OPTIONS.keys())[0])
    tone_menu = ttk.Combobox(alarm_win, textvariable=tone_var, values=list(TONE_OPTIONS.keys()), state="readonly")
    tone_menu.pack()

    # Save Alarm
    def save_alarm():
        alarm_time = f"{hour_var.get()}:{minute_var.get()}:{second_var.get()}"
        selected_tone = tone_var.get()
        tone_path = TONE_OPTIONS.get(selected_tone)

        if not os.path.exists(tone_path):
            messagebox.showerror("Error", "Tone file not found!")
            return

        add_alarm(alarm_time, tone_path)

        # For UI list
        alarm_items.append({
            "time": alarm_time,
            "tone": selected_tone
        })

        refresh_alarm_list()
        messagebox.showinfo("Alarm", f"Alarm set for {alarm_time}")
        alarm_win.destroy()

    tk.Button(alarm_win, text="Save Alarm", command=save_alarm, bg="#4CAF50", fg="white").pack(pady=20)

# ============ Popup When Alarm Rings ============
def show_alarm_popup():
    popup = tk.Toplevel(root)
    popup.title("Alarm Ringing!")
    popup.geometry("300x150")
    popup.configure(bg="#ffcccc")

    tk.Label(popup, text="⏰ Wake Up!", font=("Helvetica", 18, "bold"), bg="#ffcccc").pack(pady=10)

    def dismiss():
        stop_alarm()
        popup.destroy()

    def snooze():
        stop_alarm()
        popup.destroy()
        # Snooze for 5 mins can be implemented later

    tk.Button(popup, text="Snooze", command=snooze, bg="orange", fg="white").pack(pady=5)
    tk.Button(popup, text="Dismiss", command=dismiss, bg="red", fg="white").pack(pady=5)

# ============ Alarm Checker Thread ============
t = threading.Thread(target=alarm_checker, args=(show_alarm_popup,), daemon=True)
t.start()

# ============ Home Button ============
tk.Button(
    root,
    text="Set New Alarm",
    font=HEADER_FONT,
    bg="#4CAF50",
    fg="white",
    command=open_alarm_screen,
    padx=10,
    pady=5
).pack(pady=10)

# ============ Start App ============
root.mainloop()