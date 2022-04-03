from os import getenv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get the environment variables from docker-compose
sender_email: str = getenv("SENDER_EMAIL")
sender_password: str = getenv("SENDER_PASSWORD")


def send_html_email(email: str, subject: str, html: str):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email

    # Turn these into plain/html MIMEText objects
    final_message = MIMEText(html, "html")
    message.attach(final_message)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
