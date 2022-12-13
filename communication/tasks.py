from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from communication.models import Ticket
from communication.serializers import MessageSerializer
from tech_support.celery import celery_app

from communication.services_views import send

@celery_app.task
def send_new_message(user, data, pk):
    """

    :param user: user_id for ticket's author
    :param data: message's body
    :param pk: ticket's id
    :return: JsonResponse
    """
    ticket = Ticket.objects.get(id=pk)
    message_author = User.objects.get(id=user)
    serializer = MessageSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['message_author'] = message_author
    serializer.validated_data['ticket'] = ticket
    serializer.save(ticket=ticket, message_author=message_author, message=data['message'])
    return serializer.data


@celery_app.task
def email_notification(user_email, text):
    send(user_email=user_email, text=text)

