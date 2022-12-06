from django.core.mail import send_mail


def send(user_email, text):
    send_mail(
        'You have new message in chat!',
        text,
        'pilip4yk.ilya@gmail.com',
        [user_email],
        fail_silently=False
    )
