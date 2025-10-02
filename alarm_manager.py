import threading
import time
from datetime import datetime
import pygame
import os

pygame.mixer.init()

TONE_FOLDER = "tones"
TONE_OPTIONS = {
    "Beep": os.path.join(TONE_FOLDER, "beep.wav"),
    "Birds": os.path.join(TONE_FOLDER, "birds.wav"),
    "Digital": os.path.join(TONE_FOLDER, "digital.wav")
}

alarms = []

def add_alarm(alarm_time, tone_path):
    alarm = {"time": alarm_time, "tone": tone_path, "active": True}
    alarms.append(alarm)

def toggle_alarm(index, state):
    alarms[index]["active"] = state

def play_alarm(tone_path):
    pygame.mixer.music.load(tone_path)
    pygame.mixer.music.play()

def stop_alarm():
    pygame.mixer.music.stop()

def alarm_checker(show_popup_callback):
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        for alarm in alarms:
            if alarm["active"] and alarm["time"] == now:
                print(f"[ALARM] Ringing at {now}")
                play_alarm(alarm["tone"])
                show_popup_callback()
                alarm["active"] = False
        time.sleep(1)