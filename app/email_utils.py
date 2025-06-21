from flask_mail import Message
from flask import current_app
from . import mail

def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)
