from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from communication.models import Ticket, Message
from communication.permissions import IsOwnerOfTicket
from communication.serializers import TicketSerializer, MessageSerializer
from communication.tasks import send_new_message, email_notification


class TicketsAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return self.list(request, *args, **kwargs)
        else:
            self.queryset = Ticket.objects.filter(author=self.request.user)
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TicketsAPIDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOfTicket | IsAdminUser]

    def get(self, request, *args, **kwargs):
        print(self.permission_classes)
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(status=self.request.data['status'])

    def put(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return self.update(request, *args, **kwargs)
        else:
            return Response({"Error": "You have no permission to update"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MessageAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOfTicket | IsAdminUser]

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        self.queryset = Message.objects.filter(ticket=ticket).order_by('time_created')
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.request.user.id
        data = request.data
        author_email = Ticket.objects.get(id=pk).author.email

        send_new_message.apply_async((user, data, pk))
        if self.request.user.is_staff:
            print(author_email)
            email_notification.apply_async((author_email, request.data['message']))
        return Response(status=status.HTTP_201_CREATED)
