import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(to_email, code):
    subject = "Verify Your Email"
    html = f"""
    <html>
        <body>
            <h2>Welcome!</h2>
            <p>Your verification code is:</p>
            <h1>{code}</h1>
        </body>
    </html>
    """
    send_email(to_email, subject, html)

def send_password_reset_email(to_email, new_password):
    subject = "Your Password Has Been Reset"
    html = f"""
    <html>
        <body>
            <h2>Password Reset</h2>
            <p>Your new password is:</p>
            <h1>{new_password}</h1>
        </body>
    </html>
    """
    send_email(to_email, subject, html)

def send_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
