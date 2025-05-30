from flask_mail import Message
from app import mail
from flask import current_app

def send_verification_email(to_email, link):
    msg = Message("Verify Your Email", recipients=[to_email])
    msg.body = f"Click the following link to verify your email: {link}"
    mail.send(msg)
