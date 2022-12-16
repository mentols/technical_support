import os

from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


def send(user_email, text):
    send_mail(
        'You have new message in chat!',
        text,
        os.getenv('SENDER_EMAIL'),
        [user_email],
        fail_silently=False
    )
