import smtplib
import os
import ssl
from datetime import date
from email.message import EmailMessage


def formatter(scheduled_reminders):
    result = []
    for k, v in scheduled_reminders.items():
        body = ""
        for idx, reminder in enumerate(v):
            body += f"<< Reminder {idx+1} >>{chr(10)}"
            body += f'  —  {f"{chr(10)}  —  ".join(reminder["recipients"])}{chr(10)}'
            body += (
                f'{chr(10)}"{reminder["message"]}"{chr(10)}{chr(10)}{chr(10)}'
            )
        result.append((k, body))
    return result


def send_emails(emails):
    for email in emails:
        # Define email sender and receiver
        email_sender = "soontmteam@gmail.com"
        email_password = os.environ["EMAIL_PASSWORD"]
        email_receiver = email[0]

        # Set the subject and body of the email
        subject = f"Your reminders for {date.today()}"
        body = email[1]

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()
        try:
            # Log in and send the email
            with smtplib.SMTP_SSL(
                "smtp.gmail.com", 465, context=context
            ) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        except Exception:
            continue
