from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from dotenv import load_dotenv
from typing import List

import os

load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = int(os.environ.get("MAIL_PORT", 465))

def send_mail(to: List[str], subject: str, body: str):
    message = MIMEText(body, "html")
    message["From"] = USERNAME
    message["To"] = ",".join(to)
    message["Subject"] = subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return True
    except Exception as e:
        return {"status": 500, "errors": str(e)}
    
def generate_confirmation_email(ticket_information, technician):
    email_to = []
    retrived_email = technician.get("email")
    if retrived_email is not None:
        email_to.append(retrived_email)
    email_to.append("rostering99@gmail.com")
    email_subject = f"Task Assigned: {ticket_information['title']}"
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Assigned</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            p {{
                color: #666;
                line-height: 1.6;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .footer {{
                margin-top: 20px;
                color: #888;
                font-size: 12px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Task Assigned</h1>
            <p>Dear {technician['name']},</p>
            <p>A new task has been assigned to you with the following details:</p>
            <ul>
                <li><strong>Task:</strong> {ticket_information['title']}</li>
                <li><strong>Task Description:</strong> {ticket_information['description']}</li>
                <li><strong>Priority:</strong> {ticket_information['priority']}</li>
                <li><strong>Location:</strong> {ticket_information['location']}</li>
                <li><strong>Created At:</strong> {ticket_information['created_at']}</li>
                <li><strong>Task UID:</strong> {ticket_information['uid']}</li>
            </ul>
            <p>Please proceed accordingly.</p>
            <p>Regards,<br>
            Rostering Team</p>
            <p><i>This email was generated automatically. Please do not reply.</i></p>
        </div>
        <div class="footer">
            <p>If you have any questions, please contact us at [Your Contact Information].</p>
        </div>
    </body>
    </html>

    """

    return email_to, email_subject, email_body

def generate_cancellation_email(ticket_information, technician):
    email_to = []
    retrieved_email = technician.get("email")
    if retrieved_email is not None:
        email_to.append(retrieved_email)
    email_to.append("rostering99@gmail.com")
    email_subject = f"Task Cancelled: {ticket_information['title']}"
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Cancelled</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            p {{
                color: #666;
                line-height: 1.6;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .footer {{
                margin-top: 20px;
                color: #888;
                font-size: 12px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Task Cancelled</h1>
            <p>Dear {technician['name']},</p>
            <p>Previously assigned task to you has been cancelled. Below are the details of the cancelled task:</p>
            <ul>
                <li><strong>Task:</strong> {ticket_information['title']}</li>
                <li><strong>Task Description:</strong> {ticket_information['description']}</li>
                <li><strong>Priority:</strong> {ticket_information['priority']}</li>
                <li><strong>Location:</strong> {ticket_information['location']}</li>
                <li><strong>Created At:</strong> {ticket_information['created_at']}</li>
                <li><strong>Task UID:</strong> {ticket_information['uid']}</li>
            </ul>
            <p>Regards,<br>
            Rostering Team</p>
            <p><i>This email was generated automatically. Please do not reply.</i></p>
        </div>
        <div class="footer">
            <p>If you have any questions, please contact us at rostering99@gmail.com.</p>
        </div>
    </body>
    </html>

    """

    return email_to, email_subject, email_body
