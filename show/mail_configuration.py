import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "admin@ticketshow.com"
SENDER_PASSWORD = "mypassword"


def send_email(to_address, subject, message, attachment=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["Subject"] = subject
    mail["To"] = to_address
    mail.attach(MIMEText(message, "html"))
    if attachment:
        with open(attachment, "rb") as attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)

            part.add_header("Content-Disposition", 
                            f"attachment; filename={attachment.split('/')[-1]}")
            mail.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()
    
    return True

