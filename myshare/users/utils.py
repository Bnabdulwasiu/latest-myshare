from flask import url_for, flash
import yagmail
from yagmail import YagConnectionClosed
import socket
import os
from dotenv import load_dotenv
load_dotenv()

def send_reset_email(user):
    email_sender = os.getenv('EMAIL_USERNAME')
    email_password = os.getenv('EMAIL_PASSWORD') 
    email_receiver = user.email
    token = user.get_reset_token()
    subject = "Password Reset Request"
    body = f"""To reset your password, visit the folowing link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes would be made."""
    try:
        yag = yagmail.SMTP(email_sender, email_password)
        contents = [body]
        yag.send(email_receiver, subject, contents)
        flash("An email has been sent to your address with instructions to reset your password.", category="success")
    except socket.error:
        flash("Sorry we couldn't send your email. Please check your internet connection and try again.", category="error")