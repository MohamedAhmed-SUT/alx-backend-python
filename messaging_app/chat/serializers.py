from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    # Use ReadOnlyField to display the username instead of the user ID
    sender = serializers.ReadOnlyField(source='sender.username')
    # Use PrimaryKeyRelatedField for writing, so we can send a receiver ID
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']