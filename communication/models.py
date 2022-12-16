import django
from django.contrib.auth.models import User
from django.db import models

from communication.utils import Status


class Ticket(models.Model):
    status = models.TextField(
        max_length=254,
        choices=Status.choices(),
        default=Status.U,
    )
    tittle = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID: {self.id} AUTHOR: {self.author} status: {self.status}'


class Message(models.Model):
    message_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=False)
    time_created = models.DateTimeField(default=django.utils.timezone.now)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message}'
