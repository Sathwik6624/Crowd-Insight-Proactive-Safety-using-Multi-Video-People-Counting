import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from playsound import playsound
import os

from config import *


# ✅ FULL PATH (SAFE)
SOUND_PATH = r"C:\alert.wav"


def play_sound():
    try:
        if os.path.exists(SOUND_PATH):
            playsound(SOUND_PATH)
        else:
            print("[ERROR] Sound file not found")
    except Exception as e:
        print("[ERROR] Sound failed:", e)


def send_email(cam_id, count):
    try:
        subject = f"ALERT: Camera {cam_id}"
        body = f"""
Camera {cam_id} exceeded threshold!

People Count: {count}
Time: {datetime.now()}
"""

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("[INFO] Email sent successfully")

    except Exception as e:
        print("[ERROR] Email failed:", e)


def send_alert(cam_id, count):
    print(f"[ALERT] Camera {cam_id} → Count: {count}")

    if ALERT_SOUND:
        play_sound()   # 🔊 SOUND HERE

    if EMAIL_ALERT:
        send_email(cam_id, count)