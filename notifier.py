import smtplib
from email.mime.text import MIMEText
from typing import Optional
import config

def send_email(subject: str, body: str) -> bool:
    """
    Sends an email
    """
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_FROM
        msg["To"] = config.EMAIL_TO

        server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT, timeout=20)
        server.starttls()
        server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {config.EMAIL_TO}: {subject}")
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

def alert_user(title: str, message: str, email_body: Optional[str] = None):

    send_email(title, email_body or message)
