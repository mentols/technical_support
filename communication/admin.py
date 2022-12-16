from django.contrib import admin

from communication.models import Ticket, Message

admin.site.register(Ticket)
admin.site.register(Message)
