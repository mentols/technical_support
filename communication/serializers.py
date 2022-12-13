from rest_framework import serializers

from communication.models import Ticket, Message
from communication.models import Status


class TicketSerializer(serializers.ModelSerializer):
    tittle = serializers.CharField(max_length=120, required=True)
    status = serializers.ChoiceField(Status.choices(), required=False)
    author_id = serializers.IntegerField(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'status', 'tittle', 'author_id')

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tittle = validated_data.get('tittle', instance.tittle)
        instance.status = validated_data.get('status', instance.status)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_author', 'message', 'time_created', 'ticket')
        read_only_fields = ('message_author', 'time_created', 'ticket')

    def save(self, **validated_data):
        return Message.objects.create(**validated_data)
