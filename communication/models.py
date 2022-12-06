import datetime

import django
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    RESOLVED = 'RESLV', _('Resolved')
    UNRESOLVED = 'UNRES', _('Unresolved')
    FROZEN = 'FROZN', _('Frozen')


class Ticket(models.Model):
    status = models.CharField(
        max_length=5,
        choices=Status.choices,
        default=Status.UNRESOLVED,
        null=False
    )
    tittle = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID: {self.id} AUTHOR: {self.author} status: {self.status}'


class Message(models.Model):
    message_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=10000, null=True)
    time_created = models.DateTimeField(default=django.utils.timezone.now)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message}'
