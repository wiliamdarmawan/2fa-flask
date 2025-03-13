import smtplib
from email.mime.text import MIMEText
from app.config import Config
from app import celery

@celery.task(name="send_email_task")
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "generousbil@gmail.com"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail("generousbil@gmail.com", [to_email], msg.as_string())
        return f"Email sent to {to_email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"
